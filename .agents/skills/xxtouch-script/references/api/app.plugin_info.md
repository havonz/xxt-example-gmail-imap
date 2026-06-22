# app.plugin_info

Purpose: App plugin information

## Signature
```lua
plugin_info = app.plugin_info(bundle_identifier)
```

## Example
```lua
local info = app.plugin_info("com.tencent.mqq") -- Get the QQ app plugin information.
nLog(info)
```

## Parameters
- bundle_identifier
    string

## Returns
- plugin_info
    table, the app plugin information in the format `{{bid = "xxx", bundle_path = "xxx", data_path = "xxx"}, ...}`. Returns an empty table if none exists.
