# clear.idfav

Purpose: Clear IDFA/V

## Signature
```lua
old_idfav_info = clear.idfav([ new_idfav_info ])
```

## Example
```lua
-- Back up and clear idfav information.
app.quit('*') -- Close all apps.
local old_idfavs = clear.idfav("read") -- Read the current idfav information.
local ok, err = file.writes(XXT_SCRIPTS_PATH.."/old_idfavs.txt", old_idfavs) -- Save the current idfav information to a file.
if ok then
    clear.idfav() -- Clear idfav information.
    sys.alert("Backup succeeded")
else
    sys.alert("Backup failed\n"..tostring(err))
end

-- Restore idfav information from a file.
app.quit('*') -- Close all apps.
local old_idfavs, err = file.reads(XXT_SCRIPTS_PATH.."/old_idfavs.txt") -- Read the saved idfav information.
if old_idfavs then
    local current_idfavs = clear.idfav(old_idfavs)
    if current_idfavs then
        local ok, err = file.writes(XXT_SCRIPTS_PATH.."/current_idfavs.txt", current_idfavs) -- Save the current idfav information to another file.
        sys.alert("Restored idfav information successfully")
    else
        sys.alert("Failed to restore idfav information")
    end
else
    sys.alert("Failed to open file\n"..tostring(err))
end
```

## Parameters
- new_idfav_info
    string, optional. Specifies the information to use as the device's new idfav information. If omitted, the current information is cleared and the system generates new values automatically. Pass `"read"` to read the device's IDFAV information without clearing it.

## Returns
- old_idfav_info
    string | nil, the device's previous idfav information, or `nil` if the operation fails.

## Notes
Resets device identifier information such as IDFA and IDFV.
If the provided idfav information is invalid, the operation fails and returns `nil`.
If no argument is passed, the device's current idfav information is cleared and iOS later assigns new random idfav values.
The returned idfav information text can be saved to a file. To restore it later, pass it back as the argument.
