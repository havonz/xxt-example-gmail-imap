# json.decode / json.encode / json.null

Purpose: JSON encode/decode/null

## JSON to Lua
```lua
value, error_message = json.decode(json_text)
```

### Example
```lua
sys.alert(json.decode([["\u0068\u0069"]])) -- outputs: hi

print(json.decode("true"))
print(json.decode("17"))
print(json.decode('"hello"'))
print(json.decode("null"))
print(table.deep_dump(json.decode("{}")))
print(table.deep_dump(json.decode('{"name":"alice","hello":"world"}')))
```

### Parameters
- json_text
    string, JSON text to convert to a Lua value

### Returns
- value
    table, string, number, boolean, `json.null`, or nil. On success, returns a Lua value corresponding to the JSON string structure; otherwise returns nil.
- error_message
    string or nil. On failure, returns the specific error message.

## Lua to JSON
```lua
json_text, error_message = json.encode(value)
```

### Example
```lua
local tb = {
    name = "alice",
    message = "hello, world",
    scores = {90, 85, 72, 100, 68},
    nullvalue = json.null,
}
local jsonstr = json.encode(tb)
sys.alert(jsonstr)
```

### Parameters
- value
    table, string, number, boolean, or `json.null`; the Lua value to convert to JSON text

### Returns
- json_text
    string or nil. On success, returns a JSON string; otherwise returns nil.
- error_message
    string or nil. On failure, returns the specific error message.

### Notes
Not every Lua value can be converted to JSON, such as userdata, functions, or tables containing userdata or functions.

## JSON NULL Constant
```lua
json.null
```

### Example
```lua
local tb = json.decode('{"nullvalue":null}')
if tb.nullvalue == json.null then
    sys.alert(json.null)
end
```

### Notes
`json.null` is not a function; it is a constant. When printed as text, it appears as "`userdata: 0x0`".
In a Lua table, nil is treated as absent. After conversion to JSON, the corresponding key disappears, so a dedicated value is needed to represent null.
These APIs can be used in XUI.
