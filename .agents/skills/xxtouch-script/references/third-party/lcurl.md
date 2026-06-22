# lcurl

Source: https://lua-curl.github.io/lcurl/modules/lcurl.html

## Require

```lua
local curl = require 'lcurl'
```

or, for safer request execution:

```lua
local curl = require 'curl.safe'
```

Prefer XXTouch `http` and `ftp` APIs for normal transfers. Use lcurl for URL escaping, custom curl options, multipart upload control, or protocols not covered by built-ins.

## Topic Slice

- Easy handle request, callbacks, multipart form, info, cleanup: `lcurl-easy.md`.

## URL Escape

```lua
local curl = require 'lcurl'

local easy = curl.easy()
local encoded = easy:escape('abcd$%^&*()')
local decoded = easy:unescape(encoded)
easy:close()
sys.log(encoded, decoded)
```

## Notes

- Prefer `curl.safe` for request execution so errors can be handled cleanly.
- Use `http.get` / `http.post` first unless curl-specific options are required.
- Always close easy handles.
