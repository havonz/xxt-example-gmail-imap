# device.forget_wifi

Purpose: Forget Wi-Fi

## Signature
```lua
success = device.forget_wifi(SSID)
```

## Example
```lua
local ok = device.forget_wifi('Tenda_9B3F')
```

## Parameters
- SSID
    string, the name of the Wi-Fi network to forget.

## Returns
- success
    boolean, returns `true` if the network was removed from the saved Wi-Fi network list successfully; otherwise returns `false`.
