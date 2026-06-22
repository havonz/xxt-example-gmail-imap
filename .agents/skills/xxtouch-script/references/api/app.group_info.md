# app.group_info

Purpose: App group information

## Signature
```lua
app_group_info = app.group_info(bundle_identifier)
```

## Example
```lua
local info = app.group_info("com.tencent.mqq") -- Get the QQ app group information.

local function clear_dir(path)
    for _, fn in ipairs(file.list(path) or {}) do
        local full_path = path .. '/' .. fn
        file.remove(full_path)
    end
end

-- Remove the contents of all group directories.
for _,p in pairs(info) do
    for _,v in ipairs(file.list(p) or {}) do
        local path = p .. '/' .. v
        if file.exists(path) == 'directory' then
            clear_dir(path)
        elseif v ~= '.com.apple.mobile_container_manager.metadata.plist' then
            file.remove(path)
        end
    end
end
```

## Parameters
- bundle_identifier
    string

## Returns
- app_group_info
    table, the app group information in the format `{group_id = data_path, ...}`. Returns an empty table if none exists.
