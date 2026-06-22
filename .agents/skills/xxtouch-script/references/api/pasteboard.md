# pasteboard

Purpose: Clipboard read/write/clear

## Signature
```lua
data = pasteboard.read([ uti ])
success = pasteboard.write(data [, uti ])
success = pasteboard.write(pasteboard_item_or_list [, options ])
success = pasteboard.write_items(pasteboard_item_or_list [, options ])
old_data_list = pasteboard.clear()
```

## Example
```lua
local text = pasteboard.read()
local forced_text = pasteboard.read("public.text")
pasteboard.write("hello")
pasteboard.write(screen.image():png_data(), "public.png")
pasteboard.write([[{\rtf1\ansi\b bold \i italic}]], "public.rtf")

pasteboard.write({
    ["public.utf8-plain-text"] = "plain text",
    ["public.rtf"] = [[{\rtf1\ansi\b bold \i italic}]],
    ["public.html"] = "<b>html</b>",
}, {
    local_only = true,
    expiration_date = os.time() + 3600,
})

for _, item in ipairs(pasteboard.clear()) do
    nLog(item.type, item.data)
end
```

## Parameters
- uti
    string, optional. Uniform Type Identifier. When reading, specifying it forces reading in that format and returns `""` on failure. When writing, the default is `"public.utf8-plain-text"`.
- data
    string, content to write to the pasteboard.
- pasteboard_item_or_list
    table. For an item, keys are Uniform Type Identifiers and values are string data. For a list, each entry is one pasteboard item.
- options
    table, optional. `local_only` stores only on the local device, and `expiration_date` is a Unix timestamp in seconds, supported on iOS 10+. iOS 9 ignores options.

## Returns
- data
    string. May be text or binary data. Returns `""` when it cannot be read as the specified type.
- success
    boolean.
- old_data_list
    table. `pasteboard.clear()` returns the data list before clearing; each item contains `type` and `data`.

## Notes
`pasteboard.write_items(...)` is the explicit form for writing pasteboard items. `pasteboard.write(pasteboard_item_or_list, options)` also supports the same data shape. Common UTIs: `public.utf8-plain-text`, `public.rtf`, `public.html`, `public.png`.
