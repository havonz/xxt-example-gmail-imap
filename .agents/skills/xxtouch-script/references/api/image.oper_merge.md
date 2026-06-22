# image.oper_merge

Purpose: Image merge

## Signature
```lua
status = image.oper_merge(image_file_name_array, output_path, merge_type, output_quality)
```

## Example
```lua
image.oper_merge({"1.png","2.png","3.png"}, "4.jpg", 0, 0.5)
```

## Parameters
- image_file_name_array
    table, list of image file names to merge. Absolute paths are supported.
- output_path
    string, file name for the generated image. Absolute paths are supported.
- merge_type
    integer, merge type. `0` means horizontal merge; `1` means vertical merge.
- output_quality
    number, controls image quality when the generated image format is JPG, in the range `0.0` to `1.0`.

## Returns
- status
    integer, `0` means success; `1`, `2`, and `3` mean failure.

## Notes
Relative paths are resolved under `/var/mobile/Media/1ferver/res/`. Use absolute paths to specify another directory.
