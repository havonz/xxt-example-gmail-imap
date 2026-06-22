# sys.ctlbyname

Purpose: sysctl read

## Signature
```lua
data = sys.ctlbyname(key_name)
```

## Example
```lua
local raw = sys.ctlbyname('hw.machine')
if type(raw) == 'string' then
    nLog('Device type: '..raw:gsub('%z+$', ''))
else
    nLog('Unable to read hw.machine')
end

local sec, usec = string.unpack('li', sys.ctlbyname('kern.boottime'))
nLog('Booted seconds', os.time() - sec)
```

## Parameters
- key_name
    string, full sysctl key name, such as `kern.boottime` or `hw.memsize`.

## Returns
- data
    string, raw byte data for the specified key, or `nil` if it cannot be read.

## Notes
Calls the underlying `sysctlbyname` to read kernel/hardware runtime parameters. The returned raw bytes usually need to be unpacked.
Keywords: read system information, get sysctl parameters, parse kernel state.
