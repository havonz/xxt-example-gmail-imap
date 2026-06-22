# file.mkdir_p

Purpose: Create directories recursively.

## Signature
```lua
success, error_message = file.mkdir_p(directory_path [, user_id, group_id, permissions ])
```

## Example
```lua
local success, err = file.mkdir_p("/var/mobile/Media/1ferver/lua/scripts/a/b/c/d")
if success then
    sys.alert("Create succeeded")
else
    sys.alert("Create failed: "..err)
end
```

## Parameters
- directory_path
    string.
- user_id
    integer, optional. Defaults to 501.
- group_id
    integer, optional. Defaults to 501.
- permissions
    integer or string, optional. Defaults to `"0777"`.

## Returns
- success
    boolean, returns true on success and false on failure.
- error_message
    string, error message on failure.

## Notes
Creates directories recursively. When optional arguments are not specified, new directories use owner UID/GID 501 and octal permissions 0777.
Keywords: create folder, create directory.
