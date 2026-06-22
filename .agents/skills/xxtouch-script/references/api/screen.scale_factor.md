# screen.scale_factor

Purpose: Screen scale factor

## Signature
```lua
local factor = screen.scale_factor()
```

## Example
```lua
-- Convert pixel resolution to logical points.
local w_px, h_px = screen.size()
local scale = screen.scale_factor()
local w_pt, h_pt = w_px / scale, h_px / scale

sys.log(string.format("Pixel resolution: %dx%d, scale: %.1fx, logical points: %.0fx%.0f", w_px, h_px, scale, w_pt, h_pt))

-- Adjust UI coordinates based on the scale factor.
local x_point, y_point = 100, 200           -- Point coordinates from Apple HIG or a third-party UI description.
local x_px, y_px = x_point * scale, y_point * scale

touch.tap(x_px, y_px)
```

## Returns
- factor
    number, the ratio between current device screen pixels and logical points (pt).

## Notes
The return value is used to convert between the screen's actual pixel resolution and the logical coordinate system.
Common values: `2.0` for most Retina iPhones and iPads, and `3.0` for Plus/Max models and recent full-screen iPhones. Modern iPhones generally do not have a `1.0` non-Retina scale.
Used together with `screen.size()`, it can derive logical point dimensions: `width_pt = width_px / factor`. Image search and color sampling are still based on pixel dimensions; conversion is only needed when handling UI point coordinates.
