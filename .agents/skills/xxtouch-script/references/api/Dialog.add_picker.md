# Dialog:add_picker

Purpose: Add a picker to a dialog.

## Signature
```lua
dialog_object = dialog_object:add_picker(picker_label, option_list [, default_selected_item ])
```

## Example
```lua
local c, s = dialog():add_picker('Picker', {'Choice 1', 'Choice 2', 'Choice 3'}):show()
sys.alert('Your choice: '..s['Picker'])
```

## Parameters
- picker_label
    string, the label displayed on the left side of the picker.
- option_list
    table, an ordered list of option names for the picker. Option names must not be duplicated.
- default_selected_item
    string, optional. The option name selected by default; defaults to the first item in `option_list`.

## Returns
- dialog_object
    Dialog, returns the dialog itself.
- Return type when using `:show()`
    string, returns the selected option name.

## Notes
Adds a picker to the dialog.
