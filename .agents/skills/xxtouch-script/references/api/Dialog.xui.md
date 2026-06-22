# Dialog XUI Engine

Purpose: Use the XUI-backed `dialog` engine in normal scripts. This is not XPP `.xui`; non-XPP scripts still use `dialog()` / `Dialog:*`.

## Enable

```lua
dialog.engine = "xui"
local dlg = dialog()
```

- iOS 16+ uses XUI by default.
- iOS < 16 can opt in with `dialog.engine = "xui"`.
- TrollStore edition only partially implements XUI dialog features; validate complex controls on-device.

## APIs

```lua
dlg:set_config("script-options")
dlg:set_timeout(30)
dlg:set_title("Script Settings")
dlg:set_close_title("Close")
dlg:set_submit_title("Save")
```

```lua
dlg:add_group("Account", "Saved locally only")
dlg:add_input("Username", {placeholder = "Enter username", max_length = 64})
dlg:add_switch("Enable Feature", false)
dlg:add_picker("Mode", {"Normal", "Fast"}, "Normal")
dlg:add_range("Interval", {1, 60, 1}, 5)
```

```lua
dlg:add_image(screen.image())
dlg:add_image({image = screen.image(), height = 420})
```

- `add_group(header, footer)`: following non-group controls belong to this group until the next group.
- `add_input(label, options)`: `options` supports `no_title`, `alignment`, `multiline`, `secure`, `keyboard`, `placeholder`, `default`, `validation_regex`, `prompt`, `message`, `max_length`.
- `add_radio(label, options, default)`: `options` can include `num_per_line`, `no_title`, `mode = "Segment"`.
- `add_checkbox(label, options, defaults)`: `options` can include `num_per_line`, `no_title`.
- `add_range(label, {min, max, step}, default)`: numeric range selector; options can include `no_title`.
- `add_image(...)`: accepts `ImageObject`, image path, PNG/JPEG data, or `{image = ..., height = ...}`. XUI does not auto-scale images to dialog width.

## Control Objects

XUI add-control calls return `dialog, control`. Use the control object for live updates, then reload the dialog.

```lua
local dlg = dialog()
local label, button

dlg, label = dlg:add_label("Waiting", {alignment = "Center"})
dlg, button = dlg:add_button("Generate", {
    alignment = "Center",
    callback = function()
        label:set("label", utils.gen_uuid())
        dlg:reload()
    end,
})

dlg:show()
```

Common control methods: `control:set(key, value)`, `control:remove_from_dialog()`. Call `dlg:reload()` after changing a displayed dialog.

## Read Configuration

```lua
local ok, values = dlg:show()
local loaded, cached = dlg:load()
```

- `show()`: displays the dialog and returns submission status plus option values.
- `load()`: reads persisted values without display; the first return value indicates no submission.

## Ignored Legacy APIs

These APIs have no layout effect under XUI:

```lua
dlg:set_frame(...)
dlg:size(...)
dlg:set_size(...)
dlg:set_corner_radius(...)
```

Only read the corresponding legacy API pages when using the webview engine.
