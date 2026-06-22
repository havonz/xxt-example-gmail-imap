# xxtouch.call_callback

Purpose: Phone call callback

## Signature
```lua
thread.register_event("xxtouch.call_callback", function(val)
    if (val == "in") then
        -- Incoming call
    elseif (val == "out") then
        -- Outgoing call
    elseif (val == "disconnected") then
        -- Call disconnected
    end
end)
```

## Example
```lua
sys.msleep(20000) -- Wait 20 seconds.

sys.toast("The script starts listening for call events now and stops after twenty seconds")

-- Clear the message queue.
proc_queue_clear("xxtouch.call_callback")
```

## Notes
When a system incoming or outgoing call message is received, a status is pushed into the process queue dictionary identified by this message.
