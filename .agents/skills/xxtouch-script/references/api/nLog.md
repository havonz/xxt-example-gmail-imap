# nLog

Purpose: Network log

## Signature
```lua
nLog(log_content)
```

## Example
```lua
-- Send the print buffer content back to the development tool log window.
nLog(print.out())
```

## Parameters
- log_content
    string, log content

## Notes
This is a protocol function (empty function). By default, calling it has no effect; implementation details are determined by the paired development environment.
When debugging with a paired development environment, this function sends logs back to the environment's log window.
