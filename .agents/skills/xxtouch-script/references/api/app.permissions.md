# app.permissions

Purpose: Read/set app notification and Local Network permissions

Version requirement: XXTouch later than 20260529 is required.

iOS requirement: iOS 14 or later.

## Notification Permissions
```lua
info = app.notification_permissions(bundle_identifier [, operation])
app.notification_permissions(bundle_identifier, "set", info)
app.notification_permissions(bundle_identifier, "reset")
```

### Example
```lua
local info = app.notification_permissions("com.example.app", "get")
if info then
    info.allowsNotifications = true
    info.authorizationStatus = 2
    app.notification_permissions("com.example.app", "set", info)
end
```

### Parameters
- bundle_identifier
    string, target app bundle identifier.
- operation
    string, optional. One of `"get"`, `"set"`, or `"reset"`. Defaults to `"get"`.
- info
    table, notification permission state. Prefer starting from the table returned by `"get"` and changing only needed fields.

### Returns
- info
    table | nil. Returned by `"get"` when a permission record exists.

### Common Fields
- allowsNotifications
    boolean, whether notifications are allowed.
- authorizationStatus
    integer, notification authorization status.
- alertType
    integer, notification alert style.
- pushSettings
    integer, notification delivery settings.

## Local Network Permissions
```lua
info = app.local_network_permissions(bundle_identifier [, operation])
success = app.local_network_permissions(bundle_identifier, "set", allow)
success = app.local_network_permissions(bundle_identifier, "set", info)
success = app.local_network_permissions(bundle_identifier, "reset")
```

### Example
```lua
app.local_network_permissions("com.example.app", "set", true)

local info = app.local_network_permissions("com.example.app", "get")
if info then
    info.allowsLocalNetwork = false
    app.local_network_permissions("com.example.app", "set", info)
end
```

### Parameters
- bundle_identifier
    string, target app bundle identifier.
- operation
    string, optional. One of `"get"`, `"set"`, or `"reset"`. Defaults to `"get"`.
- allow
    boolean | integer. `true` or non-zero allows Local Network access; `false` or `0` denies it.
- info
    table, Local Network permission state. Prefer changing `allowsLocalNetwork` or `authorizationStatus`.

### Returns
- info
    table | nil. Returned by `"get"` when a permission record exists.
- success
    boolean. Returned by `"set"` and `"reset"`.

### Common Fields
- allowsLocalNetwork
    boolean, whether Local Network access is allowed.
- authorizationStatus
    integer. `0` means not determined, `1` means denied, and `2` means allowed.
