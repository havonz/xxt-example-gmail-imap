# XXTDo Framework Guide

XXTDo is a UI-state automation framework built around repeated screen matching.

## Install Helper

When the framework file is missing, use the bundled installer from the skill scripts instead of hand-copying paths:

```bash
python3 scripts/install_xxtdo.py . --apply
```

The installer detects XXT/XPP layout, keeps an existing `lua/scripts/XXTDo.lua` in XXT projects, and writes only when `--apply` is passed.

## Main Concept

Write each recognizable screen as a table, then pass all screen tables to `XXTDo.runloop`.

```lua
local XXTDo = require 'XXTDo'

XXTDo.runloop {
    name = 'main',
    csim = 90,
    interval_ms = 100,
    log = sys.log,

    {
        name = 'home',
        {100, 100, 0xffffff},
        {120, 100, 0x000000},
        run = function(self, index, parent, filter_result)
            XXTDo.log('home matched')
            touch.tap(100, 100)
            sys.msleep(500)
        end,
    },
}
```

## Loop Table Fields

- `name`: required loop name.
- `csim`: global color similarity, default 90.
- `interval_ms`: delay between detection rounds, default 100.
- `log`: optional log function, usually `sys.log`.
- `log_date`: prefix non-table log messages with date time.
- `error`: optional error handler.
- `match_rules`: rule-name to matcher function map.
- `pre_run`: called before each detection round.
- `post_run`: called after each detection round.
- `else_run`: called when no screen matched.
- `timeout_s`: global timeout in seconds.
- `timeout_run`: timeout callback.
- `enter`: called once before the loop.
- `finally`: called when loop exits via `XXTDo.breakloop`.

## Screen Table Fields

- `name`: screen name.
- `csim`: screen-specific similarity.
- `rule`: uses `match_rules[rule]`.
- `run`: action callback after match.
- `timeout_s`: screen stay timeout.
- `timeout_run`: screen timeout callback.
- `group`: multiple color groups; any group can match.

## Return Conventions

- `nil`, `true`, or `'success'`: callback succeeded.
- `false`, `'failed'`, or other values: callback failed; runloop continues trying later screens.

## Important Rules

- `XXTDo.runloop` calls `screen.keep()` before matching each round.
- If `run` changes the screen and immediately checks the new screen, call `screen.keep()` again first.
- Call `XXTDo.breakloop(...)` only inside runloop callbacks.
- Do not call `XXTDo.breakloop` from `match_rules` functions.
- Use `XXTDo.match_rules_default_super()` inside a custom default rule to reuse built-in color matching.
- Use `XXTDo.config('name')` for simple persisted values.
