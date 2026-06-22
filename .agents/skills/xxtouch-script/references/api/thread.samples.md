# thread.samples

Purpose: Thread sample code

## Common Examples
```lua
-- Dispatch an asynchronous task and wait.
local tid = thread.dispatch(function()
    sys.msleep(300)
    nLog("worker done")
end)

thread.wait(tid)

-- Long-running tasks can be killed explicitly.
local loop_tid = thread.dispatch(function()
    while true do
        nLog("loop")
        sys.msleep(1000)
    end
end)

sys.msleep(3000)
thread.kill(loop_tid)

-- Register a process queue event. Returning true from the callback stops the current listener.
proc_queue_clear("remote.message")
local event_id = thread.register_event("remote.message", function(value)
    nLog("Received message", value)
    return true
end)

thread.dispatch(function()
    sys.msleep(500)
    proc_queue_push("remote.message", "ok")
end)

sys.msleep(1000)
thread.unregister_event("remote.message", event_id)

-- Multi-finger action: dispatch touch sequences concurrently with multiple threads.
thread.dispatch(function()
    touch.on(59, 165):move(297, 522):msleep(500):off()
end)

thread.dispatch(function()
    touch.on(580, 1049):move(371, 1049):msleep(500):off()
end)
```
