# XUI Format

`.xui` files are configuration UI description files for XPP script packages. Each file must return a Lua table. The XXTouch App renders the UI from root properties, the component list, and the theme, then saves user configuration by `defaults` / `key`.

## Minimal File

```lua
return {
    title = "Settings";
    defaults = "com.example.demo";
    items = {
        {
            cell = "Group";
            label = "General";
        };
        {
            cell = "Switch";
            label = "Enabled";
            key = "enabled";
            default = true;
        };
        {
            cell = "TextField";
            label = "Speed";
            key = "speed";
            default = "1";
            keyboard = "DecimalPad";
            alignment = "Right";
        };
    };
}
```

## Root Fields

| Field | Type | Description |
|---|---|---|
|`title`|string|Navigation bar title; localizable|
|`header`|string|Main header at the top of the page; localizable|
|`subheader`|string|Secondary header at the top of the page; localizable|
|`defaults`|string|Default configuration domain name, usually `BundleIdentifier`|
|`items`|component array|Component list rendered in order|
|`theme`|table|UI theme; components can override some keys with their own `theme`|
|`stringsTable`|string|Localization table name, default `Localizable`|

`defaults = "com.example.demo"` maps to configuration domain `com.example.demo`. Script code should not concatenate `uicfg/com.example.demo.plist` paths; prefer:

```lua
xui.setup("interface.xui")
local enabled = xui.get("com.example.demo", "enabled")
local config = xui.read("com.example.demo")
```

## Common Component Fields

| Field | Type | Description |
|---|---|---|
|`cell`|string|Component type; required|
|`label`|string|Left-side title or main display text, used according to component semantics; localizable|
|`defaults`|string|Overrides the root-level configuration domain|
|`key`|string|Configuration key name; required for components that save values|
|`default`|any|Default configuration value; its type should match the component's saved value|
|`value`|any|Static display value, or the immediate value for some components|
|`icon`|string|Icon path; prefer placing it under `res/`|
|`readonly`|boolean|When read-only, the component cannot be modified and cannot enter subpages|
|`height`|number|Component height; required for image components|
|`theme`|table|Component theme; merged with the root-level theme|

`default` is used to generate or repair configuration; `value` is mostly used for display. For input components, use `default` for default configuration unless the documentation explicitly requires `value`.

## Theme

Use `#RRGGBB` or `#RRGGBBAA` strings for colors.

| Scope | Theme Keys |
|---|---|
|Page|`style`, `tintColor`, `backgroundColor`, `separatorColor`, `backgroundImage`|
|Navigation bar|`navigationBarColor`, `navigationTitleColor`|
|Header and footer|`headerTextColor`, `subheaderTextColor`, `footerTextColor`, `headerBackgroundColor`, `footerBackgroundColor`|
|Common components|`cellBackgroundColor`, `disclosureIndicatorColor`, `selectedColor`, `highlightedColor`, `labelColor`, `valueColor`|
|Status colors|`dangerColor`, `warningColor`, `successColor`|

`style` can be `Grouped` or `Plain`; the default is `Grouped`.

```lua
theme = {
    style = "Grouped";
    tintColor = "#0A84FF";
    navigationBarColor = "#F9FAFB";
    navigationTitleColor = "#111827";
}
```

## Localization

Fields marked as "localizable" are resolved through the iOS localization table named by `stringsTable`. When localization is not needed, write the final display text directly.

## APIs Available Inside XUI

`.xui` and `.snippet` files run in a restricted Lua environment. Use only the following modules and functions. Do not call XXTouch APIs that are not listed here from `.xui` files.

| Module | Available Capabilities |
|---|---|
|`xpp`|XPP script package module|
|`xui`|Configuration UI module; reads/writes configuration and refreshes UI|
|`string`|`string.compare_version`|
|`app`|`app.open_url`|
|`screen`|`screen.size`|
|`sys`|`sys.version`, `sys.xtversion`|
|`device`|`device.type`, `device.name`|
|`plist`|`plist.read`, `plist.write`|
|`json`|`json.encode`, `json.decode`, `json.null`|

See `references/api/xui.md` for runtime `xui.*` signatures and return values.
