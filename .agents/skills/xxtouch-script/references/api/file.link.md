# file.link

Purpose: Create file link.

## Signature
```lua
success, error_message = file.link(source_file_path, destination_file_path [, symbolic_link])
```

## Example
```lua
local info, err = file.link(jbroot("/var/mobile/Media/1ferver"), "/var/mobile/Media/1ferver", true)
if info then
    sys.alert("Symbolic link created")
else
    sys.alert("Failed to create symbolic link: "..err)
end
```

## Parameters
- source_file_path
    string.
- destination_file_path
    string.
- symbolic_link
    boolean, optional. If true, creates a symbolic link; otherwise creates a hard link.

## Returns
- success
    boolean, returns true on success and false on failure.
- error_message
    string, error message on failure.

## Notes
Creates a file link, equivalent to `lfs.link`.
