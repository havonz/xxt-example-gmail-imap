# Dialog:set_corner_radius

Purpose: Configure a dialog's corner radius.

## Signature
```lua
dialog_object = dialog_object:set_corner_radius(corner_radius)
```

## Example
```lua
local dlg = dialog()
dlg:set_frame(0, 0, 600, 800)
dlg:set_corner_radius(50)
dlg:show()
```

## Parameters
- corner_radius
    integer, corner radius. `0` means square corners.

## Returns
- dialog_object
    Dialog, returns the dialog itself.

## Notes
Configures a dialog's corner radius for scenarios that need rounded dialogs.
This method is valid only for dialogs using the webview engine.
