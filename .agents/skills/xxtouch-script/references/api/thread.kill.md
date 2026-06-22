# thread.kill

Purpose: Remove task

## Signature
```lua
thread.kill(task_id)
```

## Example
```lua
local tid = thread.dispatch(function()
    while true do
        sys.msleep(1000)
    end
end)

sys.msleep(3000)
thread.kill(tid)
```

## Parameters
- task_id
    integer

## Notes
Removes a task from the queue, regardless of whether it has started or completed.
