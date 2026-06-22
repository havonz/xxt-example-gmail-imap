# image.new_text_image

Purpose: Text image

## Signature
```lua
image = image.new_text_image(text[, {
   font = font,
   size = font_size,
   color = font_color,
   alpha = font_opacity,
   back_color = background_color,
   back_alpha = background_opacity,
}])
```

## Example
```lua
local img = image.new_text_image('Hello', {
    font = 'Arial',
    size = 32,
    color = 0xffffff,
    alpha = 255,
    back_color = 0x000000,
    back_alpha = 180,
})

img:save_to_png_file(XXT_HOME_PATH..'/tmp/text.png')
```

## Parameters
- text
    string, the text content to draw.
- font
    string, optional font for the text to draw. Defaults to `"Arial"`.
- font_size
    number, optional font size for the text to draw. Defaults to `20.0`.
- font_color
    integer, optional font color for the text to draw. Defaults to `0xffffff` (white).
- font_opacity
    integer, optional font opacity for the text to draw, in the range `0` to `255`. Defaults to `255`.
- background_color
    integer, optional image background color. Defaults to `0x000000` (black).
- background_opacity
    integer, optional image background opacity, in the range `0` to `255`. Defaults to `255`.

## Returns
- image
    ImageObject, returns a newly created ImageObject.

## Notes
Creates an ImageObject of suitable size and draws the text onto it.
This method creates a new ImageObject. To keep frequent usage efficient, use it together with the `image:destroy` method.
