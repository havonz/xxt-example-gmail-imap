# device.flash

Purpose: Flashlight switch

## Signature
```lua
success = device.flash_on()
success = device.flash_off()
```

## Example
```lua
if device.flash_on() then
    sys.msleep(1000)
    device.flash_off()
else
    sys.log('The current device cannot turn on the flashlight')
end
```

## Returns
- success
    boolean, returns `true` when the device has flashlight hardware and the camera is available; otherwise returns `false`.

## Notes
The flashlight on iPad Pro cannot be turned on.
When the script terminates, any flashlight turned on by the script is turned off automatically.
