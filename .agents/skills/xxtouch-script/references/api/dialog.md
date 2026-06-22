# dialog

Purpose: Create a dialog object.

## Signature
```lua
dialog_object = dialog()
dialog(popup_content, timeout_seconds)
```

## Example
```lua
dialog():show()

dialog('Hello, XXTouch!', 10)
```

## Returns
- dialog_object
    Dialog, returns a newly created dialog object.

## Notes
Creates a dialog object.

Note: this function does not accept parameters. Calling it with parameters shows a popup. Declaration:

```lua
dialog(popup_content:string, timeout_seconds:number)
```

The dialog UI uses the webview engine by default. In TrollStore builds or on iOS 16 and later, the XUI engine is used by default.

Force a specific engine with:
```lua
dialog.engine = "webview" -- Force the webview engine.
dialog.engine = "xui"     -- Force the XUI engine.
```

For XUI-engine specific controls, custom close/submit titles, groups, button callbacks, control object return values, `:reload()`, and XUI-only layout limits, read `references/api/Dialog.xui.md`.
