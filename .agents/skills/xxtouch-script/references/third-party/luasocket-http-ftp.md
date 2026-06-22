# LuaSocket HTTP, FTP, LTN12 Slice

Sources:
- https://lunarmodules.github.io/luasocket/http.html
- https://lunarmodules.github.io/luasocket/ftp.html

Prefer XXTouch `http` and `ftp` modules for normal scripts. Use `socket.http`, `socket.ftp`, and LTN12 when maintaining legacy code or when a library requires LTN12 sources/sinks.

## HTTP Simple Form

```lua
local http = require 'socket.http'

http.TIMEOUT = 10
local body, code, headers, status = http.request('http://example.com/')
if not body then
    return nil, code
end
if code ~= 200 then
    return nil, status
end
```

## HTTP Generic Form With Sink

```lua
local http = require 'socket.http'
local ltn12 = require 'ltn12'

local chunks = {}
local ok, code, headers, status = http.request {
    method = 'GET',
    url = 'http://example.com/data',
    sink = ltn12.sink.table(chunks),
    headers = {
        ['user-agent'] = 'XXTouch',
    },
}

if ok ~= 1 then
    return nil, code
end
return table.concat(chunks), code, headers, status
```

## HTTP POST With Explicit Body

```lua
local http = require 'socket.http'
local ltn12 = require 'ltn12'

local request_body = 'a=1&b=2'
local response = {}
local ok, code = http.request {
    method = 'POST',
    url = 'http://example.com/form',
    source = ltn12.source.string(request_body),
    sink = ltn12.sink.table(response),
    headers = {
        ['content-type'] = 'application/x-www-form-urlencoded',
        ['content-length'] = tostring(#request_body),
    },
}
```

## FTP

```lua
local ftp = require 'socket.ftp'

ftp.TIMEOUT = 20
local content, err = ftp.get('ftp://user:pass@example.com/path/file.txt;type=i')
if not content then
    return nil, err
end
```

## Notes

- `socket.http.TIMEOUT`, `PROXY`, and `USERAGENT` are module globals; changing them affects other code using the same module.
- Generic `http.request` returns `1, code, headers, status`; the body goes to the sink.
- Simple `http.request(url[, body])` returns `body, code, headers, status`.
- When posting with an LTN12 source, set `content-length`; otherwise some servers reject chunked uploads.
- LuaSocket HTTP is not HTTPS by itself.
