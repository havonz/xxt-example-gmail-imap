# lua-iconv

Source: https://github.com/lunarmodules/lua-iconv

## Require

```lua
local iconv = require 'iconv'
```

Use for text encoding conversion when `string.from_gbk` or other built-in helpers are insufficient.

## GBK To UTF-8

```lua
local iconv = require 'iconv'

local cd, open_err = iconv.new('utf-8', 'gbk')
if not cd then
    return nil, open_err
end
local input = file.reads(XXT_RES_PATH..'/input-gbk.txt')
local output, err = cd:iconv(input)
if not output then
    return nil, err
end
sys.log(output)
```

## UTF-16LE To UTF-8

```lua
local iconv = require 'iconv'

local cd, open_err = iconv.new('utf-8', 'utf-16le')
if not cd then
    return nil, open_err
end
local input = file.reads(XXT_RES_PATH..'/input-utf16le.txt')
local output, err = cd:iconv(input)
if not output then
    return nil, err
end
sys.log(output)
```

## Notes

- `iconv.new(toEncoding, fromEncoding)` converts from the second encoding to the first.
- `iconv.open(toEncoding, fromEncoding)` is an alias of `iconv.new`.
- Add `//IGNORE` or `//TRANSLIT` to the target encoding only when the user accepts lossy conversion.
- Conversion can return `nil, err`; handle invalid and incomplete byte sequences.
- Read encoded files as raw data; do not pre-process bytes as UTF-8 strings.
- Prefer project resource paths over device-global paths.
