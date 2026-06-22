# key.send_text

Purpose: Type text

## Signature
```lua
key.send_text(text [, per_key_delay, shift_key_delay])
```

## Example
```lua
key.send_text("AbC12#") -- Type text as fast as possible.

key.send_text("AbC12#", 300) -- Delay 0.3 seconds for each key press.
```

## Parameters
- text
    string, text to input. Only English letters, digits, spaces, half-width characters, and `"\b"`, `"\r"`, `"\t"` are supported.
- per_key_delay
    integer, delay for each key press, in milliseconds. Defaults to no delay, typing at the device performance limit.
- shift_key_delay
    integer, in milliseconds. Uppercase letters or certain special symbols require holding Shift, for example `@` is `Shift + 2`.

## Notes
This function can be used to forcibly simulate keyboard typing when `sys.input_text` does not work.
