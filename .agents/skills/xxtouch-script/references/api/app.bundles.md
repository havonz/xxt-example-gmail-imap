# app.bundles

Purpose: App BID list

## Signature
```lua
bundle_identifier_array = app.bundles()
```

## Example
```lua
-- Close all apps.
for _,bid in ipairs(app.bundles()) do
    app.close(bid)
end
```

## Returns
- bundle_identifier_array
    array table, a table containing all app bundle identifiers on the device, including built-in system apps.

## Notes
Gets the bundle identifier list for all apps on the device.
