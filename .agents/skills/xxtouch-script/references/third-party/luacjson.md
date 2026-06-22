# LuaCJSON

Source: https://kyne.au/~mark/software/lua-cjson-manual.html

## Require

```lua
local cjson = require 'cjson'
local cjson_safe = require 'cjson.safe'
```

XXTouch also exposes the global `json` module. Prefer `json.encode` and `json.decode` unless the script specifically needs direct LuaCJSON behavior.

## Use Cases

- Compatibility with existing Lua code that imports `cjson`.
- Error-returning decode/encode with `cjson.safe`.
- Explicit use of LuaCJSON options in code the user already owns.

## Common Pattern

```lua
local cjson = require 'cjson'

local text = cjson.encode({ok = true, count = 1})
local data = cjson.decode(text)
sys.log(data.ok, data.count)
```

## Safe Decode

```lua
local cjson = require 'cjson.safe'

local data, err = cjson.decode(text)
if not data then
    return nil, err
end
```

## Safe Encode

```lua
local cjson = require 'cjson.safe'

local text, err = cjson.encode({
    ok = true,
    items = {'a', 'b'},
})
if not text then
    return nil, err
end
```

## Null And Array Checks

```lua
local cjson = require 'cjson'

local data = cjson.decode('{"value":null,"items":[1,2]}')
if data.value == cjson.null then
    data.value = nil
end

-- Dense integer keys encode as JSON arrays.
local text = cjson.encode({10, 20, 30})
```

## Notes

- `cjson.encode` and `cjson.decode` throw on invalid data; `cjson.safe` returns `nil, err`.
- `cjson.null` represents JSON `null`.
- Lua tables with only positive integer keys encode as arrays; other keys encode as objects.
- Do not mix `json.null` assumptions with raw `cjson` unless behavior has been checked.
- For normal XXTouch scripts, global `json` keeps code clearer and matches the platform docs.
- Configuration options are in `luacjson-options.md`.
- For untrusted input, prefer `cjson.safe.decode` and validate the resulting Lua table shape before using fields.
