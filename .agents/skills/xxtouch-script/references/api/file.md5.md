# file.md5

Purpose: File MD5.

## Signature
```lua
md5_value, error_message = file.md5(file_path)
```

## Example
```lua
local md5, err = file.md5("/var/mobile/1.zip")
if md5 then
    sys.alert("MD5 value of `/var/mobile/1.zip`: "..md5)
else
    sys.alert("`/var/mobile/1.zip` is not a file: "..err)
end
```

## Parameters
- file_path
    string, absolute file path.

## Returns
- md5_value
    string or nil. Returns nil if the file does not exist or the filename is a directory; otherwise returns the file MD5 value.
- error_message
    string, error message on failure.

## Notes
Gets the MD5 value of a file.
