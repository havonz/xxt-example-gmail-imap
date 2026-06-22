# string.atrim

Purpose: Remove all whitespace characters from text.

## Signature
```lua
processed_text = string.atrim(input_text)
```

## Example
```lua
local text = string.atrim(" 1 2\t3\n")
sys.alert(text) -- 123
```

## Parameters
- input_text
    string, text whose whitespace characters should all be removed.

## Returns
- processed_text
    string, text after all whitespace characters have been removed.

## Notes
Removes all whitespace characters from text.
Whitespace characters include `"\r"`, `"\n"`, and `"\t"`.
