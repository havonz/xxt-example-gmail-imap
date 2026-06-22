# utils.is_launch_via_app

Purpose: Detect launch from App

## Signature
```lua
launched_via_app = utils.is_launch_via_app()
```

## Example
```lua
local dlg = dialog():set_config('script-options')
dlg:add_switch('Enable notifications', true)

local _, opts
if utils.is_launch_via_app() then
    _, opts = dlg:show()
else
    _, opts = dlg:load()
end
```

## Returns
- launched_via_app
    boolean, returns `true` if the current script was started from the launch button inside the app; otherwise returns `false`.

## Notes
Determines whether the current script was started from the launch button inside the app.
