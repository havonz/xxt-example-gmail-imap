# string.rtrim

Purpose: Remove whitespace characters from the right side of text.

## Signature
```lua
processed_text = string.rtrim(input_text)
```

## Example
```lua
local text = string.rtrim(" \t hello \n")
sys.alert(text) -- " \t hello"
```

## Parameters
- input_text
    string, text whose right-side whitespace should be removed.

## Returns
- processed_text
    string, text after right-side whitespace has been removed.

## Notes
Removes whitespace characters from the right side of text.
Whitespace characters include `"\r"`, `"\n"`, and `"\t"`.
