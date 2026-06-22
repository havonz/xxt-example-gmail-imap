# xpp.info / xpp.bundle_path / xpp.resource_path

Purpose: XPP runtime information/paths

## Get Script Bundle Metadata
```lua
metadata = xpp.info()
```

### Example
```lua
local info = xpp.info()
```

### Returns
- metadata
    table, returns metadata for the current script bundle. If the currently running script is not a script bundle, returns an empty table.

## Get Script Bundle Path
```lua
bundle_path = xpp.bundle_path()
```

### Example
```lua
local path = xpp.bundle_path()
```

### Returns
- bundle_path
    string, returns the current script bundle path. If the currently running script is not a script bundle, returns the current running script path.

## Get Script Bundle Resource Path
```lua
resource_path = xpp.resource_path(resource_file_name)
```

### Example
```lua
local path = xpp.resource_path("appicon.png")
```

### Parameters
- resource_file_name
    string, resource file name to get

### Returns
- resource_path
    string or nil, returns the path to a resource file in the current script bundle. If the resource does not exist, returns nil.

## Notes
These functions get information about the current script bundle from a running script. See `references/xpp.md` for the XPP bundle structure and `Info.lua` fields.
`xpp.resource_path` supports localized resource lookup.
