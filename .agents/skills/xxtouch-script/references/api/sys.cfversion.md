# sys.cfversion

Purpose: CoreFoundation version

## Signature
```lua
version_number = sys.cfversion()
```

## Example
```lua
sys.alert('Current CoreFoundation version: '..sys.cfversion())
```

## Returns
- version_number
    number, CoreFoundation version on the current device. The CoreFoundation version can usually be used to determine the current iOS version range. See `CoreFoundationVersionNumber`.
