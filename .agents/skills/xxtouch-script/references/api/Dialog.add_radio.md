# Dialog:add_radio

Purpose: Add a radio group to a dialog.

## Signature
```lua
dialog_object = dialog_object:add_radio(group_label, option_list [, default_selected_item ])
```

## Example
```lua
local c, s = dialog():add_radio('Radio Group', {'Radio 1', 'Radio 2', 'Radio 3'}):show()
sys.alert('Your choice: '..s['Radio Group'])
```

## Parameters
- group_label
    string, the title label displayed for the radio group.
- option_list
    table, an ordered list of option names in the radio group. Option names must not be duplicated.
- default_selected_item
    string, optional. The option name selected by default; defaults to the first item in `option_list`.

## Returns
- dialog_object
    Dialog, returns the dialog itself.
- Return type when using `:show()`
    string, returns the selected option name.

## Notes
Adds a radio group to the dialog.
