# alerthelper

Purpose: Configure automatic handling rules for system alerts.

## APIs

```lua
local alerthelper = require("alerthelper")
alerthelper.setRules(rule_list)
alerthelper.clearRules()
alerthelper.plainPattern(text)
alerthelper.equalPattern(text)
```

- Activated rules continue after the script stops; call `clearRules()` to stop them.
- `plainPattern(text)`: turns text into a plain-character pattern so Lua pattern metacharacters are not interpreted.
- `equalPattern(text)`: creates an exact-match pattern.

## Runtime Limits

- TrollStore edition is unsupported.
- Jailbreak environments that do not enable system-level tweak injection into SpringBoard cannot use alerthelper.
- Safe mode disables the required system tweak environment.
- The module handles system alerts and does not inject third-party Apps.
- Portable scripts should provide a `clearRules()` entry point instead of hardcoding tweak configuration paths.

## Rule Shape

```lua
alerthelper.setRules({
    {
        name = "Deny tracking request",
        conditions = {
            processName = alerthelper.equalPattern("SpringBoard"),
            title = "Allow.-to track",
            buttons = {"Ask App Not to Track", "Allow"},
        },
        actions = {
            clickButton = "Ask App Not to Track",
            log = true,
        },
        wait = 100,
    },
})
```

All conditions in a rule are matched with `and`. String fields use Lua pattern containment matching.

```lua
conditions = {
    bundleIdentifier = "com.example.app",
    processName = "SpringBoard",
    parentClassName = "SBUserNotificationAlert",
    className = "SFDialogController",
    source = "ReportCrash",
    title = "title pattern",
    message = "message pattern",
    cancelButton = "Cancel",
    preferredButton = "Continue",
    buttons = {"Button 1", "Button 2"},
    textFields = {"Placeholder 1", "Placeholder 2"},
}
```

- `buttons` / `textFields` can be strings for single-item matching. When passed as tables, count and matching positions must line up.
- Use `plainPattern` for plain text matching; use `equalPattern` for exact equality.

```lua
actions = {
    textFields = "fill the first text field",
    clickButton = "Allow",
    clickCancel = true,
    clickPreferred = true,
    log = true,
}
```

- `textFields` can be a string, an array, or `{["placeholder"] = "fill value"}`.
- `clickButton` can be a button title or numeric index.
- `clickCancel` / `clickPreferred` click the corresponding button when set to `true`.
- `log = true` uses default logging. A function receives alert info and can decide how to log.
- Button titles and text-field keys in `actions` are treated as literal text, not Lua patterns.

### Match Flow

- Conditions are checked in this order: `bundleIdentifier`, `processName`, `parentClassName`, `className`, `source`, `title`, `message`, `cancelButton`, `preferredButton`, `buttons`, `textFields`.
- Actions run in this order: `textFields`, `clickButton`, `clickCancel`, `clickPreferred`, `log`.
- By default, matching stops after the first matched rule. Set `continue = true` to keep checking later rules.
- `wait` delays action execution in milliseconds; use it when alert animation needs time to settle.
