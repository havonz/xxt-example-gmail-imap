# string.rpad

Purpose: Right-pad a string.

## Signature
```lua
padded_string = string.rpad(source_string, length, padding_character)
```

## Example
```lua
nLog(string.rpad('ff',   6, '0'))  -- outputs ff0000
nLog(string.rpad('100',  6, '0'))  -- outputs 100000
nLog(string.rpad('1234', 6, '0'))  -- outputs 123400
nLog(string.rpad('123',  6, 'xy')) -- outputs 123xyx
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
Right-pads `source_string` so its length reaches `length`; missing characters are filled with `padding_character`.
