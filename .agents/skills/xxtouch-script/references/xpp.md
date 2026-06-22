# XPP Script Package

Use this slice when the project `AGENTS.md` or `.config` says `type` is `xpp`.

## Package Layout

XPP projects are package roots. Do not use the XXT single-script layout.

```text
project/
├── Info.lua
├── main.lua
├── module.lua
├── interface.xui
└── res/
    ├── icon.png
    └── button.png
```

- `Info.lua` defines package metadata, the default executable, icon, and optional configuration UI.
- `.lua` and `.xxt` modules usually live at package root and can be loaded with `require 'module'`.
- The default entry is `Executable` in `Info.lua`, often `main.lua`.
- The optional configuration UI is `MainInterfaceFile` in `Info.lua`, usually a `.xui` or `.xuic` file.
- Runtime resources should be placed under `res/` and resolved with `xpp.resource_path('res/name.ext')`.

## Info.lua

Keep `Info.lua` side-effect free. It should return a metadata table. If the project template already uses `_config.bid` or `_config.name`, preserve those bindings unless the user asks to hardcode values.

```lua
return {
    BundleIdentifier = 'com.example.demo';
    BundleVersion = '1.0.0';
    BundleName = 'Demo';
    BundleDisplayName = 'Demo Script';
    BundleIconFile = 'appicon.png';
    Executable = 'main.lua';
    MainInterfaceFile = 'interface.xui';
    SupportedResolutions = {
        { width = 640; height = 1136; };
    };
    PackageControl = {
        AuthorName = 'Your Name';
    };
};
```

Common fields:

- `BundleIdentifier`: stable package id, usually reverse-DNS style.
- `BundleVersion`: package version shown to users and used for release tracking.
- `BundleName`: short package name.
- `BundleDisplayName`: display name; falls back to `BundleName` when omitted.
- `BundleIconFile`: icon file name inside the package.
- `Executable`: default runnable `.lua` or `.xxt` script.
- `MainInterfaceFile`: package configuration UI file.
- `SupportedResolutions`: optional device-size allowlist.
- `PackageControl`: optional author and package metadata table.

## Runtime APIs

Open these API slices before using or changing package-specific code:

- `references/api/xpp.runtime.md`: read current package metadata and resolve package paths/resources.
- `references/api/xui.md`: validate defaults, show/dismiss/reload UI, and read/write XUI config values.

## XXTDo

For XPP projects, treat XXTDo as available only if `XXTDo.lua` exists at the project root.

If the user asks to use XXTDo and `XXTDo.lua` is missing, install the bundled framework before writing code that uses it:

```bash
python3 scripts/install_xxtdo.py . --type xpp --apply
```

The installer copies `assets/frameworks/XXTDo.lua` to root `XXTDo.lua`.

```lua
local XXTDo = require 'XXTDo'
```

## XUI Config Example

`.xui` is the package configuration UI description file shown by the XXTouch App. User changes are saved under the `defaults` domain and each component `key`, then scripts read them through the `xui.*` APIs. Read `references/xui-format.md` first for the complete `.xui` format, component fields, themes, snippets, and APIs available inside XUI files.

Call `xui.setup` before reading saved values when you need defaults and type repair.

```lua
local defaults = 'com.example.demo'

xui.setup('interface.xui')

local enabled = xui.get(defaults, 'enabled')
local speed = tonumber(xui.get(defaults, 'speed') or 1)

if enabled then
    nLog('speed', speed)
end
```

Minimal `.xui` file:

```lua
return {
    title = 'Settings';
    defaults = 'com.example.demo';
    items = {
        {
            cell = 'Switch';
            label = 'Enabled';
            key = 'enabled';
            default = true;
        };
        {
            cell = 'TextField';
            label = 'Speed';
            key = 'speed';
            default = '1';
        };
    };
}
```

## Agent Rules

- If the project is XPP, do not create or reference `lua/scripts/main.lua` unless the project already uses that path in `Info.lua.Executable`.
- Use `xpp.resource_path(...)` for package resources instead of manually concatenating package paths.
- Update `Info.lua` when changing the entry script, display name, icon, or configuration UI file.
- Check `MainInterfaceFile` before assuming the config UI filename is `interface.xui`.
- Use `scripts/inspect_project.py` when project type, `Info.lua` entry, XUI file, resource strategy, or XXTDo location is unclear.
