local defaults = "com.yourcompany.A-Script-Bundle"

xui.setup("interface.xui")
xui.setup("sub/xui-sub.xui")

sys.alert(json.encode(xui.read(defaults)))
