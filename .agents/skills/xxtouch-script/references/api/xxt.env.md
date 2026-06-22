# XXTouch Built-In Environment Variables

Use this slice when writing scripts that need XXTouch runtime paths or edition state. Prefer these runtime variables over hardcoded device paths or host-machine paths.

## Variables

| Variable | Meaning | Rootful / TrollStore value |
| --- | --- | --- |
| `XXT_HOME_PATH` | XXTouch home directory | `/var/mobile/Media/1ferver/` |
| `XXT_RES_PATH` | XXTouch resource directory | `/var/mobile/Media/1ferver/res/` |
| `XXT_SCRIPTS_PATH` | XXTouch script directory | `/var/mobile/Media/1ferver/lua/scripts/` |
| `XXT_LUA_PATH` | XXTouch Lua extension directory | `/var/mobile/Media/1ferver/lua/` |
| `XXT_LIB_PATH` | XXTouch C extension directory | `/var/mobile/Media/1ferver/lib/` |
| `XXT_LOG_PATH` | XXTouch log directory | `/var/mobile/Media/1ferver/log/` |
| `XXT_BIN_PATH` | bundled command or executable directory | derived from `XXT_HOME_PATH` |
| `XXT_TESSDATA_PATH` | Tesseract trained-data directory | derived from `XXT_HOME_PATH` |
| `IS_TROLLSTORE_EDITION` | whether runtime is TrollStore edition | boolean |

## Rules

- These variables are provided by the runtime. Do not redefine them in scripts.
- XXTouch 1.3.8 and later provide compatible values for rootful, rootless, roothide, and TrollStore environments.
- In XXT projects, packaged resources belong in `res/` and should be read with `XXT_RES_PATH..'/name.ext'`.
- In XPP projects, prefer `xpp.resource_path(...)` for package resources. Do not assume package resources are under `XXT_RES_PATH`.
- For jailbreak-root or system-root path conversion, read `references/api/rootfs.md` and use `jbroot(...)` / `rootfs(...)`.
- Chinese environment terms are mapped in `references/aliases.tsv` for lookup, but documentation prose should stay in English.
