# LuaFileSystem Directory And CWD Slice

Source: https://lunarmodules.github.io/luafilesystem/manual.html#reference

Use when a script needs iterator-style directory traversal or temporary current-directory changes. Prefer XXTouch `file.list` for simple listings.

## Directory Iterator

```lua
local lfs = require 'lfs'

for name in lfs.dir(XXT_RES_PATH) do
    if name ~= '.' and name ~= '..' then
        local full = XXT_RES_PATH..'/'..name
        sys.log(name, lfs.attributes(full, 'mode'))
    end
end
```

## Recursive Walk

```lua
local lfs = require 'lfs'

local function walk(dir, out)
    for name in lfs.dir(dir) do
        if name ~= '.' and name ~= '..' then
            local full = dir..'/'..name
            local mode = lfs.attributes(full, 'mode')
            if mode == 'directory' then
                walk(full, out)
            elseif mode == 'file' then
                out[#out + 1] = full
            end
        end
    end
end

local files = {}
walk(XXT_RES_PATH, files)
```

Manual close pattern for early exit:

```lua
local iter, dir = lfs.dir(XXT_RES_PATH)
while true do
    local name = iter(dir)
    if not name then break end
    if name == 'target.txt' then
        dir:close()
        break
    end
end
```

## Current Directory

```lua
local lfs = require 'lfs'

local old = assert(lfs.currentdir())
local ok, err = lfs.chdir(XXT_SCRIPTS_PATH)
if not ok then
    return nil, err
end

-- relative file operations here

lfs.chdir(old)
```

## Notes

- `lfs.dir(path)` raises an error if `path` is not a directory; wrap with `pcall` when input is uncertain.
- `lfs.dir` returns `.` and `..`; filter them.
- Restore the old current directory after `chdir`, especially inside framework callbacks.
- Avoid deep recursive walks on large app data directories inside UI callbacks; run them before the main loop or in a worker task.
