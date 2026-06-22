# ImageObject:qr_decode

Purpose: QR code decode

## Signature
```lua
recognized_text = image:qr_decode()
```

## Example
```lua
-- Decode a QR code currently displayed on the screen.
local str = screen.image():qr_decode()
if str then
    sys.alert("Recognition succeeded\nResult: "..str)
else
    sys.alert("Recognition failed")
end

-- Decode a local QR code image file.
local img = image.load_file("/var/mobile/qr.png")
if img then
    local str = img:qr_decode()
    img:destroy()
    if str then
        sys.alert("Recognition succeeded\nResult: "..str)
    else
        sys.alert("Recognition failed")
    end
else
    sys.alert("Failed to load image file; the file may not exist")
end
```

## Returns
- recognized_text
    string | nil, the text decoded from the QR code, or `nil` if the image is not a QR code or cannot be decoded.

## Notes
Decodes an image containing a QR code. The image may contain a small number of interfering elements and does not need to be a pure QR code.
