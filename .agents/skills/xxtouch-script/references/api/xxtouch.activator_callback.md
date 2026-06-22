# xxtouch.activator_callback

Purpose: Activator callback

## Signature
```lua
thread.register_event("xxtouch.activator_callback", function(val)
    local ret = json.decode(val)
    sys.toast("mode:"..ret.mode.."\n"
            .."event:"..ret.event.."\n"
            .."time:"..ret.time)
end)
```

## Example
```lua
sys.msleep(20000) -- Wait 20 seconds.

-- Clear the message queue.
proc_queue_clear("xxtouch.activator_callback")

-- Unregister the callback. If the listener is not unregistered, the script will not end here.
thread.unregister_event("xxtouch.activator_callback", eid)
```

## Notes
Requires Activator to be installed and configured accordingly before use.
