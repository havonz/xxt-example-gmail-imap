# ImageObject:binaryzation

Purpose: Image binarization

## Signature
```lua
image = image:binaryzation({
    [white_background = white_background,]
    [csim_mode = similarity_mode,]
    [csim_algorithm = color_similarity_algorithm,]
    {color*, color_tolerance*},
    {color*, color_tolerance*},
    ...
})

image = image:binaryzation("cx*-cox*,cx*-cox*...")
```

## Example
```lua
local pic = screen.image(462, 242, 569, 272)
pic = pic:binaryzation("9D5D39-0F1F26,D3D3D2-2C2C2D")

local pic = screen.image(462, 242, 569, 272)
pic = pic:binaryzation({
    {0x9D5D39, 0x0F1F26},
    {0xD3D3D2, 0x2C2C2D},
})

local pic = screen.image(462, 242, 569, 272)
pic = pic:binaryzation({
    csim_mode = true,
    csim_algorithm = 2,
    white_background = true,
    {0x9D5D39, 90},
    {0xD3D3D2, 90},
})
```

## Parameters
- white_background
    boolean, optional. Whether to set the background to white. Defaults to `false`, meaning white foreground on black background.
- similarity_mode
    boolean, optional. Whether to use similarity mode. When enabled, `color_tolerance*` means similarity rather than color difference. Defaults to `false`.
- color_similarity_algorithm
    integer, optional. Color similarity algorithm, effective only in similarity mode. Defaults to `0`.
- color\*, color_tolerance\*
    integer, color value whitelist. `color*` is the color value itself, and `color_tolerance*` is the maximum color difference for `color*`.
- cx\*-cox\*
    string, color value whitelist. `cx*` is the hexadecimal text description of the color value itself, and `cox*` is the hexadecimal text description of the maximum color difference for `cx*`.

## Returns
- image
    ImageObject, returns the ImageObject itself after binarization.

## Notes
Binarizes the ImageObject.
For similarity algorithm conventions, see Visual API Conventions in `references/workflow.md`.
This affects the object itself.
For performance, this function does not create a data copy during the operation.
