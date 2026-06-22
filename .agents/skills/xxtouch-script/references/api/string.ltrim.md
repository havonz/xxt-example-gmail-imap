# string.ltrim

Purpose: Remove whitespace characters from the left side of text.

## Signature
```lua
processed_text = string.ltrim(input_text)
```

## Example
```lua
local text = string.ltrim(" \t hello \n")
sys.alert(text) -- "hello \n"
```

## Parameters
- input_text
    string, text whose left-side whitespace should be removed.

## Returns
- processed_text
    string, text after left-side whitespace has been removed.

## Notes
Removes whitespace characters from the left side of text.
Whitespace characters include `"\r"`, `"\n"`, and `"\t"`.
