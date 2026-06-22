# Dialog:set_frame

Purpose: Configure a dialog's position and size.

## Signature
```lua
dialog_object = dialog_object:set_frame(x, y, width, height)
```

## Example
```lua
local dlg = dialog()
dlg:set_frame(0, 0, 600, 800)
dlg:show()
```

## Parameters
- x, y
    integer, coordinates of the dialog object's upper-left corner.
- width, height
    integer, dialog object width and height. If not set, defaults to full-screen width and height.

## Returns
- dialog_object
    Dialog, returns the dialog itself.

## Notes
Configures a dialog's position and size, using square corners.
This method is valid only for dialogs using the webview engine.
