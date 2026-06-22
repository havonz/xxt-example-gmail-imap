# XXTDo Patterns

## Screen State Loop

```lua
local XXTDo = require 'XXTDo'

XXTDo.runloop {
    name = 'task',
    csim = 92,
    interval_ms = 150,
    log = sys.log,
    timeout_s = 60,
    timeout_run = function(parent, found)
        XXTDo.log('task timeout')
        XXTDo.breakloop(false, 'timeout')
    end,

    {
        name = 'start button',
        {300, 900, 0x12aaff},
        {330, 900, 0xffffff},
        run = function()
            touch.tap(315, 900)
            sys.msleep(800)
        end,
    },

    {
        name = 'done',
        {360, 500, 0x00cc66},
        run = function()
            XXTDo.breakloop(true)
        end,
    },
}
```

## Multiple Color Groups

Use `group` when the same screen has multiple valid visual variants.

```lua
{
    name = 'confirm dialog',
    group = {
        {
            csim = 92,
            {100, 100, 0xffffff},
            {120, 100, 0x333333},
        },
        {
            csim = 90,
            {100, 100, 0xf7f7f7},
            {120, 100, 0x222222},
        },
    },
    run = function(self, index, parent, filter_result)
        touch.tap(500, 900)
        sys.msleep(300)
    end,
}
```

## Custom Match Rule

Use custom rules for image matching, OCR, or app-specific checks.

```lua
local targetImage = image.load_file(XXT_RES_PATH..'/target.png')

XXTDo.runloop {
    name = 'image rule demo',
    log = sys.log,
    match_rules = {
        image = function(self)
            local x, y = screen.find_image(targetImage, self.confidence or 95, 0, 0, 0, 0)
            if x ~= -1 then
                return true, {x = x, y = y}
            end
            return false
        end,
    },
    {
        name = 'target',
        rule = 'image',
        confidence = 95,
        run = function(self, index, parent, pos)
            touch.tap(pos.x, pos.y)
            XXTDo.breakloop(true)
        end,
    },
}

if targetImage then targetImage:destroy() end
```

## Persisted Config

```lua
local XXTDo = require 'XXTDo'
local cfg = XXTDo.config('task')

cfg.run_count = tonumber(cfg.run_count or 0) + 1
sys.log('run_count', cfg.run_count)
```
