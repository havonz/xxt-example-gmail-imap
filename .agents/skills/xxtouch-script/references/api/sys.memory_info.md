# sys.memory_info

Purpose: Memory state

## Signature
```lua
memory_status = sys.memory_info()
```

## Example
```lua
sys.alert(table.deep_dump(sys.memory_info()))
```

## Returns
- memory_status
    table, returned memory status information. See the return value example for field meanings.
