# screen.keep / screen.unkeep

Purpose: Keep/unkeep screen

## Signature
```lua
screen.keep()
screen.unkeep()
```

## Example
```lua
t = {}
screen.keep()
for k = 1, 640, 10 do
    for j = 1, 960, 10 do
        t[#t + 1] = string.format("%X", screen.get_color(k, j))
    end
end
screen.unkeep()
nLog(t)
```

## Notes
`screen.keep()` saves the current screen content as a single snapshot. Repeated color sampling, color search, screenshot, and image search calls read from the snapshot, reducing repeated screenshot cost.
Calling `screen.keep()` again replaces the old snapshot with the latest screen content. There is no need to call `screen.unkeep()` first.
`screen.unkeep()` releases the snapshot and makes screenshot and color sampling functions read from the live screen again. The two calls do not need to be paired.
`keep` only affects the data source used by XXTouch screenshot and color sampling functions. It does not freeze the actual screen image.
