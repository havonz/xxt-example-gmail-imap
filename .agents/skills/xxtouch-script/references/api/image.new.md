# image.new

Purpose: Blank image

## Signature
```lua
image = image.new(width, height)
```

## Example
```lua
local img = image.new(100, 100)
img:set_color(50, 50, 0xffffff)
img:save_to_png_file(XXT_HOME_PATH..'/tmp/blank.png')
```

## Parameters
- width, height
    integer, the width and height of the new ImageObject.

## Returns
- image
    ImageObject, returns a newly created ImageObject.

## Notes
Creates a blank ImageObject. By default, every point in the image is `0x000000` (black).
This method creates a new ImageObject. To keep frequent usage efficient, use it together with the `image:destroy` method.
