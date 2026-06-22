# sys.mkdir_p

Purpose: Create directories recursively

## Signature
```lua
sys.mkdir_p(directory_path)
```

## Example
```lua
sys.mkdir_p("/var/mobile/Media/1ferver/lua/scripts/a/b/c/d")
```

## Parameters
- directory_path
    string

## Notes
Creates directories recursively. Newly created directories have owner UID/GID `501` and permissions octal `0777`.
Keywords: new folder, create folder.
