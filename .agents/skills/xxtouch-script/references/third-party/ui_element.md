# ui_element

Use `ui_element` when an XXTouch script should interact with visible UI by element properties instead of raw touch coordinates. It is best for buttons, switches, text fields, scrollable pages, pickers, sliders, and system dialogs whose labels or roles are visible to the UI element API.

## Require

```lua
local ui_element = require("ui_element")
```

Build user scripts against this public module only.

## Development With XXTLanControl MCP

When XXTLanControl MCP tools are available, use them to inspect the current device UI before writing selectors:

1. Capture the current UI:
   - Use `device_ui_element_snapshot`.
   - Start with defaults. Increase `maxLevel` only when child elements are missing.
   - Use `includeHitState = true` when the action must verify the target is currently tappable.
   - Use `fallbackHitTest = true` for dialogs, keyboards, WebContent, or sparse element lists.
2. Pick stable fields from `data.element` or items in `data.elements`:
   - Prefer `text` or `title` plus `role`.
   - Add `identifier` or `bundle_id` when present and useful.
   - Add `index` only when duplicate matching elements are expected and their order is stable enough for the task.
   - Avoid copying the full MCP element table into Lua. Convert only the stable fields into a small selector.
3. Validate the selector:
   - Use `device_ui_element_query` with `method = "find"` for one target.
   - Use `method = "find_all"` when checking duplicates or choosing an `index`.
   - Use `method = "text_element_at_position"` only when you already have a physical pixel point to inspect.
   - Use `method = "snapshot"` or `method = "list_text_elements"` for broader page inspection.
4. Validate the action during development:
   - Use `device_ui_element_action` with `action = "click"`, `"input_text"`, `"set_checked"`, `"scroll"`, `"set_value"`, `"increase"`, or `"decrease"`.
   - After an action, query again or capture a screenshot if the script must wait for a state change.

MCP and Lua use physical pixels for exposed coordinates. For fixed-position taps, prefer the XXTouch `touch` module. For semantic UI operations, prefer `ui_element`.

Useful MCP-to-selector conversions:

| MCP element field | Lua selector field |
| --- | --- |
| `text` | `title` or `text` |
| `value` | `value` |
| `identifier` | `identifier` |
| `bundleId` | `bundle_id` |
| `traitsDescription` containing `Button` | `role = "button"` |
| `traitsDescription` containing `Adjustable` | `role = "adjustable"` or a narrower role such as `"slider"` / `"picker"` after validation |
| `canHit = true` | `hittable = true` |
| Duplicate matches from `find_all` | `index = n` |

## Selectors

Selectors are plain Lua tables passed to `find`, `find_all`, and action APIs.

```lua
local agree_button = {
    title = "Agree",
    role = "button",
}

local search_field = {
    text_contains = "Search",
    role = "text_field",
}
```

Common selector fields:

| Field | Use |
| --- | --- |
| `title` / `text` | Exact visible label match. |
| `text_contains` | Visible label substring match. |
| `value` / `value_contains` | Match control value, such as text field content or slider text. |
| `identifier` | Match an element identifier when the App exposes one. |
| `bundle_id` | Restrict matches to one App bundle. |
| `role` | Match a semantic role. Common values include `button`, `switch`, `checkbox`, `radio`, `slider`, `adjustable`, `picker`, `text_field`, `static_text`, `keyboard_key`, `scrollable`, `link`, `image`, and `map`. |
| `traits` | Require one trait or a list of traits from `traitsDescription`. |
| `visible` | Match visible state. |
| `hittable` | Match whether the element can currently be hit from the top layer. |
| `checked` | Match switches, checkboxes, or selectable controls with a known checked state. |
| `selected` | Match selected state when exposed by the UI. |
| `index` | Select the Nth match, using Lua 1-based indexing. |

Selector guidance:

- Prefer small selectors: `title/text` + `role` is usually enough.
- Use `text_contains` for localized or dynamic labels only when an exact label is not stable.
- Use `hittable = true` when a covered element must not be selected.
- Avoid relying on coordinates, size, window ids, or diagnostic fields unless the UI has no stable labels.

## Element Fields

Query APIs return plain Lua tables. Fields vary by App, iOS version, and control type, so check for nil before relying on optional fields.

Common fields:

| Field | Meaning |
| --- | --- |
| `text` | Visible label or readable title. |
| `value` | Current control value. |
| `identifier` | Element identifier, when exposed. |
| `bundleId` | Owning App bundle id. |
| `x`, `y`, `width`, `height` | Frame in physical pixels. |
| `centerPoint` | Center point table, usually `{ x = ..., y = ... }`, in physical pixels. |
| `children` | Child elements, when requested by depth options. |
| `traitsDescription` | Trait names such as `Button`, `StaticText`, or `Adjustable`. |
| `isVisible` | Visible state. |
| `checked` | Known checked state for toggles and selectable controls. |
| `hasTextEntry` | Whether the target looks like a text input. |
| `isKeyboardKey` | Whether the element is a keyboard key. |
| `absoluteValue` | Normalized numeric value for some adjustable controls. |
| `canHit` / `hitVerified` | Hit-state diagnostics when requested. |
| `hitTestPoint` | Verified hit point in physical pixels when available. |

Use returned fields to build selectors; do not persist whole element snapshots unless the script intentionally works with a fresh `snapshot()` object.

## Common Options

Most query and action APIs accept an `options` table.

| Option | Use |
| --- | --- |
| `max_level` | Limit child element depth. Use a small value unless nested children are needed. |
| `max_elements` | Limit returned element count during broad snapshots. |
| `include_hit_state` | Add fields such as `canHit`, `hitVerified`, and `hitTestPoint`. |
| `fallback_hit_test` | Let the API use top-layer hit results when the normal element list is sparse or empty. |
| `hit_test` | Force broader hit-based sampling for difficult pages. Use only when needed. |
| `hit_test_spacing` | Sampling spacing for `hit_test`, in logical screen units. |

`list_text_elements()` keeps compatibility defaults and does not enable `fallback_hit_test` unless you pass it explicitly. Other APIs that support `fallback_hit_test`, including `find`, `find_all`, `snapshot`, and action helpers, enable it by default. If a script needs old list behavior, leave `list_text_elements()` at defaults; if it needs element discovery that works better on dialogs, keyboards, WebContent, or sparse pages, prefer `find` / `snapshot` or pass `fallback_hit_test = true`.

## Query APIs

### `list_text_elements([options])`

Returns a compatible element array for the current foreground App.

```lua
local elements, err = ui_element.list_text_elements({
    max_level = 2,
    include_hit_state = true,
})

if not elements then
    return nil, err
end
```

Use it for quick page reads. For robust actions, prefer `find`, `find_all`, or `snapshot`.

### `text_element_at_position(x, y[, options])`

Returns the element at a physical pixel coordinate.

```lua
local item, err = ui_element.text_element_at_position(300, 500, {
    include_hit_state = true,
})
```

Use it after image/OCR matching or MCP coordinate inspection when you need to convert a point into UI element properties.

### `get_ui_snapshot_once([options])`

Returns a diagnostic snapshot object with `elements`, `count`, and related status fields.

```lua
local report, err = ui_element.get_ui_snapshot_once({
    include_hit_state = true,
    max_level = 4,
    max_elements = 1000,
})
```

Use it while developing or diagnosing missing elements. Business logic should usually use `find`, `find_all`, or `snapshot`.

### `find(selector[, options])`

Returns the first matching element, or `nil, err`.

```lua
local button, err = ui_element.find({
    title = "Continue",
    role = "button",
}, {
    include_hit_state = true,
})

if button then
    ui_element.click(button)
end
```

### `find_all(selector[, options])`

Returns all matching elements. No match returns an empty table.

```lua
local cells = ui_element.find_all({
    text_contains = "Apple ID",
})

if #cells >= 2 then
    ui_element.click(cells[2])
end
```

### `snapshot([options])`

Captures a reusable UI object with query and action methods.

```lua
local ui, err = ui_element.snapshot({ include_hit_state = true })
if not ui then
    return nil, err
end

local search = ui:find({ text_contains = "Search", role = "text_field" })
if search then
    ui:input_text(search, "hello")
end

ui_element.release(ui)
```

Refresh the snapshot after navigation, scrolling, page updates, or modal changes.

## Action APIs

Actions return `true, info` on success and `nil, err` on failure.

```lua
local ok, err = ui_element.click({ title = "Settings", role = "button" })
if not ok then
    return nil, err
end
```

Common actions:

| API | Example |
| --- | --- |
| `click(selector_or_element[, options])` | `ui_element.click({ title = "OK", role = "button" })` |
| `scroll(selector_or_element, direction[, options])` | `ui_element.scroll({ text = "Contacts" }, "down")` |
| `scroll(direction[, options])` | `ui_element.scroll("down", { steps = 2 })` |
| `input_text(selector_or_element, text[, options])` | `ui_element.input_text({ role = "text_field" }, "hello")` |
| `set_text(selector_or_element, text[, options])` | `ui_element.set_text({ identifier = "account" }, "abc")` |
| `clear_text(selector_or_element[, options])` | `ui_element.clear_text({ role = "text_field" })` |
| `toggle(selector_or_element[, options])` | `ui_element.toggle({ title = "Wi-Fi", role = "switch" })` |
| `set_checked(selector_or_element, checked[, options])` | `ui_element.set_checked({ title = "Wi-Fi", role = "switch" }, true)` |
| `set_value(selector_or_element, value[, options])` | `ui_element.set_value({ role = "slider" }, "50%")` |
| `increase(selector_or_element[, options])` | `ui_element.increase({ role = "picker" }, { steps = 1 })` |
| `decrease(selector_or_element[, options])` | `ui_element.decrease({ role = "picker" }, { steps = 1 })` |
| `release(element_or_snapshot)` | `ui_element.release(ui)` |

Direction values for `scroll` are `"down"`, `"up"`, `"left"`, `"right"`, `"top"`, and `"bottom"`.

## Short Patterns

### Click By Title

```lua
local ui_element = require("ui_element")

local ok, err = ui_element.click({
    title = "Continue",
    role = "button",
}, {
    include_hit_state = true,
})

if not ok then
    return nil, err
end
```

### Input Search Text

```lua
local ui_element = require("ui_element")

local ok, err = ui_element.input_text({
    text_contains = "Search",
    role = "text_field",
}, "hello")

if not ok then
    return nil, err
end
```

### Set A Switch

```lua
local ui_element = require("ui_element")

local ok, err = ui_element.set_checked({
    title = "Use Cellular Data",
    role = "switch",
}, true)

if not ok then
    return nil, err
end
```

### Scroll The Main Page

```lua
local ui_element = require("ui_element")

for _ = 1, 3 do
    local ok, err = ui_element.scroll("down", { steps = 1 })
    if not ok then
        return nil, err
    end
    sys.msleep(300)
end
```

### Reuse One Snapshot

```lua
local ui_element = require("ui_element")

local ui, err = ui_element.snapshot({ include_hit_state = true })
if not ui then
    return nil, err
end

local account = ui:find({
    text_contains = "Account",
    role = "button",
})

if account then
    local ok, click_err = ui:click(account)
    if not ok then
        ui_element.release(ui)
        return nil, click_err
    end
end

ui_element.release(ui)
```

### Convert MCP Snapshot Data To Script

If MCP returns an element like:

```json
{
  "text": "Continue",
  "traitsDescription": ["Button"],
  "x": 210,
  "y": 780,
  "width": 220,
  "height": 64,
  "canHit": true
}
```

Write a selector-based script:

```lua
local ui_element = require("ui_element")

local ok, err = ui_element.click({
    title = "Continue",
    role = "button",
    hittable = true,
})

if not ok then
    return nil, err
end
```

Only fall back to coordinates when there is no stable label or role:

```lua
touch.tap(320, 812)
```

## Failure Handling

Common failure strings include:

- `"target not found"`
- `"ambiguous target"`
- `"target is not hittable or changed"`
- `"text input target unavailable"`
- `"action unsupported"`
- `"state unavailable"`
- `"state unchanged"`
- `"value unchanged"`

Handle failures at the workflow boundary. If a selector is ambiguous, inspect with `find_all`, add `role` or `index`, then validate with MCP before shipping the script.
