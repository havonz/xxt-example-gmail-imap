# screen.get_color / screen.get_color_rgb

Purpose: Screen color/RGB

## Signature
```lua
color_value = screen.get_color(x, y)
red, green, blue = screen.get_color_rgb(x, y)
```

## Example
```lua
local c = screen.get_color(512, 133)
if c==0xffffff then
    sys.alert("The point 512, 133 is pure white")
end

local r, g, b = screen.get_color_rgb(512, 133)
if r==0xff and g==0xff and b==0xff then
    sys.alert("The point 512, 133 is pure white")
end
```

## Parameters
- x, y
    integer, the coordinate of the target point.

## Returns
- color_value
    integer, the RGB value of the target point color.
- red, green, blue
    integer, the RGB channel values of the target point color, in the range `0` to `255`.

## Notes
For coordinate conventions, see Visual API Conventions in `references/workflow.md`.
