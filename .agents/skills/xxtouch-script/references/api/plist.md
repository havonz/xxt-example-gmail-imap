# plist

Purpose: Property list read/write/convert

## Signature
```lua
table_value = plist.load(property_list_data)
table_value = plist.read(file_path)
plist.write(file_path, table_value)
property_list_data = plist.dump(table_value[, property_list_data_format])
converted_property_list_data = plist.data_convert(property_list_data[, property_list_data_format])
```

## Example
```lua
local path = "/var/mobile/Library/Caches/com.apple.mobile.installation.plist"
local tab = plist.read(path)
tab.Metadata.ProductBuildVersion = "CustomBuild"
plist.write(path, tab)

local xml = plist.dump(tab, "XML")
local loaded = plist.load(xml)
local binary = plist.data_convert(xml, "binary")
```

## Parameters
- property_list_data
    string, XML, binary, or openstep property list data.
- file_path
    string, absolute path to the plist file.
- table_value
    table, Lua table corresponding to the plist tree structure.
- property_list_data_format
    string, optional. Must be `"binary"`, `"XML"` / `"xml"`, or `"openstep"`. Default: `"XML"`.

## Returns
- table_value
    table or nil, returned when reading/parsing succeeds.
- property_list_data, converted_property_list_data
    string or nil, returned when conversion succeeds.

## Notes
`plist.load` / `plist.dump` convert between Lua tables and plist data. `plist.read` / `plist.write` operate on files. `plist.data_convert` only converts the plist data format; it does not serialize or deserialize Lua values, and the conversion can preserve plist data integrity. Non-generic data types in plist files are not supported for reading and are ignored. `plist.read` / `plist.write` can be used in XUI.
For raw `NSKeyedArchiver` / binary plist files that contain ObjC classes or `CF$UID` references, do not use `plist.read` or `plist.load` when object links matter: Lua deserialization drops unsupported ObjC/UID objects. Read bytes with `file.reads(path)`, convert only the representation with `plist.data_convert(data, "XML")`, then parse the XML while preserving `<key>CF$UID</key><integer>...</integer>` references. Do not pass that XML back through `plist.load` for graph reconstruction.
After modifying a system plist, depending on the original file scenario, you may also need `sys.chown` / `sys.chmod` to correct permissions.
