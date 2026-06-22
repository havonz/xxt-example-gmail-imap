# device.name / device.set_name

Purpose: Read/set device name

## Get Device Name
```lua
device_name = device.name()
```

### Example
```lua
sys.alert("Device name: "..device.name())
```

### Returns
- device_name
    string, the name assigned to the device by the user.

## Set Device Name
```lua
device.set_name(name)
```

### Example
```lua
device.set_name("Demo iPhone")
```

### Parameters
- name
    string, the device name to set.

## Notes
`device.name` can be used in XUI.

Setting the device name may take effect with different delays on different system versions. If `device.name` is called immediately after `device.set_name`, it may still return the old name. If this happens, add an appropriate delay for the target system version before reading the name again.
