# image.is

Purpose: ImageObject check

## Signature
```lua
is_image = image.is(value_to_check)
```

## Example
```lua
if image.is(img) then
    -- img is an ImageObject.
else
    -- img is not an ImageObject.
end
```

## Parameters
- value_to_check
    value, the value to check for whether it is an ImageObject.

## Returns
- is_image
    boolean, returns `true` if the value is an ImageObject; otherwise returns `false`.

## Notes
Checks whether a value is an ImageObject.
