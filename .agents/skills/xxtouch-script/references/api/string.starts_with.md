# string.starts_with

Purpose: Check whether a string starts with a prefix.

## Signature
```lua
starts_with_prefix = string.starts_with(source_string, prefix[, position])
```

## Example
```lua
nLog(string.starts_with('Hello, XXTouch', 'Hello')) -- outputs true
nLog(string.starts_with('Hello, XXTouch', 'ello', 2)) -- outputs true
```

## Parameters
- source_string
    string.
- prefix
    string.
- position
    integer, optional. Start position for searching; defaults to 1.

## Returns
- starts_with_prefix
    boolean.

## Notes
Checks whether `source_string` starts with `prefix`.
