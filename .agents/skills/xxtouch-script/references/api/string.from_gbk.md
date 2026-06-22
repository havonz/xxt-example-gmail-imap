# string.from_gbk

Purpose: Convert GBK-encoded text to UTF-8 text.

## Signature
```lua
usable_text = string.from_gbk(gbk_encoded_text)
```

## Example
```lua
sys.alert(gbkstr)                  -- A GBK-encoded string cannot be displayed correctly.
sys.alert(string.from_gbk(gbkstr)) -- outputs "XXTouch is powerful"
```

## Parameters
- gbk_encoded_text
    string, GBK-encoded text that should be converted to UTF-8.

## Returns
- usable_text
    string or nil. Returns UTF-8 encoded text; returns nil if encoding errors make conversion impossible.

## Notes
Converts GBK-encoded text to UTF-8.
If the input encoding itself is incorrect, the function still converts bytes according to the mapping; garbled output is not a function error.
For more complex encoding conversion needs, see luaiconv.
GBK includes GB2312, so GB2312 text is also converted with this function.
