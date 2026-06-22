# thread.register_event / thread.unregister_event

Purpose: Register/unregister event listener

## Register Event Listener
```lua
event_id = thread.register_event(event_name, callback [, error_callback ])
```

### Example
```lua
local event_id = thread.register_event("worker.done", function(msg)
    nLog("Received event", msg)
end)

thread.dispatch(function()
    sys.msleep(1000)
    proc_queue_push("worker.done", "ok")
end)
```

### Parameters
- event_name
    string, event name.
- callback
    function, callback function triggered by the event.
- error_callback
    function, optional. If an exception occurs while executing the task, this function is called and the error is not thrown. By default, errors are thrown on exception.

### Returns
- event_id
    integer

### Notes
Registers an event listener. When the process queue dictionary corresponding to the event name has a value, that value is popped and passed as the argument to trigger the event callback.

## Unregister Event Listener
```lua
thread.unregister_event(event_name, event_id)
```

### Example
```lua
local event_id = thread.register_event("worker.done", function(msg)
    nLog(msg)
end)

thread.unregister_event("worker.done", event_id)
```

### Parameters
- event_name
    string
- event_id
    integer
