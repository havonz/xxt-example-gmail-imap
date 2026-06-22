# lua-path

Sources:
- https://github.com/moteus/lua-path
- http://moteus.github.io/path/index.html

## Require

```lua
local path = require 'path'
```

## Join And Inspect Path

```lua
local path = require 'path'

local target = path.join(XXT_RES_PATH, 'images', 'button.png')
sys.log(path.dirname(target), path.basename(target), path.extension(target))
```

Use `path` when path string manipulation would be error-prone. For most XXTouch scripts, `XXT_HOME_PATH`, `XXT_RES_PATH`, and `XXT_SCRIPTS_PATH` plus simple suffixes are enough.

## Normalize User Suffix Under A Root

```lua
local path = require 'path'

local root = XXT_RES_PATH
local suffix = 'images/../images/button.png'
local target = path.normalize(path.join(root, suffix))

if target:sub(1, #root) ~= root then
    return nil, 'path escapes resource root'
end
```

## Iterate Matching Paths

```lua
local path = require 'path'

path.each(path.join(XXT_RES_PATH, '*.json'), function(filename)
    sys.log(filename)
end)
```

## Useful APIs

- `path.join(...)`
- `path.normalize(p)`
- `path.basename(p)`, `path.dirname(p)`, `path.extension(p)`
- `path.splitext(p)`, `path.splitpath(p)`
- `path.isabs(p)` / `path.isfullpath(p)`
- `path.currentdir()`, `path.chdir(p)`
- `path.exists(p)`, `path.isdir(p)`, `path.isfile(p)`
- `path.each(pattern, callback, options)` for tree iteration.

## Notes

- Prefer `file` or `lfs` APIs for filesystem operations; `path` is primarily for path strings.
- Do not normalize away user-provided absolute paths unless the task asks for it.
- Keep generated files under project or script resource paths by default.
- After normalization, verify the result is still inside the intended root before reading or writing user-derived paths.
