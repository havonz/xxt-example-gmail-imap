# string.lpad

Purpose: Left-pad a string.

## Signature
```lua
padded_string = string.lpad(source_string, length, padding_character)
```

## Example
```lua
nLog(string.lpad('ff',   6, '0'))  -- outputs 0000ff
nLog(string.lpad('100',  6, '0'))  -- outputs 000100
nLog(string.lpad('1234', 6, '0'))  -- outputs 001234
nLog(string.lpad('123',  6, 'xy')) -- outputs xyx123
```

## Parameters
- source_string
    string.
- length
    integer, target length of the padded string.
- padding_character
    string, optional. Character(s) used for padding; defaults to a space.

## Returns
- padded_string
    string.

## Notes
Left-pads `source_string` so its length reaches `length`; missing characters are filled with `padding_character`.
