# device.battery_level

Purpose: Battery level

## Signature
```lua
battery_level = device.battery_level()
```

## Example
```lua
sys.alert("Current battery level: "..(device.battery_level() * 100).."%")
```

## Returns
- battery_level
    number, the current remaining battery level of the device, in the range `0.0` to `1.0`.
