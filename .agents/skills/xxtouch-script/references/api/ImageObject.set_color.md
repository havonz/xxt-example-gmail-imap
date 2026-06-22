# ImageObject:set_color

Purpose: Set pixel color

## Signature
```lua
image = image:set_color(x, y, color)
```

## Example
```lua
local img = image.new(20, 20)
img:set_color(10, 10, 0xff0000)
img:save_to_png_file(XXT_HOME_PATH..'/tmp/point.png')
```

## Parameters
- x, y
    integer, the coordinate of the point whose color should be set in the current ImageObject.
- color
    integer, the color value to set.

## Returns
- image
    ImageObject, returns the ImageObject itself after setting the color.

## Notes
Sets the color of a point in the ImageObject.
This affects the object itself.
For performance, this function does not create a data copy during the operation.
