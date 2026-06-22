# string.compare_version

Purpose: Compare two version numbers.

## Signature
```lua
comparison_result = string.compare_version(version_a, version_b)
```

## Example
```lua
assert(string.compare_version("1.1", "1.0") == 1)
assert(string.compare_version("1.0", "1.1") == -1)
assert(string.compare_version("1.0", "1") == 0)
assert(string.compare_version("1.1", "1.10") == -1)
assert(string.compare_version("1.2-3", "1.2.3") == 0)
assert(string.compare_version("2..2", "2.2") == 0)
assert(string.compare_version("2.2.x.3", "2.2") == 0)
assert(string.compare_version("x", "") == 0)
```

## Parameters
- version_a, version_b
    string, the two version numbers to compare.

## Returns
- comparison_result
    integer. Returns `1` when `version_a` is greater than `version_b`, `-1` when `version_a` is less than `version_b`, and `0` when they are equal.

## Notes
Compares two version number strings with these rules:

- Pure numeric segments separated by `.`, `-`, or spaces are compared.
- Different separators are equivalent, and consecutive separators are treated as one separator.
- Segment weights decrease from left to right.
- Any invalid character truncates comparison of following content.
- If segment counts differ, missing segments are padded with `0`.
- Empty strings or invalid strings are treated as version `0`.
- `1.1` and `1.1.0` are equal.
- `1.1` and `1.1-0` are equal.
- `1.1` and `1-1` are equal.
- `1.0` and `1 0` are equal.
- `1.0` is greater than `0.99999`.

This function can be used in XUI.
