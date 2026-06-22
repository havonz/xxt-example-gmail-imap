# string.md5

Purpose: Compute the MD5 hash of a string.

## Signature
```lua
hash_value = string.md5(data_content)
```

## Example
```lua
sys.alert(string.md5('XXTouch is great')) -- outputs "1cd091683a3f0a1ff713322d2ef20150"
```

## Parameters
- data_content
    string, original string.

## Returns
- hash_value
    string, hexadecimal text for the string's MD5 hash.

## Notes
Computes the MD5 checksum of a string or binary data block.
