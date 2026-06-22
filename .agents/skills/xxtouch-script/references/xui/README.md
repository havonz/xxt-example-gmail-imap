# XUI Reference

This directory is only for `.xui` / `.xuic` configuration UI in XPP script packages. Do not read or apply these documents for XXT single-script projects; use the `dialog` / `Dialog` APIs for ordinary in-script configuration UI.

## Reading Order

Choose the minimum files needed for the task:

| Task | Read First |
|---|---|
| Decide whether XUI should be used | `references/xpp.md`, then this file |
| Create or fix `.xui` root structure, themes, and configuration persistence | `format.md` |
| Choose components; confirm fields and saved value types | `modules.md` |
| Implement `TitleValue` selectors or `.snippet` files | `snippets.md` |
| Show UI from script code, generate default configuration, and read/write configuration | `../api/xui.md` |
| Need complete XPP context or cross-file examples | `examples/com.yourcompany.A-Script-Bundle.xpp/` |

## Usage Rules

- `.xui` is a UTF-8 text file that returns a Lua table; `.xuic` is an encrypted XUI file.
- `Info.lua.MainInterfaceFile` determines the package configuration entry file. Update `Info.lua` when changing the UI filename.
- `defaults` is the configuration domain, and each component `key` is a configuration key. In script code, prefer `xui.setup` to generate default configuration, then read values with `xui.get` / `xui.read`.
- Use `modules.md` as the source of truth for component fields, return value types, and available theme keys; use `../api/xui.md` for runtime API behavior.
- APIs available inside `.xui` and `.snippet` files are allowlisted; see "APIs Available Inside XUI" in `format.md`.

## Output Checklist

After creating or modifying XUI, check at least:

- The root table has `defaults` and `items`, and the entry UI file is referenced by `Info.lua.MainInterfaceFile`.
- Every component that needs to save configuration has a stable `key`, and its `default` type matches the component's saved value type.
- The `default` values for `Option` / `MultipleOption` / `OrderedOption` / `Segment` / `Radio` / `Checkbox` match `options[].value`.
- Each `Button` has matching `action` and `args` fields; omit `key` when the return value does not need to be saved.
- Script code calls `xui.setup("<ui>.xui")` before reading configuration; do not hand-write `uicfg/*.plist` paths.
