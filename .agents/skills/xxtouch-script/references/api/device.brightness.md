# device.brightness / device.set_brightness

Purpose: Read/set backlight brightness

## Get Backlight Brightness
```lua
brightness = device.brightness()
```

### Returns
- brightness
    number, the current backlight brightness of the device, in the range `0.0` to `1.0`.

## Set Backlight Brightness
```lua
device.set_brightness(brightness)
```

### Example
```lua
sys.toast(device.brightness())
for i = 1, 10 do
    device.set_brightness(i/10)
    sys.msleep(200)
end
for i = 10, 5, -1 do
    device.set_brightness(i/10)
    sys.msleep(200)
end
```

### Parameters
- brightness
    number, the target backlight brightness for the device, in the range `0.0` to `1.0`.

## Notes
Calling `device.set_brightness` disables the device's automatic brightness adjustment.
