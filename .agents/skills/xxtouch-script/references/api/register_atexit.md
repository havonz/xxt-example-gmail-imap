# register_atexit

Purpose: Register exit callback

## Signature
```lua
original_callback = register_atexit(name, callback)
```

## Example
```lua
register_atexit("cleanup", function()
    sys.toast("Clean up resources before script exit")
    sys.msleep(300)
end)

while true do
    sys.toast("Try using the volume key to exit the script\n" .. os.date("%Y-%m-%d %H:%M:%S"))
    sys.msleep(1000)
end
```

## Parameters
- name
    string, required. Identifies the currently registered callback. Using the same `name` overrides the registered callback.
- callback
    function, required. Function executed when the script exits. Make sure it runs quickly and is safe to call repeatedly. If nil, unregisters the callback for the current `name`.

## Returns
- original_callback
    function, the previous callback before being overridden by a registration with the same name. Returns `nil` if none was registered before; can be used to restore the previous callback.

## Notes
Callbacks registered with `register_atexit` run when the script exits, including when the user ends the script with the volume key, and are guaranteed to be called before Lua garbage collection.
When multiple callbacks are registered with different `name` values, their call order is not controlled. If ordered execution is needed, schedule it inside a single callback.
If the callback needs to call time-consuming operations, limit their duration yourself; otherwise the exit experience may be affected.
