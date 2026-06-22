# touch.tap

Purpose: Tap screen

## Signature
```lua
touch.tap(x, y [, delay_ms, post_action_wait_ms ])
```

## Example
```lua
touch.tap(100, 100)
touch.tap(100, 100, 300)
touch.tap(100, 100, 300, 1000)
```

## Parameters
- x, y
    integer, the coordinate of the point to tap in the current rotated coordinate system.
- delay_ms
    integer, optional interval between touching the screen and leaving the screen, in milliseconds. Defaults to `30`.
- post_action_wait_ms
    integer, optional wait time after the tap is complete, in milliseconds. Defaults to `0`.

## Notes
Simulates one finger tap at the specified screen position.
For coordinate, finger ID, and thread-yield conventions, see Touch Conventions in `references/workflow.md`.
