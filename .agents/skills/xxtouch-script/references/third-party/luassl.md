# LuaSSL / SSL Module

Source: https://mauriciocarneiro.github.io/software/luassl/references.html

## Require

```lua
local ssl = require 'ssl'
```

## Minimal Connection Shape

The upstream LuaSSL reference exposes this SSL object model:

```lua
local ssl = require 'ssl'

local s = ssl.wrap(key_file, cert_file, cert_dir, dh_file, cipher_list, verify_options, options)
s:connect(host, port)
s:write('...')
local data, err = s:read()
s:shutdown()
```

Use `ssl` only when a socket workflow specifically needs TLS-level control. For ordinary HTTPS requests, prefer XXTouch `http.get`, `http.post`, or `lcurl`.

## Protected Cleanup Shape

```lua
local ssl = require 'ssl'

local conn, err = ssl.wrap(key_file, cert_file, cert_dir, dh_file, cipher_list, verify_options, options)
if not conn then
    return nil, err
end

local ok, result = pcall(function()
    assert(conn:connect(host, port))
    assert(conn:write(payload))
    return conn:read()
end)

pcall(function()
    conn:shutdown()
end)

if not ok then
    return nil, result
end
return result
```

## Notes

- Prefer high-level HTTP clients for TLS transport.
- Certificate verification defaults and constants are version-sensitive.
- Always close or shut down SSL objects.
- Do not mix LuaSSL examples from LuaSec with this module unless the target project already proves the same API is available.
- For HTTPS APIs, `lcurl` is usually less error-prone than managing TLS sockets manually.
