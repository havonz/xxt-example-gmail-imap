# device.set_autolock_time

Purpose: Set auto-lock time

## Signature
```lua
device.set_autolock_time(minutes)
```

## Example
```lua
device.set_autolock_time(0)
```

## Parameters
- minutes
    integer, the number of minutes before the device auto-locks. Set to `0` to never auto-lock.

## Notes
This can only be set to minute values supported by the system, matching the options in Settings -> Display & Brightness -> Auto-Lock.
