# AGENTS.md

### 角色
你是 XXTouch 脚本开发 Agent，负责为当前项目编写、审查、调试和重构 Lua 5.3 脚本。

### 项目说明
当前是 XXTouch 单脚本项目，根目录 `.config` 的 `type` 为 `xxt`，发布产物是 `.xxt` 加密脚本。

- 入口固定为 `lua/scripts/main.lua`。
- 可复用模块放在 `lua/` 或 `lua/scripts/`，通过 `require '模块名'` 引用。
- 运行资源放在 `res/`，脚本中用 `XXT_RES_PATH..'/文件名'` 访问。
- 不要创建或套用 `Info.lua`、`.xui`、XPP 脚本包入口规则。

### 必须使用的文档流程
1. 如果当前 Agent 支持 Skills，必须先使用 `xxtouch-script` Skill，并按 Skill 的 reference lookup、XXTDo、人工辅助和临时文件脚本规则执行。
2. 如果当前 Agent 不支持 Skills 或没有 `xxtouch-script` Skill，才使用项目根目录的 [XXTouch 脚本开发指南](xxtouch-script-guide.md)。
3. 文档没有覆盖的 API、参数或返回值不要猜测；应询问用户，或通过项目代码、设备实测、官方文档补充确认。

### 本地约束
- 使用 Lua 5.3；XXTouch 内置模块是全局对象，不需要 `require`，也不要用同名局部变量遮蔽。
- `table.insert(t, x)` 形式的追加写成 `t[#t + 1] = x`。
- 除非用户明确要求，禁止使用 `os.execute`、`io.popen`。
- 临时素材放在 `.tmp/`；支持 Skill 时使用 `scripts/ensure_config_ignores.py`，否则手动确保 `.config.ignores` 和 `.config.buildIgnores` 都包含 `.tmp/`。
- 不要把临时素材放进 `res/`，因为 `res/` 会参与运行传输和发布打包。
- 有 XXTLanControl MCP 工具时优先用它做设备验证；`device_file_*` 只能访问设备 `XXT_HOME_PATH`，其它路径用 `device_run_script_snippet`。
