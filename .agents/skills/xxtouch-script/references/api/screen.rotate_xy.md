# screen.rotate_xy / screen.unrotate_xy

Purpose: Coordinate rotation/reverse conversion

## Signature
```lua
x, y = screen.rotate_xy(x, y, rotation_direction)
x, y = screen.unrotate_xy(x, y, original_coordinate_rotation_direction)
```

## Example
```lua
rx, ry = screen.rotate_xy(100, 200, 1)
ux, uy = screen.unrotate_xy(rx, ry, 1)
```

## Parameters
- x, y
    integer, the coordinate to rotate.
- rotation_direction
    `0` means no rotation.
    `1` means rotate 90 degrees left.
    `2` means rotate 90 degrees right.
    `3` means rotate 180 degrees.
- original_coordinate_rotation_direction
    `0` means the original coordinates are portrait with Home downward. In this case, the original values are returned directly.
    `1` means the original coordinates are landscape with Home on the right.
    `2` means the original coordinates are landscape with Home on the left.
    `3` means the original coordinates are portrait with Home at the top.

## Returns
- x, y
    integer, the converted coordinate.

## Notes
`screen.rotate_xy` is commonly used to convert portrait coordinates to landscape coordinates, `init(0) -> init(rotation_direction)`.
`screen.unrotate_xy` is commonly used to convert landscape coordinates back to portrait coordinates, `init(original_coordinate_rotation_direction) -> init(0)`.
