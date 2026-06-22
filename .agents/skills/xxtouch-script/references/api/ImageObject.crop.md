# ImageObject:crop

Purpose: Image crop

## Signature
```lua
cropped_image = image:crop([left, top, right, bottom])
```

## Example
```lua
scrn = screen.image()
img2 = scrn:crop(100, 100, 200, 200)
```

## Parameters
- left, top, right, bottom
    integer, optional coordinates of the left, top, right, and bottom edges of the region in the original image. Defaults to `0, 0, original_width - 1, original_height - 1`.

## Returns
- cropped_image
    ImageObject, the ImageObject cropped from the original ImageObject.

## Notes
Creates a new copied ImageObject by cropping part of an ImageObject.
This method creates a new ImageObject. To keep frequent usage efficient, use it together with the `image:destroy` method.
