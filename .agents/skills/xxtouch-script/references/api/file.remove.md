# file.remove

Purpose: Delete file/directory.

## Signature
```lua
success, error_message = file.remove(file_path)
```

## Example
```lua
ok, err = file.remove(XXT_SCRIPTS_PATH.."/1.zip")
if not ok then
    sys.alert('Delete failed: '..err)
end
```

## Parameters
- file_path
    string, absolute file path.

## Returns
- success
    boolean, returns true on success and false on failure.
- error_message
    string, error message on failure.

## Notes
Deletes a file or directory.
Keywords: delete file, delete directory, delete folder.
