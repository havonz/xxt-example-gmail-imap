# lua-openssl

Source: https://zhaozg.github.io/lua-openssl/index.html

## Require

```lua
local openssl = require 'openssl'
```

## SHA256 Hex

```lua
local openssl = require 'openssl'

local md = openssl.digest.get('sha256')
local hash = md:digest('hello world')
local hex = openssl.hex(hash)
sys.log(hex)
```

## One-Step HMAC

```lua
local openssl = require 'openssl'

local hex = openssl.hmac.hmac('sha256', 'message', 'secret')
local raw = openssl.hmac.hmac('sha256', 'message', 'secret', true)
```

## Streaming Digest

```lua
local openssl = require 'openssl'

local ctx = openssl.digest.new('sha256')
ctx:update('part-1')
ctx:update('part-2')
local raw = ctx:final()
local hex = openssl.hex(raw)
```

## Useful API Shapes

```lua
local openssl = require 'openssl'

local md, err = openssl.digest.get('sha256')
if not md then
    return nil, err
end
local digest_hex = openssl.hex(md:digest('message'))

local hmac = openssl.hmac.new('sha256', 'secret')
hmac:update('message')
local hmac_hex = hmac:final()
```

## Use When

- Prefer XXTouch string helpers for simple hashes and HMAC: `string.md5`, `string.sha1`, `string.hmac_sha1`, `string.hmac_sha256`.
- Prefer `http` / `lcurl` for TLS transport.
- Use OpenSSL for certificate parsing, signatures, asymmetric crypto, or compatibility with existing OpenSSL-based Lua code.
- Keep OpenSSL usage isolated in a helper file so scripts do not mix crypto details into UI or automation flow.

## Offline Details

Open `lua-openssl-reference.md` before going online. It contains the module map, common digest/HMAC/cipher/pkey/x509 shapes, and examples for the APIs most likely to be needed in XXTouch scripts.

## Notes

- OpenSSL APIs are broad and version-sensitive. For a concrete algorithm, check the exact submodule API before writing final code.
- Do not invent crypto formats. Match input, output, encoding, padding, and key format exactly.
- Avoid crypto changes unless the user provides test vectors or a protocol spec.
- Default OpenSSL digest/HMAC helpers often return hex unless `raw = true`; confirm expected encoding with a known test vector.
- Use lowercase algorithm names such as `'sha256'` in examples unless existing code uses OpenSSL NID or object identifiers.
