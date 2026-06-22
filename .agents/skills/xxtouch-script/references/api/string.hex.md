# string.to_hex / string.from_hex

Purpose: Convert between strings and hexadecimal text.

## Convert To Hexadecimal Text
```lua
hex_text = string.to_hex(data_content[, prefix, suffix])
```

### Example
```lua
sys.alert(string.to_hex("some data"))
-- outputs "736f6d652064617461"
```

### Parameters
- data_content
    string, the string to convert to hexadecimal.
- prefix
    string, optional. Prefix for each converted byte; defaults to `""`.
- suffix
    string, optional. Suffix for each converted byte; defaults to `""`.

### Returns
- hex_text
    string, hexadecimal text.

## Convert Back From Hexadecimal Text
```lua
data_content = string.from_hex(hex_text)
```

### Example
```lua
sys.alert(string.from_hex("736f6d652064617461"))
-- outputs "some data"
```

### Parameters
- hex_text
    string, hexadecimal text to convert back to a string.

### Returns
- data_content
    string or nil. Returns the string, or nil if the input is not hexadecimal text.

## Notes
Can be used for strings or binary data blocks. Keywords: image hexadecimal, file hexadecimal, data hexadecimal.
