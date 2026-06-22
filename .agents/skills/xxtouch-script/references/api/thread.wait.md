# thread.wait

Purpose: Wait for task completion

## Signature
```lua
thread.wait(task_id, timeout_seconds)
```

## Example
```lua
local tid = thread.dispatch(function()
    sys.msleep(1000)
    nLog('done')
end)

thread.wait(tid, 3)
```

## Parameters
- task_id
    integer
- timeout_seconds
    number, wait timeout in seconds. Returns after timeout.

## Notes
Blocks the current thread while waiting for another task to complete.
