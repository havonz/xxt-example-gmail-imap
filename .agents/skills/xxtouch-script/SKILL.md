---
name: xxtouch-script
description: Use when writing, reviewing, debugging, or refactoring XXTouch Lua 5.3 scripts, XXT/XPP project files, XPP `.xui`/`.xuic` configuration UIs, screen/touch/image automation, or optional XXTDo runloop scripts.
---

# XXTouch Script

Use this skill to produce correct XXTouch Lua scripts while keeping context small.

All `references/`, `scripts/`, and `assets/` paths in this skill are relative to the skill root. When running helper scripts, invoke the helper from the skill root path and pass the target XXTouch project root as an argument when required.

## Reference Lookup

Do not write or change XXTouch API calls from memory when signatures, return values, callback shapes, or module availability matter.

- Read the project `AGENTS.md` first if present; determine project type (`xxt` or `xpp`) and whether XXTDo is present or requested.
- XPP `.xui` files and `xui.*` APIs apply only to XPP projects. In `xxt` projects, do not read `references/xui-format.md` or `references/xui/`, and do not create `Info.lua`, `.xui`, or `.xuic` files unless the user asks to convert to or inspect XPP/XUI.
- Before using an XXTouch API, search `references/api-index.tsv` and `references/aliases.tsv`, then open the matching `references/api/*.md` slice.
- Before editing an XXT single-script project layout, entry script, or resources, read `references/xxt.md`.
- Before editing an XPP script package, `Info.lua`, `.xui`/`.xuic`, or package resources, read `references/xpp.md`; only after confirming the project is XPP should you read `references/xui-format.md` for `.xui` format, components, themes, snippets, or configuration persistence behavior.
- Before relying on XXTouch path globals, rootless/rootful path compatibility, or default resource/log/model directories, read `references/api/xxt.env.md`.
- Before using XUI-engine `dialog` features such as custom button titles, groups, button callbacks, control objects, or `reload`, read `references/api/Dialog.xui.md`.
- Before using automatic system alert handling, read `references/api/alerthelper.md`.
- Before writing UI element automation or using `device_ui_element_*` MCP tools, read `references/third-party/ui_element.md`.
- Before using a bundled third-party module, read `references/third-party/index.md`, then open the matching module or topic slice.
- Before creating or consuming XXTLanControl human-assist tasks, read `references/human-assist.md`.
- Before writing XXTDo code, read `references/xxtdo.md` and `references/xxtdo-patterns.md`.
- If no reference slice covers the requested API, treat it as unknown and ask for clarification or inspect project-local code; do not invent APIs.

## Workflow

1. For API details, search bundled references before opening files:
   - `rg -n "<keyword|symbol>" references/api-index.tsv references/aliases.tsv`
   - Open only the matching files under `references/api/`, or the referenced topic file.
   - Check the signature first, then adapt the shortest matching example.
2. For non-trivial code changes, read `references/style.md`; for common screen/touch/image patterns, read `references/workflow.md`.
3. Treat XXTDo as available only when the user/project asks for it or the framework file already exists. When available, prefer it for UI-state automation unless the user asks for plain XXTouch code. If the user asks for XXTDo and it is missing, run `scripts/install_xxtdo.py <project-root> --apply`, then read the XXTDo references.
4. If a workflow needs screenshots, color samples, action points, rectangles, matrix dictionaries, or user confirmation, read `references/human-assist.md`; use the helper scripts there instead of hand-formatting Lua tables, editing `.config`, or deleting screenshots manually. If XXTLanControl assist tooling is unavailable, ask the user to provide the needed samples or screenshots.
5. When XXTLanControl MCP tools are available, use them for device-oriented validation when practical.

## Rules

- Use Lua 5.3 and documented XXTouch APIs only.
- For non-XPP projects that need temporary or in-script configuration UI, use `dialog` / `Dialog` APIs, including the XUI-backed dialog engine when appropriate.
- Built-in XXTouch modules such as `app`, `sys`, `touch`, `screen`, `image`, `file`, `http`, `json`, and `dialog` are globals; do not `require` them.
- Avoid local variable names that shadow built-in modules.
- Prefer `t[#t + 1] = value` instead of `table.insert(t, value)`.
- Do not use `os.execute` or `io.popen` unless explicitly requested.
- Prefer documented XXTouch APIs over third-party modules. Use third-party modules only when they solve a specific need not covered cleanly by built-ins.
- Do not assume host-specific absolute paths, usernames, workspace paths, private IPs, or local services. Use project-relative paths and placeholders unless the user provides concrete values.
- Treat XXTLanControl MCP tools as portable but optional in the current environment; continue with pure XXTouch script guidance when they are unavailable.
- Store temporary development artifacts under `.tmp/` and use `scripts/ensure_config_ignores.py` to ensure the project ignores that directory.
- In XXT projects, store runtime resources that must be packaged under `res/` and reference them with `XXT_RES_PATH`.
- In XPP projects, do not assume `lua/scripts/main.lua`; use `Info.lua.Executable` for the default entry and `xpp.resource_path(...)` for package resources.

## XXTDo Paths

- XPP project: root `XXTDo.lua`.
- XXT project: `lua/XXTDo.lua`, unless the project already uses `lua/scripts/XXTDo.lua`.
