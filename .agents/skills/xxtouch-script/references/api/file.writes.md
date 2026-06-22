# file.writes

Purpose: Overwrite file.

## Signature
```lua
write_success, error_message = file.writes(file_path, content_to_write)
```

## Example
```lua
local success, err = file.writes("/var/mobile/1.txt", "content")
if success then
    sys.alert("Write succeeded")
else
    sys.alert("Write failed: "..err)
end
```

## Parameters
- file_path
    string, absolute file path.
- content_to_write
    string, data to write.

## Returns
- write_success
    boolean, returns true on success and false on failure.
- error_message
    string, error message on failure.

## Notes
Overwrites data into a file. Creates the file if it does not exist; returns false if the directory does not exist.
