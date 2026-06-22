# screen.init

Purpose: Initialize rotated coordinates

## Signature
```lua
previous_coordinate_system = screen.init(coordinate_system)
```

## Example
```lua
screen.init(0)    -- Home button at the bottom.
screen.init(1)    -- Home button on the right.
screen.init(2)    -- Home button on the left.
screen.init(3)    -- Home button at the top.

screen.init_home_on_bottom()    -- Home button at the bottom.
screen.init_home_on_right()     -- Home button on the right.
screen.init_home_on_left()      -- Home button on the left.
screen.init_home_on_top()       -- Home button at the top.
```

## Parameters
- coordinate_system
    integer
    `0` means portrait with the Home button at the bottom.
    `1` means landscape with the Home button on the right.
    `2` means landscape with the Home button on the left.
    `3` means portrait with the Home button at the top.

## Returns
- previous_coordinate_system
    integer, the coordinate system used before this function call.

## Notes
Initializes the coordinate system for color sampling or tapping. This affects the meaning of coordinate parameters and return values for the following functions.

Common affected functions:
- screen.get_color
- screen.is_colors
- screen.find_color
- screen.ocr_text
- screen.image
- touch.on
- touch.move
- touch.off
- touch.tap

Coordinate system meanings:
- `0`: default portrait, origin at the physical top-left corner, x to the right, y downward.
- `1`: landscape with Home on the right, logical size becomes `height x width`.
- `2`: landscape with Home on the left, logical size becomes `height x width`.
- `3`: portrait with Home at the top, origin at the physical bottom-right corner.

For one block of color sampling, color search, or tapping logic, set a fixed coordinate system first, then use screenshots or coordinate data from the same coordinate system. Use `screen.rotate_xy` / `screen.unrotate_xy` when converting between physical coordinates and rotated coordinates.

Using iPhone 8 as an example (750x1334 resolution).
