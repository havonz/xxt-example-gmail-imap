# LuaFileSystem

Source: https://lunarmodules.github.io/luafilesystem/manual.html#reference

## Require

```lua
local lfs = require 'lfs'
```

Prefer XXTouch `file` APIs for simple exists/list/read/write operations. Use LuaFileSystem when a script needs directory iterators, file attributes, current-directory control, or LFS-style locks.

## Topic Slices

- Attributes, symlink attributes, modes, timestamps: `luafilesystem-attributes.md`.
- Directory iteration and current directory: `luafilesystem-dir-cwd.md`.
- `mkdir`, `rmdir`, links, touch, file locks: `luafilesystem-mutate-lock.md`.

## Quick Directory Iteration

```lua
local lfs = require 'lfs'

for name in lfs.dir('/var/mobile') do
    if name ~= '.' and name ~= '..' then
        sys.log(name)
    end
end
```

## Notes

- `lfs.dir` includes `.` and `..`; filter them.
- Restore the previous current directory after temporary `chdir`.
- Prefer `XXT_HOME_PATH`, `XXT_RES_PATH`, and `XXT_SCRIPTS_PATH` over hardcoded XXTouch paths.
