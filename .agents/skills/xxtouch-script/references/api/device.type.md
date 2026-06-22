# device.type

Purpose: Device type

## Signature
```lua
device_type = device.type()
```

## Example
```lua
if device.type() == "iPhone3,1" then
    -- It is an iPhone 4.
end
```

## Returns
- device_type
    string, a model identifier such as `"iPhone3,1"` or `"iPad13,1"`.

## Notes
Gets the device type.
This function can be used in XUI.
