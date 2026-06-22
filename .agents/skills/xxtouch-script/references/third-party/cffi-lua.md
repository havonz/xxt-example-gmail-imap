# cffi-lua

Source: https://github.com/q66/cffi-lua

## Require

```lua
local ffi = require 'ffi'
```

## Minimal Library Call

```lua
local ffi = require 'ffi'

ffi.cdef[[
int my_func(const char *text);
]]

local lib = ffi.load(XXT_RES_PATH..'/libmy.dylib')
local rc = lib.my_func('hello')
sys.log('rc', rc)
```

Use this shape only when the user provides the library path and C signature.

## Output Buffer Shape

```lua
local ffi = require 'ffi'

ffi.cdef[[
int fill_buffer(char *buf, int len);
]]

local lib = ffi.load(XXT_RES_PATH..'/libmy.dylib')
local buf = ffi.new('char[?]', 1024)
local n = lib.fill_buffer(buf, 1024)
if n < 0 then
    return nil, 'fill_buffer failed'
end
local text = ffi.string(buf, n)
```

## Pointer Checks

```lua
local ptr = lib.create_object()
if ptr == ffi.nullptr then
    return nil, 'create_object failed'
end
```

## Core Concepts

- `ffi.cdef` declares C types and functions.
- `ffi.load` loads a shared library.
- `ffi.new`, `ffi.cast`, and cdata values are not identical to plain Lua values.
- Use `ffi.nullptr` for null pointer checks rather than comparing cdata to `nil`.

## Offline Details

Open `cffi-lua-reference.md` for the offline API checklist: declaration/loading, allocation, casts, cdata strings, struct/array access, callbacks, lifetime rules, and LuaJIT compatibility gaps.

## Rules

- Use only when the user explicitly needs to call a C library that has no XXTouch or Lua wrapper.
- Do not use FFI for filesystem, HTTP, JSON, UI, or screen automation.
- Keep declarations minimal and local to the feature that needs them.
- Validate pointer lifetimes and buffer sizes before passing data across the boundary.
- Treat LuaJIT FFI examples as guidance only; `cffi-lua` intentionally differs in edge cases.

## Notes

- If a task can be solved with documented XXTouch APIs, do not introduce FFI.
- Require user-provided headers, signatures, or known-good sample code before writing nontrivial FFI.
- Keep cdata object lifetimes longer than any C call that uses their pointers.
