# ImageObject:cv_binaryzation

Purpose: cv auto-binarization

## Signature
```lua
image = image:cv_binaryzation([ binarization_threshold ])
```

## Example
```lua
local img = screen.image(462, 242, 569, 272)
img:cv_binaryzation()
img:save_to_png_file(XXT_HOME_PATH..'/tmp/binary.png')

local img2 = screen.image(462, 242, 569, 272)
img2:cv_binaryzation(128)
```

## Parameters
- binarization_threshold
    number, optional threshold, in the range `0` to `255`. Defaults to the theoretically most suitable threshold.

## Returns
- image
    ImageObject, returns the ImageObject itself after binarization.

## Notes
OpenCV extension feature for automatic image binarization.
This affects the object itself.
For performance, this function does not create a data copy during the operation.
