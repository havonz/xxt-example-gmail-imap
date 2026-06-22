# Dialog:set_size

Purpose: Configure a dialog's size.

## Signature
```lua
dialog_object = dialog_object:set_size(width, height)
```

## Example
```lua
local dlg = dialog()
dlg:set_size(600, 800)
dlg:show()
```

## Parameters
- width, height
    integer, dialog object width and height. If not set, defaults to full-screen width and height.

## Returns
- dialog_object
    Dialog, returns the dialog itself.

## Notes
Sets the dialog size. If the dialog is not full screen, it is centered on the screen and uses rounded corners with radius 10.
This method is valid only for dialogs using the webview engine.
