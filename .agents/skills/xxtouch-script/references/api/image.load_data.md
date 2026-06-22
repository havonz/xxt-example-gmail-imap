# image.load_data

Purpose: Create image from data

## Signature
```lua
image = image.load_data(image_data)
```

## Example
```lua
local code, headers, body = http.get('https://www.xxtouch.app/img/Logo.png', 10)
if code == 200 then
    local img = image.load_data(body)
    if image.is(img) then
        img:save_to_album()
    end
end
```

## Parameters
- image_data
    string, image data in PNG or JPEG format.

## Returns
- image
    ImageObject | nil, returns a newly created ImageObject, or `nil` if the data is not an image format.

## Notes
Creates an ImageObject from data.
This method creates a new ImageObject. To keep frequent usage efficient, use it together with the `image:destroy` method.
