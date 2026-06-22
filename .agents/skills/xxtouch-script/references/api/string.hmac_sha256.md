# string.hmac_sha256

Purpose: Compute the HMAC-SHA256 hash of a string.

## Signature
```lua
hexHash = string.hmac_sha256(data, key)
```

## Example
```lua
local signature = string.hmac_sha256('hello world', 'secret')
sys.alert(signature) -- outputs "734cc62f32841568f45715aeb9f4d7891324e6d948e4c6c60c0621cdac48623a"
```

## Parameters
- data
    string, data content used to compute the hash.
- key
    string, secret key used by the HMAC algorithm.

## Returns
- hexHash
    string, lowercase hexadecimal text for the HMAC-SHA256 checksum.

## Notes
Uses HMAC-SHA256 to compute a keyed hash digest for any string or binary data.
