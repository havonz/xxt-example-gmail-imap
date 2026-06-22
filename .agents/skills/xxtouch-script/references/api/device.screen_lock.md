# device.lock_screen / device.is_screen_locked / device.unlock_screen

Purpose: Lock screen/status/unlock

## Lock Screen
```lua
device.lock_screen()
```

## Get Screen Lock Status
```lua
locked = device.is_screen_locked()
```

### Example
```lua
if device.is_screen_locked() then
    -- The screen is locked.
else
    -- The screen is unlocked.
end
```

### Returns
- locked
    boolean, returns whether the screen is currently locked.

## Unlock Screen
```lua
device.unlock_screen([ lock_screen_passcode ])
```

### Example
```lua
device.unlock_screen()
```

### Parameters
- lock_screen_passcode
    string, optional screen lock passcode. This parameter can be used when a passcode is set; leave it unset if there is no passcode. Its use is not recommended.

## Notes
Unlocking the screen with a passcode only works in a full jailbreak environment with plugin injection enabled. The TrollStore version cannot unlock the screen with a passcode.
