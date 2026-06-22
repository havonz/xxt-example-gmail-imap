# ImageObject:cv_find_image

Purpose: cv image search

## Signature
```lua
x, y, similarity = large_image:cv_find_image(small_image)
```

## Example
```lua
local big = screen.image()
local small = image.load_file(XXT_SCRIPTS_PATH..'/target.png')
local x, y, similarity = big:cv_find_image(small)
if similarity >= 95 then
    touch.tap(x, y)
end
```

## Parameters
- small_image
    ImageObject, the small image to search for.

## Returns
- x, y
    integer, the top-left coordinate of the best-matched position of the found small image in the large image.
- similarity
    number, the similarity of the best-matched position of the found small image in the large image, in the range `0` to `100`.

## Notes
OpenCV extension feature for finding the position of one ImageObject inside another ImageObject.
