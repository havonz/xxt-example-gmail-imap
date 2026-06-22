# clear.caches

Purpose: Clear system caches

## Signature
```lua
clear.caches()
```

## Example
```lua
clear.caches()

clear.caches{no_uicache = true} -- Supports clearing without uicache. uicache takes a long time; os.execute('su mobile -c uicache') can be used instead.
```

## Notes
Clears system caches. The system will visibly stutter during execution, and all threads are blocked during this time.
This function may take a very long time. Forcibly stopping the script while it is running will make stopping slow, because the script must be forcibly terminated.
