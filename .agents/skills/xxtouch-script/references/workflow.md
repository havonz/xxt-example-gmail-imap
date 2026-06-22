# Common XXTouch Workflows

## Tap A Known Coordinate

```lua
screen.init(0)
touch.tap(320, 640)
sys.msleep(500)
```

## Touch Conventions

- Touch coordinates follow the current `screen.init(...)` coordinate system.
- `touch.tap` and `touch.on` allocate finger IDs; release long touches with `:off()`.
- Manual finger IDs are `1~29`; use them only when coordinating multi-touch.
- Too many active fingers can raise `finger pool overflow`.
- Touch methods may yield before returning, so other threads can run during long gestures.

## Precise Swipe Without Inertia

```lua
touch.on(125, 2000)
    :step_len(10):step_delay(1)
    :move(125, 505 - 20)
    :step_len(1):step_delay(20)
    :move(125, 505)
    :delay(200)
:off()
```

Fast precise swipe: overshoot slightly in the swipe direction, slow down, return to the target, pause, then lift. If overshoot would leave the screen, move to the edge, move back a little, then slowly return to the target.

## Match Screen Colors

```lua
screen.keep()
local ok = screen.is_colors({
    {100, 100, 0xffffff},
    {120, 100, 0x000000},
}, 90)
if ok then
    touch.tap(100, 100)
end
```

## Visual API Conventions

- `screen.*` coordinate parameters and returned coordinates follow the current `screen.init(...)` coordinate system.
- `ImageObject:*` coordinates are image-local pixel coordinates.
- In visual APIs that accept `left, top, right, bottom`, `0, 0, 0, 0` means the whole screen or whole image.
- Search APIs usually return `-1, -1` when no match is found; `find_all = true` returns a result table instead.
- `screen.keep()` stores one screen snapshot; a later `screen.keep()` replaces it with a fresh snapshot. `screen.unkeep()` is optional unless you want to release the snapshot or resume live screen reads immediately.
- Image confidence and color similarity use `0~100` style thresholds. Keep thresholds conservative unless false positives are acceptable.
- `csim_algorithm`: `0` XXT default with a steep similarity falloff, `1` Manhattan, `2` Euclidean.
- In `find_color` similarity mode, a negative per-point similarity means anti-match.
- Color ranges like `{0x456789, 0x123456}` match RGB ranges `0x45 +/- 0x12`, `0x67 +/- 0x34`, `0x89 +/- 0x56`, i.e. `0x333333` through `0x579BDF` by channel.

## Find And Tap Image

```lua
local tpl = image.load_file(XXT_RES_PATH..'/button.png')
local x, y = screen.find_image(tpl, 95, 0, 0, 0, 0)
if tpl then tpl:destroy() end
if x ~= -1 then
    touch.tap(x, y)
end
```

## OCR Text

Keep OCR regions small and stable. Use OCR only after color/image checks if a simpler visual check can identify the state reliably.

## Persist Simple State

Plain XXTouch: use documented file/json/plist APIs. In XXTDo mode, prefer `XXTDo.config` for simple values.
