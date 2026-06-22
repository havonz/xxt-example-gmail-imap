# screen.size

Purpose: Screen size

## Signature
```lua
screen_width, screen_height = screen.size()
```

## Example
```lua
-- Determine device type by resolution.
width, height = screen.size()
if width == 640 and height == 1136 then
    -- iPhone 5, 5S, iPod touch 5
elseif width == 640 and height == 960 then
    -- iPhone 4, 4S, iPod touch 4
elseif width == 750 and height == 1334 then
    -- iPhone 6, 6S, 7, 8
elseif width == 1242 and height == 2208 then
    -- iPhone 6+, 6S+, 7+, 8+
elseif width == 768 and height == 1024 then
    -- iPad 1, 2, mini 1
elseif width == 1536 and height == 2048 then
    -- iPad 3, 4, 5, mini 2
elseif width == 320 and height == 480 then
    -- iPhone 3GS / iPhone 4 (listed only for completeness; XXTouch does not support devices this old)
end
```

## Returns
- screen_width integer
- screen_height integer

## Notes
The return values of this function are not affected by the current Home Screen or app portrait/landscape state, and are not affected by Zoomed Display mode.
This function can be used in XUI.
