# proc_get

Purpose: Read process dictionary

## Signature
```lua
value = proc_get(key)
```

## Example
```lua
local bill = proc_get("billno")
if bill ~= "" then
    print("has a bill: ".. bill)
else
    print("no bill")
end
```

## Parameters
- key
    string

## Returns
- value
    string, the value stored at this key, or an empty string if no value exists at the key.

## Notes
All process dictionaries starting with `"xxtouch."` or `"1ferver."` are reserved.
Reads the value from the specified key in the process dictionary.
If no value previously existed at the key, returns an empty string.
