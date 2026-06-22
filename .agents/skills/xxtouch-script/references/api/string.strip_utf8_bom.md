# string.strip_utf8_bom

Purpose: Remove a UTF-8 BOM from the start of text.

## Signature
```lua
processed_text = string.strip_utf8_bom(input_text)
```

## Example
```lua
txt = string.strip_utf8_bom(txt)
sys.alert(txt..', '..#txt) -- outputs "XXTouch, 7"
```

## Parameters
- input_text
    string, text from which the UTF-8 BOM should be removed.

## Returns
- processed_text
    string, text after the UTF-8 BOM has been removed.

## Notes
A UTF-8 BOM appears as three invisible bytes at the beginning of a document: `"\xEF\xBB\xBF"`. In Lua source, `\x` followed by two hexadecimal digits represents one byte with that value. For example, `\x58` represents the printable character `X`; see ASCII encoding references for printable characters.
