# file.appends

Purpose: Append to a file.

## Signature
```lua
success, error_message = file.appends(file_path, content_to_append)
```

## Example
```lua
local success, err = file.appends("/var/mobile/1.txt", "append text")
if success then
    sys.alert("Write succeeded")
else
    sys.alert("Write failed: "..err)
end
```

## Parameters
- file_path
    string, absolute file path.
- content_to_append
    string, data to append.

## Returns
- success
    boolean, returns true on success and false on failure.
- error_message
    string, error message on failure.

## Notes
Appends data to the end of a file. Creates the file if it does not exist; returns false if the directory does not exist.
