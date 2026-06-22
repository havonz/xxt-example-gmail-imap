# sys.msleep

Purpose: Millisecond delay

## Signature
```lua
sys.msleep(milliseconds)
```

## Example
```lua
sys.msleep(1000) -- Wait 1 second.
```

## Parameters
- milliseconds
    number, delay duration to wait, in milliseconds.

## Notes
Blocks the current thread for a specified time.
This method may yield. Before it returns, other threads may get a chance to run.
