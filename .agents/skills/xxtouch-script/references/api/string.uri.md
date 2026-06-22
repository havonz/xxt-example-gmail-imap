# string.encode_uri / string.decode_uri / string.encode_uri_component / string.decode_uri_component

Purpose: Percent-encode and decode URI or URI components.

## URI Encode
```lua
encoded_uri = string.encode_uri(URI)
```

### Example
```lua
nLog(string.encode_uri("https://www.example.com/test path")) -- https://www.example.com/test%20path
```

## URI Decode
```lua
URI = string.decode_uri(encoded_uri)
```

### Example
```lua
nLog(string.decode_uri("https://www.example.com/test%20path")) -- https://www.example.com/test path
```

## URI Component Encode
```lua
encoded_uri_component = string.encode_uri_component(uri_component)
```

### Example
```lua
nLog(string.encode_uri_component("https://www.example.com/test path")) -- https%3A%2F%2Fwww.example.com%2Ftest%20path
```

## URI Component Decode
```lua
uri_component = string.decode_uri_component(encoded_uri_component)
```

### Example
```lua
nLog(string.decode_uri_component("https://www.example.com/test%20path")) -- https://www.example.com/test path
```

## Parameters
- URI / uri_component
    string, URI or URI component to encode.
- encoded_uri / encoded_uri_component
    string, text to decode.

## Returns
- encoded_or_decoded_text
    string.

## Notes
Compared with `string.encode_uri`, `string.encode_uri_component` escapes reserved characters such as `/`, `?`, `&`, and `=` more strictly.
Keywords: URL encode, URL decode, URI encode, URI decode, URI component encode, URI component decode.
