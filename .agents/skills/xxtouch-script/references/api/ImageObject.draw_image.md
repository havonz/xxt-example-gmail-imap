# ImageObject:draw_image

Purpose: Draw image onto image

## Signature
```lua
large_image = large_image:draw_image(small_image[, {
   left = top_left_x,
   top = top_left_y,
   alpha = opacity,
   background = {
      {color*, color_tolerance*},
      {color*, color_tolerance*},
      ...
   },
}])
```

## Example
```lua
local bg = screen.image()
local badge = image.new_text_image('OK', {
    size = 24,
    color = 0xffffff,
    back_color = 0x00aa00,
})

bg:draw_image(badge, {
    left = 20,
    top = 20,
    alpha = 230,
    background = {
        {0x000000, 0x050505}, -- Do not draw near-black areas in the small image.
    },
})
bg:save_to_png_file(XXT_HOME_PATH..'/tmp/marked.png')
```

## Parameters
- small_image
    ImageObject, the image to draw onto `large_image`.
- top_left_x
    integer, optional x-coordinate of the top-left corner where `small_image` should be drawn onto `large_image`. Defaults to `0`.
- top_left_y
    integer, optional y-coordinate of the top-left corner where `small_image` should be drawn onto `large_image`. Defaults to `0`.
- opacity
    integer, optional opacity of `small_image`, in the range `0` to `255`. Defaults to `255`.
- color\*, color_tolerance\*
    array table, optional. Colors in `small_image` whose color difference from `color*` is within `color_tolerance*` are not drawn onto `large_image`. By default, no colors are ignored.

## Returns
- large_image
    ImageObject, returns the large image itself.

## Notes
Draws another image onto an image.
This affects the object itself.
For performance, this function does not create a data copy during the operation.
