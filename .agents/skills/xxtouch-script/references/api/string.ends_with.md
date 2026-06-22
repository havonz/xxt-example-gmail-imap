# string.ends_with

Purpose: Check whether a string ends with a suffix.

## Signature
```lua
ends_with_suffix = string.ends_with(source_string, suffix[, length])
```

## Example
```lua
nLog(string.ends_with('Hello, XXTouch', 'XXTouch')) -- outputs true
nLog(string.ends_with('Hello, XXTouch', 'ello', 5)) -- outputs true
```

## Parameters
- source_string
    string.
- suffix
    string.
- length
    integer, optional. Search length; defaults to the length of `source_string`.

## Returns
- ends_with_suffix
    boolean.

## Notes
Checks whether `source_string` ends with `suffix`.
