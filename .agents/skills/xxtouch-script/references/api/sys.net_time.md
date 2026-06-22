# sys.net_time

Purpose: Network time

## Signature
```lua
seconds_timestamp = sys.net_time([ timeout ])
```

## Example
```lua
local nt = sys.net_time() -- Gets network time. Default timeout is 2 seconds; returns 0 on timeout.

local nt = sys.net_time(5) -- Gets network time with a 5-second timeout; returns 0 on timeout.
if nt==0 then
    sys.alert('Failed to get network time')
else
    sys.alert(os.date('Current network time\n%Y-%m-%d %H:%M:%S', nt))
end
```

## Parameters
- timeout
    number, optional maximum wait time for connecting to get network time, in seconds. Defaults to `2`.

## Returns
- seconds_timestamp
    integer, current network time as a UNIX timestamp in seconds on success. Returns `0` on connection timeout or if network time cannot be obtained successfully.

## Notes
This method may yield. Before it returns, other threads may get a chance to run.
