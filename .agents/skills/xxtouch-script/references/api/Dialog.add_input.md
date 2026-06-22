# Dialog:add_input

Purpose: Add a text input field to a dialog.

## Signature
```lua
dialog_object = dialog_object:add_input(input_label [, default_content ])
```

## Example
```lua
local c, s = dialog():add_input('Input Field', 'Default content'):show()
sys.alert('Input content: '..s['Input Field'])
```

## Parameters
- input_label
    string, the label displayed on the left side of the text field.
- default_content
    string or number, the default value in the text field.

## Returns
- dialog_object
    Dialog, returns the dialog itself.
- Return type when using `:show()`
    string, returns the user input.

## Notes
Adds a text input field to the dialog.
