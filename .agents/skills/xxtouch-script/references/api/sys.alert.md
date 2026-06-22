# sys.alert

Purpose: Show system alert

## Signature
```lua
choice = sys.alert(text_content [, auto_dismiss_seconds, title, button0_title, button1_title, button2_title ])
```

## Example
```lua
local choice = sys.alert('Please choose an action', 10, 'Your Choice', 'Cancel', 'Eat', 'Sleep')
if choice==0 then
    sys.alert('You chose "Cancel"')
elseif choice==1 then
    sys.alert('You chose "Eat"')
elseif choice==2 then
    sys.alert('You chose "Sleep"')
elseif choice==3 then
    sys.alert('No choice was made; timed out')
else
    sys.alert('SpringBoard crashed')
end
```

## Parameters
- text_content
    string, popup alert content.
- auto_dismiss_seconds
    number, optional auto-dismiss time for the popup, in seconds. Set `0` to disable auto-dismiss. Defaults to `0`.
- title
    string, optional popup alert title. Defaults to `"Script Alert"`.
- button0_title
    string, optional title of the default button in the popup alert. Defaults to `"OK"`.
- button1_title
    string, optional title of the first extra button in the popup alert. This button is hidden by default.
- button2_title
    string, optional title of the second extra button in the popup alert. This button is hidden by default.

## Returns
- choice
    integer
    - Returns `0` when button 0, the cancel button, is selected.
    - Returns `1` when button 1 is selected.
    - Returns `2` when button 2 is selected.
    - Returns `3` when the dialog times out after reaching the auto-dismiss duration.
    - Returns `71` when SpringBoard crashes while waiting.

## Notes
Shows a system alert dialog with up to 3 buttons, blocking all threads while waiting for the return value.
In versions after 20260108, this function yields in a multitasking environment.
