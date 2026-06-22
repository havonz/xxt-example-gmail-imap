# proc_dict_run

Purpose: Process dictionary transaction

## Signature
```lua
return_content, error_message = proc_dict_run(transaction_code)
```

## Example
```lua
function proc_inc(key, int_value)
    return proc_dict_run(string.format([[
        local key = %q
        local value = %d
        local ov = proc_get(key)
        if ov == '' then
            ov = 0
        else
            ov = tonumber(ov)
        end
        if not ov then
            error('not a number')
        end
        proc_put(key, tostring(ov + value))
        return ov
    ]], key, int_value))
end

for i = 1, 20 do
    nLog(proc_inc('haha', 10))
end
```

## Parameters
- transaction_code
    string, transaction Lua code to execute.

## Returns
- return_content
    string | nil, returns the value returned by the code on successful execution, or `nil` on failure.
- error_message
    string | nil, returns `nil` on successful execution, or the error message when code execution errors.

## Notes
All process queue dictionaries starting with `"xxtouch."` or `"1ferver."` are reserved.
Executes process dictionary transaction code. While the transaction code is running, other threads are blocked from accessing and executing `proc_` functions.
A single run cannot exceed 1000000 lines.
If execution succeeds, this Lua code can return a string value.
   That string value is returned to the caller as the return value.
   If the code returns `nil`, an empty string is returned to the caller.
If execution fails, returns `nil, error_message`.

base module, excluding `require`
table module
string module
math module
utf8 module
bit32 module
json module
os.time()
os.clock()
sys.mtime()
utils.gen_uuid()
proc_put(key, value)
proc_get(key)
proc_queue_push_back(key, value)
proc_queue_push_front(key, value)
proc_queue_pop_front(key)
proc_queue_pop_back(key)
proc_queue_pop_value(key, value)
proc_queue_count_value(key, value)
proc_queue_clear(key)
proc_queue_read(key)
proc_queue_size(key)
