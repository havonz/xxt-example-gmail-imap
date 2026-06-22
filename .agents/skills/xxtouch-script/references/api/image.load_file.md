# image.load_file

Purpose: Create image from file

## Signature
```lua
image = image.load_file(file_path)
```

## Example
```lua
local img = image.load_file(XXT_SCRIPTS_PATH..'/target.png')
if image.is(img) then
    local w, h = img:size()
    nLog('image size', w, h)
end
```

## Parameters
- file_path
    string, absolute path to the image file.

## Returns
- image
    ImageObject | nil, returns a newly created ImageObject, or `nil` if the file does not exist.

## Notes
Creates an ImageObject from a file.
This method creates a new ImageObject. To keep frequent usage efficient, use it together with the `image:destroy` method.
