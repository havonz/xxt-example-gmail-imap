# file.chdir

Purpose: Change working directory.

## Signature
```lua
success, error_message = file.chdir(directory_path)
```

## Example
```lua
local success, err = file.chdir("/var/mobile/Media/1ferver/lua/scripts/")
if success then
    sys.alert("Change succeeded")
else
    sys.alert("Change failed: "..err)
end
```

## Parameters
- directory_path
    string.

## Returns
- success
    boolean, returns true on success and false on failure.
- error_message
    string, error message on failure.

## Notes
Changes the current working directory, equivalent to `lfs.chdir`.
