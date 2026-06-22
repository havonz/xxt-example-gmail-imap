# app.all_procs / app.front_bid / app.front_pid / app.pid_for_bid / app.is_running

Purpose: App processes/frontmost/running state

## Get Process List
```lua
process_info_array = app.all_procs()
```

### Example
```lua
proc_list = app.all_procs()
```

### Returns
- process_info_array
    array table, the process list.

    ```lua
    {
        {pid = process_id_1, name = process_name_1},
        {pid = process_id_2, name = process_name_2},
        ...
    }
    ```

### Notes
This function does not guarantee that full process names can be obtained.

## Get Frontmost App BID
```lua
bundle_identifier = app.front_bid()
```

### Example
```lua
local bid = app.front_bid()
sys.alert("Frontmost app bundle identifier: "..bid)
```

### Returns
- bundle_identifier
    string, the bundle identifier of the frontmost app.
    If no app is in the foreground but the Home Screen (SpringBoard) has loaded, returns `"com.apple.springboard"`.
    If no app is in the foreground and SpringBoard has not started yet, during early system boot, returns the background service `"com.apple.backboardd"`.

## Get Frontmost App PID
```lua
pid = app.front_pid()
```

### Example
```lua
local pid = app.front_pid()
sys.alert("Frontmost app process ID: "..pid)
```

### Returns
- pid
    integer, the process ID of the frontmost app. Returns `0` if no app is in the foreground.

### Notes
Returns `0` when no app is in the foreground, instead of returning the process ID of SpringBoard, the Home Screen.

## Get PID by BID
```lua
pid = app.pid_for_bid(bundle_identifier)
```

### Example
```lua
local qqpid = app.pid_for_bid("com.tencent.mqq")
if qqpid ~= 0 then
    sys.alert("QQ is running, process ID: "..qqpid)
else
    sys.alert("QQ is not running")
end
```

### Parameters
- bundle_identifier
    string

### Returns
- pid
    integer, the app PID if the app is running; otherwise returns `0`.

## Check Whether App Is Running
```lua
status = app.is_running(bundle_identifier)
```

### Example
```lua
if app.is_running("com.tencent.mqq") then
    sys.alert("QQ is running")
end
```

### Parameters
- bundle_identifier
    string

### Returns
- status
    boolean, whether the app is running.

### Notes
This function checks whether an app is running. It does not distinguish foreground from background. To check whether an app is running in the foreground, get the frontmost app BID with `app.front_bid` and compare it.
