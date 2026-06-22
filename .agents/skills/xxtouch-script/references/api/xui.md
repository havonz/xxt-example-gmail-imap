# xui

Purpose: XUI configuration UI/read/write

Scope: XPP script bundles only. Do not use `xui.*` in XXT single-script projects; use the `dialog` / `Dialog` API when an in-script configuration UI is needed.

## Signature
```lua
xui.show(config_ui_file_name)
xui.dismiss()
xui.reload()
xui.setup(config_ui_file_name)
value = xui.get(config_section, config_key)
success = xui.set(config_section, config_key, value)
config = xui.read(config_section)
success = xui.write(config_section, config)
success = xui.clear(config_section)
```

## Example
```lua
xui.setup("interface.xui")
local section = "com.yourcompany.A-Script-Bundle"
local enabled = xui.get(section, "enabled")

xui.set(section, "enabled", true)
local dict = xui.read(section)
dict.enabled = true
xui.write(section, dict)
xui.setup("interface.xui")

xui.show("interface.xui")
xui.reload()
xui.dismiss()
```

## Parameters
- config_ui_file_name
    string, `.xui` file name in the current script bundle.
- config_section
    string, defaults identifier for the configuration section in the configuration UI.
- config_key
    string, control key identifier.
- value
    any type. Different control types use different values.
- config
    table, key-value pairs for the configuration section.

## Returns
- value
    any type; returns nil when the configuration value does not exist.
- config
    table; returns an empty table when the configuration section does not exist.
- success
    boolean.

## Notes
`xui.setup` generates default configuration and validates/corrects stored value types according to XUI control declarations. `get/read` do not filter value types, so you can call `setup` before reading. `set` writes a single key, and `write` overwrites the entire configuration section. If the UI is currently displayed, written values are reflected immediately. You can call `setup` again after writing to validate. `show` is non-blocking, and display failures are shown inside the app. `dismiss` only jumps to the app when no UI is displayed. `reload` does nothing when no UI is displayed, and frequent calls may make the app lag. See `references/xpp.md` for the XPP bundle structure and XUI configuration entry point.
`xui.clear` clears the entire configuration section. It usually returns false if the configuration does not exist. After clearing, call `xui.setup(...)` again to generate default configuration; if the UI is currently displayed, values update immediately.
