local defaults = "com.yourcompany.A-Script-Bundle"

xui.setup("interface.xui")
xui.setup("sub/xui-sub.xui")

local config = xui.read(defaults)
local enabled = config.auto_run == true
local mode = config.mode or "normal"
local delay = tonumber(config.delay_seconds or 0.5)

sys.alert(json.encode({
    enabled = enabled;
    mode = mode;
    delay = delay;
}))

xui.show("interface.xui")
