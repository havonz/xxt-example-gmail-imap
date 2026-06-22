# Dialog:add_image

Purpose: Add an image to a dialog.

## Signature
```lua
dialog_object = dialog_object:add_image(image_object_or_data_or_path)
```

## Example
```lua
dialog():add_image(screen.image()):show() -- Show a screen screenshot.

local img_data = screen.image():png_data()
dialog():add_image(img_data):show()

dialog():add_image({
    image = screen.image(),
    height = 420,
}):show()
```

## Parameters
- image_object_or_data_or_path
    ImageObject, image file path, or PNG/JPEG image data.
    In the XUI dialog engine, this can also be a table with `image` and `height` fields.

## Returns
- dialog_object
    Dialog, returns the dialog itself.

## Notes
Adds an image to the dialog.
In the XUI dialog engine, images are not automatically scaled to exactly match dialog width. Pass `{image = ..., height = ...}` when the display height needs to be constrained.
