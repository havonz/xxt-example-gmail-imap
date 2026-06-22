# lua-ev

Source: https://github.com/brimworks/lua-ev

## Require

```lua
local ev = require 'ev'
```

In XXTouch, use `lua-ev` only inside a child process created with `fork_dostring`. `loop:loop()` takes over the current process event loop, so running it in the main script can block stop handling, UI automation, and cleanup. Normal automation should use XXTouch `thread`, `sys.msleep`, or the selected framework run loop.

## Fork Child Process Pattern

```lua
thread.register_event('ev-child.done', function(msg)
    nLog('ev result', msg)
end)

thread.dispatch(function()
    local out, ok, statusText, statusCode, err = fork_dostring([[
        local ev = require 'ev'

        local loop = ev.Loop.default
        local timer

        timer = ev.Timer.new(function(loop, watcher)
            proc_queue_push('ev-child.done', 'timer fired')
            watcher:stop(loop)
            loop:unloop()
        end, 1.0)

        timer:start(loop)
        loop:loop()
    ]], 5000)

    if not ok then
        nLog('ev child failed', statusText, statusCode, err, out)
    end
end)
```

## Core APIs

```lua
local ev = require 'ev'

local loop = ev.Loop.default
local timer = ev.Timer.new(function(loop, watcher)
    watcher:stop(loop)
end, 1.0)

timer:start(loop)
loop:loop()
```

Useful constructors: `ev.Timer.new`, `ev.IO.new`, `ev.Signal.new`, `ev.Idle.new`, `ev.Async.new`.

## Repeating Timer With Stop Flag

```lua
local ev = require 'ev'

local loop = ev.Loop.default
local ticks = 0
local timer

timer = ev.Timer.new(function(loop, watcher)
    ticks = ticks + 1
    sys.log('tick', ticks)
    if ticks >= 5 then
        watcher:stop(loop)
        loop:unloop()
    end
end, 0.5, 0.5)

timer:start(loop)
loop:loop()
```

## Socket-Oriented Shape

Use `ev.IO.new` only when the file descriptor is known and the socket/module exposes it. Most XXTouch scripts should prefer LuaSocket timeouts or `thread.dispatch`.

## Notes

- Prefer `fork_dostring` for all `lua-ev` event loops; do not call `loop:loop()` in the main script.
- Watchers must be explicitly started on a loop.
- Do not start an event loop that prevents the script from responding to stop conditions.
- If combining with sockets, set socket timeouts and close handles on exit.
- Keep watcher variables reachable while the loop runs; do not create watchers as throwaway locals inside a short helper and then expect them to stay alive.
