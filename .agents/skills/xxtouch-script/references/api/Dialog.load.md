# Dialog:load

Purpose: Load dialog configuration without showing the dialog.

## Signature
```lua
submitted, option_map = dialog_object:load()
```

## Example
```lua
local dlg = dialog()
dlg:set_config('test')
dlg:add_range('HP', {0, 1000, 1}, 300)
dlg:add_input('Account', 'ccc')
dlg:add_input('Password', 'aaaa')
dlg:add_switch('Enable Notifications', false)
dlg:add_checkbox('Favorite Games', {'Overwatch', 'World of Warcraft', 'Hearthstone'}, {'Overwatch'})
dlg:add_radio('Top Favorite Game', {'Overwatch', 'World of Warcraft', 'Hearthstone'}, 'World of Warcraft')

local _, selects
if utils.is_launch_via_app() then
    _, selects = dlg:show()
else
    _, selects = dlg:load()
end

print("Top favorite game:"..selects["Top Favorite Game"])
print("HP", selects["HP"])
print("Enable Notifications", selects["Enable Notifications"])
```

## Returns
- submitted
    boolean, retained for compatibility with the `:show` return format. This method always returns `false`.
- option_map
    table, a key-value table mapped by option labels.

## Notes
Loads dialog configuration without showing the dialog. If the dialog currently has no saved configuration, default values are loaded.
