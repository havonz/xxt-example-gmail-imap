# app.png_data_for_bid

Purpose: App icon data

## Signature
```lua
png_image_data = app.png_data_for_bid(bundle_identifier)
```

## Example
```lua
-- Save the WeChat icon to the album.
image.load_data(app.png_data_for_bid("com.tencent.xin")):save_to_album()
```

## Parameters
- bundle_identifier
    string

## Returns
- png_image_data
    string | nil, the PNG binary data of the app icon, or `nil` if the app does not exist.
