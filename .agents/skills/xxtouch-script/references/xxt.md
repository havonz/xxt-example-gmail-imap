# XXT Single Script Project

Use this slice when the project `AGENTS.md` or `.config` says `type` is `xxt`.

## Project Layout

XXT projects build into a single encrypted `.xxt` script. The default entry is fixed.

```text
project/
├── .config
├── res/
│   └── target.png
└── lua/
    ├── helper.lua
    └── scripts/
        ├── main.lua
        └── screen_state.lua
```

- Entry script: `lua/scripts/main.lua`.
- Reusable Lua or encrypted `.xxt` modules: place under `lua/` or `lua/scripts/`.
- Runtime resources: place under `res/` and read with `XXT_RES_PATH..'/name.ext'`.
- For all built-in XXTouch path variables, read `references/api/xxt.env.md` and avoid hardcoded host paths.
- Temporary development files: place under `.tmp/` and run `scripts/ensure_config_ignores.py` to add `.tmp/` to `.config.ignores` and `.config.buildIgnores`.
- Do not create `Info.lua`, `.xui`, or XPP package metadata for an XXT project.
- If a single-script XXT project needs a configuration UI, use `dialog` / `Dialog` APIs instead of XUI.

## .config Notes

- `type` should be `xxt`.
- `bid` is the project identifier.
- `name` is the display name used by tooling.
- `entitlements.allow-external-require` controls whether the built `.xxt` can be required by other scripts.
- `ignores` should include generated local files such as `.tmp/` and Agent prompt files.
- `buildIgnores` can exclude files from the packaged output when needed.
- Use `scripts/ensure_config_ignores.py` instead of hand-editing the `.tmp/` ignore entries.

## XXTDo Detection

For XXT projects, treat XXTDo as available only if one of these files exists:

- `lua/XXTDo.lua`
- `lua/scripts/XXTDo.lua`

If the user asks to use XXTDo and neither file exists, install the bundled framework before writing the runloop:

```bash
python3 scripts/install_xxtdo.py . --type xxt --apply
```

The installer copies `assets/frameworks/XXTDo.lua` to `lua/XXTDo.lua` by default. If the project already uses `lua/scripts/XXTDo.lua`, it keeps that location.

For UI-state automation with XXTDo, read `references/xxtdo.md` and `references/xxtdo-patterns.md` before writing the runloop.

## Agent Rules

- Keep the entry at `lua/scripts/main.lua` unless the user asks to reorganize the project.
- Use `XXT_RES_PATH` for resources that ship with the project.
- Use `require 'module_name'` for project modules; do not require built-in XXTouch globals.
- Use `scripts/inspect_project.py` when project type, entry path, resource strategy, or XXTDo location is unclear.
- If XXTDo is present, it is acceptable to implement UI-state automation with the framework by default.
