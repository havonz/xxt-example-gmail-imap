# string.base64_encode / string.base64_decode

Purpose: Base64 encode or decode.

## Encode
```lua
b64_text = string.base64_encode(data_content)
```

### Example
```lua
b64s = screen.image(0, 0, 100, 100):png_data():base64_encode()
b64s = file.reads("/var/mobile/1.png"):base64_encode()
```

### Parameters
- data_content
    string, the original string.

### Returns
- b64_text
    string, base64-encoded text for the string.

## Decode
```lua
data_content = string.base64_decode(b64_text)
```

### Example
```lua
local raw = string.base64_decode("SGVsbG8=")
sys.alert(raw) -- Hello
```

### Parameters
- b64_text
    string, base64-encoded text.

### Returns
- data_content
    string, decoded string.

## Notes
Can be used for strings or binary data blocks. Keywords: image Base64, file Base64, data Base64, binary Base64.
