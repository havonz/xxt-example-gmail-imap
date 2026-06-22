# app.data_path

Purpose: App data path

## Signature
```lua
data_path = app.data_path(bundle_identifier)
```

## Example
```lua
path = app.data_path("com.tencent.mqq") -- Get the QQ app data path.
```

## Parameters
- bundle_identifier
    string

## Returns
- data_path
    string | nil, the app data path, or `nil` if the app does not exist.

## Notes
Gets the app data path.
