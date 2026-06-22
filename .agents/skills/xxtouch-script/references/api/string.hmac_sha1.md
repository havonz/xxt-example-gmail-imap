# string.hmac_sha1

Purpose: Compute the HMAC-SHA1 hash of a string.

## Signature
```lua
hexHash = string.hmac_sha1(data, key)
```

## Example
```lua
local signature = string.hmac_sha1('hello world', 'secret')
sys.alert(signature) -- outputs "03376ee7ad7bbfceee98660439a4d8b125122a5a"
```

## Parameters
- data
    string, data content used to compute the hash.
- key
    string, secret key used by the HMAC algorithm.

## Returns
- hexHash
    string, lowercase hexadecimal text for the HMAC-SHA1 checksum.

## Notes
Uses HMAC-SHA1 to compute a keyed hash digest for any string or binary data.
