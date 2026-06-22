# file.touch

Purpose: Update file timestamp.

## Signature
```lua
success, error_message = file.touch(file_path [, access_time, modification_time])
```

## Example
```lua
local success, err = file.touch("/var/mobile/Media/1ferver/lua/scripts/", os.time() - 86400 * 3, os.time() - 86400 * 2)
if success then
    sys.alert("Update succeeded")
else
    sys.alert("Update failed: "..err)
end
```

## Parameters
- file_path
    string.
- access_time
    integer, optional. Unix timestamp in seconds. If not specified, `os.time()` is used.
- modification_time
    integer, optional. Unix timestamp in seconds. If not specified, `access_time` is used.

## Returns
- success
    boolean, returns true on success and false on failure.
- error_message
    string, error message on failure.

## Notes
Updates file access and modification times, equivalent to `lfs.touch`.
