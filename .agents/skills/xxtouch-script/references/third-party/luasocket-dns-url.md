# LuaSocket DNS And URL Slice

Sources:
- https://lunarmodules.github.io/luasocket/dns.html
- https://lunarmodules.github.io/luasocket/url.html

Use these helpers when existing LuaSocket code expects them. Prefer XXTouch string URI helpers for simple encode/decode.

## DNS

```lua
local socket = require 'socket'

local ip, resolved = socket.dns.toip('example.com')
local host, names = socket.dns.tohostname('93.184.216.34')
local addrs, err = socket.dns.getaddrinfo('example.com')
local local_name = socket.dns.gethostname()
```

Return shapes:

- `toip(host) -> first_ip, { name = ..., alias = {...}, ip = {...} } | nil, err`
- `tohostname(address) -> canonical_name, info | nil, err`
- `getaddrinfo(address) -> { { family = 'inet'|'inet6', addr = '...' }, ... } | nil, err`

## URL Parse And Build

```lua
local url = require 'socket.url'

local parsed = url.parse('https://user:pass@example.com:8443/a/b?q=1#frag')
sys.log(parsed.scheme, parsed.host, parsed.port, parsed.path, parsed.query)

local rebuilt = url.build {
    scheme = 'https',
    host = 'example.com',
    path = '/a/b',
    query = 'q=1',
}
```

Common parsed fields: `scheme`, `authority`, `path`, `params`, `query`, `fragment`, `userinfo`, `host`, `port`, `user`, `password`.

## URL Escape

```lua
local url = require 'socket.url'

local encoded = url.escape('/#?;')
local decoded = url.unescape(encoded)
```

## Notes

- DNS helpers can block in the resolver; keep them off tight UI/automation loops.
- `socket.url.escape` percent-encodes bytes. For normal query parameters, `string.encode_uri_component` may be clearer in XXTouch scripts.
- Do not log URLs containing passwords or tokens.
