# XXTouch 脚本开发指南
XXTouch 基于 Lua 5.3 开发了大量扩展模块，方便脚本编写者调用系统底层功能。

## 编码原则
只允许使用 Lua 5.3 内置函数和本手册中提及的模块、函数、方法及变量。非必要不引入第三方模块。

## 全局变量
- `XXT_HOME_PATH`: XXT 主路径
  - `XXT_HOME_PATH` 在不同版本的 XXT 中可能不同，脚本中应使用该变量来引用主路径
- `XXT_RES_PATH`: XXT 资源路径
  - 通常为 `XXT_HOME_PATH.."/res"`
- `XXT_LUA_PATH`: XXT Lua 模块路径
  - 通常为 `XXT_HOME_PATH.."/lua"`
- `XXT_SCRIPTS_PATH`: XXT 脚本路径
  - 通常为 `XXT_HOME_PATH.."/lua/scripts"`
- `XXT_LIB_PATH`: XXT C 库路径
  - 通常为 `XXT_HOME_PATH.."/lib"`
- `XXT_LOG_PATH`: XXT 日志路径
  - 通常为 `XXT_HOME_PATH.."/log"`
- `XXT_DAEMONS_PATH`: XXT 额外守护脚本路径
  - 通常为 `XXT_HOME_PATH.."/daemons"`
- `XXT_TESSDATA_PATH`: XXT Tesseract 语言数据路径
  - 通常为 `XXT_HOME_PATH.."/tessdata"`
- `XXT_MODELS_PATH`: XXT 模型数据路径，PaddleOCR 和 CoreML 的模型存放位置
  - 通常为 `XXT_HOME_PATH.."/models"`
- `IS_TROLLSTORE_EDITION`: XXT 是否为 TrollStore 版本
- `XXT_SYSTEM_PATH`: XXT 执行文件根路径
- `XXT_EXE_PATH`: XXT 服务程序路径

## 项目结构
脚本启动文件为 main.lua，且必须位于 `lua/scripts/` 目录下。
扩展名为 *.xxt 和 *.lua 格式模块可以放到 `lua/` 或者 `lua/scripts/` 目录下的任意位置，可通过 require "<module_name>" 引用。
资源文件放到当前项目的 `res/` 目录下，可以在脚本中通过 XXT_RES_PATH 变量访问，例如 `XXT_RES_PATH.."/1.png"`。
```
脚本路径/
├── res/
│   ├── 1.png
│   └── 2.png
└── lua
  ├── a.lua
  ├── b.xxt
  └── scripts/
      ├── c.lua
      └── main.lua
```

## 全局函数
### nLog(argA, argB, ...)
```lua
-- 输出日志到开发工具
nLog('haha')
nLog(1, 2, 3, {3, 2, 2})
```

## 开发辅助模块
### get_elapsed_ms()
```lua
-- 获取当前脚本已执行的毫秒数
local tm = get_elapsed_ms()
sys.msleep(1)
tm = get_elapsed_ms() - tm
nLog('sys.msleep(1) 耗时 '..tm..' ms')
```

### jbroot(systemPath)
```lua
-- 获取系统根路径对应的越狱根路径
jbr = jbroot('/')
nLog(jbr) -- 输出：/var/containers/Bundle/Application/.jbroot-XXXXXXXXXXXXXXXX/
```

### rootfs(jailbreakPath)
```lua
-- 获取越狱根路径对应的系统根路径
rfs = rootfs('/var/containers/Bundle/Application/.jbroot-XXXXXXXXXXXXXXXX/')
nLog(rfs) -- 输出：/
```

### print(...)
```lua
-- 打印内容到缓冲区
print('调试', 1, {foo = 'bar'})
```

### print.out()
```lua
-- 将打印缓冲区的内容提出来
local list = file.list(XXT_SCRIPTS_PATH)
if list then
  for _, name in ipairs(list) do
    print(name)
  end
  sys.alert(print.out())
end
```

### fork_dostring(luacode, timeout_ms)
```lua
-- 创建一个进程执行 Lua 代码，阻塞当前 thread
thread.dispatch(function()
  local out, ok, statusText, statusCode, err = fork_dostring([[
    print('子进程开始执行')
    proc_queue_push('子进程消息1', 'ok')
  ]], 5000)
  nLog('输出内容', out)
end)

thread.register_event('子进程消息1', function(msg)
  nLog('收到子进程消息', msg)
end)
```

## 控制流程模块
### register_atexit(name, callback)
```lua
-- 注册脚本退出时执行的回调
register_atexit("cleanup", function()
  sys.toast("脚本退出前清理资源")
  sys.msleep(300)
end)

while true do
  sys.toast("使用音量键尝试退出脚本\n" .. os.date("%Y-%m-%d %H:%M:%S"))
  sys.msleep(1000)
end
```

### os.restart(scriptPath)
```lua
-- 重启当前脚本或跳转到指定脚本文件
os.restart() -- 重启到 “当前脚本”
os.restart(utils.launch_args().path) -- 重启到 “当前脚本文件”
os.restart(XXT_SCRIPTS_PATH..'/1.lua') -- 重启到脚本目录中的 1.lua
```

## 应用程序模块
### 类 app*

### app.bundle_path(appID)
```lua
-- 获取 App 的捆绑包路径
nLog(app.bundle_path('com.apple.mobilesafari'))
```

### app.data_path(appID)
```lua
-- 获取 App 的数据容器路径
nLog(app.data_path('com.apple.mobilesafari'))
```

### app.group_info(appID)
```lua
-- 获取 App 的分组信息
nLog(app.group_info('com.apple.mobilesafari'))
```

### app.plugin_info(appID)
```lua
-- 获取 App 的插件信息
nLog(app.plugin_info('com.apple.mobilesafari'))
```

### app.team_id(appID)
```lua
-- 获取 App 的 TEAM ID
local teamID = app.team_id('com.apple.mobilesafari')
nLog(teamID or '未找到 Team ID')
```

### app.set_tcc(appID, service, state)
```lua
-- 设置 App 的 TCC 权限
-- 传入服务标识（如 kTCCServicePasteboard），返回是否成功与原状态值
local ok, oldState = app.set_tcc('com.apple.SafariViewService', 'kTCCServicePasteboard', 2)
nLog(ok, oldState)
```

### app.notification_permissions(appID, operation, info)
```lua
-- 获取、设置或重置 App 通知权限，20260529 以后版本、iOS 14 以上可用
local bid = 'com.apple.mobilesafari'
local info = app.notification_permissions(bid, 'get')
if info then
  info.allowsNotifications = true
  app.notification_permissions(bid, 'set', info)
end
app.notification_permissions(bid, 'reset')
```

### app.local_network_permissions(appID, operation, value)
```lua
-- 获取、设置或重置 App 本地网络权限，20260529 以后版本、iOS 14 以上可用
local bid = 'com.apple.mobilesafari'
local info = app.local_network_permissions(bid, 'get')
nLog(info)
app.local_network_permissions(bid, 'set', true)
app.local_network_permissions(bid, 'reset')
```

### app.pop_banner(appID, title, content)
```lua
-- 弹出一个 App 通知，依赖于完整越狱环境，并在 Cydia 或者 Sileo 安装基础依赖 “libbulletin” 方可使用
app.pop_banner('com.tencent.mqq', 'QQ', '[QQ红包]您收到一个假红包')
```

### app.run(appID)
```lua
-- 运行 App
-- status 为 0 表示成功启动，非 0 则表示启动失败，msg 为启动状态文本描述
local status, msg = app.run('com.apple.mobilesafari')
if status == 0 then
  nLog('Safari 启动成功')
else
  nLog('Safari 启动失败', msg)
end
```

### app.close(appID)
```lua
-- 关闭 App
app.close('com.apple.mobilesafari')
```

### app.quit(appID)
```lua
-- 模拟使用上划退出 App
app.quit('com.apple.mobilesafari')
```

### app.is_running(appID)
```lua
-- 检测 App 是否正在运行
if app.is_running('com.apple.mobilesafari') then
  sys.alert('Safari 正在运行')
end
```

### app.lsof(identifier)
```lua
-- 获取 App 打开的文件描述符及套接字信息
local files, errMsg = app.lsof('com.apple.mobilesafari')
```

### app.localized_name(appID)
```lua
-- 获取 App 的本地化名字
nLog(app.localized_name('com.apple.mobilesafari'))
```

### app.png_data_for_bid(appID)
```lua
-- 获取 App 的图标数据
local png_data = app.png_data_for_bid('com.apple.mobilesafari')
```

### app.pid_for_bid(appID)
```lua
-- 获取正在运行 App 的进程号
local pid = app.pid_for_bid('com.apple.mobilesafari')
```

### app.used_memory(appID)
```lua
-- 获取 App 当前内存消耗
nLog(app.used_memory('com.apple.mobilesafari'))
```

### app.front_bid()
```lua
-- 获取前台 App 的标识符
if 'com.apple.mobilesafari' == app.front_bid() then
  sys.alert('Safari 正在前台运行')
end
```

### app.front_pid()
```lua
-- 获取前台 App 的进程号
local pid = app.front_pid()
```

### app.open_url(URL)
```lua
-- 前台打开一个 URL
app.open_url('http://www.google.com') -- 使用默认浏览器打开网页
app.open_url('prefs:root=SAFARI&path=CLEAR_HISTORY_AND_DATA') -- 打开系统设置中的 Safari 清除历史记录页面
```

### app.open_url(bid, URL)
```lua
-- 使用某 App 前台打开一个 URL
app.open_url('com.google.chrome.ios', 'http://www.google.com') -- 使用 Chrome 打开网页
```

### app.bundles()
```lua
-- 获取 App 标识符列表
for _, bid in ipairs(app.bundles()) do
    app.close(bid)
end
```

### app.all_procs()
```lua
-- 获取进程列表
for _, proc in ipairs(app.all_procs()) do
    nLog(proc.pid, proc.name, proc.path)
end
-- app.all_procs() 返回结构示例：
--[[
{
  {
    pid = 1234,
    ppid = 1,
    uid = 501,
    name = "MobileSafari",
    path = "/Applications/MobileSafari.app/MobileSafari",
  },
  {
    pid = 1235,
    ppid = 1,
    uid = 501,
    name = "Preferences",
    path = "/Applications/Preferences.app/Preferences",
  },
  ...
}
--]]
```

### app.install(ipaPath)
```lua
-- 安装 IPA
-- 第二个参数为 true 表示强制覆盖安装
local ok = app.install(XXT_SCRIPTS_PATH..'/1.ipa', true)
nLog('安装状态', ok)
```

### app.uninstall(appID)
```lua
-- 卸载一个 App
local ok = app.uninstall('com.tencent.mqq')
nLog('卸载状态', ok)
```

## 清理模块
### 类 clear*

### clear.keychain(teamid)
```lua
-- 清理某个或某组钥匙串信息
clear.keychain(app.team_id('com.google.chrome.ios')) -- 按照 Team ID 关联清理，推荐
clear.keychain('com.google') -- 按照反域名关联清理，不推荐，可能清理不干净也可能误伤
```

### clear.all_keychain()
```lua
-- 清理所有 App 的钥匙串信息
clear.all_keychain()
```

### clear.cookies()
```lua
-- 清理浏览器 Cookies
clear.cookies()
```

### clear.caches()
```lua
-- 清理系统缓存
clear.caches()
```

### clear.all_photos()
```lua
-- 清除相册中所有本地照片
clear.all_photos()
```

### clear.app_data(appID)
```lua
-- 清理某个应用的存档数据
local ok = clear.app_data('com.google.chrome.ios')
nLog('清理存档结果', ok)
```

### clear.idfav(newIDFAs)
```lua
-- 清理 IDFA/V
local oldIdfav = clear.idfav('read') -- 只读取当前 IDFAV
file.writes(XXT_SCRIPTS_PATH..'/idfavs.bak', oldIdfav)
clear.idfav() -- 不带参数则清理后让系统重新生成
clear.idfav(oldIdfav) -- 传入旧 IDFAV 进行恢复
```

## 设备模块
### 类 device*

### device.reset_idle()
```lua
-- 重置自动锁屏倒计时
device.reset_idle() -- 维持常亮时可周期调用
```

### device.set_autolock_time(minutes)
```lua
-- 设置自动锁屏分钟数
device.set_autolock_time(0) -- 不自动锁屏
device.set_autolock_time(5) -- 5 分钟自动锁屏
```

### device.lock_screen()
```lua
-- 锁定屏幕
device.lock_screen()
nLog('是否已锁定', device.is_screen_locked())
device.unlock_screen('1234') -- 如设置了密码需传入
```

### device.unlock_screen(password)
```lua
-- 解锁屏幕
device.unlock_screen('1234')
nLog('解锁结果', device.is_screen_locked())
```

### device.is_screen_locked()
```lua
-- 获取屏幕锁定状态
nLog('锁屏状态', device.is_screen_locked())
```

### device.front_orien()
```lua
-- 获取前台应用的画面方向
nLog('前台方向', device.front_orien())
```

### device.lock_orien()
```lua
-- 锁定屏幕旋转
device.lock_orien()
```

### device.unlock_orien()
```lua
-- 解锁屏幕旋转
device.unlock_orien()
```

### device.is_orien_locked()
```lua
-- 获取屏幕旋转锁定状态
device.is_orien_locked()
```

### device.vibrator()
```lua
-- 振动设备
device.vibrator()
```

### device.assistive_touch_on()
```lua
-- 打开 AssistiveTouch
device.assistive_touch_on()
```

### device.assistive_touch_off()
```lua
-- 关闭 AssistiveTouch
device.assistive_touch_off()
```

### device.play_sound(soundPath)
```lua
-- 后台播放声音（不会阻塞脚本运行）
device.play_sound(XXT_SCRIPTS_PATH..'/十年.mp3')
sys.msleep(3 * 1000) -- 播放期间脚本继续运行
```

### device.set_volume(volume)
```lua
-- 设置设备音量
device.set_volume(0.3) -- 0.0~1.0
```

### device.type()
```lua
-- 获取设备类型
nLog('设备类型', device.type())
```

### device.name()
```lua
-- 获取设备名
nLog('设备名', device.name())
```

### device.set_name(name)
```lua
-- 设置设备名
device.set_name('iPhavonz')
```

### device.udid()
```lua
-- 获取设备UDID
nLog(device.udid())
```

### device.serial_number()
```lua
-- 获取设备的序列号
nLog(device.serial_number())
```

### device.wifi_mac()
```lua
-- 获取设备的 Wi-Fi MAC 地址
nLog(device.wifi_mac())
```

### device.bluetooth_mac()
```lua
-- 获取设备的蓝牙 MAC 地址
nLog(device.bluetooth_mac())
```

### device.ifaddrs()
```lua
-- 获取设备所有的接口 IP
nLog(device.ifaddrs())
```

### device.battery_level()
```lua
-- 获取当前设备电池剩余电量
nLog('电量', device.battery_level())
```

### device.battery_state()
```lua
-- 获取当前设备充电状态
nLog('充电状态', device.battery_state())
```

### device.brightness()
```lua
-- 获取背光亮度值
nLog('亮度', device.brightness())
```

### device.set_brightness(value)
```lua
-- 设置背光亮度值
device.set_brightness(0.2) -- 0.0~1.0
```

### device.reduce_motion_on()
```lua
-- 打开减弱动态效果开关
device.reduce_motion_on()
```

### device.reduce_motion_off()
```lua
-- 关闭减弱动态效果开关
device.reduce_motion_off()
```

### device.reduce_motion_slide_on()
```lua
-- 打开减弱交叉淡出过渡效果开关
device.reduce_motion_slide_on()
```

### device.reduce_motion_slide_off()
```lua
-- 关闭减弱交叉淡出过渡效果开关
device.reduce_motion_slide_off()
```

### device.wifi_on()
```lua
-- 打开 Wi-Fi
device.wifi_on()
```

### device.wifi_off()
```lua
-- 关闭 Wi-Fi
device.wifi_off()
```

### device.is_wifi_on()
```lua
-- 获取 Wi-Fi 开关状态
nLog('Wi-Fi 是否开启', device.is_wifi_on())
```

### device.wifi_info()
```lua
-- 获取当前 Wi-Fi 信息
local info = device.wifi_info()
nLog(info and info.SSID, info and info.BSSID)
```

### device.data_on()
```lua
-- 打开蜂窝数据
device.data_on()
```

### device.data_off()
```lua
-- 关闭蜂窝数据
device.data_off()
```

### device.is_data_on()
```lua
-- 获取蜂窝数据开关状态
nLog('蜂窝数据', device.is_data_on())
```

### device.bluetooth_on()
```lua
-- 打开蓝牙
device.bluetooth_on()
```

### device.bluetooth_off()
```lua
-- 关闭蓝牙
device.bluetooth_off()
```

### device.is_bluetooth_on()
```lua
-- 获取蓝牙开关状态
nLog('蓝牙状态', device.is_bluetooth_on())
```

### device.airplane_on()
```lua
-- 打开飞行模式
device.airplane_on()
```

### device.airplane_off()
```lua
-- 关闭飞行模式
device.airplane_off()
```

### device.is_airplane_on()
```lua
-- 获取飞行模式开关状态
device.is_airplane_on()
```

### device.vpn_on()
```lua
-- 连接当前所选 VPN
device.vpn_on()
```

### device.vpn_off()
```lua
-- 断开当前已连接的 VPN
device.vpn_off()
```

### device.is_vpn_on()
```lua
-- 获取 VPN 开关状态
device.is_vpn_on()
```

### device.flash_on()
```lua
-- 打开闪光灯
device.flash_on()
```

### device.flash_off()
```lua
-- 关闭闪光灯
device.flash_off()
```

### device.is_flash_on()
```lua
-- 获取闪光灯开关状态
device.is_flash_on()
```

### device.join_wifi(SSID, password)
```lua
-- 加入到一个无线接入点
local ok, err = device.join_wifi('Tenda_9B3F', '12345678', 15000)
nLog('连入 Wi-Fi', ok, err)
```

### device.forget_wifi(SSID)
```lua
-- 遗忘无线接入点
device.forget_wifi('Tenda_9B3F') -- 移除已保存的 Wi-Fi 配置
```

## 对话框模块
### 类 dialog*

### 类 Dialog*

### dialog(configName)
```lua
-- 建立一个对话框
dlg = dialog()
```

### Dialog:set_config(configName)
```lua
-- 设置对话框配置分区
dlg:set_config('wifi-helper') -- 配置文件保存在 XXT_HOME_PATH..'/uicfg/wifi-helper.xcfg'
```

### Dialog:set_timeout(timeout, shouldSubmit)
```lua
-- 配置对话框自动消失时间
dlg:set_timeout(15) -- 15 秒超时自动关闭
dlg:set_timeout(15, true) -- 15 秒超时自动提交，false 则为超时关闭
```

### Dialog:set_title(title)
```lua
-- 配置对话框的标题
dlg:set_title('Wi-Fi 选择')
```

### Dialog:set_close_title(title)
```lua
-- 配置对话框关闭按钮的标题
dlg:set_close_title('取消')
```

### Dialog:set_submit_title(title)
```lua
-- 配置对话框提交按钮的标题
dlg:set_submit_title('连接')
```

### Dialog:add_group(groupName)
```lua
-- 给对话框加上一个分组
dlg:add_group('基本配置')
```

### Dialog:add_label(labelText)
```lua
-- 给对话框加上一个标签
dlg:add_label('请输入要连接的 Wi-Fi')
```

### Dialog:add_input(labelText, defaultValue)
```lua
-- 给对话框加上一个文本框
dlg:add_input('SSID', 'Tenda_9B3F')
```

### Dialog:add_switch(labelText, defaultValue)
```lua
-- 给对话框加上一个开关
dlg:add_switch('自动重连', true)
```

### Dialog:add_range(labelText, opts, defaultValue)
```lua
-- 给对话框加上一个滑块
dlg:add_range('音量', {0, 100, 5}, 50)
```

### Dialog:add_picker(labelText, optionList, defaultValue)
```lua
-- 给对话框加上一个单项选择器
dlg:add_picker('地区', {'中国', '美国', '日本'}, '中国')
```

### Dialog:add_radio(labelText, optionList, defaultValue)
```lua
-- 给对话框加上一个单选组
dlg:add_radio('环境', {'测试', '生产'}, '生产')
```

### Dialog:add_checkbox(labelText, optionList, defaultList)
```lua
-- 给对话框加上一个多选组
dlg:add_checkbox('同步到', {'iPhone', 'iPad', 'Mac'}, {'iPhone'})
```

### Dialog:add_image(image)
```lua
-- 给对话框加上一张图片
dlg:add_image(image)
```

### Dialog:add_button(labelText, callbackFunc)
```lua
-- 触发回调函数
dlg:add_button('刷新列表', function() nLog('reload wifi list') end)
```

### Dialog:show()
```lua
-- 将对话框弹出来并返回用户的选择
local didSubmit, opts = dlg:show()
if didSubmit then
    nLog(opts['SSID'], opts['自动重连'])
end
```

### Dialog:load()
```lua
-- 在不弹出对话框的情况下获得对话框配置
local _, opts = dlg:load()
nLog('上次记录的 SSID', opts and opts['SSID'])
```

## 扩展字符串模块
### 类 string*

### string.to_hex(data)
```lua
-- 转成十六进制文本
local hex = string.to_hex('Hi')
nLog(hex) -- 4869
```

### string.from_hex(hexStr)
```lua
-- 从十六进制文本转回
local raw = string.from_hex('48656c6c6f')
nLog(raw) -- Hello
```

### string.from_gbk(encStr)
```lua
-- 将 GBK 编码的文本转成 UTF-8 编码的文本
local utf8 = string.from_gbk('\xd6\xd0\xce\xc4')
nLog(utf8) -- 中文
```

### string.md5(data)
```lua
-- 计算 MD5
local hash = string.md5('123456')
nLog(hash) -- e10adc3949ba59abbe56e057f20f883e
```

### string.sha1(data)
```lua
-- 计算 SHA-1
nLog(string.sha1('123456')) -- 7c4a8d09ca3762af61e59520943dc26494f8941b
```

### string.sha256(data)
```lua
-- 计算 SHA-256
nLog(string.sha256('123456'))
```

### string.hmac_sha1(data, key)
```lua
-- 计算 HMAC-SHA1
nLog(string.hmac_sha1('payload', 'secret'))
```

### string.hmac_sha256(data, key)
```lua
-- 计算 HMAC-SHA256
nLog(string.hmac_sha256('payload', 'secret'))
```

### string.sha512(data)
```lua
-- 计算 SHA-512
nLog(string.sha512('123456'))
```

### string.base64_encode(data)
```lua
-- 编码
local b64 = string.base64_encode('hello world')
nLog(b64) -- aGVsbG8gd29ybGQ=
```

### string.base64_decode(encStr)
```lua
-- 解码
local raw = string.base64_decode('aGVsbG8gd29ybGQ=')
nLog(raw) -- hello world
```

### string.aes128_encrypt(data, secret)
```lua
-- 加密
local cipher = string.aes128_encrypt('top-secret', '0123456789abcdef')
nLog(cipher:base64_encode())
```

### string.aes128_decrypt(encData, secret)
```lua
-- 解密
local cipher = string.aes128_encrypt('top-secret', '0123456789abcdef')
local plain = string.aes128_decrypt(cipher, '0123456789abcdef')
nLog(plain) -- top-secret
```

### string.encode_uri(uri)
```lua
-- 编码 URI 字符串
local encoded = string.encode_uri('https://a.com/?q=空 格')
nLog(encoded)
```

### string.encode_uri_component(component)
```lua
-- 编码 URI 组件
local part = string.encode_uri_component('北京/上海')
nLog(part)
```

### string.decode_uri(encodedUri)
```lua
-- 解码 URI 字符串
local decoded = string.decode_uri('https://a.com/?q=%E7%A9%BA%20%E6%A0%BC')
nLog(decoded)
```

### string.decode_uri_component(encodedComponent)
```lua
-- 解码 URI 组件
local city = string.decode_uri_component('%E5%8C%97%E4%BA%AC%2F%E4%B8%8A%E6%B5%B7')
nLog(city)
```

### string.split(haystack, sep)
```lua
-- 用分隔符规则分割一个文本
local parts = string.split('a,b,c,d', ',')
nLog(table.concat(parts, '|')) -- a|b|c,d
```

### string.starts_with(src, prefix, position)
```lua
-- 判断字符串 src 是否以 prefix 开头，position 指定开始搜索的位置，position 默认为 1
nLog(string.starts_with('Hello, XXTouch', 'Hello')) -- 输出 true
nLog(string.starts_with('Hello, XXTouch', 'ello', 2)) -- 输出 true
```

### string.ends_with(src, suffix, length)
```lua
-- 判断字符串 src 是否以 suffix 结尾，length 指定搜索的长度，length 默认为 src 的长度
nLog(string.ends_with('Hello, XXTouch', 'XXTouch')) -- 输出 true
nLog(string.ends_with('Hello, XXTouch', 'ello', 5)) -- 输出 true
```

### string.ltrim(text)
```lua
-- 去除文本左边的空白字符
nLog(string.ltrim('   hello  '))
```

### string.rtrim(text)
```lua
-- 去除文本右边的空白字符
nLog(string.rtrim('   hello  '))
```

### string.trim(text)
```lua
-- 去除文本两边的空白字符
nLog(string.trim('   hello  '))
```

### string.atrim(text)
```lua
-- 去除文本中所有的空白字符
nLog(string.atrim('  h e l l o  '))
```

### string.lpad(text, length, padText)
```lua
-- 左侧补齐（别名）
nLog(string.lpad('42', 5, '0')) -- 00042
```

### string.pad_start(text, padLen, padText)
```lua
-- 左补齐
nLog(string.pad_start('42', 5, '0'))
```

### string.rpad(text, length, padText)
```lua
-- 右侧补齐（别名）
nLog(string.rpad('A', 3, '.')) -- A..
```

### string.pad_end(text, padLen, padText)
```lua
-- 右补齐
nLog(string.pad_end('A', 3, '.'))
```

### string.strip_utf8_bom(text)
```lua
-- 去除掉文本前的 UTF8-BOM
nLog(string.strip_utf8_bom('\239\187\191hello'))
```

### string.random(charPool, charCnt)
```lua
-- 生成随机文本
local token = string.random('abcdefghijklmnopqrstuvwxyz0123456789', 8, 1)
nLog(token)
```

### string.compare_version(verA, verB)
```lua
-- 比较两个版本号大小
-- 返回 1 表示 verA > verB，-1 表示 verA < verB，0 表示相等
nLog(string.compare_version('1.10.0', '1.9.9'))
```

### 逐字符或逐字节分割函数封装

```lua
-- 按 UTF8 编码 "逐字符" 分割字符串
function utf8_explode(str)
  local ret = {}
  for p, c in utf8.codes(str) do
    ret[#ret + 1] = utf8.char(c)
  end
  return ret
end

-- "逐字节" 分割字符串
function bytes_explode(str)
  local ret = {}
  for ch in str:gmatch('(.)') do
    ret[#ret + 1] = ch
  end
  return ret
end

local t = utf8_explode('你好，XXTouch')
nLog(table.concat(t, '/')) -- 输出 "你/好/，/X/X/T/o/u/c/h"

local t = bytes_explode('你好，XXTouch') -- 这个可能不会产生你想要的结果
nLog(table.concat(t, '/')) -- 输出 "�/�/�/�/�/�/�/�/�/X/X/T/o/u/c/h"
```

## 扩展表模块
### 类 table*

### table.deep_copy(inTab)
```lua
-- 深拷贝一个表
local origin = {a = 1, b = {c = 2}}
local copy = table.deep_copy(origin)
copy.b.c = 9
nLog(origin.b.c, copy.b.c) -- 2  9
```

### table.deep_dump(inTab, dumpLuaFunctions)
```lua
-- 将表深度转储成字符串
-- dumpLuaFunctions 可选参数表示是否转储 Lua 函数，默认为 false
local dumped = table.deep_dump({foo = 1, bar = {2, 3}})
nLog(dumped)
```

### table.load_string(tabStr)
```lua
-- 从字符串加载一个表
local t = table.load_string[[ { a = 1, b = 2, c = 3 } ]]
nLog(t.b)
```

## 文件操作模块
### 类 file*

### 类 file.path*

### file.exists(path)
```lua
-- 判断文件或目录是否存在
nLog(file.exists(XXT_SCRIPTS_PATH..'/main.lua'))
```

### file.list(path, deep_and_full)
```lua
-- 列出目录内所有文件名
for _, name in ipairs(file.list(XXT_SCRIPTS_PATH) or {}) do
    nLog(name)
end

-- 完整文件路径列表 = file.list(文件路径, 深层完整遍历)
-- 获取一个目录的文件名列表，第二个参数用于控制是否递归获取子目录文件完全路径列表，默认为 false
list = file.list(XXT_HOME_PATH, true)
nLog(list)
--[[
可能输出
{ -- table: 0xc4cc58a30
  [1] = "/var/mobile/Media/1ferver/snippets/syntax - do __ end.snippet",
  [2] = "/var/mobile/Media/1ferver/snippets/app - app.uninstall(bid).snippet",
  [3] = "/var/mobile/Media/1ferver/snippets/test - snippet.snippet",
  ...
}
--]]
```

### file.attrs(path, fields)
```lua
-- 获取文件属性
local info, err = file.attrs(XXT_SCRIPTS_PATH)
nLog(info and info.size, err)
-- 只获取某个属性
local mode, err = file.attrs(XXT_SCRIPTS_PATH..'/1.lua', 'mode')
nLog(mode, err)
```

### file.lattrs(path, fields)
```lua
-- 获取符号链接属性
local linkInfo, err = file.lattrs(XXT_EXE_PATH)
nLog(linkInfo and linkInfo.mode, err)
-- 只获取某个属性
local mode, err = file.lattrs(XXT_SCRIPTS_PATH, 'mode')
nLog(mode, err)
```

### file.chdir(path)
```lua
-- 切换当前工作目录
file.chdir(XXT_SCRIPTS_PATH)
```

### file.currentdir()
```lua
-- 获取当前工作目录
nLog(file.currentdir())
```

### file.size(path)
```lua
-- 获得文件的尺寸
nLog(file.size(XXT_SCRIPTS_PATH..'/1.lua'))
```

### file.md5(path)
```lua
-- 计算文件的 MD5 值
nLog(file.md5(XXT_SCRIPTS_PATH..'/1.lua'))
```

### file.sha1(path)
```lua
-- 计算文件的 SHA-1 值
nLog(file.sha1(XXT_SCRIPTS_PATH..'/1.lua'))
```

### file.reads(path)
```lua
-- 读取文件中的数据
local content, err = file.reads(XXT_SCRIPTS_PATH..'/1.lua')
nLog(content, err)
```

### file.writes(path, content)
```lua
-- 将数据写入到文件
local tmp = XXT_SCRIPTS_PATH..'/demo.txt'
local ok, err = file.writes(tmp, 'hello\nworld')
nLog(ok, err)
```

### file.appends(path, content)
```lua
-- 将数据追加到文件末尾
local tmp = XXT_SCRIPTS_PATH..'/demo.txt'
file.appends(tmp, '\nappend line')
```

### file.line_count(path)
```lua
-- 统计文本文件的总行数
local tmp = XXT_SCRIPTS_PATH..'/demo.txt'
nLog(file.line_count(tmp))
```

### file.get_line(path, lineNum)
```lua
-- 获取文本文件指定行的内容
local tmp = XXT_SCRIPTS_PATH..'/demo.txt'
local line = file.get_line(tmp, 1)
nLog(line)
```

### file.set_line(path, lineNum, content)
```lua
-- 设置文本文件指定行的内容
local tmp = XXT_SCRIPTS_PATH..'/demo.txt'
file.set_line(tmp, 1, '-- header')
```

### file.insert_line(path, lineNum, content)
```lua
-- 在文本文件指定行前插入内容
local tmp = XXT_SCRIPTS_PATH..'/demo.txt'
file.insert_line(tmp, 2, 'middle')
```

### file.remove_line(path, lineNum)
```lua
-- 移除文本文件指定行
local tmp = XXT_SCRIPTS_PATH..'/demo.txt'
file.remove_line(tmp, 3)
```

### file.get_lines(path)
```lua
-- 获取一个文本文件的所有行
local tmp = XXT_SCRIPTS_PATH..'/demo.txt'
local lines = file.get_lines(tmp)
nLog(lines and lines[1])
```

### file.set_lines(path, lineArr)
```lua
-- 将一个顺序表转换逐行覆盖写入到文件中
local tmp = XXT_SCRIPTS_PATH..'/demo.txt'
file.set_lines(tmp, {'first', 'second'})
```

### file.insert_lines(path, lineNum, lineArr)
```lua
-- 将一个顺序表转换逐行插入到文件指定行前
local tmp = XXT_SCRIPTS_PATH..'/demo.txt'
file.insert_lines(tmp, 2, {'mid1', 'mid2'})
```

### file.remove(path)
```lua
-- 删除文件或目录
file.remove(XXT_SCRIPTS_PATH..'/tmpdir')
```

### file.copy(srcPath, dstPath, mode)
```lua
-- 拷贝文件或目录
local tmp = XXT_SCRIPTS_PATH..'/demo.txt'
local ok, err = file.copy(tmp, XXT_SCRIPTS_PATH..'/demo.bak', 'overwrite')
nLog(ok, err)
```

### file.move(srcPath, dstPath, mode)
```lua
-- 移动文件或目录
file.move(XXT_SCRIPTS_PATH..'/demo.bak', XXT_SCRIPTS_PATH..'/demo.old', 'overwrite')
```

### file.link(srcPath, dstPath, symbolic)
```lua
-- 创建硬链接或符号链接
local tmp = XXT_SCRIPTS_PATH..'/demo.txt'
file.link(tmp, XXT_SCRIPTS_PATH..'/demo.link', true)
```

### file.mkdir_p(path, uid, gid, perm)
```lua
-- 递归创建目录
file.mkdir_p(XXT_SCRIPTS_PATH..'/tmp/a/b', 0, 0, '0755')
```

### file.touch(path, accessTime, modifyTime)
```lua
-- 更新文件访问和修改时间
local now = os.time()
local tmp = XXT_SCRIPTS_PATH..'/demo.txt'
file.touch(tmp, now, now)
```

### file.zip(zipPath, entries, password)
```lua
-- 使用 ZIP 打包文件或目录
file.zip(XXT_SCRIPTS_PATH..'/bundle.zip', {
    {XXT_SCRIPTS_PATH..'/main.lua', 'scripts/main.lua'},
})
```

### file.unzip(zipPath, targetPath, password)
```lua
-- 解压 ZIP 文件
file.unzip(XXT_SCRIPTS_PATH..'/bundle.zip', XXT_SCRIPTS_PATH..'/unzipped')
```

### file.find(pattern)
```lua
-- 在文件系统中搜索文件或目录
-- 说明：  
-- 	使用通配符模式或 Lua 精确匹配搜索文件或目录，返回匹配的文件名列表。  
-- 	如果 pattern 是字符串，则使用通配符模式匹配，通配符模式匹配仅支持 *、?、[...] 这三种通配符。  
-- 	如果 pattern 是表，则使用 Lua 精确匹配。  

-- 简单通配符模式，仅支持 * ? [...] 三种基本通配符
-- * 表示匹配任意长度任意字符（长度也可以是 0）
-- ? 表示匹配单个任意字符
-- [...]  表示匹配单个中括号里的任意字符，例如 [abc]haha.txt 表示 ahaha.txt bhaha.txt chaha.txt 都匹配
-- [!...] 表示匹配单个非中括号里的任意字符，例如 [!abc]haha.txt 表示 ahaha.txt bhaha.txt chaha.txt 不匹配，其它单个字符例如 xhaha.txt 才能匹配
local results = file.find("/var/mobile/Containers/Shared/AppGroup/*/Library/Preferences/*.plist")

-- 精确 Lua 模式匹配模式
-- 精确匹配使用 Lua 表分段构造匹配模式，字符串为字面量判断，模式匹配可以使用返回真假的函数来决定当前分段是否有效
local results = file.find{ --<--- 注意这里是大括号
  "/var/mobile/Containers/Shared/AppGroup/", -- 普通字符串不需要模式匹配
  function(s) return s:match("^[A-F0-9]+%-[A-F0-9]+%-[A-F0-9]+%-[A-F0-9]+%-[A-F0-9]+$") end, -- 使用函数匹配当前分段
  "/Library/Preferences/", -- 普通字符串不需要模式匹配
  function(s) return s:match("%.plist$") end, -- 使用函数匹配当前分段
}

-- 精确 Lua 模式匹配模式也可使用大括号包裹单个字符串以构造一个简易模式匹配函数
local results = file.find{ --<--- 注意这里是大括号
  "/var/mobile/Containers/Shared/AppGroup/", -- 普通字符串不需要模式匹配
  {"^[A-F0-9]+%-[A-F0-9]+%-[A-F0-9]+%-[A-F0-9]+%-[A-F0-9]+$"}, -- 使用表包裹单个字符串构造简单的匹配函数匹配当前分段
  "/Library/Preferences/", -- 普通字符串不需要模式匹配
  {"%.plist$"}, -- 使用表包裹单个字符串表示这是一个需要使用模式匹配的分段
}
```

### file.path.components(path)
```lua
-- 将路径字符串分解为其组成部分。
local parts = file.path.components('/tmp/a/b.txt')
nLog(table.concat(parts, '|'))
```

### file.path.last_component(path)
```lua
-- 返回路径字符串的最后一个组成部分。
nLog(file.path.last_component('/tmp/a/b.txt'))
```

### file.path.remove_last_component(path)
```lua
-- 返回通过删除最后一个路径组成部分生成的新路径字符串。
nLog(file.path.remove_last_component('/tmp/a/b.txt'))
```

### file.path.add_component(path, component)
```lua
-- 返回通过将指定路径组成部分附加到接收者而生成的新路径字符串。
nLog(file.path.add_component('/tmp/a', 'c.txt'))
```

### file.path.extension(path)
```lua
-- 返回路径字符串的文件扩展名（如果存在）。
nLog(file.path.extension('/tmp/a/b.txt'))
```

### file.path.remove_extension(path)
```lua
-- 返回通过删除文件扩展名（如果存在）生成的新路径字符串。
nLog(file.path.remove_extension('/tmp/a/b.txt'))
```

### file.path.add_extension(path, extension)
```lua
-- 返回通过将指定文件扩展名附加到接收者而生成的新路径字符串。
nLog(file.path.add_extension('/tmp/a/b', 'log'))
```

### file.path.normalize(path)
```lua
-- 返回通过标准化路径生成的新路径字符串。
nLog(file.path.normalize('/tmp//a/../b'))
```

### file.path.resolve_symlinks(path)
```lua
-- 返回通过解析路径中的符号链接并标准化路径生成的新路径字符串。
nLog(file.path.resolve_symlinks('/var/mobile/../mobile'))
```

## FTP 模块
### 类 ftp*

### ftp.download(remoteURL, localPath, timeout, shouldContinue, blockCallback, bufSiz)
```lua
-- FTP 文件下载
local ok, info = ftp.download('ftp://user:pass@192.168.0.2/1.zip', XXT_SCRIPTS_PATH..'/1.zip', 15, true, function(chunk)
  local percent = math.floor(((chunk.start_pos + chunk.size_download) / chunk.resource_size) * 100)
  sys.toast('下载进度 '..percent..'%')
end)
nLog(ok, info)
```

### ftp.upload(localPath, remoteURL, timeout, shouldContinue, blockCallback, bufSiz)
```lua
-- FTP 文件上传
local ok, info = ftp.upload(XXT_SCRIPTS_PATH..'/1.zip', 'ftp://user:pass@192.168.0.2/upload/1.zip', 15, false)
nLog(ok, info)
```

## HTTP 模块
### 类 http*

### http.get(optionsOrURL, timeout, headers)
```lua
-- 发起 GET 请求
local code, resHeaders, body = http.get('https://httpbin.org/get', 15, {['User-Agent'] = 'XXTouch'})
nLog(code, body and #body)

local code, res_headers, body = http.get{
  url = "https://httpbin.org/get";
  timeout = 15;
  headers = {
    ["User-Agent"] = "Mozilla/4.0 (compatible; MSIE 8.0; Windows NT 6.0)"; -- 模拟 IE8 的请求
    ["Cookie"] = "a=1; b=2; c=3"; -- 顺带 Cookie 提交
  };
  params = { -- query 参数表
    ["hello"] = "world";
    ["你好"] = "世界";
  };
  progress = function(info)
    nLog(info.count_of_bytes_received, info.count_of_bytes_expected_to_receive)
  end;
  progress_interval_ms = 500;
}
if code == 200 then -- 如果返回的状态码是 HTTP_OK
  sys.alert(body)
end
```

### http 命名参数进度回调
```lua
-- progress/progress_interval_ms 适用于 http.get/post/put/head/delete 的命名参数调用，20260402 以后版本支持
local code, headers, path = http.get{
  url = 'https://example.com/big.zip';
  timeout = 60;
  download_file = XXT_SCRIPTS_PATH..'/big.zip';
  progress_interval_ms = 500;
  progress = function(info)
    local total = info.count_of_bytes_expected_to_receive
    local done = info.count_of_bytes_received or 0
    if total and total > 0 then
      sys.toast(('下载 %d%%'):format(math.floor(done * 100 / total)))
    end
  end;
}
nLog(code, path)

-- 上传进度看 count_of_bytes_sent/count_of_bytes_expected_to_send
http.post{
  url = 'https://httpbin.org/post';
  upload_file = XXT_SCRIPTS_PATH..'/upload.zip';
  progress = function(info)
    nLog('sent', info.count_of_bytes_sent, info.count_of_bytes_expected_to_send)
  end;
  progress_interval_ms = 300;
}
```

### http.post(optionsOrURL, timeout, headers, body)
```lua
-- 发起 POST 请求
local payload = json.encode({name = 'xxtouch'})
local code, resHeaders, body = http.post('https://httpbin.org/post', 15, {['Content-Type'] = 'application/json'}, payload)
nLog(code, body)

HTTP状态码, 返回头JSON文本, 返回主体 = http.post{
  url = URL;
  timeout = 超时秒;
  headers = 请求头;
  params = Query参数;

  -- 以下请求主体参数不可并存，优先顺序为 multipart > data > json > upload_file
  multipart = 请求主体multipart表单;
  data = 请求主体数据;
  json = 请求主体JSON;
  upload_file = 请求主体上传文件路径;

  download_file = 请求成功返回主体保存文件路径;
  progress = 进度回调函数;
  progress_interval_ms = 进度回调间隔毫秒;
}
```

### http.download(remoteURL, localPath, timeout, shouldContinue, blockCallback, bufSize)
```lua
-- HTTP 文件下载
local ok, info = http.download('https://httpbin.org/image/png', XXT_SCRIPTS_PATH..'/httpbin.png', 30, true, function(chunk)
  local percent = math.floor(((chunk.start_pos + chunk.size_download) / chunk.resource_size) * 100)
  sys.toast('下载 '..percent..'%')
end, 512 * 1024)
nLog(ok, info)
```

### http.head(optionsOrURL, timeout, headers)
```lua
-- 发起 HEAD 请求
local code, resHeaders = http.head('https://httpbin.org/get', 10, {})
nLog(code, resHeaders)

HTTP状态码, 返回头JSON文本, 返回主体 = http.head{
  url = URL;
  timeout = 超时秒;
  headers = 请求头;
  params = Query参数;
  progress = 进度回调函数;
  progress_interval_ms = 进度回调间隔毫秒;
}
```

### http.delete(optionsOrURL, timeout, headers)
```lua
-- 发起 DELETE 请求
local code, resHeaders, body = http.delete('https://httpbin.org/delete', 10, {Authorization = 'Bearer token'})
nLog(code, body)

http.delete{
  url = 'https://httpbin.org/delete';
  timeout = 10;
  progress = function(info) nLog(info.count_of_bytes_received) end;
  progress_interval_ms = 500;
}
```

### http.table_to_form_urlencoded(formTable)
```lua
-- 将表编码为 application/x-www-form-urlencoded
local form = http.table_to_form_urlencoded({foo = 'bar', msg = '你好'})
nLog(form) -- foo=bar&msg=%E4%BD%A0%E5%A5%BD
```

### http.form_urlencoded_to_table(formText)
```lua
-- 将 application/x-www-form-urlencoded 表单文本解码为表
local tab = http.form_urlencoded_to_table('foo=bar&msg=%E4%BD%A0%E5%A5%BD')
nLog(json.encode(tab))
```

### http.put(optionsOrURL, timeout, headers, body)
```lua
-- 发起 PUT 请求
local code, resHeaders, body = http.put('https://httpbin.org/put', 15, {['Content-Type'] = 'text/plain'}, 'hello xxTouch')
nLog(code, body)

HTTP状态码, 返回头JSON文本, 返回主体 = http.put{
  url = URL;
  timeout = 超时秒;
  headers = 请求头;
  params = Query参数;

  -- 以下请求主体参数不可并存，优先顺序为 multipart > data > json > upload_file
  multipart = 请求主体multipart表单;
  data = 请求主体数据;
  json = 请求主体JSON;
  upload_file = 请求主体上传文件路径;

  download_file = 请求成功返回主体保存文件路径;
  progress = 进度回调函数;
  progress_interval_ms = 进度回调间隔毫秒;
}
```

### http.move(optionsOrURL, timeout, headers, body)
```lua
-- 发起 MOVE 请求
local code, resHeaders, body = http.move('https://httpbin.org/anything', 15, {Destination = '/target/path'})
nLog(code, body)
```

### http.lock(optionsOrURL, timeout, headers, body)
```lua
-- 发起 LOCK 请求
local code, resHeaders, body = http.lock('https://httpbin.org/anything', 15, {Depth = 'infinity'}, '<lockinfo></lockinfo>')
nLog(code, body)
```

### http.unlock(optionsOrURL, timeout, headers, body)
```lua
-- 发起 UNLOCK 请求
local code, resHeaders, body = http.unlock('https://httpbin.org/anything', 15, {LockToken = 'opaquelocktoken:123'})
nLog(code, body)
```

### http.proppatch(optionsOrURL, timeout, headers, body)
```lua
-- 发起 PROPPATCH 请求
local code, resHeaders, body = http.proppatch('https://httpbin.org/anything', 15, {['Content-Type'] = 'application/xml'}, '<prop><a>1</a></prop>')
nLog(code, body)
```

### http.copy(optionsOrURL, timeout, headers, body)
```lua
-- 发起 COPY 请求
local code, resHeaders, body = http.copy('https://httpbin.org/anything', 15, {Destination = '/copy/target'})
nLog(code, body)
```

### http.mkcol(optionsOrURL, timeout, headers, body)
```lua
-- 发起 MKCOL 请求
local code, resHeaders, body = http.mkcol('https://httpbin.org/anything', 15, {})
nLog(code, body)
```

### http.patch(optionsOrURL, timeout, headers, body)
```lua
-- 发起 PATCH 请求
local code, resHeaders, body = http.patch('https://httpbin.org/patch', 15, {['Content-Type'] = 'application/json'}, '{"flag":true}')
nLog(code, body)
```

### http.propfind(optionsOrURL, timeout, headers, body)
```lua
-- 发起 PROPFIND 请求
local code, resHeaders, body = http.propfind('https://httpbin.org/anything', 15, {Depth = '1'})
nLog(code, body)
```

### http.trace(optionsOrURL, timeout, headers, body)
```lua
-- 发起 TRACE 请求
local code, resHeaders, body = http.trace('https://httpbin.org/anything', 10, {})
nLog(code, body)
```

## CoreML 模块

### 类 coreml*

### coreml.compile_model(modelPath)
```lua
-- 本机编译 CoreML 模型
local compiled, err = coreml.compile_model(XXT_MODELS_PATH..'/yolo11m.mlpackage')
if not compiled then
  error(err)
end
nLog('编译后模型路径', compiled)
```

### coreml.new_vision_request(compiledModelPath)
```lua
-- 创建一个 CoreML 视觉推理器，参数为编译后的 CoreML 模型路径
local vnr, err = coreml.new_vision_request(XXT_MODELS_PATH..'/yolo11m.mlmodelc')
if not vnr then
  error(err)
end
local img = image.load_file(XXT_RES_PATH..'/dog.jpg')
local results, err = vnr:predict(img)
nLog(results, err)
--[[
-- 目标检测模型返回结果示例
{
  {
    ["y"] = number_value,
    ["x"] = number_value,
    ["w"] = number_value,
    ["h"] = number_value,
    ["confidence"] = number_value(0.0 ~ 100.0),
    ["name"] = string_value,
  },
  ...
}
-- 图像分类模型返回结构
{
    {
        ["confidence"] = number_value(0.0 ~ 100.0),
        ["name"] = string_value,
    },
    ...
}
-- 其它类模型返回结构
{
  number_value,
  number_value,
  ...
}
--]]
```

### 分析使用 YOLO11-OBB 模型进行旋转目标检测
```lua
vnr, err = coreml.new_vision_request(XXT_HOME_PATH..'/models/obb.mlmodelc')
if not vnr then
    error(err)
end
function yolo11_obb_max_output(tab)
  local max
  local pos
  for i=33601, 42000 do
    local v = tab[i]
    if not max or max < v then
      max = v
      pos = i - 33600
    end
  end
  local mean = {'x中心', 'y中心', '宽', '高', '置信度', '弧度'}
  local channel_start = {0, 8400, 16800, 25200, 33600, 42000}
  local ret = {}
  for channel_i,start in ipairs(channel_start) do
    ret[mean[channel_i]] = tab[start + pos]
  end
  return ret
end
img = image.load_file(XXT_SCRIPTS_PATH..'/001.jpg')
tm = sys.mtime()
rets = vnrequest:predict(img) -- 使用推理器推理图片
rets = yolo11_obb_max_output(rets[1])
tm = sys.mtime()-tm
nLog(tm, rets)
--[[
模型输出分析过程：
查看模型的推理输出的结构是 Float32 1 × 6 × 8400
查看推理输出样本，发现数组的数据数值断层在如下几个位置
8400
16800
25200
33600
42000
50400
因此推断出这是六个通道的数据，每个通道有 8400 个数据
于是遍历每个通道，然后找到每个通道的最大值，然后找到对应的索引，然后找到对应的数据
其中肯定有一个通道是表示置信度，配合样本发现倒数第二个通道是置信度
--]]
```

## 图像模块
### 类 image*

### 类 ImageObject*
- ImageObject 表示一个图片对象

### image.is(value)
```lua
-- 判断一个值是否为图片对象
local img = image.load_file(XXT_RES_PATH..'/1.png')
nLog('是否图片对象', image.is(img))
```

### image.new(width, height)
```lua
-- 创建指定尺寸空白图片对象
local blank = image.new(200, 100)
blank:save_to_png_file(XXT_SCRIPTS_PATH..'/blank.png')
```

### image.new_text_image(text, opts)
```lua
-- 新建一个文本图片对象
local img = image.new_text_image('XXTouch', {
    font = 'Arial',
    size = 28,
    color = 0xff409bff,
    back_color = 0x00000000,
})
img:save_to_png_file(XXT_SCRIPTS_PATH..'/text.png')
```

### image.load_file(imgPath)
```lua
-- 从文件创建图片对象
local img = image.load_file(XXT_RES_PATH..'/1.png')
nLog(image.is(img))
```

### image.load_data(imgData)
```lua
-- 从数据创建图片对象
local data = file.reads(XXT_RES_PATH..'/1.png')
local img = image.load_data(data)
```

### utils.qr_encode(text, opts)
```lua
-- 将文本编码成二维码图片
local img = utils.qr_encode('https://xxtouch.app', {
    size = 256,
    fill_color = 0xff000000,
    background_color = 0xffffffff,
})
img:save_to_album()
```

### image.oper_merge(imageNameList, outputPath, direction, quality)
```lua
-- 图像拼接
image.oper_merge({XXT_RES_PATH..'/1.png', XXT_RES_PATH..'/2.png'}, XXT_SCRIPTS_PATH..'/merged.jpg', 1, 0.8)
```

### image.image_to_album(imagePath)
```lua
-- 导入一个图片文件到相册
image.image_to_album(XXT_RES_PATH..'/1.png')
```

### image.video_to_album(videoPath)
```lua
-- 导入一个视频文件到相册
image.video_to_album(XXT_RES_PATH..'/demo.mp4')
```

### ImageObject:size()
```lua
-- 获取图片对象的尺寸
local img = screen.image()
local w, h = img:size()
nLog('截图尺寸', w, h)
```

### ImageObject:copy()
```lua
-- 从图片对象创建拷贝图片对象
local img = screen.image()
local dup = img:copy()
dup:turn_left():save_to_png_file(XXT_SCRIPTS_PATH..'/copy_rotated.png')
```

### ImageObject:crop(left, top, right, bottom)
```lua
-- 截取部分区域新建图片对象
local img = screen.image()
local part = img:crop(100, 100, 300, 300)
part:save_to_album()
```

### ImageObject:destroy()
```lua
-- 立即释放图片对象的内存占用，被销毁的图片对象不能再使用
-- Lua 自身有垃圾回收机制，失去引用的图片对象会被自动回收，此方法用于提前释放内存，重复调用没有后果
local img = screen.image()
img:destroy()
```

### ImageObject:save_to_album()
```lua
-- 保存图片对象到相册
ImageObject:save_to_album()
```

### ImageObject:save_to_png_file(imagePath)
```lua
-- 输出图片对象到 PNG 文件或数据
local img = screen.image()
img:save_to_png_file(XXT_SCRIPTS_PATH..'/screen.png')
```

### ImageObject:png_data()
```lua
-- 输出图片对象到 PNG 文件或数据
local img = screen.image(100, 100, 200, 200)
local data = img:png_data()
pasteboard.write(data, 'public.png')
```

### ImageObject:save_to_jpeg_file(imagePath, quality)
```lua
-- 输出图片对象到 JPEG 文件或数据
local img = screen.image()
img:save_to_jpeg_file(XXT_SCRIPTS_PATH..'/screen.jpg', 0.85)
```

### ImageObject:jpeg_data(quality)
```lua
-- 输出图片对象到 JPEG 文件或数据
local img = screen.image()
local data = img:jpeg_data(0.8)
nLog('JPEG 大小', #data)
```

### ImageObject:turn_left()
```lua
-- 逆时针旋转 90 度 ⤴️
local img = screen.image()
img:turn_left():save_to_png_file(XXT_SCRIPTS_PATH..'/turn_left.png')
```

### ImageObject:turn_right()
```lua
-- 顺时针旋转 90 度 ⤵️
local img = screen.image()
img:turn_right():save_to_png_file(XXT_SCRIPTS_PATH..'/turn_right.png')
```

### ImageObject:turn_upondown()
```lua
-- 上下翻转
local img = screen.image()
img:turn_upondown():save_to_png_file(XXT_SCRIPTS_PATH..'/flip.png')
```

### ImageObject:resize(newWidth, newHeight)
```lua
-- 缩放图片对象
local img = screen.image()
img:resize(200, 200):save_to_png_file(XXT_SCRIPTS_PATH..'/resize200.png')
```

### ImageObject:cv_resize(newWidth, newHeight)
```lua
-- OpenCV 缩放图片对象
local img = screen.image()
img:cv_resize(200, 200):save_to_png_file(XXT_SCRIPTS_PATH..'/cv_resize200.png')
```

### ImageObject:get_color(coordX, coordY)
```lua
-- 获取图片对象某点颜色
local img = screen.image()
local c, a = img:get_color(100, 200)
nLog(string.format('0x%06X alpha=%d', c, a))
```

### ImageObject:set_color(coordX, coordY, color)
```lua
-- 设置图片对象某点颜色
local img = image.new(10, 10)
img:set_color(1, 1, 0xff0000)
img:save_to_png_file(XXT_SCRIPTS_PATH..'/red_dot.png')
```

### ImageObject:replace_color(origColor, replColor, similarity)
```lua
-- 颜色替换
local img = screen.image()
img:replace_color(0xffffff, 0xff0000, 10):save_to_png_file(XXT_SCRIPTS_PATH..'/replace_white.png')
```

### ImageObject:draw_image(smallImg, opts)
```lua
-- 图中贴图
local bg = screen.image()
local icon = image.load_file(XXT_RES_PATH..'/icon.png')
bg:draw_image(icon, {left = 50, top = 80, alpha = 200})
```

### ImageObject:cv_binaryzation(threshold)
```lua
-- OpenCV 自动二值化
local img = screen.image(462, 242, 569, 272)
img:cv_binaryzation(120):save_to_png_file(XXT_SCRIPTS_PATH..'/cv_bin.png')
```

### ImageObject:binaryzation(opts)
```lua
-- 图像色偏/相似度二值化处理
-- 色偏（或偏色） 通常用于表示某个颜色范围，一个颜色附带色偏（或偏色）是指该颜色的红、绿、蓝偏移范围内的所有颜色
-- {0x456789, 0x123456} 实际上就是表示从 0x333333 到 0x579BDF 之间所有的颜色
local pic = screen.image(462, 242, 569, 272)
pic = pic:binaryzation({
    {0x9D5D39, 0x0F1F26},
    {0xD3D3D2, 0x2C2C2D},
})

local pic = screen.image(462, 242, 569, 272)
pic = pic:binaryzation("9D5D39-0F1F26,D3D3D2-2C2C2D")

local pic = screen.image(462, 242, 569, 272)
pic = pic:binaryzation({
    csim_mode = true,        -- 使用相似度模式
    csim_algorithm = 2,      -- 使用欧几里得算法
    white_background = true, -- 将背景设置为白色
    {0x9D5D39, 90},          -- 颜色 0x9D5D39 的相似度为 90%
    {0xD3D3D2, 90},          -- 颜色 0xD3D3D2 的相似度为 90%
})
```

### ImageObject:cv_compare_image(other, opts)
```lua
-- 使用 OpenCV 比较另一张图片的差异区域
local before = screen.image()
local after = screen.image()
local shapes, viz = before:cv_compare_image(after, {should_visualize = true})
nLog('差异数量', shapes and #shapes)
```

### ImageObject:cv_to_shapes(opts)
```lua
-- 将图片转换成形状轮廓集合
local img = screen.image()
local shapes, viz = img:cv_to_shapes({should_visualize = true, closed = true})
nLog('轮廓数量', shapes and #shapes)
```

### ImageObject:cv_find_shapes(shapes, opts)
```lua
-- 在图片中查找给定形状集合
local shapes = {{points = {{0,0},{10,0},{10,10},{0,10}}}}
local matches, viz = screen.image():cv_find_shapes(shapes, {should_visualize = true, min_area = 20})
nLog('匹配数量', matches and #matches)
```

### ImageObject:cv_detect_templates(templates)
```lua
-- 使用 OpenCV 特征点匹配检测模板
local tpl = image.load_file(XXT_RES_PATH..'/target.png')
local results, viz = screen.image():cv_detect_templates({tpl})
nLog('模板结果', results and #results)
```

### ImageObject:cv_find_image(smallImg)
```lua
-- 在图片中使用 OpenCV 找图
local img = screen.image()
local tpl = image.load_file(XXT_RES_PATH..'/target.png')
local x, y, sim = img:cv_find_image(tpl)
nLog('CV 找图', x, y, sim)
```

### ImageObject:qr_decode()
```lua
-- 解码当前图片中的二维码
local img = utils.qr_encode('hello XXTouch')
local text = img:qr_decode()
nLog('二维码内容', text)
```

### ImageObject:is_colors(colors, similarity)
```lua
-- 图片多点颜色匹配
local ok = screen.image():is_colors({
    {100, 200, 0xec1c23},
    {110, 205, 0xffffff},
}, 90)
nLog('图片多点匹配', ok)
```

### ImageObject:find_color(opts, similarity, left, top, right, bottom)
```lua
-- 图中找色（多点相似度模式）
-- opts: { {dx, dy, color[, sim]}, ... , [find_all=true], [max_results=100], [max_miss=0], [find_order=1], [csim_algorithm=0] }
-- find_order 取 1~8 控制扫描顺序：1上下左右 2左右上下 3右左上下 4上下右左 5下上右左 6右左下上 7左右下上 8下上左右
-- similarity: 全局相似度(1~100)，未传默认 100；区域未传则默认为整张图
-- 返回首个匹配坐标，未找到返回 -1, -1；find_all=true 时返回 {{x1,y1},{x2,y2},...}
local x, y = ImageObject:find_color({
    {0, 0, 0xec1c23},
    {12, -3, 0xffffff, 85},
    {5, -18, 0x00adee},
}, 90, 0, 0, 300, 300)
nLog('相似度找色', x, y)
```

### ImageObject:find_color(opts, left, top, right, bottom)
```lua
-- 图中找色（多点色偏模式）
-- opts: { {dx, dy, {color,偏色}}, ... , [find_all=true], [max_results=100], [max_miss=0], [find_order=1] }
-- find_order 取 1~8 控制扫描顺序：1上下左右 2左右上下 3右左上下 4上下右左 5下上右左 6右左下上 7左右下上 8下上左右
-- 偏色表示允许的 RGB 偏移量；未传区域默认整张图
-- 返回首个匹配坐标，未找到返回 -1, -1；find_all=true 时返回 {{x1,y1},{x2,y2},...}
local results = ImageObject:find_color({
    {0, 0, {0xec1c23, 0x000000}},
    {12, -3, {0xffffff, 0x101010}},
    find_all = true,
    max_results = 5,
}, 0, 0, 300, 300)
nLog('色偏找色', json.encode(results))
```

### ImageObject:find_image(smallImg, confidence_threshold, left, top, right, bottom)
```lua
-- 图中找图（confidence_threshold 取 0~100，表示置信度百分比）
local big = screen.image()
local small = image.load_file(XXT_RES_PATH..'/target.png')
local x, y = big:find_image(small, 85) -- 85% 置信度，省略区域即全图
if x ~= -1 then
    nLog('找到目标', x, y)
end
```

### ImageObject:ocr_text(lang_opt, bin_opt)
```lua
-- 图片进行光学字符识别（不需要额外的区域参数）
local img = screen.image(100, 100, 300, 200)
-- lang_opt 可传字符串（如 'zh-Hans'、'en-US'）或表 {engine='apple'|'paddle'|'tesseract', lang='zh-Hans'}
-- 参考 Vision 内置语言：iOS14+ 支持 en-US/fr-FR/it-IT/de-DE/es-ES/pt-BR/zh-Hans/zh-Hant，iOS16+ 额外 yue-Hans/yue-Hant/ko-KR/ja-JP/ru-RU/uk-UA
-- bin_opt 可传阈值或色偏表/字符串，用于二值化
local txt, boxes = img:ocr_text({engine = 'apple', lang = 'zh-Hans'}, '9D5D39-0F1F26')
local first = boxes and boxes[1]
nLog('OCR 文本', txt)
nLog('首块置信度', first and first.confidence, '内容', first and first.text, '坐标', first and first.x, first and first.y, first and first.w, first and first.h)
```

### ImageObject:dm_ocr(md, opts)
```lua
-- 使用点阵字库识别图像内容（opts 可传相似度或表 {sim=..., nms=true, nms_threshold=...}）
local dict = matrix_dict.load_file(XXT_RES_PATH..'/dict.txt')
local text, boxes = screen.image():dm_ocr(dict, {sim = 98, nms = true})
for _, box in ipairs(boxes or {}) do
  nLog('字', box.word, '坐标', box.x, box.y, box.w, box.h)
end
```
`opts` 里 `sim` 取 0~100，默认 98；`nms` 默认 true，`nms_threshold` 默认 0.2（当 `nms` 为 false 时自动归零）。
返回的 `boxes` 中坐标含义为 `{word, x, y, w, h}`，其中 `x=rect.top`、`y=rect.left`，宽高为 `rect.bottom-rect.top` / `rect.right-rect.left`，不包含 score 字段。

### ImageObject:dm_find_str(md, sim_or_opts, keyword)
```lua
-- 支持 sim+字符串、字符串、选项表
local dict = matrix_dict.load_string([[
80002000180007FFFF01004080106000100004000100006004080101FFC000300004$h$0.0.51$18.15
00000000000005000140007000180007FFFFFFFFC000100004000100004000000000$1$0.0.50$18.15
]])
local x, y, boxes = screen.image():dm_find_str(dict, {find = '1h', sim = 95})
if x >= 0 then
  nLog('找到了', x, y, json.encode(boxes))
end
```
`sim_or_opts` 也可以直接传字符串或相似度数值配合 `keyword`；选项表额外支持 `find`（字符串或字符串列表）和 `loose/loose_find`（兼容旧行为，只允许单个目标串）。参数非法会直接返回 `-1, -1, {}`，未命中同样返回 `-1, -1` 与空表。使用 `find` 传入字符串数组时需保持默认非宽松模式；开启 `loose/loose_find` 后仅允许单个字符串。

## 矩阵字库模块
### 类 matrix_dict*
提供点阵字模的构造与加载接口，配合 `ImageObject:dm_ocr` / `dm_find_str` 使用。

### matrix_dict.new()
```lua
local dict = matrix_dict.new()
```
返回一个空字库，自动关联元表与缓存。

### matrix_dict.load_file(filename)
```lua
local dict = matrix_dict.load_file(XXT_RES_PATH..'/dict.txt')
```
从文件逐行加载点阵，每行格式 `HexCode$Word$Left.Right.MatchCount$Height.Width`，打开失败返回 `nil, errMsg`。

### matrix_dict.load_string(matrixStr)
```lua
local dict = matrix_dict.load_string([[
0018001E001C800C200C080E021E00860021FFFFFFFFF00084$4$0.0.67$18.11
0780EF080C802C00C006003001800E0050044061DE03C0$o$0.0.46$13.14
1FC1839804803800C006003001800A005804F060020$c$0.0.40$13.13
]])
```
从字符串按行解析点阵定义，也支持多条记录。

### MatrixDict:copy()
```lua
local copy = dict:copy()
```
快速复制整个字库，方便在多个线程/模块复用。

### MatrixDict:add_with_string(matrixStr)
向已有字库追加多行点阵，重复键会自动跳过。

### MatrixDict:add_with_file(filename)
从文件追加新记录，返回新增条目数。

### MatrixDict:add_with_dict(other)
合并另一个 `matrix_dict` 的全部记录。

### MatrixDict:size()
返回当前字库条目数。

### MatrixDict:dump()
按换行拼接所有原始点阵行，迭代顺序遵循哈希遍历（非排序），适合持久化或调试。

### MatrixDict:remove(matrixStr)
删除指定点阵记录，成功返回 `true`。

`ImageObject:dm_ocr` / `dm_find_str` 是 `matrix_dict` 模块最常见的用法，先准备好字库再在图像上调用识别即可。

## JSON 模块
### 类 json*

### json.null
```lua
json.null()
```

### json.encode(value)
```lua
-- 将 Lua 值转储为 JSON 文本
local jsonText = json.encode({foo = 'bar', n = 1})
nLog(jsonText)
```

### json.decode(jsonStr)
```lua
-- 将 JSON 文本加载为 Lua 值，解码失败返回 nil 和错误信息，不会抛出错误
local tab = json.decode('{"foo":"bar","n":1}')
nLog(tab.foo, tab.n)
```

## 模拟按键模块
### 类 key*

### key.press(keyCode)
```lua
-- 模拟按一下物理按键
-- 常用键码：HOMEBUTTON、LOCK、VOLUMEUP、VOLUMEDOWN、RETURN、ESCAPE、SPACE、LEFTCOMMAND、LEFTCONTROL、LEFTSHIFT
key.press('HOMEBUTTON') -- 按一下 Home 键
key.press('LOCK') -- 按一下锁屏键
key.press('VOLUMEUP') -- 按一下音量 +
```

### key.down(keyCode)
```lua
-- 模拟按下物理按键
key.down('LOCK') -- 按下锁屏键 (需配合 up)
```

### key.up(keyCode)
```lua
-- 松开按下的物理按键
key.up('LOCK')
```

### key.send_text(text, delay, shift_delay)
```lua
-- 模拟键入文本
key.send_text('AbC12#', 200, 30) -- 每键 200ms，带 Shift 延迟
```

### key 相关例子
```lua
key.press('HOMEBUTTON') -- 模拟按一下物理 主屏幕键

key.down("HOMEBUTTON")  -- 按住主屏幕键
sys.msleep(1000)        -- 等待 1000 毫秒
key.up("HOMEBUTTON")    -- 松开主屏幕键

key.press("LOCK")       -- 模拟按一下锁屏键（电源键）

key.press("RETURN")     -- 模拟按一下回车键

-- 下面这个例子是模拟组合键 [command + v] 粘贴剪贴板的文本（不是 windows 上的 control + v ）
key.down("LEFTCOMMAND") -- 按住 command 键
sys.msleep(20) -- 等待 20 毫秒
key.press("V") -- 按一下 v 键
sys.msleep(20) -- 等待 20 毫秒
key.up("LEFTCOMMAND") -- 松开 command 键

-- 下面这个例子是模拟组合键 command + `[` 返回上一页
key.down("LEFTCOMMAND") -- 按下 command 键
sys.msleep(20) -- 等待 20 毫秒
key.press("[") -- 按一下 `[` 键
sys.msleep(20) -- 等待 20 毫秒
key.up("LEFTCOMMAND") -- 松开 command 键
```

## 剪贴板模块
### 类 pasteboard*

### pasteboard.read(utiType)
```lua
-- 获取剪贴板中的数据
local txt = pasteboard.read('public.utf8-plain-text')
nLog(txt)
```

### pasteboard.write(data, utiType)
```lua
-- 写内容进剪贴板
pasteboard.write('复制到剪贴板', 'public.utf8-plain-text')
```

### pasteboard.write_items(itemOrItems, opts)
```lua
-- pasteboard.write_items 需要 20260428 以后版本支持，成功返回 true；同一项目可提供纯文本、RTF、HTML、图片等多种 UTI 表示
pasteboard.write_items({
  ["public.utf8-plain-text"] = "normal bold red\n你好",
  ["public.html"] = '<p>normal <b>bold</b> <span style="color:red">red</span><br>你好</p>',
}, {
  local_only = true,
  expiration_date = os.time() + 3600,
})

-- 写多个项目
pasteboard.write_items({
  {["public.utf8-plain-text"] = "第一项"},
  {["public.utf8-plain-text"] = "第二项"},
})
```

### pasteboard.dump()
```lua
-- 获取剪贴板中所有数据内容
local list = pasteboard.dump()
nLog(list)
--[[
-- 可能的返回值示例：
{ -- table: 0x111e1d130
	{ -- table: 0x111e1bb30
		type = "public.utf8-plain-text",
		data = "xxxx",
	},
	{ -- table: 0x111e1bb40
		type = "public.html",
		data = "<html><body>xxxx</body></html>",
	},
}
--]]
```
### pasteboard.types()
```lua
-- 获取剪贴板中所有数据类型
local types = pasteboard.types()
nLog(types)
--[[
-- 可能的返回值示例：
{ -- table: 0x1091d6b10
	"public.utf8-plain-text",
	"public.html",
}
--]]
```

### pasteboard.clear()
```lua
-- 清空剪贴板并返回原内容
list = pasteboard.clear()
nLog(list)
```

## 属性表模块
### 类 plist*

### plist.read(path)
```lua
-- 读取属性表文件
local cfg = plist.read(XXT_RES_PATH..'/config.plist')
nLog(cfg and cfg.version)
```

### plist.write(path, tab, fmt)
```lua
-- 写入属性表文件
plist.write(XXT_SCRIPTS_PATH..'/config.plist', {foo = 'bar'}, 'xml')
file.writes(XXT_SCRIPTS_PATH..'/dumped.plist', plist.dump({foo = 'bar', n = 1}, 'xml')) -- 建议使用 plist.dump 生成数据后写文件
```

### plist.load(data)
```lua
-- 将属性表数据加载为 Lua 表
local tab = plist.load(file.reads(XXT_RES_PATH..'/config.plist'))
nLog(tab and tab.foo)
```

### plist.dump(tab, fmt)
```lua
-- 将 Lua 表转储为属性表数据
local data = plist.dump({foo = 'bar', n = 1}, 'xml')
nLog(data:sub(1, 60)..'...')
```

### plist.data_convert(data, fmt)
```lua
-- 属性表数据格式转换
local xmlData = plist.data_convert(file.reads('/var/mobile/Library/UserNotifications/Library.plist'), 'xml')
sys.alert(xmlData:sub(1, 120)..'...')
```

## 进程字典模块
### proc_put(key, value)
```lua
-- 存储值到进程字典
local old = proc_put('session', 'abc123')
nLog('旧值', old)
```

### proc_get(key)
```lua
-- 查看进程字典存储的值
local token = proc_get('session')
nLog('当前 session', token)
```

### proc_dict_run(code)
```lua
-- 执行进程字典事务代码
local ret, err = proc_dict_run([[
    local cnt = tonumber(proc_get('counter')) or 0
    proc_put('counter', tostring(cnt + 1))
    return cnt
]])
nLog(ret, err)
```

### proc_queue_push(key, value)
```lua
-- 向进程队列词典的尾部压入一个值
proc_queue_push('jobs', 'task-1')
```

### proc_queue_pop(key)
```lua
-- 从进程队列词典的尾部弹出一个值
local v = proc_queue_pop('jobs')
nLog('弹出', v)
```

### proc_queue_push_back(key, value)
```lua
-- 向进程队列词典的尾部压入一个值
proc_queue_push_back('jobs', 'tail')
```

### proc_queue_push_front(key, value)
```lua
-- 向进程队列词典的头部压入一个值
proc_queue_push_front('jobs', 'head')
```

### proc_queue_pop_back(key)
```lua
-- 从进程队列词典的尾部弹出一个值
local v = proc_queue_pop_back('jobs')
nLog('pop_back', v)
```

### proc_queue_pop_front(key)
```lua
-- 从进程队列词典的头部弹出一个值
local v = proc_queue_pop_front('jobs')
nLog('pop_front', v)
```

### proc_queue_read(key)
```lua
-- 读取进程队列词典中所有的值
local list = proc_queue_read('jobs')
nLog(list)
```

### proc_queue_pop_value(key, value)
```lua
-- 从进程队列词典弹出所有指定值
proc_queue_pop_value('jobs', 'tail')
```

### proc_queue_count_value(key, value)
```lua
-- 统计进程队列词典中特定值个数
nLog(proc_queue_count_value('jobs', 'head'))
```

### proc_queue_clear(key)
```lua
-- 从进程队列词典中弹出所有值
proc_queue_clear('jobs')
```

### proc_queue_size(key)
```lua
-- 获取进程队列词典的尺寸
nLog(proc_queue_size('jobs'))
```

## 屏幕模块
### 类 screen*

### screen.init(coordinate)
```lua
-- 初始化旋转坐标系
-- 0 竖屏，1 home 在右，2 home 在左，3 竖屏 home 在上
screen.init(0)
local w, h = screen.size()
nLog('当前坐标系', w, h)
```

### screen.init_home_on_bottom()
```lua
-- 初始化旋转坐标系（Home 在下）
screen.init_home_on_bottom()
```

### screen.init_home_on_right()
```lua
-- 初始化旋转坐标系（Home 在右）
screen.init_home_on_right()
```

### screen.init_home_on_left()
```lua
-- 初始化旋转坐标系（Home 在左）
screen.init_home_on_left()
```

### screen.init_home_on_top()
```lua
-- 初始化旋转坐标系（Home 在上）
screen.init_home_on_top()
```

### screen.rotate_xy(coordX, coordY, direction)
```lua
-- 坐标旋转转换
local rx, ry = screen.rotate_xy(100, 200, 1) -- 将竖屏坐标转换为横屏 home 在右
nLog(rx, ry)
```

### screen.unrotate_xy(coordX, coordY, direction)
```lua
-- 反向坐标旋转转换
local ox, oy = screen.unrotate_xy(rx, ry, 1) -- 再转回原始竖屏坐标
nLog(ox, oy)
```

### screen.size()
```lua
-- 获取屏幕尺寸
local w, h = screen.size()
nLog('屏幕分辨率', w, h)
```

### screen.scale_factor()
```lua
-- 获取屏幕缩放因子（像素与逻辑点倍率）
-- 2.0 表示视网膜屏幕，3.0 表示超视网膜屏幕，现在没有该值为 1.0 的 iOS 设备了
local scale = screen.scale_factor()
nLog(scale)
```

### screen.keep()
```lua
-- 保持屏幕
screen.keep()
-- 在保持期间批量取色/找色/找图，优化效率并且避免取色不一致
local color = screen.get_color(100, 200)
screen.unkeep()
```

### screen.unkeep()
```lua
-- 退出屏幕保持状态
screen.unkeep()
```

### screen.get_color(coordX, coordY)
```lua
-- 获取屏幕上某点颜色
local c = screen.get_color(100, 200)
nLog(string.format('0x%06X', c))
```

### screen.get_color_rgb(coordX, coordY)
```lua
-- 获取屏幕上某点颜色 RGB
local r, g, b = screen.get_color_rgb(100, 200)
nLog('RGB', r, g, b)
```

### screen.is_colors(colors, similarity)
```lua
-- 屏幕多点颜色匹配
-- colors: { {x, y, color[, sim]}, ... , [max_miss=0], [xy_tolerance=0], [csim_algorithm=0] }
-- similarity: 全局相似度(1~100)，未传默认 100；坐标/颜色默认按当前 screen.init 坐标系
-- max_miss 允许最多未命中数；xy_tolerance 坐标容差；csim_algorithm 0/1/2 为默认/曼哈顿/欧几里得
local matched = screen.is_colors({
  {509, 488, 0xec1c23},
  {514, 470, 0x00adee},
  {508, 478, 0xffc823},
}, 90)
nLog('多点匹配', matched)
```

### screen.find_color(opts, similarity, left, top, right, bottom)
```lua
-- 多点相似度模式找色
-- opts: { {dx, dy, color[, sim]}, ... , [find_all=true], [max_results=100], [max_miss=0], [csim_algorithm=0] } -- 不支持 find_order
-- similarity: 全局相似度(1~100)，未传默认 100；区域参数未传则默认为全屏（*不可用 0,0,0,0 表示全屏*）
-- 返回首个匹配坐标，未找到返回 -1, -1
local x, y = screen.find_color({
  {0, 0, 0xec1c23},
  {12, -3, 0xffffff, 85},
  {5, -18, 0x00adee},
}, 90, 0, 0, 200, 200)
nLog('相似度找色', x, y)
```

### screen.find_color(opts, left, top, right, bottom)
```lua
-- 多点色偏模式找色
-- opts: { {dx, dy, {color,偏色}}, ... , [find_all=true], [max_results=100], [max_miss=0] } -- 不支持 find_order
-- 偏色表示允许的 RGB 偏移量；区域未传默认为全屏（*不可用 0,0,0,0 表示全屏*）
-- find_all 返回 {{x1,y1},{x2,y2},...}
local results = screen.find_color({
  {0, 0, {0xec1c23, 0x000000}},
  {12, -3, {0xffffff, 0x101010}},
  find_all = true,
  max_results = 5,
}, 0, 0, 300, 300)
nLog('色偏找色', json.encode(results))
```

### screen.image(left, top, right, bottom)
```lua
-- 获取屏幕内容
-- 区域参数可省略，默认为全屏
local fullImg = screen.image()
fullImg:save_to_png_file(XXT_SCRIPTS_PATH..'/screenshot.png')
local regionImg = screen.image(100, 100, 200, 200)
regionImg:save_to_album()
```

### screen.find_image(smallImg, confidence_threshold, left, top, right, bottom)
```lua
-- 屏幕找图（confidence_threshold 取 0~100，表示置信度百分比）
-- 区域参数可省略，默认为全屏（*不可用 0,0,0,0 表示全屏*）
local target = image.load_file(XXT_RES_PATH..'/target.png')
local x, y = screen.find_image(target, 85) -- 85% 置信度，省略区域即全屏
if x ~= -1 then touch.tap(x, y) end
```

### screen.ocr_text(left, top, right, bottom, lang_opt, bin_opt)
```lua
-- 屏幕区域光学字符识别
-- 若 left, top, right, bottom 为 0,0,0,0 表示识别范围为全屏
local txt, boxes = screen.ocr_text(100, 200, 400, 260, 'zh-Hans', '9D5D39-0F1F26')
local first = boxes and boxes[1]
nLog('OCR 文本', txt)
nLog('第一行置信度', first and first.confidence, '内容', first and first.text, '坐标', first and first.x, first and first.y, first and first.w, first and first.h)
```

## 系统模块
### 类 sys*

### sys.toast(text, options)
```lua
-- 在屏幕下方展示提示文字 总计显示时间为 2.8 秒 会淡出消失 iOS 13.2 以上版本不再影响取色
sys.toast('任务完成', device.front_orien()) -- 根据当前屏幕方向显示
sys.toast('任务完成', {allow_screenshot = true, orien = 0}) -- 允许截屏时显示，根据竖屏 Home 在下方向显示
```

### sys.alert(content, autoDismissalInSeconds, title, btn0, btn1, btn2)
```lua
-- 弹出系统提示
-- 选择 = sys.alert(文字内容 [, 自动消失秒数, 标题, 按钮0标题, 按钮1标题, 按钮2标题 ])
local choice = sys.alert('你现在将要干啥？', 10, '你的选择', '取消', '吃饭', '睡觉')
if choice==0 then
  sys.alert('你选择‘取消’')
elseif choice==1 then
  sys.alert('你选择‘吃饭’')
elseif choice==2 then
  sys.alert('你选择‘睡觉’')
elseif choice==3 then
  sys.alert('你没有选择，超时了')
else
  sys.alert('春板挂了')
end
```

### sys.input_box(title, message, placeholderOpts, defaultTexts, btn0, btn1, btn2, autoDismissalInSeconds)
```lua
-- 弹出输入提示，有以下一些重载调用方式
text = sys.input_box("message")

text = sys.input_box("title", "message")

text = sys.input_box("title", "message", 0)

text = sys.input_box("title", "message", "placeholder", 0)

text = sys.input_box("title", "message", "placeholder", "default text", 0)

text = sys.input_box("title", "message", "placeholder", "default text", "button0", 0)

text, choice = sys.input_box("title", "message", "placeholder", "default text", "button0", "button1", 0)

text, choice = sys.input_box("title", "message", "placeholder", "default text", "button0", "button1", "button2", 0)

text1, text2 = sys.input_box("title", "message", {"placeholder 1", "placeholder 2"}, 0)

text1, text2 = sys.input_box("title", "message", {"placeholder 1", "placeholder 2"}, {"default text 1", "default text 2"}, 0)

text1, text2, choice = sys.input_box("title", "message", {"placeholder 1", "placeholder 2"}, {"default text 1", "default text 2"}, "button0", "button1", "button2", 0)
```

### sys.input_box(title, message, shadowOpts, defaultTexts, autoDismissalInSeconds)
```lua
-- 弹出输入提示
local text, choice = sys.input_box('输入验证码', '请输入短信验证码', 'code', '123456', '取消', '确定', 15)
if choice==0 then
  sys.alert('你选择了取消')
  return
end
if text=='123456' then
  sys.alert('验证码正确')
else
  sys.alert('验证码错误')
end
```

### sys.input_text(text, shouldPressEnter)
```lua
-- 输入文字
sys.input_text('我爱XXTouch', true)
```

### sys.msleep(delayInMilliseconds)
```lua
-- 毫秒级延迟
sys.msleep(1000) -- 延迟 1 秒
```

### sys.mtime()
```lua
-- 获取当前毫秒级时间戳
tm = sys.mtime()
nLog('当前毫秒时间戳', tm)
```

### sys.net_time(timeoutInSeconds)
```lua
-- 获取网络时间 默认请求超时为 2 秒，超时返回 0
local nt = sys.net_time(5) -- 获取网络时间，5 秒超时，超时返回 0
if nt==0 then
  sys.alert('获取网络时间失败')
else
  sys.alert(os.date('当前网络时间\n%Y-%m-%d %H:%M:%S', nt))
end
```

### sys.rnd()
```lua
-- 产生一个随机数
math.randomseed(sys.rnd())
```

### sys.available_memory()
```lua
-- 获取设备当前可用内存值 (单位：MB)
local am = sys.available_memory()
nLog('可用内存', am)
```

### sys.memory_info()
```lua
-- 获取设备当前内存状态信息，返回一个表
nLog(sys.memory_info())
-- 返回值字段示例：
--[[
{
	cow_faults = 19685870,
	vm_page_size = 16384,
	active_count = 62849,
	zero_fill_count = 142162200,
	hits = 0,
	lookups = 0,
	free_count = 22914,
	faults = 303643083,
	physical_memory = 3144810496,
	pageouts = 4467,
	inactive_count = 55006,
	reactivations = 196414,
	pageins = 803265,
	wire_count = 24134,
}
--]]
```

### sys.free_disk_space(mountPoint)
```lua
-- 获取设备当前未使用的存储空间值 单位 MB
nLog(sys.free_disk_space('/'), 'MB')
```

### sys.log(...)
```lua
-- 输出标准系统日志，可在 https://<设备IP>:46952/log.html 实时查看，同时写入 XXT_HOME_PATH..'/log/sys.log'（约 4000 行轮转）
-- 可接受任意个任意类型参数，使用 tab 分隔
sys.log('Hello', 'World', 123, {foo = 'bar'})
```

### sys.mgcopyanswer(question)
```lua
-- 问系统一个问题
nLog(sys.mgcopyanswer('ProductVersion'))
```

### sys.ctlbyname(keyName)
```lua
-- 读取指定的 sysctl 键值
nLog(sys.ctlbyname('hw.memsize'))
```

### sys.version()
```lua
-- 获取系统版本
v = sys.version()
nLog('系统版本', v)
```

### sys.cfversion()
```lua
-- 获取 CoreFoundation 版本
v = sys.cfversion()
nLog('CoreFoundation 版本', v)
```

### sys.xtversion()
```lua
-- 获取 XXTouch 版本
v = sys.xtversion()
nLog('XXTouch 版本', v)
```

### sys.user_tracking() / sys.set_user_tracking(allow)
```lua
-- 读取或设置 `设置 > 隐私与安全性 > 跟踪 > 允许 App 请求跟踪` 开关，20260529 以后版本可用
local allow = sys.user_tracking()
sys.set_user_tracking(false)
```

### sys.personalized_advertising() / sys.set_personalized_advertising(allow)
```lua
-- 读取或设置 `设置 > 隐私与安全性 > Apple 广告 > 个性化广告` 开关，20260529 以后版本可用
local allow = sys.personalized_advertising()
sys.set_personalized_advertising(false)
```

### sys.location_services() / sys.set_location_services(enabled)
```lua
-- 读取或设置 `设置 > 隐私与安全性 > 定位服务` 总开关，20260529 以后版本可用
local enabled = sys.location_services()
sys.set_location_services(enabled)
```

### sys.port()
```lua
-- 获取与 XXTouch OpenAPI 通讯的端口号，通常是 46952
p = sys.port()
nLog('端口号', p)
```

### sys.kill(pid, signal)
```lua
-- 向指定进程发送信号
sys.kill(app.front_pid(), 9) -- 强制结束前台进程
```

### sys.killall(signal, ...)
```lua
-- 向指定名称的进程发送信号
sys.killall(9, 'WeChat') -- 强制结束进程
```

### sys.reboot()
```lua
-- 重启
sys.reboot()
```

### sys.halt()
```lua
-- 关机
sys.halt()
```

### sys.lchown_r(path, uid, gid)
```lua
-- 递归修改文件所有者
sys.lchown_r(XXT_SCRIPTS_PATH, 501, 501)
```

### sys.lchmod_r(path, perm)
```lua
-- 递归修改文件权限
sys.lchmod_r(XXT_SCRIPTS_PATH, '0755')
```

### sys.lchownmod_r(path, uid, gid, perm)
```lua
-- 递归修改文件所有者与权限
sys.lchownmod_r(XXT_SCRIPTS_PATH, 501, 501, '0755')
```

### sys.mkdir_p(path)
```lua
-- 递归创建目录
sys.mkdir_p(XXT_SCRIPTS_PATH..'/tmp/cache')
```

### 类 sys_task_pipe_object*
- sys_task_pipe_object 是 sys_task_object 对象的输入输出错误管道流对象。

### sys_task_pipe_object:read(bytes)
```lua
-- 从管道中读取已经准备好的数据；传 0 读完所有数据
local tsk = sys.task(jbroot('/bin/echo'), 'pipe text')
tsk:launch()
tsk:wait_until_exit()
local out = tsk:stdout():read(0)
nLog('子进程输出', out)
```

### sys_task_pipe_object:write(data)
```lua
-- 向管道中写入数据（例如喂给 cat）
local tsk = sys.task(jbroot('/bin/cat'))
tsk:launch()
tsk:stdin():write('hello\nXXTouch\n')
tsk:stdin():wclose() -- 告诉子进程输入结束
tsk:wait_until_exit()
nLog('回显内容', tsk:stdout():read())
```

### sys_task_pipe_object:wclose()
```lua
-- 关闭管道写端，避免子进程一直等待输入
local tsk = sys.task(jbroot('/bin/cat'))
tsk:launch()
tsk:stdin():write('only once\n')
tsk:stdin():wclose()
```

### sys_task_pipe_object:rclose()
```lua
-- 关闭管道读端
local tsk = sys.task(jbroot('/bin/echo'), 'bye')
tsk:launch()
tsk:wait_until_exit()
local outPipe = tsk:stdout()
nLog(outPipe:read())
outPipe:rclose()
```

### 类 sys_task_object*
- sys_task_object 是 sys.task 函数创建返回的，用于表示一个系统任务/进程的对象。

### sys_task_object:launch()
```lua
-- 启动任务（异步），可搭配 is_running 轮询
local tsk = sys.task(jbroot('/bin/sleep'), '1')
tsk:launch()
nLog('sleep 是否运行', tsk:is_running())
```

### sys_task_object:wait_until_exit()
```lua
-- 同步等待任务结束，避免留下僵尸进程
local tsk = sys.task(jbroot('/bin/sleep'), '1')
tsk:launch()
tsk:wait_until_exit()
nLog('退出码', tsk:termination_status())
```

### sys_task_object:set_stdin(input)
```lua
-- 设置任务输入流，可为 '/dev/null'、文件路径或另一条管道
local gz = sys.task(jbroot('/usr/bin/gzip'), '-fc')
local gunzip = sys.task(jbroot('/usr/bin/gzip'), '-dfc')
gunzip:set_stdin(gz:stdout())
```

### sys_task_object:stdin()
```lua
-- 获取任务输入流并写入数据
local tsk = sys.task(jbroot('/bin/cat'))
tsk:launch()
local stdin = tsk:stdin()
stdin:write('hello stdin\n')
stdin:wclose()
```

### sys_task_object:set_stdout(output)
```lua
-- 设置任务输出流（支持文件路径或管道）
local outFile = XXT_SCRIPTS_PATH..'/ls.txt'
local tsk = sys.task(jbroot('/bin/ls'), '-1')
tsk:set_stdout(outFile)
tsk:launch()
tsk:wait_until_exit()
nLog(file.reads(outFile))
```

### sys_task_object:stdout()
```lua
-- 获取任务输出流
local tsk = sys.task(jbroot('/bin/echo'), 'stdout sample')
tsk:launch()
tsk:wait_until_exit()
nLog(tsk:stdout():read())
```

### sys_task_object:set_stderr(output)
```lua
-- 设置任务错误流（可重定向到文件或 /dev/null）
local tsk = sys.task(jbroot('/bin/ls'), '/no/such/path')
tsk:set_stderr('/dev/null')
tsk:launch()
tsk:wait_until_exit()
```

### sys_task_object:stderr()
```lua
-- 获取任务错误流
local tsk = sys.task(jbroot('/bin/ls'), '/no/such/path')
tsk:launch()
tsk:wait_until_exit()
nLog('错误输出', tsk:stderr():read())
```

### sys_task_object:set_work_dir(workDir)
```lua
-- 设置任务的工作目录
local tsk = sys.task(jbroot('/bin/ls'), '-l')
tsk:set_work_dir('/var/mobile')
tsk:launch()
tsk:wait_until_exit()
```

### sys_task_object:work_dir()
```lua
-- 获取任务的工作目录
local tsk = sys.task(jbroot('/bin/ls'))
tsk:set_work_dir('/var/mobile')
nLog(tsk:work_dir())
```

### sys_task_object:set_env(env)
```lua
-- 设置任务环境变量
local tsk = sys.task(jbroot('/usr/bin/printenv'))
tsk:set_env({HELLO = 'XXTouch'})
tsk:launch()
tsk:wait_until_exit()
nLog(tsk:stdout():read())
```

### sys_task_object:env()
```lua
-- 获取任务环境变量
local tsk = sys.task(jbroot('/usr/bin/printenv'))
local env = tsk:env()
env.LANG = 'en_US.UTF-8'
tsk:set_env(env)
```

### sys_task_object:pid()
```lua
-- 获取任务进程号
local tsk = sys.task(jbroot('/bin/sleep'), '2')
nLog('启动前 PID', tsk:pid())
tsk:launch()
nLog('启动后 PID', tsk:pid())
```

### sys_task_object:is_running()
```lua
-- 判断任务是否正在运行
local tsk = sys.task(jbroot('/bin/sleep'), '1')
tsk:launch()
while tsk:is_running() do
    sys.msleep(100)
end
tsk:wait_until_exit()
```

### sys_task_object:interrupt()
```lua
-- 向任务发送 SIGINT
local tsk = sys.task(jbroot('/bin/sleep'), '10')
tsk:launch()
sys.msleep(500)
tsk:interrupt()
```

### sys_task_object:terminate()
```lua
-- 向任务发送 SIGTERM
local tsk = sys.task(jbroot('/bin/sleep'), '10')
tsk:launch()
sys.msleep(500)
tsk:terminate()
```

### sys_task_object:kill()
```lua
-- 向任务发送 SIGKILL
local tsk = sys.task(jbroot('/bin/sleep'), '10')
tsk:launch()
sys.msleep(500)
tsk:kill()
```

### sys_task_object:termination_status()
```lua
-- 获取任务终止状态
local tsk = sys.task(jbroot('/bin/false'))
tsk:launch()
tsk:wait_until_exit()
nLog('退出码', tsk:termination_status())
```

### sys_task_object:termination_reason()
```lua
-- 获取任务终止原因
local tsk = sys.task(jbroot('/bin/ls'), '/no/such/path')
tsk:launch()
tsk:wait_until_exit()
nLog('终止原因', tsk:termination_reason())
```

### sys.task(executablePath, ...)
```lua
-- 创建一个执行任务；可用管道把多个任务串联
-- 示例：用 gzip 压缩再解压一段文本
local comp = sys.task(jbroot('/usr/bin/gzip'), '-fc')    -- 压缩任务
local decomp = sys.task(jbroot('/usr/bin/gzip'), '-dfc') -- 解压任务
decomp:set_stdin(comp:stdout()) -- 解压任务接收压缩任务的输出

decomp:launch()
comp:launch()

comp:stdin():write('你好世界')
comp:stdin():wclose() -- 输入结束

comp:wait_until_exit()
decomp:wait_until_exit()

nLog('解压结果', decomp:stdout():read())
```

### 调用巨魔安装卸载 App 示例
```lua
function troll_install(ipapath)
  local troll_path = app.bundle_path('com.opa334.TrollStore')
  assert(type(troll_path) == 'string', 'TrollStore needs to be installed.')
  local tsk = sys.task(troll_path..'/trollstorehelper', 'install', ipapath)
  tsk:stdin():wclose()
  tsk:launch()
  while tsk:is_running() do
    sys.msleep(100)
  end
  tsk:wait_until_exit()
  if tsk:termination_status() == 0 then
    local ret = tsk:stdout():read()
    return ret
  else
    local ret = tsk:stderr():read()
    return nil, ret
  end
end
function troll_uninstall(bid)
  local troll_path = app.bundle_path('com.opa334.TrollStore')
  assert(type(troll_path) == 'string', 'TrollStore needs to be installed.')
  local tsk = sys.task(troll_path..'/trollstorehelper', 'uninstall', bid)
  tsk:stdin():wclose()
  tsk:launch()
  while tsk:is_running() do
    sys.msleep(100)
  end
  tsk:wait_until_exit()
  if tsk:termination_status() == 0 then
    local ret = tsk:stdout():read()
    return ret
  else
    local ret = tsk:stderr():read()
    return nil, ret
  end
end
nLog(troll_install(XXT_SCRIPTS_PATH..'/TrollDecrypt.tipa')) -- 安装 TrollDecrypt
nLog(troll_uninstall('com.fiore.trolldecrypt')) -- 卸载 TrollDecrypt
```

## 线程模块
### 类 thread*

thread.dispatch 创建的任务会在 sys.msleep、http 请求、touch 的 :msleep() 及 :move()、dialog 的 :show() 等阻塞操作时让出当前任务的执行权，从而允许其他任务运行。

### thread.dispatch(taskClousure, errorCallback)
```lua
-- 派发一个任务
local tid = thread.dispatch(function()
  sys.msleep(100)
  nLog('任务完成')
end, function(err)
  nLog('任务出错', err)
end)
nLog('任务ID', tid)
```

### thread.current_id()
```lua
-- 获取当前任务的 ID
nLog('当前任务ID', thread.current_id())
```

### thread.kill(taskID)
```lua
-- 从队列中移除一项任务
thread.kill(tid)
thread.kill(thread.current_id()) -- 立即终止当前任务
```

### thread.wait(taskID, timeout_seconds)
```lua
-- 阻塞等待一个任务完成，可设置超时时间（单位秒）
local ok = thread.wait(tid, 3)
nLog('等待结果', ok)
```

### thread.register_event(eventName, eventCallback, errorCallback)
```lua
-- 注册监听一个事件
local eid = thread.register_event('jobs', function(val)
    nLog('收到事件', val)
end, function(err)
    nLog('事件错误', err)
end)
```

### thread.unregister_event(eventName, eventID)
```lua
-- 反注册监听一个事件
thread.unregister_event('jobs', eid)
```

## 模拟触摸模块
### 类 touch*

### 类 TouchObject*
- TouchObject 是由 touch.on() 创建的触摸事件对象，用于链式调用模拟复杂的触摸操作。

### touch.show_pose(shouldShow)
```lua
-- 设置触摸事件可视化显示
touch.show_pose(true)
```

### touch.tap(coordX, coordY, delayBetweenDownAndUpInMs, delayAfterUpInMs)
```lua
-- 模拟手指轻触一次屏幕
touch.tap(100, 200)
touch.tap(100, 200, 30, 50) -- 按下 30ms 再抬起，抬起后延迟 50ms
```

### touch.on(coordX, coordY)
```lua
-- 模拟手指接触屏幕
local finger = touch.on(100, 200)
```

### TouchObject:off(coordX, coordY)
```lua
-- 模拟手指离开屏幕
local finger = touch.on(100, 200)
finger:off(100, 200)
```

### TouchObject:move(coordX, coordY, pressure, twist, flags)
```lua
-- 模拟手指在屏幕上移动
local finger = touch.on(100, 200)
finger:move(200, 300, 0, 0, 0):off(200, 300)
```

### TouchObject:step_delay(stepDelay)
```lua
-- 设置触摸事件对象移动每步延迟
local finger = touch.on(100, 200)
finger:step_delay(10):move(200, 300):off(200, 300)
```

### TouchObject:step_len(stepLength)
```lua
-- 设置触摸事件对象移动步长
local finger = touch.on(100, 200)
finger:step_len(5):move(150, 250):off(150, 250)
```

### TouchObject:msleep(delayInMs)
```lua
-- 毫秒级延迟
local finger = touch.on(100, 200)
finger:msleep(50):off(100, 200)
```

### TouchObject:press(pressure, twist)
```lua
-- 模拟手指在屏幕上施加压力
local finger = touch.on(100, 200)
finger:press(0.5, 0):off(100, 200)
```

### touch.on(finger_id, coordX, coordY)
```lua
-- 模拟手指接触屏幕
-- 可直接调用 touch.on(x, y) 自动分配手指，或 touch.on(fingerId, x, y) 指定手指
-- 例：编号为 1 的手指在 100,100 按下
touch.on(1, 100, 100)
```

### touch.move(finger_id, coordX, coordY)
```lua
-- 模拟手指在屏幕上移动
-- :move 按设定步进滑动，touch.move(fingerId, x, y) 为立即位移
-- 例：延续上例，编号为 1 的手指移动到 105,105
touch.move(1, 105, 105)
```

### touch.off(finger_id, coordX, coordY)
```lua
-- 模拟手指离开屏幕
-- 例：编号为 1 的手指抬起，或指定抬起坐标
touch.off(1)
touch.off(1, 105, 105)
```

### 快速精确滑动技巧
```lua
-- 快速精确滑动可能需要一些技巧，看下面的例子以及注释
touch.on(125, 2000) -- 在起始坐标按下
  :step_len(10) -- 步长设长以便加速滑动
  :step_delay(1) -- 步延时设短以便加速滑动
  :move(125, 555) -- 快速移动到接近目标位置
  :step_len(1) -- 步长设短缓冲防止惯性
  :step_delay(2) -- 步延时设长缓冲防止惯性
  :move(125, 505) -- 慢速移动目标位置
  :msleep(300) -- 抬起前等待一段时间
:off() -- 抬起手指
```

### 多指同时滑动技巧
```lua
-- 双指合拢缩小相册图片示例
thread.dispatch(function() -- 派发一个滑动任务
  touch.on(59,165):move(297,522):msleep(500):off()
end)
thread.dispatch(function() -- 再派发一个滑动任务
  touch.on(580,1049):move(371,1049):msleep(500):off()
end)
```

## 文本元素模块
`ui_element` 在 20260507 以后版本可用。`ui_element` 通过当前界面的文本、角色、状态查找控件并执行点击、输入、滚动、切换、调节等操作；坐标均为物理像素。
查询类失败通常返回 `nil, err`，`find_all` 无匹配时返回空数组；动作类成功返回 `true, info`，失败返回 `nil, err`。

### 类 ui_element*

### 常用选择器
```lua
local ui_element = require("ui_element")

-- 优先用可读文本 + role，重名时再加 index
local selector = {
  title = "搜索", -- 等价于 text
  role = "text_field", -- button/text_field/static_text/switch/checkbox/radio/slider/picker/scrollable/link/image/keyboard_key
  index = 1,
}

-- 常用字段：text_contains/value/value_contains/identifier/bundle_id/traits/visible/hittable/checked/selected/index
local item, err = ui_element.find(selector)
```

### 常用选项与返回字段
```lua
local opts = {
  pid = app.front_pid(),
  max_level = 2,
  max_elements = 200,
  include_hit_state = true,
  fallback_hit_test = false,
}

-- 其它查询选项：fallback_children/hit_test/hit_test_spacing
-- 动作选项：point/x/y/steps
-- 元素常见字段：text/value/identifier/hint/bundleId/x/y/width/height/centerPoint/children
-- 状态字段：isVisible/isSelected/isToggle/isAdjustable/checked/hasTextEntry/isKeyboardKey/absoluteValue
-- 命中字段：canHit/hitVerified/hitTestPoint
local item = ui_element.find({text_contains = "隐私"}, opts)
```

### ui_element.find(selector, opts)
```lua
local item, err = ui_element.find({title = "搜索", role = "text_field"})
if item then
  ui_element.click(item)
else
  sys.toast(err)
end
```

### ui_element.find_all(selector, opts)
```lua
local buttons = ui_element.find_all({role = "button"})
for i, item in ipairs(buttons) do
  nLog(i, item.text or "")
end
```

### ui_element.snapshot(opts)
```lua
local ui, err = ui_element.snapshot({max_level = 2})
if ui then
  local search = ui:find({title = "搜索", role = "text_field"})
  if search then
    ui:set_text(search, "XXTouch")
  end
else
  sys.toast(err)
end

-- 快照方法：find/find_all/click/scroll/input_text/set_text/clear_text/toggle/set_checked/set_value/increase/decrease
-- 界面跳转、弹窗、滚动、刷新后重新 snapshot()
```

### ui_element.list_text_elements(opts)
```lua
local list, err = ui_element.list_text_elements({max_level = 1})
if list then
  for _, item in ipairs(list) do
    if item.text then nLog(item.text) end
  end
end
```

### ui_element.text_element_at_position(x, y, opts)
```lua
local item, err = ui_element.text_element_at_position(300, 500, {
  include_hit_state = true,
  max_level = 1,
})
if item then
  nLog(item.text or item.value or "")
else
  sys.toast(err)
end
```

### ui_element.click(selectorOrElement, opts)
```lua
local ok, info_or_err = ui_element.click({title = "继续", role = "button"})
if not ok then sys.toast(info_or_err) end

ui_element.click({x = 100, y = 200}) -- 固定坐标点击优先用 touch.tap
```

### ui_element.scroll(direction, opts)
```lua
ui_element.scroll("down", {point = {x = 200, y = 700}})
ui_element.scroll({text_contains = "列表"}, "up", {steps = 2})
-- direction: "down"/"up"/"left"/"right"/"top"/"bottom"
```

### ui_element.input_text(selectorOrElement, text, opts)
```lua
ui_element.input_text({title = "搜索", role = "text_field"}, "XXTouch") -- 追加输入
```

### ui_element.set_text(selectorOrElement, text, opts)
```lua
ui_element.set_text({title = "搜索", role = "text_field"}, "XXTouch") -- 替换文本
```

### ui_element.clear_text(selectorOrElement, opts)
```lua
ui_element.clear_text({title = "搜索", role = "text_field"})
```

### ui_element.toggle(selectorOrElement, opts)
```lua
ui_element.toggle({title = "飞行模式", role = "switch"})
```

### ui_element.set_checked(selectorOrElement, checked, opts)
```lua
ui_element.set_checked({title = "飞行模式", role = "switch"}, false)
```

### ui_element.set_value(selectorOrElement, value, opts)
```lua
ui_element.set_value({role = "slider", index = 1}, 0.5)
ui_element.set_value({role = "slider", index = 1}, "50%")
```

### ui_element.increase(selectorOrElement, opts)
```lua
ui_element.increase({role = "slider", index = 1})
```

### ui_element.decrease(selectorOrElement, opts)
```lua
ui_element.decrease({role = "picker", index = 1}, {steps = 2})
```

## 小工具模块
### 类 utils*

### utils.date_to_format(format, timestamp, opts)
```lua
-- 时间戳转换为格式化时间文本
nLog(utils.date_to_format('yyyy-MM-dd HH:mm:ss ZZZZ', os.time(), {tz = 'Asia/Shanghai', locale = 'zh-CN'}))
```

### utils.date_from_format(format, dateText, opts)
```lua
-- 格式化时间文本转换为时间戳
local ts = utils.date_from_format('yyyy-MM-dd HH:mm:ss', '2025-06-09 10:40:00', {tz = 'Asia/Shanghai'})
nLog(ts)
```

### utils.date_to_rfc1123(timestamp)
```lua
-- 时间戳转换为 RFC 1123 文本
nLog(utils.date_to_rfc1123(os.time()))
```

### utils.date_from_rfc1123(rfc1123)
```lua
-- RFC 1123 文本转换为时间戳
nLog(utils.date_from_rfc1123('Mon, 09 Jun 2025 10:40:00 GMT'))
```

### utils.date_to_rfc3339(timestamp)
```lua
-- 时间戳转换为 RFC 3339 文本
nLog(utils.date_to_rfc3339(os.time()))
```

### utils.date_from_rfc3339(rfc3339)
```lua
-- RFC 3339 文本转换为时间戳
nLog(utils.date_from_rfc3339('2025-06-09T10:40:00Z'))
```

### utils.gen_uuid()
```lua
-- 生成一个 UUID
local uuid = utils.gen_uuid()
nLog(uuid)
```

### utils.totp_next(timestamp, url, secret)
```lua
-- 生成基于时间的一次性验证码，20260107 以后版本可用
local url = 'otpauth://totp/Demo:alice?secret=JBSWY3DPEHPK3PXP&digits=6&period=30&algorithm=SHA1'
local code, err = utils.totp_next(-1, url)
nLog(code or err)
```

### utils.hotp_counter(counter, url, secret)
```lua
-- 按计数器生成一次性验证码，20260107 以后版本可用
local url = 'otpauth://hotp/Demo:alice?secret=JBSWY3DPEHPK3PXP&digits=6&algorithm=SHA1'
local code, err = utils.hotp_counter(1, url)
nLog(code or err)
```

### utils.hotp_next(url, secret)
```lua
-- 生成下一个基于计数器的一次性验证码，20260107 以后版本可用
local url = 'otpauth://hotp/Demo:alice?secret=JBSWY3DPEHPK3PXP&digits=6&algorithm=SHA1'
local code, err = utils.hotp_next(url)
nLog(code or err)
```

### utils.qr_encode(text, opts)
```lua
-- 将文本编码成二维码图片
local img = utils.qr_encode('XXTouch 真棒', {
  size = 320,
  fill_color = 0xff409bff,
  shadow_color = 0xff308bef,
})
img:save_to_album()
```

### utils.video_to_album(videoPath)
```lua
-- 导入一个视频文件到相册
utils.video_to_album(XXT_SCRIPTS_PATH..'/1.mp4')
```

### utils.add_contacts(contacts)
```lua
-- 给通讯录添加一个或多个联系人
utils.add_contacts({
  {
    firstName = "小",
    lastName = "明",
    phoneNumbers = {
      "13800001111",
      "13800002222",
    },
    emails = {
        "xiaoming@qq.com",
        "xiaoming@163.com",
    },
  },
  {
    firstName = "小",
    lastName = "红",
    phoneNumbers = {
      "13800003333",
      "13800004444",
    },
    emails = {
        "xiaohong@qq.com",
        "xiaohong@163.com",
    },
  },
})
```

### utils.remove_all_contacts()
```lua
-- 删除通讯录所有联系人
utils.remove_all_contacts()
```

### utils.launch_args()
```lua
-- 获得当前脚本的启动参数
sys.log(utils.launch_args())
--[[
可能的日志输出
{
    ["path"] = "/var/mobile/Media/1ferver/lua/scripts/1.lua",
    ["type"] = "APPLICATION",
}
--]]
```

### utils.is_launch_via_app()
```lua
-- 判断当前脚本是否从 XXTouch 的 App 内启动
local fromXXTApp = utils.is_launch_via_app()
nLog('是否从 XXTouch 的 App 启动', fromXXTApp)
```

## VPN 配置模块
### 类 vpnconf*

### vpnconf.create(configTab)
```lua
-- 创建一个 VPN 配置
vpnconf.create({
    display = 'My Work VPN',
    server = 'vpn.example.com',
    account = 'user',
    password = 'pass',
    secret = 'shared',
})
```

### vpnconf.list()
```lua
-- 获取当前系统 VPN 的列表
vpnconf.list()
```

### vpnconf.select(displayID)
```lua
-- 选择一个 VPN 配置
vpnconf.select('My Work VPN')
```

### vpnconf.delete(displayID)
```lua
-- 删除一个 VPN 配置
vpnconf.delete('My Work VPN')
```

### vpnconf.connect()
```lua
-- 以当前选择的 VPN 建立连接
vpnconf.connect()
```

### vpnconf.disconnect()
```lua
-- 断开当前的 VPN 连接
vpnconf.disconnect()
```

### vpnconf.status()
```lua
-- 获取当前选择的 VPN 的状态
local status = vpnconf.status()
nLog('VPN 状态', status)
```

## Web 视图模块
webview 视图模块允许在屏幕上现实一个可交互的 Web 内容区域，可用于显示自定义界面、接收用户输入等操作。  
webview 最好固定加上 `<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />` 以避免获取输入焦点缩放导致崩溃的问题。  

### 类 webview*

### webview.show(opts)
```lua
-- webview.show 的参数是一个表，没有返回值，使用 id 字段指定视图 ID，省略时默认为 1，webview.show 重复调用只有 html 参数不会覆盖其它字段都会覆盖
-- webview.show 用于展现或更新一个 Web 视图；带 animation_duration 时会从上一次状态平滑过渡到本次设定
-- opts 所有字段可选：id(整数,默认1)、html(文本)、url(文本)、x/y/width/height(整数)、alpha(实数0~1)、
-- corner_radius(实数)、animation_duration(实数秒)、rotate(实数角度)、level(实数,默认1100)、
-- opaque(布尔)、ignores_hit(布尔)、can_drag(布尔)、is_secure(布尔)
-- corner_radius 是不受 screen.scale_factor 影响的点数值，其余坐标尺寸均受 screen.scale_factor 影响
local html = '<html><body><h3>Hello XXTouch</h3><button onclick=\"alert(1)\">Click</button></body></html>'
webview.show{
    id = 1,
    html = html,
    x = 10 * screen.scale_factor(),
    y = 25 * screen.scale_factor(),
    width = 160 * screen.scale_factor(),
    height = 100 * screen.scale_factor(),
    alpha = 0.8,
    corner_radius = 8,
    animation_duration = 0.3, -- 有上一状态时平滑过渡
}

local midY = ({screen.size()})[2] / screen.scale_factor()
webview.show{
  id = 2,
  html = [[<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
  <style>body{margin:0;overflow:hidden;} .btn{width:50px;height:50px;line-height:50px;border-radius:50%;text-align:center;background:#ff4757;color:#fff;user-select:none;}</style>
  <script src="/js/jquery.min.js"></script>
  <script src="/js/jquery.json.min.js"></script>
  <script>
    $(function(){
      $('#btn').click(function(e){
        var txt = $('#btn').text();
        if (txt == '暂停') {
          $.post('/proc_queue_push', $.toJSON({key:'circle_buttons_clicked', value:txt}), function(){
            $('#btn').text('继续');
          });
        } else {
          $.post('/resume_script','',function(){
            $.post('/proc_queue_push', $.toJSON({key:'circle_buttons_clicked', value:txt}), function(){
              $('#btn').text('暂停');
            });
          });
        }
      });
    });
  </script>
  <body><div id="btn" class="btn">暂停</div></body>]],
  y = midY,
  width = 120 * screen.scale_factor() / 2,
  height = 125 * screen.scale_factor() / 2,
  alpha = 1,
  corner_radius = 25,
  can_drag = true,
  opaque = false,
}
thread.register_event('circle_buttons_clicked', function(val)
  sys.toast('点击：'..tostring(val))
end)
```

### webview.hide(viewID)
```lua
-- 隐藏一个 Web 视图
webview.hide(1) -- id 可省略，默认为 1
```

### webview.eval(jsContent, viewID)
```lua
-- 在一个 Web 视图上执行一段 JavaScript
local ret = webview.eval('document.title = "Injected"; "done"', 1)
nLog(ret)
```

### webview.frame(viewID)
```lua
-- 获取一个 Web 视图的区域及层级信息
local f = webview.frame(1)
if f then
  sys.alert(("位置:(%d,%d)\n大小:(宽:%d,高:%d)\n层级:%s"):format(f.x, f.y, f.width, f.height, tostring(f.level)))
end
```

```lua
local w, h = screen.size()
local wvid = 382
local function ensure_log_view()
  local frame = webview.frame(wvid) or {width = 0}
  if frame.width == 0 then
    webview.destroy(wvid)
    webview.show{
      id = wvid,
      x = 0, y = h - 200,
      width = 200 * screen.scale_factor(),
      height = 120 * screen.scale_factor(),
      corner_radius = 6,
      is_secure = true, -- 不可截屏/取色
      ignores_hit = true, -- 点击穿透
      opaque = false,
      html = [[<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" /><style>body{margin:0;background:rgba(0,0,0,.5);}div{height:100%;overflow:hidden;  color:#fff;font-size:10px;}</style><div id="log"> </div>
      <script>function setLog(t){var d=document.getElementById('log');d.innerHTML=t;d.scrollTop=d.  scrollHeight;}</script>]],
    }
  end
end
local logs = {}
local function push_log(msg)
  ensure_log_view()
  table.insert(logs, msg)
  if #logs > 10 then table.remove(logs, 1) end
  webview.eval(string.format('setLog(%q);', table.concat(logs, "<br>")), wvid)
end

ensure_log_view()
sys.msleep(1000)

for i=1, 10 do
  push_log('webview 日志浮层 ready ' .. i)
  sys.msleep(1000)
end

-- 示例：webview 交互演示（弹窗、全屏切换、下滑动画、消息回传）
local w, h = screen.size()
local factor = screen.scale_factor() / 2
local demo_html = [=[
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no" />
<html>
<head>
<script src="/js/jquery.min.js"></script>
<script src="/js/jquery.json.min.js"></script>
<script>
$(function(){
  $('#toast_content').val('toast内容');
  $('#close_page').click(function(){ $.post('/proc_queue_push','{"key":"来自webview的消息","value":"关闭页面"}'); });
  $('#show_toast').click(function(){
    $.post('/proc_put',$.toJSON({key:'toast内容',value:$('#toast_content').val()}));
    $.post('/proc_queue_push','{"key":"来自webview的消息","value":"显示toast"}');
  });
  $('#slide_down').click(function(){
    $.post('/proc_queue_push','{"key":"来自webview的消息","value":"往下滑动"}');
    $(this).hide();
  });
  $('#full_vertical').click(function(){ $.post('/proc_queue_push','{"key":"来自webview的消息","value":"竖屏全屏"}'); });
  $('#full_landscape').click(function(){ $.post('/proc_queue_push','{"key":"来自webview的消息","value":"横屏全屏"}'); });
  $('#prompt_test').click(function(){
    var p = prompt('请输入你的名字','Harry Potter');
    if(p){ var x='你好 '+p+'! 今天感觉如何?';
      $.post('/proc_put',$.toJSON({key:'toast内容',value:x}));
      $.post('/proc_queue_push','{"key":"来自webview的消息","value":"显示toast"}');
    }
  });
});
</script>
</head>
<body>
  <p>动脚 webview 演示</p>
  <p><button id="close_page" type="button">点我关闭页面</button></p>
  <p><button id="show_toast" type="button">显示一个 toast</button><input type="text" id="toast_content" /></p>
  <p><button id="full_vertical" type="button">竖屏全屏</button><button id="full_landscape" type="button">横屏全屏</button></p>
  <p><button id="slide_down" type="button">视图往下滑动</button></p>
  <p><button id="prompt_test" type="button">输入文字弹窗测试</button></p>
</body>
</html>
]=]
webview.show{ -- 初始置顶，透明
  x = 0, y = 0,
  width = w - 40 * factor,
  height = 500 * factor,
  alpha = 0,
  animation_duration = 0,
  can_drag = true,
}
webview.show{ -- 动画滑入
  html = demo_html,
  x = 20 * factor,
  y = 50 * factor,
  width = (w - 40 * factor),
  height = 500 * factor,
  corner_radius = 10,
  alpha = 0.7,
  animation_duration = 0.3,
  can_drag = true,
}
proc_queue_clear('来自webview的消息', '')
thread.register_event('来自webview的消息', function(val)
  if val == '关闭页面' then
    webview.show{
      x = 20 * factor,
      y = 500 * factor * 2,
      width = (w - 40 * factor),
      height = (500 - 70) * factor,
      corner_radius = 10,
      alpha = 0,
      animation_duration = 0.8,
      can_drag = true,
    }
    sys.msleep(800)
    webview.destroy()
    sys.toast('页面线程结束')
    return true
  elseif val == '往下滑动' then
    webview.show{
      x = 20 * factor,
      y = (50 + 300) * factor,
      width = (w - 40 * factor),
      height = (500 - 70) * factor,
      corner_radius = 10,
      alpha = 0.7,
      animation_duration = 0.5,
      can_drag = true,
    }
  elseif val == '竖屏全屏' then
    webview.show{}
  elseif val == '横屏全屏' then
    webview.show{rotate = 90}
  elseif val == '显示toast' then
    sys.toast(proc_get('toast内容'))
  end
end)
```

### webview.destroy(viewID)
```lua
-- 销毁一个 Web 视图
webview.destroy(1)
```

## 回调消息

目前 XXTouch 内置的回调事件只有 xxtouch.call_callback 和 xxtouch.hid_event 两种。  
其它的事件回调消息需要使用 proc_queue_push 函数推送到对应的消息队列中。  

### 电话呼入回调示例
```lua
-- 清空消息队列
proc_queue_clear("xxtouch.call_callback")
--
sys.toast("脚本从现在开始监听来电事件，二十秒后取消监听")
--
-- 开始建立监听回调
local eid = thread.register_event("xxtouch.call_callback", function(val)
  if (val == "in") then
    sys.toast("来电话了")
  elseif (val == "out") then
    sys.toast("正在打电话出去")
  elseif (val == "disconnected") then
    sys.toast("电话挂断了")
  end
end)
--
sys.msleep(20000) -- 等待 20 秒
--
-- 反注册回调函数，如果不反注册监听，那么脚本不会在此结束
thread.unregister_event("xxtouch.call_callback", eid)
```

### HID 事件回调示例
```lua
-- 清空消息队列
proc_queue_clear("xxtouch.hid_event")
--
-- 建立监听回调
local eid = thread.register_event("xxtouch.hid_event", function(val)
  local event = json.decode(val)
  if event.event_type == "touch" then
    if event.event_name == "touch.on" then
      sys.toast("触摸接触位置: (" .. event.x .. ", " .. event.y .. ")\n" .. event.time)
    elseif event.event_name == "touch.move" then
      sys.toast("触摸移动到位置: (" .. event.x .. ", " .. event.y .. ")\n" .. event.time)
    elseif event.event_name == "touch.off" then
      sys.toast("触摸从位置: (" .. event.x .. ", " .. event.y .. ") 离开屏幕\n" .. event.time)
    end
  else
    if event.event_name == "key.down" then
      sys.toast("按下按键: " .. event.key_name .. "\n" .. event.time)
    elseif event.event_name == "key.up" then
      sys.toast("抬起按键: " .. event.key_name .. "\n" .. event.time)
    end
  end
end)
--
touch.on(100, 100):off()
sys.msleep(1000)
key.press('homebutton')
--
sys.msleep(20000) -- 等待 20 秒
--
-- 反注册回调函数，如果不反注册监听，那么脚本不会在此结束
thread.unregister_event("xxtouch.hid_event", eid)
```

### 自定义消息回调示例

自定义消息回调可以通过 proc_queue_push 函数或者 /proc_queue_push 接口推送消息到指定的消息队列中，然后通过 thread.register_event 监听该消息队列来接收消息。

```lua
-- 清空消息队列
proc_queue_clear("my_custom_event")
local eid = thread.register_event("my_custom_event", function(val)
  nLog("收到自定义事件消息: ", val)
end)
proc_queue_push("my_custom_event", "Hello from custom event!")
http.post("http://127.0.0.1:"..sys.port().."/proc_queue_push", 10, {}, '{"key":"my_custom_event","value":"Hello via HTTP!"}')
sys.msleep(1000) -- 让出当前线程等待消息处理
thread.unregister_event("my_custom_event", eid)
```

## 内置的第三方模块（可以直接 require 使用）
- `luasocket`: 可通过 `require "socket"`
  - https://lunarmodules.github.io/luasocket/reference.html
- `luassl`: 可通过 `require "ssl"`
  - https://mauriciocarneiro.github.io/software/luassl/references.html
- `lua-openssl`: 可通过 `require "openssl"`
  - https://zhaozg.github.io/lua-openssl/index.html
- `lpeg`: 可通过 `require "lpeg"`
  - https://www.inf.puc-rio.br/~roberto/lpeg/
- `luafilesystem`: 可通过 `require "lfs"`
  - https://lunarmodules.github.io/luafilesystem/manual.html#reference
- `lua-cjson`: 可通过 `require "cjson"`
  - https://github.com/openresty/lua-cjson
- `lua-iconv`: 可通过 `require "iconv"`
  - https://github.com/lunarmodules/lua-iconv
- `LuaSQLite3`: 可通过 `require "lsqlite3"`
  - https://lua.sqlite.org/home/doc/tip/doc/lsqlite3.wiki
- `lcurl`: 可通过 `require "lcurl"`
  - https://lua-curl.github.io/lcurl/modules/lcurl.html
- `lunix`: 可通过 `require "unix"`
  - https://xxtouch.app/assets/files/lunix-a491331e03b45cb97fcf546b9dcb2eb4.pdf
- `lua-posix`: 可通过 `require "posix"`
  - https://luaposix.github.io/luaposix/
- `cffi-lua`: 可通过 `require "ffi"`
  - https://github.com/q66/cffi-lua
- `lua-ev` : 可通过 `require "ev"`
  - https://github.com/brimworks/lua-ev
- `lua-archive` : 可通过 `require "archive"`
  - https://github.com/brimworks/lua-archive
- `lua-path` : 可通过 `require "path"`
  - https://github.com/moteus/lua-path
- `lua-zip` : 可通过 `require "zip"`
  - https://raw.githubusercontent.com/brimworks/lua-zip/refs/heads/master/README.txt
- `lua-websockets` : 可通过 `require "websocket"`
  - https://github.com/lipp/lua-websockets
