# device.ifaddrs

Purpose: Interface IP addresses

## Signature
```lua
interface_info_array = device.ifaddrs()
```

## Example
```lua
-- Get the device Wi-Fi IP.
local ip = "Wi-Fi is off"
for i,v in ipairs(device.ifaddrs()) do
    if (v[1]=="en0") then
        ip = v[2]
    end
end
sys.alert(ip)
```

## Returns
- interface_info_array
    array table | nil, returns a table with the following structure on success, or `nil` on failure.

    ```lua
    {
        {"interface name 1", "IP1"},
        {"interface name 2", "IP2"},
        ...
    }
    ```

## Notes
Gets all interface IP addresses of the device.
