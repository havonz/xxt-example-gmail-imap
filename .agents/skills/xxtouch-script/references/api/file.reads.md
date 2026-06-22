# file.reads

Purpose: Read file.

## Signature
```lua
content, error_message = file.reads(file_path)
```

## Example
```lua
local data, err = file.reads("/var/mobile/1.zip")
if data then
    sys.alert("Size of `/var/mobile/1.zip`: "..#data.." bytes")
else
    sys.alert("Read failed: "..err)
end
```

## Parameters
- file_path
    string, absolute file path.

## Returns
- content
    string or nil. Returns nil if the file does not exist; otherwise returns all file data.
- error_message
    string, error message on failure.

## Notes
Reads all data from a file.
