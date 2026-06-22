# sys.lchmod_r / sys.lchown_r / sys.lchownmod_r

Purpose: Recursively change permissions/owner

## Change Permissions
```lua
sys.lchmod_r(file_path, permissions)
```

### Example
```lua
sys.lchmod_r("/var/mobile/Media/1ferver", 7 * 8^2 | 5 * 8^1 | 5)
sys.lchmod_r("/var/mobile/Media/1ferver", "0755")
sys.lchmod_r("/var/mobile/Media/1ferver", "rwxr-xr-x")
```

### Parameters
- file_path
    string
- permissions
    integer | string, permission value, such as octal `0755`, `7 * 8^2 | 5 * 8^1 | 5`, or `"rwxr-xr-x"`.

## Change Owner
```lua
sys.lchown_r(file_path, user_id, group_id)
```

### Example
```lua
sys.lchown_r("/var/mobile/Media/1ferver", 501, 501)
```

### Parameters
- file_path
    string
- user_id
    integer
- group_id
    integer

## Change Owner and Permissions Together
```lua
sys.lchownmod_r(file_path, user_id, group_id, permissions)
```

### Example
```lua
sys.lchownmod_r("/var/mobile/Media/1ferver", 501, 501, 7 * 8^2 | 5 * 8^1 | 5)
sys.lchownmod_r("/var/mobile/Media/1ferver", 501, 501, "0755")
sys.lchownmod_r("/var/mobile/Media/1ferver", 501, 501, "rwxr-xr-x")
```

### Parameters
- file_path
    string
- user_id
    integer
- group_id
    integer
- permissions
    integer | string, permission value, such as octal `0755`, `7 * 8^2 | 5 * 8^1 | 5`, or `"rwxr-xr-x"`.

## Notes
These APIs recursively modify all files and subdirectories under a directory. They do not traverse directories pointed to by deep symbolic links.
Keywords: repair permissions, modify permissions, change permissions.
