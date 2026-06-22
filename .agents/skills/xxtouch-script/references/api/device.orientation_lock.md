# device.orientation_lock

Purpose: Orientation lock

## Signature
```lua
locked = device.is_orien_locked()
device.lock_orien()
device.unlock_orien()
```

## Example
```lua
if not device.is_orien_locked() then
    device.lock_orien()
end

-- Restore it after the task if needed.
device.unlock_orien()
```

## Returns
- locked
    boolean, returns whether screen rotation lock is currently enabled.
