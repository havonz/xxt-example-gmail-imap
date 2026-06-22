# LuaCJSON Options Slice

Source: https://kyne.au/~mark/software/lua-cjson-manual.html

Use this only when default `json` / `cjson` behavior is not acceptable.

## Error Behavior

```lua
local cjson = require 'cjson'
local cjson_safe = require 'cjson.safe'
```

- `cjson.encode` / `cjson.decode` throw on errors.
- `cjson.safe.encode` / `cjson.safe.decode` return `nil, err`.
- `cjson.new()` creates an independent module table with separate settings.

## Null And Invalid Data

- JSON `null` decodes to `cjson.null`.
- Strings should be valid UTF-8 for interoperable JSON.
- Binary data should be encoded, commonly with Base64, before JSON.
- Unsupported table keys can raise errors; JSON object keys must be strings.

## Common Settings

```lua
local cjson = require 'cjson'

cjson.encode_invalid_numbers(false) -- default: error on NaN/infinity
cjson.decode_invalid_numbers(true)  -- allow non-standard numeric input
cjson.encode_max_depth(1000)
cjson.decode_max_depth(1000)
cjson.encode_keep_buffer(false)     -- reduce retained memory after large encodes
```

## Sparse Arrays

Lua CJSON decides array vs object from table keys. Sparse arrays can error by default.

```lua
local convert, ratio, safe = cjson.encode_sparse_array()
cjson.encode_sparse_array(true, 2, 10)
```

Only change sparse-array settings to match a known payload contract.
