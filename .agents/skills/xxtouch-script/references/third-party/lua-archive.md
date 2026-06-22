# lua-archive

Source: https://github.com/brimworks/lua-archive

## Require

```lua
local archive = require 'archive'
```

## List Archive Entries

```lua
local archive = require 'archive'

local fh = assert(io.open(XXT_RES_PATH..'/data.tar.gz', 'rb'))
local ar = assert(archive.read {
    reader = function()
        return fh:read(8192)
    end,
})

while true do
    local entry = ar:next_header()
    if not entry then break end
    sys.log(entry:pathname())
    while ar:data() do end
end

ar:close()
fh:close()
```

## Useful APIs

- `archive.version() -> major, minor, patch`
- `archive.read { reader = function(...) ... end } -> read`
- `read:next_header()`, `read:data()`, `read:close()`
- `archive.write { writer = function(_, chunk) ... end } -> write`
- `write:header(entry)`, `write:data(chunk)`, `write:close()`
- `archive.entry { pathname = ..., size = ..., mode = ... }`

## Use When

- ZIP create/extract: prefer `file.zip` and `file.unzip`.
- Streaming read/write or non-ZIP formats: consider `archive`.
- Keep extraction targets under project-owned paths unless the user names another path.

## Notes

- Validate archive entry paths before extracting.
- Close archive readers/writers explicitly.
- Writer callbacks should return the number of bytes written.
