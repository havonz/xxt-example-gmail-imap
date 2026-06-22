# clear.keychain / clear.all_keychain

Purpose: Clear keychain

## Clear Specific Keychain
```lua
clear.keychain(association_name)
```

### Example
```lua
clear.keychain("com.doglobal") -- Clear keychain information related to com.doglobal.
```

### Parameters
- association_name
    string, usually a company's reverse-domain name or an app TeamID, such as `"com.doglobal"` or `"GN26HFBMX6"`.

### Notes
Clears keychain information for an app or group. If you are not familiar with what this means, use `clear.all_keychain` instead.
Warning: the effect of calling this function is irreversible.
Warning: do not pass arbitrary arguments. Incorrect arguments may cause extremely serious consequences.

## Clear All Keychains
```lua
clear.all_keychain()
```

### Notes
Warning: the effect of calling this function is irreversible.
