# proc_put

Purpose: Write process dictionary

## Signature
```lua
old_value = proc_put(key, new_value)
```

## Example
```lua
local bill = ""
while bill == "" do
    bill = proc_put("billno", "")
end
print("billno: ".. bill)
```

## Parameters
- key
    string
- new_value
    string, the value to set.

## Returns
- old_value
    string, the previous value at this key, or an empty string if none existed.

## Notes
All process dictionaries starting with `"xxtouch."` or `"1ferver."` are reserved.
Stores a value in the process dictionary and returns the previous value at the key.
If no value previously existed at the key, returns an empty string.
Storing an empty string clears the key.
