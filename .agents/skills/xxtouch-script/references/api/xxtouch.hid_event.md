# xxtouch.hid_event

Purpose: HID event message

## Signature
```lua
thread.register_event("xxtouch.hid_event", function(val)
    local event = json.decode(val)
    if event.event_type=="touch" then
        if event.event_name=="touch.on" then
            sys.toast("Touch contact position: ("..event.x..", "..event.y..")\n"..event.time)
        elseif event.event_name=="touch.move" then
            sys.toast("Touch moved to position: ("..event.x..", "..event.y..")\n"..event.time)
        elseif event.event_name=="touch.off" then
            sys.toast("Touch left the screen from position: ("..event.x..", "..event.y..")\n"..event.time)
        end
    else
        if event.event_name=="key.down" then
            sys.toast("Key down: "..event.key_name.."\n"..event.time)
        elseif event.event_name=="key.up" then
            sys.toast("Key up: "..event.key_name.."\n"..event.time)
        end
    end
end)
```

## Example
```lua
sys.msleep(20000) -- Wait 20 seconds.

-- Clear the message queue.
proc_queue_clear("xxtouch.hid_event")

touch.on(100, 100):off()
sys.msleep(1000)
key.press('homebutton')
```
