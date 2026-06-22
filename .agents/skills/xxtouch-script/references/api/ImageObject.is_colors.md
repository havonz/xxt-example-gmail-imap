# ImageObject:is_colors

Purpose: Multi-point color match in image

## Signature
```lua
fully_matched = image:is_colors(...)
```

## Example
```lua
local img = screen.image()
if img:is_colors({
    {100, 200, 0xffffff},
    {120, 220, 0x333333},
}, 90) then
    touch.tap(100, 200)
end
```

## Returns
- fully_matched
    boolean, returns whether it fully matches.

## Notes
Multi-point color matching for images.
Parameters and return values are the same as screen multi-point color matching (`screen.is_colors`).
