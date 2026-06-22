# table.deep_copy

Purpose: Deep-copy a table

## Signature
```lua
copied_table = table.deep_copy(table_value)
```

## Example
```lua
local _g = table.deep_copy(_G)
```

## Parameters
- table_value
    table, the table to copy.

## Returns
- copied_table
    table, a deep-copied copy of the original table.

## Notes
Recursively copies the entire table structure. All values except `function` and `userdata` are copied.
If the original table contains cyclic references, the copy preserves the same reference relationships.
