# LuaSocket UDP Slice

Source: https://lunarmodules.github.io/luasocket/udp.html

Use UDP for datagram protocols, local discovery, broadcast, and fire-and-forget packets. UDP has no delivery guarantee, ordering guarantee, or connection stream.

## Core API

```lua
local socket = require 'socket'

local udp = assert(socket.udp())         -- or socket.udp4(), socket.udp6()
udp:settimeout(seconds)
udp:setsockname(local_ip, local_port)    -- bind local endpoint
udp:setpeername(remote_ip, remote_port)  -- optional connected mode
udp:send(data)                           -- connected mode
udp:sendto(data, ip, port)               -- unconnected mode
udp:receive([size])                      -- data or nil, err
udp:receivefrom([size])                  -- data, ip, port or nil, err
udp:close()
```

## Unconnected Send/Receive

```lua
local socket = require 'socket'

local udp = assert(socket.udp())
udp:settimeout(1)
assert(udp:setsockname('*', 18081))

assert(udp:sendto('hello', '192.0.2.10', 18082))
local data, ip, port = udp:receivefrom(8192)
udp:close()

if data then
    sys.log(ip, port, data)
end
```

## Connected UDP

```lua
local socket = require 'socket'

local udp = assert(socket.udp())
udp:settimeout(1)
assert(udp:setpeername('192.0.2.10', 18082))
assert(udp:send('hello'))
local data, err = udp:receive(8192)
udp:close()
```

## Options

- Broadcast: `udp:setoption('broadcast', true)` before sending to a broadcast address.
- Reuse address: `udp:setoption('reuseaddr', true)` before binding when multiple listeners may be involved.
- Multicast options exist, but use them only for an explicit multicast task.

## Notes

- `receive(size)` discards bytes beyond `size` for that datagram.
- Bind with `setsockname` before receiving.
- Keep datagrams small; large UDP packets can fragment and be lost.
