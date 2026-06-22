# Dialog:add_switch

Purpose: Add a switch to a dialog.

## Signature
```lua
dialog_object = dialog_object:add_switch(switch_label [, default_state ])
```

## Example
```lua
local c, s = dialog():add_switch('Switch', false):show()
sys.alert(s["Switch"])
```

## Parameters
- switch_label
    string, the label displayed on the left side of the switch.
- default_state
    boolean, optional. Initial switch state; `true` means on, `false` means off. Defaults to `false`.

## Returns
- dialog_object
    Dialog, returns the dialog itself.
- Return type when using `:show()`
    boolean, returns the final switch state.

## Notes
Adds a switch to the dialog.
