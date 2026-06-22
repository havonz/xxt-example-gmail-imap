# thread.dispatch

Purpose: Dispatch task

## Signature
```lua
task_id = thread.dispatch(task [, error_callback ])
```

## Example
```lua
local tid = thread.dispatch(function()
    for i = 1, 5 do
        nLog('worker', i)
        sys.msleep(1000)
    end
end, function(err)
    nLog('thread error', err)
end)

nLog('Task ID', tid)
```

## Parameters
- task
    function, this function is added to the task queue.
- error_callback
    function, optional. If an exception occurs while executing the task, this function is called and the error is not thrown. By default, errors are thrown on exception.

## Returns
- task_id
    integer

## Notes
Dispatches a task to the queue. The task starts running when the scheduler is idle.
