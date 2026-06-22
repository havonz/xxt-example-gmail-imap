# device.battery_state

Purpose: Charging state

## Signature
```lua
charging_state = device.battery_state()
```

## Example
```lua
local state_names = {
    Full = "Connected and fully charged",
    Charging = "Connected and charging",
    Unplugged = "Unplugged",
    Unknown = "Unknown state",
}

sys.alert("Current battery charging state: "..state_names[device.battery_state()])
```

## Returns
- charging_state
    string, one of the following values:
    `"Full"`: connected to power and fully charged
    `"Charging"`: connected to power and charging
    `"Unplugged"`: not connected to power
    `"Unknown"`: unknown state
