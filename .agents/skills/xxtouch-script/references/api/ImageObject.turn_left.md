# ImageObject:turn_left

Purpose: Rotate left 90 degrees

## Signature
```lua
image = image:turn_left()
```

## Example
```lua
local img = screen.image()
img:turn_left()
img:save_to_png_file(XXT_HOME_PATH..'/tmp/left.png')
```

## Returns
- image
    ImageObject, returns the ImageObject itself.

## Notes
Rotates the ImageObject 90 degrees left.
This affects the object itself.
For performance, this function does not create a data copy during the operation.
