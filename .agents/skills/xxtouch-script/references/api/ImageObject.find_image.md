# ImageObject:find_image

Purpose: Find image in image

## Signature
```lua
x, y = large_image:find_image(small_image [, confidence, left, top, right, bottom ])
search_results = large_image:find_image(small_image [, options, left, top, right, bottom ])
```

## Example
```lua
local big = screen.image()
local small = image.load_file(XXT_SCRIPTS_PATH..'/target.png')

local x, y = big:find_image(small, 95)
if x ~= -1 then
    touch.tap(x, y)
end

local all = big:find_image(small, {
    find_all = true,
    confidence_threshold = 90,
    downscale = 0.5,
}, 0, 0, 0, 0)
```

## Parameters
- small_image
    ImageObject, the small image to search for.

## Returns
- x, y
    integer, the top-left coordinate of the best-matched position of the found small image in the large image.

## Notes
Parameter, return value, and `find_all` conventions are the same as `references/api/screen.find_image.md`; coordinates are local image pixel coordinates.
