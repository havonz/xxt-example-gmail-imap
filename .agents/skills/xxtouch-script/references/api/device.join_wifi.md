# device.join_wifi

Purpose: Join Wi-Fi

## Signature
```lua
success, error_message = device.join_wifi(SSID, password[, timeout_ms])
```

## Example
```lua
local ok, err = device.join_wifi('Tenda_9B3F', '12345678')
```

## Parameters
- SSID
    string, the Wi-Fi SSID, which is the network name.
- password
    string, the Wi-Fi password.
- timeout_ms
    integer, optional timeout in milliseconds. Defaults to `10000`.

## Returns
- success
    boolean, returns `true` on success and `false` on failure.
- error_message
    string, the error message returned when the operation fails.
