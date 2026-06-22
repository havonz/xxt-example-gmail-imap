# ImageObject export

Purpose: Image encoding/export

## Signature
```lua
jpeg_image_data = image:jpeg_data([ image_quality ])
png_image_data = image:png_data()
image:save_to_jpeg_file(file_path [, image_quality ])
image:save_to_png_file(file_path)
image:save_to_album()
```

## Example
```lua
local img = screen.image()
file.writes("/var/mobile/1.jpg", img:jpeg_data(0.8))
file.writes("/var/mobile/1.png", img:png_data())
img:save_to_jpeg_file("/var/mobile/1.jpg", 0.8)
img:save_to_png_file("/var/mobile/1.png")
img:save_to_album()

local local_img = image.load_file("/var/mobile/1.png")
if image.is(local_img) then
    local_img:save_to_album()
end

local code, headers, body = http.get("https://www.xxtouch.app/img/Logo.png", 10)
if code == 200 then
    local remote_img = image.load_data(body)
    if image.is(remote_img) then
        remote_img:save_to_album()
    end
end
```

## Parameters
- file_path
    string, absolute path where the image file should be saved.
- image_quality
    number, optional JPEG image quality, in the range `0.0` to `1.0`. Defaults to `1.0`.

## Returns
- jpeg_image_data
    string, JPEG data. Modifying this data does not affect the ImageObject.
- png_image_data
    string, PNG data. Modifying this data does not affect the ImageObject.

## Notes
JPEG is lossy compression, while PNG is lossless encoding. `jpeg_data` / `png_data` return binary data suitable for writing files, uploading, or writing to the pasteboard. `save_to_*_file` writes files directly and does not enforce extension validation. `save_to_album` writes to the system photo library. Data export usually creates extra data copies; after high-frequency screenshot export, call `ImageObject:destroy()` promptly.
