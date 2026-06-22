# LuaFileSystem Mutate And Lock Slice

Source: https://lunarmodules.github.io/luafilesystem/manual.html#reference

Prefer XXTouch `file.mkdir_p`, `file.remove`, `file.touch`, `file.move`, `file.copy`, `file.zip`, and `file.unzip` for normal file operations. Use LFS here when the exact LFS behavior is needed.

## Directory And Link APIs

```lua
local lfs = require 'lfs'

lfs.mkdir(path)              -- true or nil, err, code
lfs.rmdir(path)              -- removes empty directory
lfs.link(old, new[, true])   -- third arg true creates symlink
lfs.touch(path[, atime[, mtime]])
```

## File Lock APIs

```lua
local lfs = require 'lfs'

local f = assert(io.open(XXT_RES_PATH..'/lockable.txt', 'a+'))
local ok, err = lfs.lock(f, 'w')
if ok then
    f:write('locked write\n')
    lfs.unlock(f)
end
f:close()
```

Directory lock:

```lua
local lock, err = lfs.lock_dir(XXT_RES_PATH, 30)
if not lock then
    return nil, err
end

-- exclusive work

lock:free()
```

## Notes

- `lfs.rmdir` only removes an empty directory.
- `lfs.lock(file, 'r')` is shared/read; `lfs.lock(file, 'w')` is exclusive/write.
- `lfs.lock_dir` creates `lockfile.lfs` in the target directory and returns a lock object; call `lock:free()`.
- Use `pcall` or explicit cleanup when lock-protected code can error.
