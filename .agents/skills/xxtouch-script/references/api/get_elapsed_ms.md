# get_elapsed_ms

Purpose: Script elapsed milliseconds

## Signature
```lua
elapsed_ms = get_elapsed_ms()
```

## Example
```lua
local tm = get_elapsed_ms()
sys.msleep(1)
tm = get_elapsed_ms() - tm
nLog('sys.msleep(1) took '..tm..' ms')
```

## Returns
- elapsed_ms
    number, script execution time in milliseconds

## Notes
This function returns the elapsed milliseconds of the current script. Time spent while the script is paused is not counted.
