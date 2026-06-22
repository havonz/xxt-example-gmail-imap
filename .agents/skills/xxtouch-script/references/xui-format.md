# XUI Format

This slice applies only to XPP script packages. Before reading or applying it, confirm the project is XPP: `Info.lua` exists, `.config` / `AGENTS.md` declares `type = xpp`, or the user explicitly asks to handle XPP / XUI / `.xui` / `.xuic`. If the current project is an XXT single-script project, do not read `references/xui/` and do not create `.xui` files; ordinary in-script configuration UI should use the `dialog` / `Dialog` APIs.

`.xui` is the configuration UI description file for an XPP script package: it is UTF-8 Lua text that returns a table describing root properties, a component list, and component properties. The XXTouch App renders the configuration UI from it. After the user completes configuration, values are saved by `defaults` domain and component `key`; scripts read or maintain those values through `xui.setup`, `xui.get`, `xui.read`, `xui.set`, `xui.write`, `xui.clear`, and related APIs. `.xuic` is an XUI file encrypted by the App.

## Documentation Entry Points

Read the minimum files needed for the task; do not expand the whole directory at once:

| Task | Read |
|---|---|
| Confirm how to use the XUI directory and its checklist | `references/xui/README.md` |
| Create or modify root structure, common fields, themes, configuration persistence, and APIs available inside XUI | `references/xui/format.md` |
| Choose components; confirm fields, default value types, saved value types, and button actions | `references/xui/modules.md` |
| Create or call `.snippet` / `TitleValue` selectors | `references/xui/snippets.md` |
| Show UI from script code, generate default configuration, and read/write configuration values | `references/api/xui.md` |
| Package structure, `Info.lua.MainInterfaceFile`, resource paths, and entry-script rules | `references/xpp.md` |

If the bundled XUI documentation is missing, first search the current project for existing `.xui` files. If none are found, use only the confirmed bundled API slices and tell the user the XUI format documentation is missing; do not invent fields.

## Example Package

When you need the full project structure or cross-file relationships, read `references/xui/examples/com.yourcompany.A-Script-Bundle.xpp/`:

- `Info.lua`: `MainInterfaceFile`, entry script, icon, version, bundle identifier, and `PackageControl` metadata.
- `interface.xui`: root properties, `defaults`, groups, links, buttons, single/multiple/ordered options, editable lists, segments, radio/checkbox controls, sliders, steppers, text fields, and static text.
- `another_ui.xui`: another UI file in the same XPP package, plus a root-level `theme`.
- `sub/xui-sub.xui`: subpage, `Image` / `AnimatedImage`, switches, `TitleValue`, snippet selectors, file selectors, date-time controls, run-script buttons, and text areas.
- `snippets/*.snippet`: how `TitleValue` uses snippets to select applications, multiple applications, locations, keys, point colors, regions, and other configuration values.
- The example package keeps resource path references to demonstrate XUI syntax, but it does not bundle binary resources such as images, GIFs, or videos.

## Responsibilities

- Use `references/xui/*.md` as the source of truth for XUI file format, component fields, and UI behavior.
- Use `references/api/xui.md` as the source of truth when runtime scripts show UI, generate default configuration, or read/write configuration values.
- Use `references/xpp.md` as the source of truth for XPP package structure, resource paths, and entry-script rules.
