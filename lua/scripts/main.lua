local gmail_imap = require("gmail_imap")

local function show_error(message)
  sys.alert(tostring(message or "未知错误"), 0, "Gmail IMAP", "确定")
end

local function read_options()
  local dlg = dialog()
  dlg:set_title("Gmail IMAP")
  dlg:set_close_title("取消")
  dlg:set_submit_title("读取")
  dlg:add_group("账号")
  dlg:add_input("Gmail 邮箱", "")
  dlg:add_picker("认证方式", { "App Password", "XOAUTH2 Token", "XOAUTH2 Refresh Token" }, "App Password")
  dlg:add_input("密码 / Access Token / Refresh Token", "")
  dlg:add_group("OAuth Refresh")
  dlg:add_input("OAuth Client ID", "")
  dlg:add_input("OAuth Client Secret", "")
  dlg:add_group("读取")
  dlg:add_range("邮件数量", { 1, 20, 1 }, 5)

  local did_submit, opts = dlg:show()
  if not did_submit then
    return nil
  end

  local auth_type = "app_password"
  if opts["认证方式"] == "XOAUTH2 Token" then
    auth_type = "xoauth2"
  elseif opts["认证方式"] == "XOAUTH2 Refresh Token" then
    auth_type = "xoauth2_refresh"
  end

  return {
    email = opts["Gmail 邮箱"],
    auth_type = auth_type,
    secret = opts["密码 / Access Token / Refresh Token"],
    client_id = opts["OAuth Client ID"],
    client_secret = opts["OAuth Client Secret"],
    limit = tonumber(opts["邮件数量"]) or 5,
    mailbox = "INBOX",
    save_dir = XXT_SCRIPTS_PATH .. "/gmail_attachments",
    timeout = 15,
  }
end

local function attachment_names(attachments)
  local names = {}
  for _, item in ipairs(attachments or {}) do
    names[#names + 1] = item.filename
  end
  if #names == 0 then
    return "无"
  end
  return table.concat(names, ", ")
end

local function show_result(result)
  local dlg = dialog()
  dlg:set_title("Gmail IMAP 结果")
  dlg:set_close_title("关闭")
  dlg:set_submit_title("确定")
  dlg:add_group("汇总")
  dlg:add_input("读取结果", {
    multiline = true,
    default = table.concat({
      ("邮箱：%s"):format(result.mailbox or "INBOX"),
      ("附件目录：%s"):format(result.save_dir or ""),
      ("读取到 %d 封邮件"):format(#(result.messages or {})),
    }, "\n"),
  })

  dlg:add_group("邮件")
  for index, message in ipairs(result.messages or {}) do
    local subject = message.subject ~= "" and message.subject or "(无主题)"
    local title = ("%02d %s"):format(index, subject)
    local lines = {}
    lines[#lines + 1] = ("发件人：%s"):format(message.from ~= "" and message.from or "(未知)")
    lines[#lines + 1] = ("时间：%s"):format(message.date ~= "" and message.date or "(未知)")
    lines[#lines + 1] = ("附件：%s"):format(attachment_names(message.attachments))
    if message.preview ~= "" then
      lines[#lines + 1] = ""
      lines[#lines + 1] = message.preview
    end
    dlg:add_input(title, {
      multiline = true,
      default = table.concat(lines, "\n"),
    })
  end

  dlg:show()
end

local opts = read_options()
if not opts then
  return
end

sys.toast("正在读取 Gmail 邮件...")
local result, err = gmail_imap.fetch_recent(opts)
if not result then
  show_error(err)
  return
end

show_result(result)
