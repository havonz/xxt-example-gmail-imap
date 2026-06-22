# device.front_orien

Purpose: Frontmost screen orientation

## Signature
```lua
orientation_state = device.front_orien()
```

## Example
```lua
sys.toast('This toast is displayed using the frontmost app orientation', device.front_orien())
```

## Returns
- orientation_state
    integer, the orientation identifier of the frontmost app's screen.
    `0`: Home button at the bottom (portrait upright)
    `1`: Home button on the right (landscape)
    `2`: Home button on the left (landscape)
    `3`: Home button at the top (portrait upside down)
    `4`: failed to get the orientation
