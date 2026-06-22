# LuaSocket

Source: https://lunarmodules.github.io/luasocket/reference.html

Use LuaSocket for low-level TCP/UDP, DNS, raw protocol work, and legacy modules built around LTN12. Prefer XXTouch `http` / `ftp` for ordinary HTTP, HTTPS, download, upload, and form requests.

## Require Map

```lua
local socket = require 'socket'
local http = require 'socket.http'
local ftp = require 'socket.ftp'
local url = require 'socket.url'
local ltn12 = require 'ltn12'
local mime = require 'mime'
```

## Topic Slices

- TCP client/server, timeout, send, receive: `luasocket-tcp.md`.
- UDP datagrams: `luasocket-udp.md`.
- DNS and URL parsing/escaping: `luasocket-dns-url.md`.
- `socket.http`, `socket.ftp`, and LTN12 sink/source patterns: `luasocket-http-ftp.md`.

## Selection Rules

- Plain HTTP/HTTPS: use XXTouch `http.*` first.
- FTP upload/download: use XXTouch `ftp.*` first.
- Custom TCP protocol, port probe, raw socket timeout: use `socket.tcp`.
- UDP broadcast or local datagram protocol: use `socket.udp`.
- URL escaping only: prefer `string.encode_uri_component`; use `socket.url` or `lcurl` when matching existing code.

## Timeout And Sleep Helpers

```lua
local socket = require 'socket'

socket.sleep(0.2)
local now = socket.gettime()
```

Use `socket.sleep` only in socket-heavy helper code. In ordinary XXTouch automation, prefer `sys.msleep`.

## Error Shape

```lua
local ok, err = sock:connect(host, port)
if not ok then
    sock:close()
    return nil, err
end

local data, status, partial = sock:receive(4096)
```

Many LuaSocket calls return `nil, err` or `nil, status, partial`. Preserve `partial` when reading protocols that may close after sending data.

## Safety Rules

- Set timeouts before `connect`, `accept`, `receive`, or protocol helpers.
- Close sockets explicitly.
- Handle `nil, err, partial` returns; do not discard `partial` data on reads.
- Do not use LuaSocket alone for HTTPS. Use XXTouch `http`, `lcurl`, or `ssl` wrapping when TLS is truly required.
