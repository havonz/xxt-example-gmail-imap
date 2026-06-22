# lua-posix

Source: https://luaposix.github.io/luaposix/

## Require

```lua
local posix = require 'posix'
```

Use only when XXTouch `sys`, `file`, `lfs`, or `unix` APIs do not cover the needed POSIX behavior.

## Common Areas

- File metadata and permissions: prefer `lfs` or `unix` first.
- Directory iteration: prefer `file.list` or `lfs.dir`.
- Process, signal, terminal, and environment APIs: use only when explicitly requested.

## Safe Pattern

```lua
local posix = require 'posix'

local st, err = posix.stat(XXT_HOME_PATH..'/1ferver.conf')
if st then
    sys.log('mode', st.mode)
else
    sys.log('posix.stat failed', err)
end
```

## Permission And Directory Helpers

```lua
local posix = require 'posix'

local dir = XXT_HOME_PATH..'/tmp-posix'
local ok, err = posix.mkdir(dir)
if not ok and err then
    return nil, err
end

local changed, chmod_err = posix.chmod(dir, 'rwx------')
if not changed and chmod_err then
    return nil, chmod_err
end
```

## Glob Files

```lua
local posix = require 'posix'

local matches, err = posix.glob {
    pattern = XXT_RES_PATH..'/*.json',
    MARK = false,
}
if not matches then
    return nil, err
end
for _, filename in ipairs(matches) do
    sys.log(filename)
end
```

## Process APIs

Only use `posix.popen`, `posix.spawn`, or `posix.execx` when the user explicitly asks for subprocess behavior. Prefer XXTouch APIs for normal automation.

```lua
local posix = require 'posix'

local status, how = posix.spawn {'/bin/echo', 'hello'}
sys.log(status, how)
```

## Notes

- Many lua-posix functions return `nil, err`; handle both values.
- Avoid process control or shell execution unless the user explicitly asks for it.
- Prefer project paths and documented XXTouch constants over device-global paths.
- Permission modes are often strings like `'rwx------'`; do not mix them with numeric modes unless the target function documents numeric mode support.
