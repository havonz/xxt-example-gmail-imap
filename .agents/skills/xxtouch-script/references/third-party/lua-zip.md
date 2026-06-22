# lua-zip

Source: https://raw.githubusercontent.com/brimworks/lua-zip/refs/heads/master/README.txt

## Require

```lua
local zip = require 'zip'
```

XXTouch lists `require 'zip'`. Upstream brimworks documentation uses `require 'brimworks.zip'`; keep the XXTouch require name unless the target project already proves otherwise.

## Read One Entry

```lua
local zip = require 'zip'

local arc = assert(zip.open(XXT_RES_PATH..'/data.zip'))
local idx = assert(arc:name_locate('config.json'))
local f = assert(arc:open(idx))
local chunks = {}

while true do
    local s = f:read(8192)
    if not s then break end
    chunks[#chunks + 1] = s
end

f:close()
arc:close()

local config = json.decode(table.concat(chunks))
```

Use only when direct ZIP archive access is required. For normal compression and extraction, prefer XXTouch `file.zip` and `file.unzip`.

## Useful APIs

- `zip.open(filename[, flags]) -> archive | nil, err`
- `zip.CREATE`, `zip.EXCL`, `zip.CHECKCONS`, `zip.OR(...)`
- `archive:close()`
- `archive:get_num_files()` or `#archive`
- `archive:name_locate(name[, flags])`
- `archive:open(name_or_index[, flags]) -> file`
- `file:read(n)`, `file:close()`
- `archive:stat(name_or_index[, flags])`
- `archive:add_dir(name)`, `archive:add(name, source...)`, `archive:delete(name_or_index)`

## List Entries

```lua
local zip = require 'zip'

local arc = assert(zip.open(XXT_RES_PATH..'/data.zip'))
for i = 1, #arc do
    local st = arc:stat(i)
    sys.log(i, st.name, st.size)
end
arc:close()
```

## Add A File

```lua
local zip = require 'zip'

local arc = assert(zip.open(XXT_HOME_PATH..'/out.zip', zip.CREATE))
assert(arc:add('config.json', XXT_RES_PATH..'/config.json'))
arc:close()
```

## Notes

- `archive:close()` can throw; protect it when data loss matters.
- Close file handles explicitly.
- Sanitize extracted entry names before writing to disk.
