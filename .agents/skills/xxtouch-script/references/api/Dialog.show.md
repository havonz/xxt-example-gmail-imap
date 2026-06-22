# Dialog:show

Purpose: Show a dialog and return the user's selections.

## Signature
```lua
submitted, option_map = dialog_object:show()
```

## Example
```lua
local ok, values = dialog():add_switch('Enable Notifications', false):show()
if ok and values['Enable Notifications'] then
    sys.toast('Notifications enabled')
end
```

## Combined Controls Example
```lua
local dlg = dialog()
dlg:set_config('demo')
dlg:set_timeout(30)
dlg:add_label('Script Configuration')
dlg:add_range('HP', {0, 1000, 1}, 300)
dlg:add_input('Account', 'user')
dlg:add_input('Password', '')
dlg:add_picker('Gender', {'Male', 'Female', 'Unknown'}, 'Unknown')
dlg:add_switch('Enable Notifications', false)
dlg:add_checkbox('Favorite Games', {'Overwatch', 'World of Warcraft', 'Hearthstone'}, {'Overwatch'})
dlg:add_radio('Top Favorite Game', {'Overwatch', 'World of Warcraft', 'Hearthstone'}, 'World of Warcraft')

local confirm, selects = dlg:show() -- Show the dialog object in the foreground and get its return value.

if confirm then
    print('Account', selects['Account'])
    print('HP', selects['HP'])
    print('Enable Notifications', selects['Enable Notifications'])
    for _, name in ipairs(selects['Favorite Games']) do
        print('Liked', name)
    end
    print('Top favorite game', selects['Top Favorite Game'])
end
```

## Returns
- submitted
    boolean, returns whether the Submit button was pressed. Timeout or tapping the top-right X returns `false`.
- option_map
    table, a key-value table mapped by option labels.

## Notes
Shows the dialog and returns the user's selection result.
If the dialog has configuration saving enabled with `:set_config(config_name)`, pressing Submit saves the configuration. Tapping the top-right X or timing out does not save it.
