# ImageObject:replace_color

Purpose: Color replacement

## Signature
```lua
image = image:replace_color(original_color, replacement_color[, original_color_similarity])
```

## Example
```lua
local img = screen.image()
img:replace_color(0xff0000, 0x00ff00, 90)
img:save_to_png_file(XXT_HOME_PATH..'/tmp/replaced.png')
```

## Parameters
- original_color
    integer, the original color.
- replacement_color
    integer, the color to replace it with.
- original_color_similarity
    integer, optional color similarity, in the range `0` to `100`. Defaults to `100`.

## Returns
- image
    ImageObject, returns the ImageObject itself after color replacement.

## Notes
Replaces a color, or an approximate color, on the ImageObject with another color.
This affects the object itself.
For performance, this function does not create a data copy during the operation.
