# ImageObject:turn_right

Purpose: Rotate right 90 degrees

## Signature
```lua
image = image:turn_right()
```

## Example
```lua
local img = screen.image()
img:turn_right()
img:save_to_png_file(XXT_HOME_PATH..'/tmp/right.png')
```

## Returns
- image
    ImageObject, returns the ImageObject itself.

## Notes
Rotates the ImageObject 90 degrees right.
This affects the object itself.
For performance, this function does not create a data copy during the operation.
