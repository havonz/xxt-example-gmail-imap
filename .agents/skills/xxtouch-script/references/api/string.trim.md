# string.trim

Purpose: Remove whitespace characters from both sides of text.

## Signature
```lua
processed_text = string.trim(input_text)
```

## Example
```lua
local text = string.trim(" \t hello \n")
sys.alert(text) -- hello
```

## Parameters
- input_text
    string, text whose left and right whitespace should be removed.

## Returns
- processed_text
    string, text after whitespace on both sides has been removed.

## Notes
Removes whitespace characters from both sides of text.
Whitespace characters include `"\r"`, `"\n"`, and `"\t"`.
