# ImageObject:destroy

Purpose: Destroy image

## Signature
```lua
image:destroy()
```

## Example
```lua
sys.msleep(1000)

sys.alert("Screen image change detected")

sys.alert("Tap OK, then screen image change monitoring starts after 1 second")
```

## Notes
Immediately releases the memory occupied by the ImageObject. After destruction, the object can no longer be used.
This method is used for performance optimization. In scenarios where new ImageObjects are created frequently, explicitly calling this method is recommended to avoid continuous memory growth and system pressure.
There is no need to call this method when ImageObjects are created only occasionally; Lua's built-in garbage collector will recycle them automatically after a delay.
