# file.currentdir

Purpose: Current working directory.

## Signature
```lua
directory_path, error_message = file.currentdir()
```

## Example
```lua
local cwd, err = file.currentdir()
if cwd then
    sys.alert("Current working directory: "..cwd)
else
    sys.alert("Failed to get current working directory: "..err)
end
```

## Returns
- directory_path
    string, returns the directory path on success and nil on failure.
- error_message
    string, error message on failure.

## Notes
Gets the current working directory, equivalent to `lfs.currentdir`.
