# device.wifi_info

Purpose: Current Wi-Fi

## Signature
```lua
wifi_info = device.wifi_info()
```

## Example
```lua
nLog(device.wifi_info())
```

## Returns
- wifi_info
    table | nil, returns a table with the following structure on success, or `nil` on failure.

    ```lua
    {
        SSID = string_value,
        BSSID = string_value,
        hidden = boolean_value,
        encryption = string_value,
        password = string_value,
        channel = integer_value,
    }
    ```
