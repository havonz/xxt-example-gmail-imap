# app.bundle_path

Purpose: App bundle path

## Signature
```lua
bundle_path = app.bundle_path(bundle_identifier)
```

## Example
```lua
path = app.bundle_path("com.tencent.mqq") -- Get the QQ app bundle path.
```

## Parameters
- bundle_identifier
    string

## Returns
- bundle_path
    string | nil, the app bundle path, or `nil` if the app does not exist.

## Notes
Gets the app bundle path.
