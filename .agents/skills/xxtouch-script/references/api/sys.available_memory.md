# sys.available_memory

Purpose: Available memory

## Signature
```lua
available_memory = sys.available_memory()
```

## Example
```lua
sys.alert('Current available memory: '..sys.available_memory()..'MB')
```

## Returns
- available_memory
    number, current free memory of the device, in MB.
