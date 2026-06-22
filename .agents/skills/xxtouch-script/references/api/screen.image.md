# screen.image

Purpose: Screen image

## Signature
```lua
image = screen.image([ left, top, right, bottom ])
```

## Example
```lua
screen.image():save_to_album()
screen.image():save_to_png_file("/var/mobile/1.png")
```

## Parameters
- left, top, right, bottom
    integer, optional image region. Defaults to full screen.

## Returns
- image
    ImageObject, returns an ImageObject. For usage, see the ImageObject module (image).

## Notes
Gets an image of a screen region or the full screen.
For coordinate and region conventions, see Visual API Conventions in `references/workflow.md`.
This method creates a new ImageObject. When using it frequently, pair it with `ImageObject:destroy`.
