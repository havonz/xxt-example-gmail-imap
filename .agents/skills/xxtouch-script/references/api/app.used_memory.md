# app.used_memory

Purpose: App memory

## Signature
```lua
memory_usage = app.used_memory(bundle_identifier_or_pid)
```

## Example
```lua
local qqmem = app.used_memory("com.tencent.mqq")
sys.alert("Current QQ process memory usage: "..qqmem.."MB")
```

## Parameters
- bundle_identifier
    string
- pid
    integer, the process ID of the app to inspect.

## Returns
- memory_usage
    number | nil, the memory used by the app in MB if it is running; otherwise returns `nil`.
