# print / print.out

Purpose: Print buffer read/write

## Write to Print Buffer
```lua
print([ arg1, arg2, ... ])
```

### Example
```lua
print("hello world")
```

### Parameters
- arg1, arg2, ...
    any type, optional varargs. Values are converted to text and output to the buffer, separated by `"\t"`.

### Notes
`print` is Lua's built-in print output function. In XXTouch, it writes content to the print buffer.

## Read the Print Buffer
```lua
buffer_content = print.out()
```

### Example
```lua
sys.alert(print.out())
```

### Returns
- buffer_content
    string, the accumulated content in the `print` print buffer

### Notes
`print.out` clears the `print` print buffer and returns its accumulated content.
