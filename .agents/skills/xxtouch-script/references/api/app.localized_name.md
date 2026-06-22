# app.localized_name

Purpose: Localized name

## Signature
```lua
localized_name = app.localized_name(bundle_identifier)
```

## Example
```lua
local name = app.localized_name("com.tencent.xin")
sys.alert(name) -- Shows an alert such as "WeChat".
```

## Parameters
- bundle_identifier
    string

## Returns
- localized_name
    string | nil, the localized app name, or `nil` if the app does not exist.
