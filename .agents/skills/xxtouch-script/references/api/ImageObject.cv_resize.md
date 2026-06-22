# ImageObject:cv_resize

Purpose: cv resize

## Signature
```lua
image = image:cv_resize(width, height)
```

## Example
```lua
local img = image.load_file(XXT_SCRIPTS_PATH..'/1.png')
img:cv_resize(224, 224)
img:save_to_png_file(XXT_HOME_PATH..'/tmp/resized.png')
```

## Parameters
- width, height
    integer, the new image width and height to set.

## Returns
- image
    ImageObject, returns the resized ImageObject itself.

## Notes
OpenCV extension feature that creates another image with a changed size from the image.
This affects the object itself.
