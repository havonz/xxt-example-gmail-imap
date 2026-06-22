# ImageObject:copy

Purpose: Image copy

## Signature
```lua
image_copy = image:copy()
```

## Example
```lua
scrn = screen.image()
img2 = scrn:copy()
```

## Returns
- image_copy
    ImageObject, a copy of the original ImageObject.

## Notes
Creates a copied ImageObject from an ImageObject.
This method creates a new ImageObject. To keep frequent usage efficient, use it together with the `image:destroy` method.
