# lobjc Objective-C Bridge Details

Read `lobjc.md` first. Use this file for concrete `objc` API shapes.

## Classes And Objects

```lua
local ffi = require 'ffi'
local objc = require 'objc'

local NSString = objc.NSString
local NSString2 = objc.class('NSString')
local NSString_meta = objc.metaclass(NSString)
local NSObject = objc.superclass(NSString)

local obj = objc.object(address)
local obj2 = ffi.cast('id', address)
```

Create a class only when a documented XXTouch API cannot solve the task:

```lua
local cls = objc.newclass('XXTCustomClass', objc.NSObject, {
    {name = 'payload', size = 8, alignment = 4, types = '@'},
})
```

`objc.newclass(name, superclass[, ivars])` returns the new class, or `nil` when the class cannot be created, including when the class already exists.

## Chained Method Calls

Use dot syntax to build selector pieces, then an empty call `()` to invoke.

```lua
local objc = require 'objc'
local ffi = require 'ffi'

local path = objc.NSFileManager.defaultManager().currentDirectoryPath()
local ok = objc.NSFileManager.defaultManager().fileExistsAtPath('1.txt')()

local e = objc.NSException
    .exceptionWithName('Unknown Exception')
    .reason('The exception reason is unknown')
    .userInfo(0)()

local str = objc.NSString.stringWithFormat('Hello %ld, %C%C',
    ffi.cast('long', 123456),
    ffi.cast('int', 0x4f60),
    ffi.cast('int', 0x597d))()
```

For Objective-C `id` parameters, Lua strings convert to `NSString`, tables convert to `NSArray` or `NSDictionary`, and `0` can represent nil.

## Method Invoker

Use this when passing all arguments at once is clearer.

```lua
local objc = require 'objc'
local ffi = require 'ffi'

local NSStringWith = objc.NSString('stringWithUTF8String:')
local NSStringWithFormat = objc.NSString('stringWithFormat:')

local a = NSStringWith('Hello')
local b = NSStringWithFormat('Hello %ld', ffi.cast('long', 123456))
```

## NSError Pointer Pattern

```lua
local ffi = require 'ffi'
local objc = require 'objc'

local perr = ffi.new('id[1]')
local data = objc.NSData
    .dataWithContentsOfFile(XXT_RES_PATH..'/1.json')
    .options(0)
    .error(perr)()

if data == 0 or data == objc.null then
    local err = perr[0]
    return nil, err and err.localizedDescription().UTF8String()
end
```

`objc.null` and `ffi.nullptr` both represent Objective-C/C null. Use one explicit null check before sending messages to an object that may not exist.

## Lua And Objective-C Conversion

```lua
local objc = require 'objc'

local num = objc.toobj(123)
local str = objc.toobj('Hello World')
local arr = objc.toobj{'Hello', 100, 88}
local dic = objc.toobj{Hello = 'World', World = 'XXT'}

local lua_value = objc.tolua(dic)
```

Options:

```lua
local empty_arr = objc.toobj({is_an_array = true}, {array_flag = 'is_an_array'})
local data = objc.toobj('NSDATA:Hello World', {data_prefix = 'NSDATA:'})
local nested = objc.toobj({a = {}, b = {2}}, {empty_table_to_array = true})
```

## Enumerating Containers

```lua
local objc = require 'objc'

local arr = objc.toobj{'Hello', 100, 88}
for i, v in objc.ipairs(arr) do
    sys.log(i, v)
end

local dic = objc.toobj{Hello = 'World', World = 'XXT'}
for k, v in objc.pairs(dic) do
    sys.log(k, v)
end
```

`objc.ipairs` supports `NSArray` and `NSDictionary`; `objc.pairs` is for `NSDictionary`.

## Ivars

```lua
local objc = require 'objc'

local app = objc.UIApplication.sharedApplication()
local delegate = app['$ivars']._delegate
local all = app['$ivars']()
```

Setting ivars is risky; avoid it unless the target ivar and value type are known.

## Blocks

```lua
local objc = require 'objc'

local keep_block
keep_block = objc.block(function(line, stop)
    sys.log(line.UTF8String())
end, 'v@^B')

local str = objc.toobj('a\nb\nc\n')
str.enumerateLinesUsingBlock(keep_block)()
keep_block = nil
```

Type encodings are required. Keep block references alive until asynchronous Objective-C code finishes.

Calling a block object:

```lua
local blk = objc.block(function(dict)
    sys.log(tostring(dict))
end, 'v@')

blk('v@', {a = 1, b = 2})
```

For asynchronous Objective-C APIs, keep the block in an outer local until completion. In child-process code, call `os.exit()` after sending the final `proc_queue_push` message.

## Fixed Blocks For arm64e

Use this when normal `objc.block` is unreliable in an arm64e app context.

```lua
local objc = require 'objc'
local ffi = require 'ffi'

local function fixed_block_2_id(func)
    local cb = new_fixed_block_8(function(a1, a2)
        return func(ffi.cast('id', a1), ffi.cast('id', a2))
    end)
    cb = ffi.cast('id', cb)
    ffi.gc(cb, release_fixed_block)
    return cb
end
```

## objc.choose

Use `objc.choose` in isolated code (`fork_dostring` or `app.eval`) when scanning live Objective-C objects.

```lua
local objc = require 'objc'

for _, item in ipairs(objc.choose('UIBarButtonItem') or {}) do
    if item.title().UTF8String() == 'Agree' then
        dispatch_sync('main', function()
            item.target().agreeItemTapped(0)()
        end)
        break
    end
end
```

## GCD Helpers

```lua
dispatch_sync('main', function()
    -- UIKit work
end)

dispatch_async('main', function()
end)

dispatch_after(1000, 'concurrent', function()
end)

dispatch_async(dispatch_get_work_queue(), function()
end)
dispatch_async(dispatch_get_work_queue('Other VM'), function()
end)
```

Queues: `'main'`, `'concurrent'`, and app-eval work queues. UIKit changes belong on `'main'`.

## Methods, Properties, Selectors

```lua
local objc = require 'objc'

local has = objc.responds(objc.NSString, 'UTF8String')
local sel = objc.SEL('UTF8String')

obj.field = value        -- setter: obj.setField(value)()
local value = obj.field() -- getter
```

Method implementation APIs:

```lua
local cls = objc.newclass('XXTCustomLogWindow', objc.UIWindow)
if cls then
    objc.addmethodimp(cls, '_ignoresHitTest', function(self, cmd)
        return true
    end, 'B@:')
end

local orig = objc.setmethodimp(objc.metaclass(objc.NSDictionary),
    'newWithContentsOf:immutable:',
    function(self, cmd, path, immutable)
        sys.log(path, immutable)
        return orig(self, cmd, path, immutable)
    end,
    '@@:@@')
```

`objc.methodimp(class_or_metaclass, selector)` returns an existing implementation, or `nil` when the selector is not implemented on that class. Save the original implementation before replacing methods that must continue to call through.

## Exception Handling

```lua
local objc = require 'objc'

local ok, err = objc.try(function()
    local e = objc.NSException
        .exceptionWithName('Unknown Exception')
        .reason('The exception reason is unknown')
        .userInfo(0)()
    objc.throw(e)
end)

if not ok then
    if type(err) == 'string' then
        sys.log(err)
    else
        sys.log(err.name().UTF8String(), err.reason().UTF8String())
    end
end
```

`objc.try_catch(try_func, catch_func)` catches Objective-C exceptions and calls `catch_func(exception)`.

## Autorelease Pool

```lua
local objc = require 'objc'

autoreleasepool(function()
    objc.NSString.stringWithUTF8String('Hello')()
end)

local wrapped = autoreleasewrap(function(text)
    objc.NSString.stringWithUTF8String(text)()
end)
wrapped('Hello')
```

Use pools around loops that create many Objective-C objects.
