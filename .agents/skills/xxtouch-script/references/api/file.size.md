# file.size

Purpose: File size.

## Signature
```lua
size, error_message = file.size(file_path)
```

## Example
```lua
local fsize, err = file.size("/var/mobile/1.zip")
if fsize then
    sys.alert("Size of `/var/mobile/1.zip`: "..fsize.." bytes")
else
    sys.alert("`/var/mobile/1.zip` is not a file: "..err)
end
```

## Parameters
- file_path
    string, absolute file path.

## Returns
- size
    integer or nil. Returns nil if the file does not exist or the filename is a directory; otherwise returns file size in bytes.
- error_message
    string, error message on failure.

## Notes
Gets the size of a file.
