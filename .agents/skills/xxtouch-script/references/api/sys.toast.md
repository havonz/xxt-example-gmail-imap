# sys.toast

Purpose: Show toast text

## Signature
```lua
sys.toast(text_content [, rotation_direction ])
```

## Example
```lua
-- Show the current date and time in real time.
while (true) do
    sys.toast("Long-press the volume key by default to stop the script\n\n"..os.date("%Y-%m-%d %H:%M:%S"), device.front_orien())
    sys.msleep(1000)
end
```

## Parameters
- text_content
    string, text to display.
- rotation_direction
    integer, optional screen rotation direction. Defaults to the direction set by the last call to `screen.init`.
    `0` means portrait with Home at the bottom.
    `1` means landscape with Home on the right.
    `2` means landscape with Home on the left.
    `3` means portrait with Home at the top.
    `-1` means hide the toast immediately.

## Notes
Displays toast text at the bottom of the screen in the current rotated coordinate system.
This function is asynchronous. The text is displayed for a total of 2.8 seconds and does not intercept taps.
On iOS 13.2+, it does not affect color sampling.
