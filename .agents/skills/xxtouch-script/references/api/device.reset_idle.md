# device.reset_idle

Purpose: Reset auto-lock idle timer

## Signature
```lua
device.reset_idle()
```

## Example
```lua
-- Dispatch a task that resets the idle countdown every 29 seconds.
thread.dispatch(function()
    while 1 do
        device.reset_idle()
        sys.msleep(29 * 1000)
    end
end)
```

## Notes
Resets the auto-lock idle timer to keep the screen awake.
Avoid calling this function too frequently. Very frequent calls, more than 10 times per second, may cause the service or system to crash.
