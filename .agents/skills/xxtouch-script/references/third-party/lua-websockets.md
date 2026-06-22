# lua-websockets

Sources:
- https://github.com/lipp/lua-websockets
- https://raw.githubusercontent.com/lipp/lua-websockets/master/API.md

## Require

```lua
local websocket = require 'websocket'
```

Use when a script must keep a WebSocket connection. Prefer XXTouch `http` for request-response workflows.

`websocket.client.ev` depends on `lua-ev`; use it only inside a `fork_dostring` child process. Keep the main script responsible for automation and receive child-process callbacks with `proc_queue_push` / `thread.register_event`.

## Ev Client Pattern

Use this shape when the client needs asynchronous callbacks. The `ev` backend is for `ws://`; use `sync` or XXTouch's GCD backend for `wss://`.

```lua
local url = 'ws://192.0.2.10:8000/ws'
local protocol = 'xxtouch-protocol'
local prefix = 'ws-ev-'..utils.gen_uuid()

for _, name in ipairs({'open', 'message', 'close', 'error'}) do
    proc_queue_clear(prefix..'.'..name)
end

thread.register_event(prefix..'.open', function()
    nLog('WebSocket connected')
end)

thread.register_event(prefix..'.message', function(payload)
    local args = table.load_string(payload) or {}
    local msg, opcode = args[1], args[2]
    nLog('WebSocket message', msg, opcode)
end)

thread.register_event(prefix..'.close', function(payload)
    local args = table.load_string(payload) or {}
    nLog('WebSocket closed', args[1], args[2], args[3])
end)

thread.register_event(prefix..'.error', function(err)
    nLog('WebSocket error', err)
end)

thread.dispatch(function()
    local child = ([[
        local ev = require 'ev'
        local websocket = require 'websocket'

        local url = %q
        local protocol = %q
        local prefix = %q
        local loop = ev.Loop.default
        local client
        local reconnect_timer
        local stopping = false

        local function stop_reconnect_timer()
            if reconnect_timer then
                reconnect_timer:stop(loop)
                reconnect_timer = nil
            end
        end

        local connect
        local function schedule_reconnect()
            if stopping then
                loop:unloop()
                return
            end
            stop_reconnect_timer()
            reconnect_timer = ev.Timer.new(function(loop, watcher)
                watcher:stop(loop)
                reconnect_timer = nil
                connect()
            end, 5.0)
            reconnect_timer:start(loop)
        end

        connect = function()
            client = websocket.client.ev({loop = loop})

            client:on_open(function(ws)
                proc_queue_push(prefix..'.open', 'ok')
                ws:send('hello', websocket.TEXT)
            end)

            client:on_message(function(ws, msg, opcode)
                proc_queue_push(prefix..'.message', table.deep_dump({msg, opcode}, true))
            end)

            client:on_close(function(ws, was_clean, code, reason)
                proc_queue_push(prefix..'.close', table.deep_dump({was_clean, code, reason}, true))
                schedule_reconnect()
            end)

            client:on_error(function(ws, err)
                proc_queue_push(prefix..'.error', tostring(err))
                schedule_reconnect()
            end)

            client:connect(url, protocol)
        end

        local lifetime = ev.Timer.new(function(loop, watcher)
            stopping = true
            watcher:stop(loop)
            stop_reconnect_timer()
            if client and client.state == 'OPEN' then
                client:close(1000, 'done', 3)
            else
                loop:unloop()
            end
        end, 30.0)

        lifetime:start(loop)
        connect()
        loop:loop()
    ]]):format(url, protocol, prefix)

    local out, ok, statusText, statusCode, err = fork_dostring(child, 45000)
    if not ok then
        nLog('websocket ev child failed', statusText, statusCode, err, out)
    end
end)
```

For reusable long-running wrappers, follow the same process boundary used by local test projects:

- Generate a unique queue prefix and clear stale `proc_queue` keys before starting.
- Push callback arguments from the child process with `table.deep_dump`, then decode them in the main script with `table.load_string`.
- Keep reconnect timers inside the child process; reset idle or deadline counters when the connection opens and when messages arrive.
- If the main script needs to call `send` or `close`, expose a small command channel in the child process with `cpdistributed_messaging_center_register_callback`, then call it from the parent with `cpdistributed_messaging_center_send_message_and_receive_reply`.
- Register `register_atexit` in the parent so exit cleanup clears queues and asks the child process to close the client.

## Client APIs

- `websocket.client.sync({timeout = seconds})`
- `websocket.client.ev({loop = ev.Loop.default})`
- `client:connect(ws_url[, protocol])`: sync returns `true | nil, err`; ev reports state through callbacks.
- `client:on_open(func)`
- `client:on_message(func)`
- `client:on_close(func)`
- `client:on_error(func)`
- `client:receive() -> message, opcode | nil, clean, code, reason`, sync client only.
- `client:send(message[, websocket.TEXT|websocket.BINARY])`
- `client:close([code[, reason[, timeout]]])`

## Notes

- Add reconnect/backoff only when the user asks for long-running behavior.
- Run `ev` mode in a `fork_dostring` child process, not in the main script.
- Close the WebSocket on stop, error, or timeout.
- `lua-websockets` is not currently maintained upstream; keep usage conservative.
- Keep automation actions outside the receive loop; dispatch work to a small handler so the connection can still close cleanly.
