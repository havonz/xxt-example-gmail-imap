# os.exit / os.restart

Purpose: Exit/restart script

## Exit Script
```lua
os.exit()
```

### Notes
`os.exit` is Lua's built-in process termination function. In XXTouch, it is used to end the logical script process.
Calling it from any thread can end the current script process; all threads and listeners terminate immediately.

## Restart Script
```lua
success, error_message = os.restart([ script_file_path ])
```

### Example
```lua
os.restart() -- Restart to the current script loaded at startup.

local ok, err = os.restart(utils.launch_args().path)
if ok == false then
    sys.alert(err)
end
```

### Parameters
- script_file_path
    string, optional. When a valid script file path is passed, restarts into the target script file. Default: `""`.

### Returns
- success
    boolean. Returns false on failure. Failure is only possible when the script file path argument is passed. On success, the function does not return.
- error_message
    string. On failure, returns the specific error message.

### Notes
When no script file path is passed, this function restarts the current script process directly, and the current script ends immediately.
When a valid script file path is passed, the current script ends and restarts into the target script file.
After a script file has been modified, `os.restart()` does not automatically load the modified file. To load the latest script from disk, pass `utils.launch_args().path`.
Avoid calling it in a multi-threaded environment when possible; a zero-delay restart may not leave other threads enough time to clean up their state.
