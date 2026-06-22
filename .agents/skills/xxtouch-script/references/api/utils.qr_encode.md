# utils.qr_encode

Purpose: QR code encode

## Signature
```lua
image = utils.qr_encode(text_content[, {
    size = size,
    fill_color = fill_color,
    shadow_color = shadow_color,
}])
```

## Example
```lua
local img = utils.qr_encode("https://www.xxtouch.app", {
    size = 320,
    fill_color = 0xff409bff,
    shadow_color = 0xff308bef,
})
img:save_to_album()

local img = utils.qr_encode("https://www.xxtouch.app", {
    size = 320,
    fill_color = 0xff000000, -- Fill with opaque black.
})
img:replace_color(0x00000000, 0xffffffff) -- Replace the transparent background with white.
img:save_to_album()
```

## Parameters
- text_content
    string, text content to encode into a QR code.
- size
    integer, side length of the QR code to encode. Defaults to `320`.
- fill_color
    integer, color used to fill the QR code image. Defaults to `0xff000000` (opaque black).
- shadow_color
    integer, QR code shadow. Defaults to `0x00000000` (fully transparent).

## Returns
- image
    ImageObject, the generated QR code ImageObject.

## Notes
Encodes text into a QR code image of the specified size with a transparent background color (`0x00000000`).
