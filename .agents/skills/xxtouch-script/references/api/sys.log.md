# sys.log

Purpose: System log

## Signature
```lua
sys.log(...)
```

## Example
```lua
sys.log("Hello World")
```

## Parameters
- ...
    Any number of arguments of any type, representing the log content to output. Arguments are separated by tabs.

## Notes
Outputs standard system logs.
Logs can be viewed in real time by opening the remote interface `https://<device IP address>:46952/log.html` in a computer browser.
Logs are also stored in `/var/mobile/Media/1ferver/log/sys.log` on the device.
`/var/mobile/Media/1ferver/log/sys.log` stores at most 4000 lines; older lines are removed when the limit is exceeded.
