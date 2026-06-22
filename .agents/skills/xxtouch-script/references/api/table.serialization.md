# table.deep_dump / table.load_string

Purpose: Table serialization/load

## Serialize Table
```lua
table_text = table.deep_dump(associative_table)
```

### Example
```lua
local s = table.deep_dump(_G)
sys.alert(s)
```

### Parameters
- associative_table
    table, the table to serialize into a string.

### Returns
- table_text
    string, tree-structured text of the table. This format is not guaranteed to be compatible between versions.

### Notes
Serialization output is not guaranteed to be compatible between versions; output may differ across versions.
Non-table reference types, such as userdata and functions, cannot be deserialized by `table.load_string`; only human readability is guaranteed.

## Load Table from Text
```lua
associative_table = table.load_string(table_text)
```

### Example
```lua
local t = table.load_string[[ {
    a = 1,
    b = 2,
    c = 3,
} ]]
sys.alert(t.b)
```

### Parameters
- table_text
    string, serialized tree-structured table text. It can only contain static data and must not contain dynamic code.

### Returns
- associative_table
    table | nil, returns the table structure on successful load, or `nil` on failure.

### Notes
`table.load_string` can be treated as an inverse of `table.deep_dump` to some extent. Actual usability depends on whether cyclic references or non-table reference types exist.
Unlike `load`, this function does not execute code in the text; it only reads static data from it.
