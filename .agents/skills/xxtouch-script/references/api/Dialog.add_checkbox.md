# Dialog:add_checkbox

Purpose: Add a checkbox group to a dialog.

## Signature
```lua
dialog_object = dialog_object:add_checkbox(group_label, option_list [, default_selected_items ])
```

## Example
```lua
local c, s = dialog()
:add_checkbox('Feature Group', {'Option 1', 'Option 2', 'Option 3', 'Option 4'}, {'Option 1', 'Option 3'})
:show()
print('Selected '..#(s['Feature Group'])..' options')
print('Selected list:')
for _, oname in ipairs(s['Feature Group']) do
    print(oname)
end
sys.alert(print.out())
```

## Parameters
- group_label
    string, the title label displayed for the checkbox group.
- option_list
    table, an ordered list of option names in the checkbox group. Option names must not be duplicated.
- default_selected_items
    table, optional. List of option names selected by default; defaults to an empty table.

## Returns
- dialog_object
    Dialog, returns the dialog itself.
- Return type when using `:show()`
    table, an array table containing all selected items.

## Notes
Adds a checkbox group to the dialog.
