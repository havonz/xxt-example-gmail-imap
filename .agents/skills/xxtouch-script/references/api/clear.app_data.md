# clear.app_data

Purpose: Clear app data

## Signature
```lua
success = clear.app_data(bundle_identifier)
```

## Example
```lua
clear.app_data("com.tencent.xin")
```

## Parameters
- bundle_identifier
    string

## Returns
- success
    boolean, returns `true` if clearing succeeds; otherwise returns `false`.

## Notes
Clears app data. All threads are blocked while the cleanup is running.
This function may take a very long time. Forcibly stopping the script while it is running will make stopping slow, because the script must be forcibly terminated.
Warning: the effect of calling this function is irreversible.
