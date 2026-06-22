# webview.show / webview.hide / webview.destroy / webview.eval / webview.frame

Purpose: webview show/hide/destroy/evaluate JS/frame

## Show Webview
```lua
webview.show { -- All parameters are optional.
    html = html_content,
    x = origin_x,
    y = origin_y,
    width = width,
    height = height,
    corner_radius = corner_radius,
    alpha = opacity,
    animation_duration = animation_duration,
    rotate = rotation_angle,
    level = window_level,
    opaque = area_opaque,
    ignores_hit = whether_to_ignore_touch_events,
    can_drag = whether_draggable,
    is_secure = whether_secure_component,
}
```

### Example
```lua
webview.show{
    html = [[
        <html>
        <body style="font-size:32px;color:white;background:rgba(0,0,0,.6);">
            Running...
        </body>
        </html>
    ]],
    x = 40,
    y = 80,
    width = 300,
    height = 120,
    corner_radius = 12,
    ignores_hit = true,
}
```

### Notes
Except for the `html` parameter, which keeps the state from the previous `show`, all other parameters are reset to their defaults on each call.

## Hide Webview
```lua
webview.hide([ id ])
```

### Example
```lua
webview.show{html = "<b>loading</b>"}
sys.msleep(1000)
webview.hide()
```

## Destroy Webview
```lua
webview.destroy([ id ])
```

### Example
```lua
webview.show{html = "<b>done</b>"}
sys.msleep(1000)
webview.destroy()
```

### Notes
When the script stops, all displayed webviews are automatically destroyed.

## Evaluate JS
```lua
str = webview.eval(js [, id ])
```

### Example
```lua
r = webview.eval("a = 3; b = 2; a * b;")
```

### Parameters
- js
    string, JS code to execute

### Returns
- str
    string, return value produced by executing the JS code

## Get Frame and Level
```lua
frame = webview.frame([ id ])
```

### Example
```lua
local frame = webview.frame(1)
sys.alert(
    "Position: ".."("..frame.x..","..frame.y..")\n"..
    "Size: " .. "(width: "..frame.width..", height: "..frame.height..")\n"..
    "Level: ".."("..frame.level..")"
)
```

### Returns
- frame
    table, returns the current webview's frame and level information

## Common Parameters
- id
    integer, optional. Represents the current webview id. Different ids can be used to display multiple webviews at the same time. Range: 1 to 1000. Default: 1.
