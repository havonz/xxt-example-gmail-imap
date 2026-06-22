# lyaml

Use when an XXTouch script must read or write YAML. Prefer `json` or `plist` when the data format is under script control.

## Require
```lua
local lyaml = require 'lyaml'
```

## Read
```lua
local text = assert(file.reads(path))
local data = lyaml.load(text)
```

Use `lyaml.load(text, { all = true })` only when a YAML stream may contain multiple documents.

## Write
```lua
local yaml = lyaml.dump({ data })
assert(file.writes(path, yaml))
```

`lyaml.dump` expects a sequence of YAML documents. Wrap a single Lua table as `{ data }`. YAML implicit scalar typing may convert strings such as booleans or numbers; preserve exact scalar semantics with loader/dumper options only when the task requires it.
