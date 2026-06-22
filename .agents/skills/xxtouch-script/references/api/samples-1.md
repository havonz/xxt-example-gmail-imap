# samples-1

Purpose: Touch examples/precise swipe

## Signature
```lua
touch.on(x, y):msleep(ms):off()
touch.on(x, y):move(x2, y2):msleep(ms):off()

local te = touch.on(x, y)
te:step_len(px)
te:step_delay(ms)
te:move(x2, y2)
te:off()
```

## Example
```lua
-- It can also be used like this to simulate a single light tap.
touch.on(306, 300):msleep(30):off()

-- Equivalent to:
touch.on(306, 300):move(350, 800):msleep(1000):off()

-- Or like this:
local te = touch.on(306,300)
te:step_len(2)
te:step_delay(0)
te:move(350, 800)
te:msleep(1000)
te:off()
```

## Fast Precise Swipe
```lua
touch.on(125, 2000)
    :step_len(10)      -- First use a longer step length to approach the target quickly.
    :step_delay(1)
    :move(125, 525)
    :step_len(1)       -- Slow down near the target to reduce inertia.
    :step_delay(20)
    :move(125, 505)
    :delay(200)
:off()
```

To reduce inertia, first move slightly past the target along the swipe direction, then slow down, move back to the target point, and lift. If going past the target would move off screen, first swipe to the screen edge, move back a little, and finally return slowly to the target.
