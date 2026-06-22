# webview.samples

Purpose: webview usage examples

## Common Examples
```lua
local html = [=[
<meta name="viewport" content="width=device-width, initial-scale=1.0" />
<script>
function pushMessage(value) {
  var xhr = new XMLHttpRequest();
  xhr.open("POST", "/proc_queue_push", true);
  xhr.send(JSON.stringify({key: "message_from_webview", value: value}));
}
</script>
<button onclick='pushMessage("close_page")'>Close</button>
<button onclick='pushMessage("show_toast")'>Toast</button>
]=]

local w, h = screen.size()
local factor = screen.scale_factor()

webview.show({
    html = html,
    x = 20 * factor,
    y = 50 * factor,
    width = w - 40 * factor,
    height = 360 * factor,
    corner_radius = 10,
    alpha = 0.9,
    animation_duration = 0.3,
})

proc_queue_clear("message_from_webview")
local eid = thread.register_event("message_from_webview", function(value)
    if value == "close_page" then
        webview.destroy()
        return true
    elseif value == "show_toast" then
        sys.toast("hello from webview")
    end
end)

sys.msleep(30000)
thread.unregister_event("message_from_webview", eid)
webview.destroy()
```

## Common View Shapes
```lua
webview.show({})            -- Fullscreen
webview.show({rotate = 90}) -- Landscape fullscreen
webview.hide()
webview.destroy()
```
