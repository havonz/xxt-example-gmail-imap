# Dialog:set_timeout

Purpose: Configure the time before a dialog disappears automatically.

## Signature
```lua
dialog_object = dialog_object:set_timeout(timeout_seconds[, submitted])
```

## Example
```lua
dialog():set_timeout(3):show() -- Timeout after 3 seconds and cancel submission.

dialog():set_timeout(3, true):show() -- Timeout after 3 seconds and submit.
```

## Parameters
- timeout_seconds
    number, time in seconds before the dialog object disappears automatically.
- submitted
    boolean, optional. Whether automatic disappearance due to timeout is treated as submission; `true` means submit, `false` means do not submit. Defaults to `false`.

## Returns
- dialog_object
    Dialog, returns the dialog itself.

## Notes
Configures the time before a dialog disappears automatically.
