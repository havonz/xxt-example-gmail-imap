# sys.mtime

Purpose: Millisecond timestamp

## Signature
```lua
timestamp = sys.mtime()
```

## Example
```lua
local ms = sys.mtime()
screen.keep()
sys.alert('One screen.keep call took: '..sys.mtime()-ms..' ms')
```

## Returns
- timestamp
    integer, UNIX timestamp in milliseconds.
