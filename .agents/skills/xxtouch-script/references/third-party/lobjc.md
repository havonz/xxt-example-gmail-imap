# lobjc / objc Bridge

Use `objc` only when XXTouch APIs and documented Lua modules cannot solve the task. It bridges Lua, FFI, and Objective-C objects, so crashes and memory/lifecycle bugs are possible.

## First Choice: Run Risky Code In A Child Process

Prefer `fork_dostring` for exploratory, private API, UIKit, or memory-sensitive Objective-C work. It isolates failures from the main script process and gives the caller a timeout.

```lua
-- fork_dostring(luacode, timeout_ms)
thread.dispatch(function()
    local out, ok, statusText, statusCode, err = fork_dostring([[
        local objc = require 'objc'
        print('child process started')
        proc_queue_push('child-process-message-1', 'ok')
    ]], 5000)

    nLog('output', out)
    if not ok then
        nLog('child process failed', statusText, statusCode, err)
    end
end)

thread.register_event('child-process-message-1', function(msg)
    nLog('received child process message', msg)
end)
```

Return values:

```lua
out, ok, statusText, statusCode, err = fork_dostring(luacode, timeout_ms)
```

- `out`: child process stdout/stderr text captured by the caller.
- `ok`: whether the child process completed successfully.
- `statusText`, `statusCode`, `err`: status and failure details.

Passing dynamic values:

```lua
local target_path = XXT_RES_PATH..'/sample.json'
local lua = ([[
    local objc = require 'objc'
    local data = objc.NSData.dataWithContentsOfFile(%q)()
    if data == 0 or data == objc.null then
        proc_queue_push('objc-read-result', 'missing')
    else
        proc_queue_push('objc-read-result', tostring(data.length()))
    end
]]):format(target_path)

thread.dispatch(function()
    local out, ok, statusText, statusCode, err = fork_dostring(lua, 5000)
    if not ok then
        nLog('objc child failed', statusText, statusCode, err, out)
    end
end)
```

Use `string.format('%q', value)` or another explicit serialization boundary when building child code. Do not concatenate untrusted text into Objective-C selectors, class names, or Lua source.

## Require

```lua
local ffi = require 'ffi'
local objc = require 'objc'
```

## Minimal Foundation Call

```lua
local objc = require 'objc'

local str = objc.NSString.stringWithUTF8String('Hello')()
sys.log(str.UTF8String())
```

The last empty `()` triggers the Objective-C call after a chain has been constructed.

## Async Objective-C Callback Shape

Use `fork_dostring` for Objective-C APIs that finish through blocks or require a run loop.

```lua
fork_dostring([[
    local objc = require 'objc'

    local handler
    handler = objc.block(function(success, error)
        if success then
            proc_queue_push('objc-task-result', 'ok')
        else
            local message = error ~= 0 and error.localizedDescription().UTF8String() or 'failed'
            proc_queue_push('objc-task-result', message)
        end
        os.exit()
    end, 'vB@')

    -- Start an Objective-C async task here and pass handler as its completion block.
    CFRunLoopRun()
]], 15000)
```

Keep block variables reachable until the callback fires. Exit the child process from the completion callback when the Objective-C API has no synchronous return.

## When To Use Directly

Direct `objc` in the main script is acceptable only for short, known-safe Foundation operations. For UI, hooks, class creation, `objc.choose`, blocks, or private selectors, use `fork_dostring` or `app.eval` isolation.

`app.eval` should only be used for XXTouch itself and SpringBoard contexts. Do not use it as a general way to inspect or automate third-party App internals.

## ObjC Extras Global Helpers

`lobjcextras.mm` registers global Lua helpers for GCD, CoreFoundation, notification centers, CPDistributedMessagingCenter, HID events, Blocks, pointer utilities, and time utilities. Pointer parameters usually accept `lightuserdata` or integers. Returned queues, RunLoops, CF objects, and handles should be treated as pointers.

These helpers are closer to system internals than ordinary `objc` calls. Prefer using them inside a `fork_dostring` child process. Use them directly in the main script only for short, synchronous, known-safe GCD or Foundation helpers.

### RunLoop Must Be Isolated

Do not use RunLoop-related functions in the main script. Do not call `CFRunLoopRun`, `CFRunLoopRunInMode`, or `CFRunLoopRunWithAutoreleasePool` in the main script. Do not create Timer, Source, Observer, notification listeners, `cpdistributed_messaging_center_run_server_on_current_thread`, or HID listeners that depend on the current RunLoop from the main script.

When a RunLoop is required, create a child process with `fork_dostring`, register callbacks and start the RunLoop inside that child process, send results back with `proc_queue_push`, then call `CFRunLoopStop()` or `os.exit()` to end the child process. The outer `fork_dostring` `timeout_ms` is the main script's fallback timeout.

```lua
thread.register_event('objc-runloop-result', function(msg)
    nLog(msg)
end)

thread.dispatch(function()
    local out, ok, statusText, statusCode, err = fork_dostring([[
        local objc = require 'objc'

        local timer
        timer = CFRunLoopTimerCreateWithHandler(nil, CFAbsoluteTimeGetCurrent() + 1, 0, 0, 0, function()
            proc_queue_push('objc-runloop-result', 'timer fired')
            CFRunLoopTimerInvalidate(timer)
            CFRunLoopStop()
        end)

        CFRunLoopAddTimer(CFRunLoopGetCurrent(), timer, 'kCFRunLoopDefaultMode')
        CFRelease(timer)
        CFRunLoopRun()
    ]], 5000)

    if not ok then
        nLog('runloop child failed', statusText, statusCode, err, out)
    end
end)
```

### GCD / Dispatch

- `dispatch_queue_attr_make_with_qos_class(attr, [qos]) -> attr_ptr`
- `dispatch_get_main_queue() -> queue_ptr`
- `dispatch_get_global_queue([qos]) -> queue_ptr`
- `dispatch_get_current_queue() -> queue_ptr`
- `dispatch_get_work_queue([name]) -> queue_ptr`
- `dispatch_queue_create(name, [attr]) -> queue_ptr`
- `dispatch_queue_create_with_target(name, attr, target_queue) -> queue_ptr`, iOS 10+
- `dispatch_queue_attr_make_initially_inactive(attr) -> attr_ptr`, iOS 10+
- `dispatch_queue_attr_make_with_autorelease_frequency(attr, frequency) -> attr_ptr`, iOS 10+
- `dispatch_sync(queue, func) -> nil`
- `dispatch_barrier_sync(queue, func) -> nil`
- `dispatch_async(queue, func) -> thread`
- `dispatch_barrier_async(queue, func) -> thread`
- `dispatch_after(ms, queue, func) -> thread`

`queue` may be `'main'`, `'concurrent'`, or a queue pointer. `dispatch_sync` executes directly when already on the same queue to avoid deadlocks. UIKit work still belongs on the main queue.

### Dispatch Source

```lua
local handle = dispatch_source_register_callback('timer', 1000, 1000, function(source)
    nLog('timer', source)
end, 'concurrent')
```

`dispatch_source_register_callback(type, handle, mask, func, [queue]) -> handle_obj` supports `data_add`, `data_or`, `mach_send`, `mach_recv`, `proc`, `read`, `signal`, `timer`, `vnode`, and `write`. When `type == 'timer'`, `handle` is the delay in milliseconds and `mask` is the interval in milliseconds.

Keep the returned handle reachable and call `handle:release()` when finished. Available methods include `get_handle()`, `get_mask()`, `get_data()`, `merge_data(value)`, `suspend()`, and `resume()`.

### Logging, Autorelease, Locks, And Blocks

- `NSLog(str) -> nil`
- `autoreleasepool(func, ...) -> ...`
- `autoreleasewrap(func) -> wrapped_func`
- `spin_lock(id) -> nil`
- `spin_trylock(id) -> boolean`
- `spin_unlock(id) -> nil`
- `new_fixed_block_8(func) -> block_ptr`
- `release_fixed_block(block_ptr) -> nil`

`new_fixed_block_8` creates a fixed-shape Objective-C Block. The callback receives up to 8 pointer arguments and returns a pointer. Keep the block reference alive until callbacks finish, and release it with `release_fixed_block` or `ffi.gc`.

### ObjC Associated Objects And Reference Counts

- `objc_getAssociatedObject(obj, key) -> value_ptr`
- `objc_setAssociatedObject(obj, key, value, [policy]) -> nil`
- `objc_removeAssociatedObjects(obj) -> nil`
- `objc_autoreleasePoolPush() -> pool_ptr`
- `objc_autoreleasePoolPop(pool_ptr) -> nil`
- `objc_autorelease(obj) -> nil`
- `objc_retain(obj) -> nil`
- `objc_release(obj) -> nil`
- `objc_description(obj) -> string`

`objc_setAssociatedObject` accepts these `policy` values: `OBJC_ASSOCIATION_ASSIGN`, `OBJC_ASSOCIATION_RETAIN_NONATOMIC`, `OBJC_ASSOCIATION_COPY_NONATOMIC`, `OBJC_ASSOCIATION_RETAIN`, and `OBJC_ASSOCIATION_COPY`.

### CoreFoundation / RunLoop

- `CFAbsoluteTimeGetCurrent() -> number`
- `CFRelease(obj) -> nil`
- `CFRunLoopRunWithAutoreleasePool([mode], [seconds]) -> int`
- `CFRunLoopRunInMode([mode], [seconds], [returnAfterSourceHandled]) -> int`
- `CFRunLoopAddCommonMode([runloop], [mode]) -> nil`
- `CFRunLoopGetCurrent() -> runloop_ptr`
- `CFRunLoopGetMain() -> runloop_ptr`
- `CFRunLoopRun() -> nil`
- `CFRunLoopStop([runloop]) -> nil`
- `CFRunLoopWakeUp([runloop]) -> nil`
- `CFRunLoopGetNextTimerFireDate([runloop], [mode]) -> number`
- `CFRunLoopIsWaiting([runloop]) -> boolean`
- `CFRunLoopPerformBlock([runloop], [mode], block_or_func) -> nil`

Timer:

- `CFRunLoopTimerCreateWithHandler([allocator], [fireDate], [interval], [flags], [order], handler) -> timer_ptr`
- `CFRunLoopContainsTimer([runloop], timer, [mode]) -> boolean`
- `CFRunLoopAddTimer([runloop], timer, [mode]) -> nil`
- `CFRunLoopRemoveTimer([runloop], timer, [mode]) -> nil`
- `CFRunLoopTimerGetNextFireDate(timer) -> number`
- `CFRunLoopTimerSetNextFireDate(timer, time) -> nil`
- `CFRunLoopTimerGetInterval(timer) -> number`
- `CFRunLoopTimerDoesRepeat(timer) -> boolean`
- `CFRunLoopTimerGetOrder(timer) -> integer`
- `CFRunLoopTimerInvalidate(timer) -> nil`
- `CFRunLoopTimerIsValid(timer) -> boolean`

Source:

- `CFRunLoopSourceCreate([allocator], order, context_ptr) -> source_ptr`
- `CFRunLoopContainsSource([runloop], source, [mode]) -> boolean`
- `CFRunLoopAddSource([runloop], source, [mode]) -> nil`
- `CFRunLoopRemoveSource([runloop], source, [mode]) -> nil`

Observer:

- `CFRunLoopObserverCreateWithHandler([allocator], [activities], [repeats], [order], handler) -> observer_ptr`
- `CFRunLoopContainsObserver([runloop], observer, [mode]) -> boolean`
- `CFRunLoopAddObserver([runloop], observer, [mode]) -> nil`
- `CFRunLoopRemoveObserver([runloop], observer, [mode]) -> nil`
- `CFRunLoopObserverGetActivities(observer) -> integer`
- `CFRunLoopObserverDoesRepeat(observer) -> boolean`
- `CFRunLoopObserverGetOrder(observer) -> integer`
- `CFRunLoopObserverInvalidate(observer) -> nil`
- `CFRunLoopObserverIsValid(observer) -> boolean`

`mode` may be `'kCFRunLoopDefaultMode'`, `'kCFRunLoopCommonModes'`, or a custom mode name string. Put all RunLoop APIs inside a `fork_dostring` child process according to the isolation rule above.

### Pointers, Notifications, Messaging, HID, And Time

- `int_to_pointer(x) -> lightuserdata`
- `pointer_to_int(ptr) -> integer`
- `memory_read_str(ptr, [len]) -> string`
- `memory_write_str(ptr, str) -> nil`
- `notification_center_register_callback(options, func) -> handle`
- `notification_center_post(center, name, [user_info]) -> nil`
- `post_distributed_notification(name, user_info) -> nil`
- `cpdistributed_messaging_center_register_callback(center_name, message_name, func) -> handle`
- `cpdistributed_messaging_center_run_server_on_current_thread(center_name) -> nil`
- `cpdistributed_messaging_center_run_server(center_name) -> nil`
- `cpdistributed_messaging_center_stop_server(center_name) -> nil`
- `cpdistributed_messaging_center_send_message(center_name, message_name, user_info) -> boolean`
- `cpdistributed_messaging_center_send_message_and_receive_reply(center_name, message_name, user_info) -> table | (nil, err)`
- `hid_event_register_callback([options], func) -> handle`
- `mach_absolute_time() -> integer`
- `mach_absolute_nano() -> integer`
- `mach_absolute_ms() -> number`

`notification_center_register_callback` accepts `options.center` as `'darwin'`, `'distributed'`, `'local'`, or a center pointer. Notification, messaging center, and HID registrations return handles. Keep them reachable until callbacks finish and call `handle:release()` when no longer listening.

### Constants

Available global constants include `__NSConcreteStackBlock`, iOS 10+ queue attribute constants, RunLoop activity constants, RunLoop result constants, Dispatch Source types, `DISPATCH_PROC_*`, `QOS_CLASS_*`, `DISPATCH_QUEUE_SERIAL`, `DISPATCH_QUEUE_CONCURRENT`, and `DISPATCH_TARGET_QUEUE_DEFAULT`.

## Topic Details

Open `lobjc-objc-bridge.md` for classes, chained method calls, method invokers, conversions, blocks, `objc.choose`, GCD helpers, exceptions, and autorelease pools.

## Safety Rules

- Prefer XXTouch built-ins before `objc` or `ffi`.
- Use `fork_dostring` for risky calls, and communicate through `print` plus `proc_queue_push`.
- RunLoop related functions must run in a `fork_dostring` child process, not in the main script.
- Wrap direct Objective-C calls with `objc.try` or `objc.try_catch` when exceptions are possible.
- Keep `objc.block` or fixed block references alive until asynchronous Objective-C code finishes.
- Dispatch UIKit work to the main queue with `dispatch_sync('main', function() ... end)` or `dispatch_async('main', function() ... end)`.
- Use `autoreleasepool(function() ... end)` around loops that create many Objective-C objects.
