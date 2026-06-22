# cffi-lua Offline Reference

Sources:
- https://github.com/q66/cffi-lua
- https://luarocks.org/modules/q66/cffi-lua

XXTouch exposes cffi-lua as:

```lua
local ffi = require 'ffi'
```

Use this file before browsing. cffi-lua aims to be mostly LuaJIT FFI-compatible, but not bug-for-bug identical. In XXTouch examples, null pointers are represented with `ffi.nullptr`; do not compare cdata with `nil`.

## Minimal Workflow

```lua
local ffi = require 'ffi'

ffi.cdef[[
int puts(const char *s);
]]

local C = ffi.load(nil) -- C runtime when supported by the platform
C.puts('hello')
```

For symbols already loaded into the process:

```lua
local C = ffi.C
```

For app-bundled libraries:

```lua
local lib = ffi.load(XXT_RES_PATH..'/libdemo.dylib')
```

## Declarations

```lua
ffi.cdef[[
typedef unsigned long size_t;

typedef struct demo_handle demo_handle;

demo_handle *demo_open(const char *path);
int demo_read(demo_handle *h, char *buf, size_t len);
void demo_close(demo_handle *h);
]]
```

Rules:

- Keep declarations minimal; declare only what the script calls.
- Prefer opaque structs (`typedef struct name name;`) when fields are not needed.
- Match C integer widths exactly when crossing binary protocols or ABI boundaries.
- Do not paste large system headers into `ffi.cdef`.

## Allocation And Strings

```lua
local buf = ffi.new('char[?]', 4096)
local n = lib.demo_read(handle, buf, 4096)
if n < 0 then
    return nil, 'read failed'
end
local data = ffi.string(buf, n)
```

Common shapes:

```lua
ptr = ffi.new('int[1]')
ptr[0] = 123

arr = ffi.new('uint8_t[?]', length)
text = ffi.string(char_ptr[, max_len])
typed = ffi.cast('const uint8_t *', arr)
```

Keep cdata alive for as long as C may use its pointer. Do not create a temporary buffer inline and store only the cast pointer.

## Null And Error Checks

```lua
local handle = lib.demo_open(path)
if handle == ffi.nullptr then
    return nil, 'demo_open failed'
end
```

cdata equality with Lua values such as `nil` is not a reliable null check.

## Structs And Arrays

```lua
ffi.cdef[[
typedef struct {
    int x;
    int y;
} point_t;
]]

local p = ffi.new('point_t')
p.x = 10
p.y = 20

local points = ffi.new('point_t[?]', 2)
points[0].x = 1
points[1].y = 2
```

Use zero-based indexes for C arrays.

## Cast, Size, Type

```lua
local p = ffi.cast('uint8_t *', buf)
local bytes = ffi.sizeof(buf)
local ctype = ffi.typeof('uint32_t')
local n = tonumber(ffi.cast('intptr_t', p))
```

Shapes used by XXTouch-side FFI code:

```lua
ffi.cast(cdecl, value)
ffi.new(cdecl[, init])
ffi.typeof(cdecl_or_cdata)
ffi.sizeof(cdecl_or_cdata)
ffi.tonumber(cdata_number)
ffi.istype(ctype, cdata)
ffi.type(cdata)
ffi.addressof(cdata)
```

Use `ffi.alignof` or `ffi.offsetof` only after checking the target runtime supports them.

## Finalizers

```lua
local handle = lib.demo_open(path)
if handle == ffi.nullptr then
    return nil, 'open failed'
end

ffi.gc(handle, lib.demo_close)

-- If closing explicitly:
lib.demo_close(handle)
ffi.gc(handle, nil)
```

## Copy, Fill, Errno

```lua
local buf = ffi.new('char[?]', 16)
ffi.fill(buf, 16, 0)
ffi.copy(buf, 'abc', 3)

local ok = lib.demo_call()
if ok ~= 0 then
    return nil, ffi.errno()
end
```

Only use `ffi.errno()` immediately after a C call whose contract reports `errno`.

Use explicit close for scarce resources. `ffi.gc` is a safety net, not lifecycle control.

## Callback Shape

Only add callbacks when the C API requires one and the callback lifetime is clear.

```lua
ffi.cdef[[
typedef int (*demo_cb)(const char *message, void *ctx);
void demo_each(demo_cb cb, void *ctx);
]]

local callbacks = callbacks or {}
callbacks.on_message = ffi.cast('demo_cb', function(message, ctx)
    sys.log(ffi.string(message))
    return 0
end)

lib.demo_each(callbacks.on_message, ffi.nullptr)
callbacks.on_message = nil
```

Keep callback cdata reachable until C is done. Releasing too early can crash the process.

## When Not To Use FFI

- Filesystem, HTTP, JSON, plist, UI, touch, screen automation: use XXTouch APIs.
- Objective-C interaction: use `objc` first; see `lobjc.md`.
- Crypto: use `openssl` or XXTouch string helpers first.
- Unknown C signatures: ask for headers or known-good sample code.

## Crash-Safety Rules

- Prefer running risky FFI/objc experiments through `fork_dostring`; see `lobjc.md`.
- Validate all pointer returns before dereferencing.
- Check buffer lengths before writing or reading.
- Keep owning cdata and callbacks alive longer than C uses them.
- Treat LuaJIT FFI examples as syntax guidance, not guaranteed cffi-lua behavior.
