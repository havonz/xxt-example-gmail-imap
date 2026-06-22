# sys.kill / sys.killall

Purpose: Process signals

## Send Signal by PID
```lua
sys.kill(pid, signal)
```

### Example
```lua
sys.kill(app.front_pid(), 9)
```

### Parameters
- pid
    integer
- signal
    integer, signal number.

## Send Signal by Process Name
```lua
sys.killall(signal, [process_name1, process_name2, ...])
```

### Example
```lua
sys.killall(9, "SpringBoard", "backboardd")
```

### Parameters
- signal
    integer, signal number.
- process_name1, process_name2, ...
    string, optional process names. Multiple process names can be specified.
