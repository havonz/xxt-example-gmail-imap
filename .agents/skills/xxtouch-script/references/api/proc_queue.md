# proc_queue

Purpose: Process queue read/write/pop/count

## Signature
```lua
size = proc_queue_push(key, value)
size = proc_queue_push_back(key, value)
size = proc_queue_push_front(key, value)
value = proc_queue_pop(key)
value = proc_queue_pop_front(key)
value = proc_queue_pop_back(key)
specified_value_pop_count = proc_queue_pop_value(key, specified_value)
specified_value_count = proc_queue_count_value(key, specified_value)
value_collection = proc_queue_read(key)
value_collection = proc_queue_clear(key)
size = proc_queue_size(key)
```

## Example
```lua
local size = proc_queue_push("billnos", "name")
local first = proc_queue_pop("billnos")
local all = proc_queue_read("billnos")
local count = proc_queue_count_value("billnos", "name")
local removed = proc_queue_pop_value("billnos", "name")
local cleared = proc_queue_clear("billnos")
```

## Parameters
- key
    string, queue key.
- value
    string, value to push. It cannot be an empty string.
- specified_value
    string, value used for counting or batch popping.

## Returns
- size
    integer, queue size. Returns `0` when pushing fails.
- value
    string, returns an empty string when the queue does not exist or is empty.
- value_collection
    array table, returns an empty table when the queue does not exist or is empty.
- specified_value_count, specified_value_pop_count
    integer.

## Notes
`proc_queue_push` is equivalent to `proc_queue_push_back` and pushes to the tail; `proc_queue_push_front` pushes to the head. `proc_queue_pop` is equivalent to `proc_queue_pop_front` and pops from the head; `proc_queue_pop_back` pops from the tail. `proc_queue_read` only reads queue values. `proc_queue_clear` returns all popped values and clears the queue. The queue size limit is `10000`; when exceeded, the earliest pushed values are discarded. All process queue dictionaries starting with `xxtouch.` or `1ferver.` are reserved.
