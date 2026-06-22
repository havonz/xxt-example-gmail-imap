# Dialog:add_range

Purpose: Add a numeric range selector to a dialog.

## Signature
```lua
dialog_object = dialog_object:add_range(range_label, range_options [, default_position ])
```

## Example
```lua
local c, s = dialog():add_range('Number', {222, 666, 1}, 333):show()
sys.alert('Number: '..s['Number'])
```

## Parameters
- range_label
    string, the title label displayed for the numeric selector.
- range_options
    table, describes the range and step. Format: `{min_value, max_value, step_value}`.
    - min_value
        number, the leftmost position of the numeric selector.
    - max_value
        number, the rightmost position of the numeric selector.
    - step_value
        number, optional. Minimum movement unit of the selector; defaults to 1.
- default_position
    number, optional. Default value; defaults to `min_value`.

## Returns
- dialog_object
    Dialog, returns the dialog itself.
- Return type when using `:show()`
    number, returns the numeric value selected by the user.

## Notes
Adds a numeric range selector to the dialog.
