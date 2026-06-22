# string.aes128_encrypt / string.aes128_decrypt

Purpose: Encrypt or decrypt strings with AES128.

## Encrypt
```lua
encrypted_data = string.aes128_encrypt(data_content, key)
```

### Example
```lua
local key = "1234567890abcdef"
local encrypted = string.aes128_encrypt("hello", key)
local decrypted = string.aes128_decrypt(encrypted, key)
sys.alert(decrypted) -- hello
```

### Parameters
- data_content
    string, the string to encrypt.
- key
    string, the password/key.

### Returns
- encrypted_data
    string, encrypted binary data block.

## Decrypt
```lua
data_content = string.aes128_decrypt(encrypted_data, key)
```

### Parameters
- encrypted_data
    string, encrypted string.
- key
    string, the password/key.

### Returns
- data_content
    string, decrypted string.

## Notes
Uses the AES128-ECB algorithm to encrypt/decrypt strings or binary data blocks.
ECB mode itself does not need an IV (initialization vector). If a third-party system requires an IV, pass `0`.
