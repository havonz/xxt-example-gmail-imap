# screen.find_image

Purpose: Screen image search

## Signature
```lua
x, y = screen.find_image(image [, confidence, left, top, right, bottom ])
search_results = screen.find_image(image [, options, left, top, right, bottom ])
```

## Example
```lua
x, y = screen.find_image("/var/mobile/1.png", 95, 0, 0, 639, 1135)

local img = image.load_file("/var/mobile/1.png")
x, y = screen.find_image(img)
x, y = screen.find_image(img, 95)

local rets = screen.find_image(img, {
    confidence_threshold = 90,
    downscale = 0.5,
    find_all = true,
}, 0, 0, 0, 0)

local code, headers, body = http.get("https://www.xxtouch.app/img/find_image_test.png", 10)
if code == 200 then
    local remote_img = image.load_data(body)
    if remote_img then
        local x, y = screen.find_image(remote_img, 95)
        if x ~= -1 then touch.tap(x, y) end
        remote_img:destroy()
    end
end
```

## Parameters
- image
    string, image data to search for, which can be PNG or JPEG data.
    ImageObject, an image object.
    string, path to the image file to search for. If the string is not a valid path, it is parsed as image data.
- confidence
    integer, optional. Defaults to `95`. A match is returned only when the confidence of the found position is at least `95`. Range: `0` to `100`.
- options
    table, optional.

    ```lua
    {
        find_all = false | true,
        confidence_threshold = number_value(0.0 ~ 100.0),
        downscale = number_value(0.1 ~ 1.0),
        mask = image_object,
    }
    ```

    `find_all` defaults to `false`; `confidence_threshold` defaults to `95`; `downscale` defaults to `1.0`, where smaller values are faster but less accurate; `mask` uses a same-size binary image to mark the valid area, with white as valid and black as invalid.

- left, top, right, bottom
    integer, optional search region. Defaults to full screen.

## Returns
- x, y
    integer, when `options.find_all` is not `true`, returns only the coordinate of the highest-confidence result.
- search_results
    table

    ```lua
    {
        {
            x = integer_value,
            y = integer_value,
            confidence = number_value(0.0 ~ 100.0),
        },
        ...
    }
    ```

## Notes
Finds the position of an image on the screen. This function references the `image.cv` module.
For coordinate, region, miss return, and `find_all` conventions, see Visual API Conventions in `references/workflow.md`.
Note: for multi-resolution compatibility, capture the reference image on the device with the smallest resolution. Screenshots from larger resolutions cannot be matched on lower-resolution devices.
