# ImageObject:size

Purpose: Image size

## Signature
```lua
width, height = image:size()
```

## Example
```lua
local img = image.load_file("/var/mobile/1.png")
local w, h = img:size()
sys.alert("Image width: "..w.."\nImage height: "..h)
```

## Returns
- width, height
    integer, the width and height of the current ImageObject.

## Notes
Gets the ImageObject size. Note that the returned width is not necessarily shorter than the height; rotation changes it.
