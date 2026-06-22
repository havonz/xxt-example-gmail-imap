# file.exists

Purpose: Existence check.

## Signature
```lua
exists_info = file.exists(file_path)
```

## Example
```lua
if file.exists("/var/mobile/1.zip") then
    sys.alert("`/var/mobile/1.zip` exists")
else
    sys.alert("`/var/mobile/1.zip` does not exist")
end

if file.exists("/var/mobile/1.zip")=="file" then
    sys.alert("`/var/mobile/1.zip` exists and is a file")
else
    sys.alert("`/var/mobile/1.zip` is not a file")
end

if file.exists("/var/mobile/123/")=="directory" then
    sys.alert("`/var/mobile/123/` exists and is a directory")
else
    sys.alert("`/var/mobile/123/` is not a directory")
end
```

## Parameters
- file_path
    string, absolute path to a file or directory.

## Returns
- exists_info
    Returns false when the path does not exist.
    Returns `"file"` when the path is a file.
    Returns `"directory"` when the path is a directory.

## Notes
Determines whether a path is a file, a directory, or nonexistent.
