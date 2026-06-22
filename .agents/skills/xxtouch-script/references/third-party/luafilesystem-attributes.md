# LuaFileSystem Attributes Slice

Source: https://lunarmodules.github.io/luafilesystem/manual.html#reference

Use when a script needs metadata that XXTouch `file` helpers do not expose directly.

## API

```lua
local lfs = require 'lfs'

local attr, err, code = lfs.attributes(path)
local mode = lfs.attributes(path, 'mode')
local link_attr = lfs.symlinkattributes(path)
```

`lfs.attributes(path)` follows symlinks. `lfs.symlinkattributes(path)` reads the link itself and can include `target`.

## Useful Fields

- `mode`: `file`, `directory`, `link`, `socket`, `named pipe`, `char device`, `block device`, or `other`.
- `size`: byte size.
- `access`, `modification`, `change`: Unix timestamps compatible with `os.date`.
- `permissions`: permission string.
- `uid`, `gid`: owner and group on Unix-like systems.
- `blocks`, `blksize`: Unix-only allocation details.

## Pattern

```lua
local lfs = require 'lfs'

local target = XXT_RES_PATH..'/data.db'
local attr, err = lfs.attributes(target)
if not attr then
    return nil, err
end

if attr.mode == 'file' then
    sys.log('size', attr.size)
    sys.log('mtime', os.date('%Y-%m-%d %H:%M:%S', attr.modification))
end
```

## Notes

- For simple existence checks, prefer `file.exists`.
- `lfs.attributes(path, name)` avoids allocating the full table.
- Always handle `nil, err`; paths may be inaccessible on iOS.
