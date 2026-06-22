# touch.on / touch.move / touch.off / TouchObject

Purpose: Touch down/move/wait/up

## Signature
```lua
touch_event = touch.on(x, y)
touch_event = touch_event:step_len(step_length)
touch_event = touch_event:step_delay(delay_per_step)
touch_event = touch_event:move(x, y)
touch_event = touch_event:msleep(milliseconds)
touch_event = touch_event:press([ pressure, speed ]) -- deprecated
touch_event:off([ x, y ])

touch.on(finger_id, x, y)
touch.move(finger_id, x, y)
touch.off(finger_id[, x, y])
```

## Example
```lua
touch.on(100, 100):move(200, 200):off()
touch.on(100, 100):off(105, 95)
touch.on(100, 100):msleep(300):off()
touch.on(100, 100):step_len(3):step_delay(0.2):move(200, 200):off()

touch.on(1, 100, 100)
for i = 1, 100 do
    touch.move(1, 100, 100 + i)
end
touch.off(1)

touch.on(100, 100):press(2000, 50):off()
```

## Parameters
- x, y
    integer, touch coordinates in the current rotated coordinate system.
- finger_id
    integer, in the range `1` to `29`. When specified manually, you must call `touch.off(finger_id[, x, y])` yourself.
- step_length
    integer, optional movement step length for `:move`. Defaults to `2`.
- delay_per_step
    number, optional delay per step for `:move`, in milliseconds. Defaults to `0.1`.
- milliseconds
    number, optional delay time that blocks the current thread, in milliseconds. Defaults to `0.1`.
- pressure
    integer, optional, in the range `1` to `10000`. Defaults to `1000`. `:press` is deprecated.
- speed
    integer, optional speed for applying pressure, in the range `1` to `100`. Defaults to fastest. `:press` is deprecated.

## Returns
- touch_event
    touch event object. Object methods return the object itself for chained calls.

## Notes
`touch.on(x, y)` automatically allocates a finger ID, and `:off()` releases the ID occupied by that touch object.
`touch.move(id, x, y)` moves to the target position immediately and cannot configure stepping. Object-style `:move(x, y)` uses the current touch object's step configuration.
`:msleep(ms)` does not change the touch object; it only blocks the current thread. Its alias is `:delay(ms)`.
`:press(...)` is deprecated. It may only work on old 3D Touch devices; new scripts should not rely on it.
For fast and precise swipes without inertia, move past the target first, then slowly return to the target. See Precise Swipe Without Inertia in `references/workflow.md`.
For coordinate, finger ID, `finger pool overflow`, and thread-yield conventions, see Touch Conventions in `references/workflow.md`.
