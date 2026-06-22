# file.lattrs

Purpose: Symlink attributes.

## Signature
```lua
attributes, error_message = file.lattrs(path [, requested_field])
```

## Example
```lua
local info, err = file.lattrs("/var/mobile/Media/1ferver/lua/scripts/")
if info then
    sys.alert("File information: "..json.encode(info))
else
    sys.alert("Failed to get file attributes: "..err)
end
```

## Parameters
- path
    string.
- requested_field
    optional. Supports these forms:
    - Omitted: creates and returns an attribute table containing all fields.
    - A table: does not create a new table; fills attributes into the provided table.
    - A single field name string: returns that field value directly.
    - `"dev"`: device where the file inode resides.
    - `"ino"`: file inode number.
    - `"mode"`: file type, possibly `"file"`, `"directory"`, `"link"`, `"socket"`, `"named pipe"`, `"char device"`, `"block device"`, or `"other"`.
    - `"nlink"`: hard link count.
    - `"uid"`: file owner ID.
    - `"gid"`: file owner group ID.
    - `"rdev"`: device type for special file inodes.
    - `"access"`: last file access time.
    - `"modification"`: last file modification time.
    - `"change"`: last file status change time.
    - `"size"`: file size in bytes.
    - `"permissions"`: file permissions.
    - `"blksize"`: filesystem I/O block size.
    - `"blocks"`: number of allocated 512-byte blocks.
    - `"target"`: path pointed to by the symlink.

## Returns
- attributes
    table, returns the attribute table on success and nil on failure.
- error_message
    string, error message on failure.

## Notes
Gets file attributes. If the target is a symlink, returns information about the symlink itself instead of the target it points to, equivalent to `lfs.symlinkattributes`.
