# file.sha1

Purpose: File SHA1.

## Signature
```lua
sha1_value, error_message = file.sha1(file_path)
```

## Example
```lua
local sha1, err = file.sha1("/var/mobile/1.zip")
if sha1 then
    sys.alert("SHA1 value of `/var/mobile/1.zip`: "..sha1)
else
    sys.alert("`/var/mobile/1.zip` is not a file: "..err)
end
```

## Parameters
- file_path
    string, absolute file path.

## Returns
- sha1_value
    string or nil. Returns nil if the file does not exist or the filename is a directory; otherwise returns the file SHA1 value.
- error_message
    string, error message on failure.

## Notes
Gets the SHA1 value of a file.
