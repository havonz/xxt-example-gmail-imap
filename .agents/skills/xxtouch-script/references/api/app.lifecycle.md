# app.run / app.close / app.quit

Purpose: Launch/close apps

## Launch App
```lua
status = app.run(bundle_identifier)
```

### Example
```lua
local r = app.run("com.apple.weather")
sys.msleep(10 * 1000)
if r == 0 then
    app.close("com.apple.weather")
else
    sys.alert("Launch failed", 3)
end
```

### Parameters
- bundle_identifier
    string

### Returns
- status
    integer, the launch status. `0` means launch succeeded; any other value means launch failed.

### Notes
If this function does not work correctly in your script, try using `runApp` instead.

## Force Close App
```lua
app.close(bundle_identifier_or_pid)
```

### Parameters
- bundle_identifier
    string
- pid
    integer, the process ID of the app to close.

### Notes
If the app is not running, nothing is done and the call does not fail.
This is a non-declinable forced termination. The target app does not receive any notification when it is closed.

## Simulate Swipe-up App Exit
```lua
app.quit(bundle_identifier)
```

### Example
```lua
app.quit("*")
app.quit("com.tencent.mqq")
```

### Parameters
- bundle_identifier
    string, pass `"*"` to quit all apps.

### Notes
This operation is also a forced termination, but unlike `app.close`, the app receives a notification before it exits and has up to 10 seconds to save its data. It also clears the app card from the app switcher.
Do not use this while the screen is locked. This function may fail to quit apps running with root privileges, and using it on root-privileged apps may cause the screen to freeze or app icons to stop responding. For root-privileged apps, use `app.close` for forced termination.
