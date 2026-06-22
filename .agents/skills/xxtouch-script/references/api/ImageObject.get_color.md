# ImageObject:get_color

Purpose: Get image color

## Signature
```lua
color, opacity = image:get_color(x, y)
```

## Example
```lua
local img = image.load_file("/var/mobile/1.png")
local clr = img:get_color(100, 100)
sys.alert(string.format("Color at coordinate (100, 100) in the image: 0x%06x", clr))
```

## Parameters
- x, y
    integer, the coordinate of the point whose color should be read in the current ImageObject.

## Returns
- color
    integer, the color value at this coordinate in the current ImageObject. Note that if the color opacity is not `255`, the actual RGB values at the point need to account for division by the opacity ratio, `opacity / 255`.
- opacity
    integer, the opacity at this coordinate in the current ImageObject, in the range `0` to `255`.

## Notes
Gets the color of a point in an ImageObject. Unlike screen color sampling, pixels in an image also have an opacity property.
