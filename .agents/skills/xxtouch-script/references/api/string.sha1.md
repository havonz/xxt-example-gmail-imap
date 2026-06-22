# string.sha1

Purpose: Compute the SHA1 hash of a string.

## Signature
```lua
hash_value = string.sha1(data_content)
```

## Example
```lua
sys.alert(string.sha1('XXTouch is great')) -- outputs "ecb86cc0dfafb8afcd6ef2d6a3b6fd1bac36df00"
```

## Parameters
- data_content
    string, original string.

## Returns
- hash_value
    string, hexadecimal text for the string's SHA1 hash.

## Notes
Computes the SHA1 checksum of a string or binary data block.
