# LuaSocket TCP Slice

Source: https://lunarmodules.github.io/luasocket/tcp.html

Use `socket.tcp` for custom TCP protocols, port checks, raw request debugging, or server sockets. Use XXTouch `http` for normal HTTP/HTTPS.

## Core API

```lua
local socket = require 'socket'

local sock, err = socket.tcp()          -- or socket.tcp4(), socket.tcp6()
sock:settimeout(seconds[, mode])        -- mode: 'b' block timeout, 't' total timeout
sock:connect(host, port)                -- returns 1 or nil, err
sock:send(data[, i[, j]])               -- returns byte index or nil, err, last_index
sock:receive(pattern_or_size)           -- returns data or nil, err, partial
sock:close()
```

`receive` patterns commonly used in scripts:

- `number`: read up to that many bytes.
- `'*l'`: read one line without line ending.
- `'*a'`: read until connection closes; risky without a timeout.

## TCP Client Pattern

```lua
local socket = require 'socket'

local sock = assert(socket.tcp())
sock:settimeout(10, 't')
local ok, err = sock:connect('example.com', 80)
if not ok then
    sock:close()
    return nil, err
end

local sent, send_err = sock:send('PING\r\n')
if not sent then
    sock:close()
    return nil, send_err
end

local chunks = {}
while true do
    local chunk, status, partial = sock:receive(4096)
    if chunk then
        chunks[#chunks + 1] = chunk
    elseif partial and #partial > 0 then
        chunks[#chunks + 1] = partial
    end
    if status == 'closed' then break end
    if status == 'timeout' then break end
    if status then
        sock:close()
        return nil, status
    end
end

sock:close()
return table.concat(chunks)
```

## Port Probe

```lua
local socket = require 'socket'

local function can_connect(host, port, timeout)
    local sock = assert(socket.tcp())
    sock:settimeout(timeout or 1, 't')
    local ok = sock:connect(host, port)
    sock:close()
    return ok == 1
end
```

## Line Protocol

```lua
local socket = require 'socket'

local sock = assert(socket.tcp())
sock:settimeout(5, 't')
assert(sock:connect('192.0.2.10', 12345))
assert(sock:send('status\r\n'))
local line, err, partial = sock:receive('*l')
sock:close()

if not line then
    return nil, err, partial
end
return line
```

## TCP Server Pattern

```lua
local socket = require 'socket'

local server = assert(socket.tcp())
server:settimeout(1)
assert(server:bind('*', 18080))
assert(server:listen(8))

local client = server:accept()
if client then
    client:settimeout(5)
    local line = client:receive('*l')
    client:send('ok\r\n')
    client:close()
end
server:close()
```

## Notes

- `settimeout(nil)` blocks indefinitely; avoid it in automation scripts.
- `connect` may spend longer in DNS resolution than the socket timeout.
- `accept` can block unless the server object has a timeout.
- Use `shutdown('send')`, `shutdown('receive')`, or `shutdown('both')` only when protocol half-close matters.
- Internal APIs such as `getfd` and `setfd` are not portable; avoid them.
- Use `setoption('reuseaddr', true)` for local test servers only when address reuse is needed.
