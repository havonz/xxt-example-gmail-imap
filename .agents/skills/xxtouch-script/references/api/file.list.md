# file.list

Purpose: Directory file list.

## Signature
```lua
file_list, error_message = file.list(path [, deep_full_traversal])
```

## Example
```lua
local list, err = file.list("/var/mobile/")
if list then
    print("Directory `/var/mobile/` contains "..#list.." files or directories")
    for _, name in ipairs(list) do
        print(name)
    end
    sys.alert(print.out())
else
    sys.alert("`/var/mobile/` is not a directory: "..err)
end

-- full_file_path_list = file.list(path, deep_full_traversal)
-- Gets a directory's filename list. The second argument controls whether to recursively return full paths for files in subdirectories. Defaults to false.
list = file.list("/var/mobile/Media/1ferver", true)
nLog(list)
--[[
Possible output:
{ -- table: 0xc4cc58a30
    [1] = "/var/mobile/Media/1ferver/snippets/syntax - do __ end.snippet",
    [2] = "/var/mobile/Media/1ferver/snippets/app - app.uninstall(bid).snippet",
    [3] = "/var/mobile/Media/1ferver/snippets/test - snippet.snippet",
    ...
}
--]]
```

## Parameters
- path
    string, absolute directory path.
- deep_full_traversal
    boolean, optional. Whether to recursively traverse subdirectories and return a full path list. Defaults to false.

## Returns
- file_list
    array table or nil. Returns nil if the directory does not exist or the path is a file; otherwise returns the directory file list.
- error_message
    string, error message on failure.

## Notes
Gets the list of all filenames in a directory.
