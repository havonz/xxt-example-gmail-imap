--[[
Gmail IMAP 模块使用说明

App Password 获取方式：
1. 打开 https://myaccount.google.com/apppasswords 并登录要读取的 Gmail 账号。
2. 如果页面提示不能创建，先在 Google 账号安全设置中开启“两步验证”。
3. 创建一个应用专用密码，名称可填写“XXTouch IMAP”。
4. 复制 Google 生成的 16 位应用专用密码。它只显示一次，丢失后只能重新生成。
5. 使用本模块时设置 auth_type = "app_password"，secret 填这个应用专用密码，不要填 Google 账号登录密码。

XOAUTH2 Access Token 获取方式：
1. 打开 Google OAuth Playground：https://developers.google.com/oauthplayground/
2. 在 Step 1 的 scope 输入框填入 https://mail.google.com/ 并点击 Authorize APIs。
3. 登录 Gmail 账号并授权后，在 Step 2 点击 Exchange authorization code for tokens。
4. 复制 Access token，使用本模块时设置 auth_type = "xoauth2"，secret 填 Access token，不要带 Bearer 前缀。
5. Access token 通常约 1 小时过期，过期后需要重新生成或改用 refresh token 流程。

XOAUTH2 Refresh Token 获取方式：
1. 打开 Google OAuth Playground：https://developers.google.com/oauthplayground/
2. 在 Step 1 的 scope 输入框填入 https://mail.google.com/ 并点击 Authorize APIs。
3. 登录 Gmail 账号并授权后，在 Step 2 点击 Exchange authorization code for tokens。
4. 复制 Refresh token。使用本模块时设置 auth_type = "xoauth2_refresh"，secret 或 refresh_token 填 Refresh token。
5. 注意：Playground 默认凭据生成的 Refresh token 会被自动撤销，页面提示通常是 24 小时。
6. 如果要长期使用，先去 https://console.cloud.google.com/apis/credentials 创建自己的 OAuth Client，
   然后在 Playground 右上角齿轮里勾选 Use your own OAuth credentials，填入自己的 Client ID 和 Client Secret，
   Access type 选择 Offline，再重复第 2-4 步。
7. 长期使用时，本模块还需要传入同一组 client_id 和 client_secret，才能用 Refresh token 自动换取临时 Access token。
8. 本模块不会持久保存 access token、refresh token、client secret。
]]

local gmail_imap = {}

local DEFAULT_HOST = "imap.gmail.com"
local DEFAULT_PORT = 993
local DEFAULT_TIMEOUT = 15
local DEFAULT_PREVIEW_BYTES = 8192
local DEFAULT_TOKEN_ENDPOINT = "https://oauth2.googleapis.com/token"

local function trim(s)
  return (tostring(s or ""):gsub("^%s+", ""):gsub("%s+$", ""))
end

local function lower(s)
  return tostring(s or ""):lower()
end

local function is_nil_atom(v)
  return v == nil or (type(v) == "string" and lower(v) == "nil")
end

local function normalize_space(s)
  return trim((s or ""):gsub("%s+", " "))
end

local function base64_encode(data)
  return string.base64_encode(data)
end

local function base64_decode(data)
  return string.base64_decode(tostring(data or ""):gsub("%s+", ""))
end

local function decode_quoted_printable(data)
  data = tostring(data or "")
  data = data:gsub("=\r\n", ""):gsub("=\n", "")
  return (data:gsub("=([0-9A-Fa-f][0-9A-Fa-f])", function(hex)
    return string.char(tonumber(hex, 16))
  end))
end

local function percent_decode(data)
  return (tostring(data or ""):gsub("%%([0-9A-Fa-f][0-9A-Fa-f])", function(hex)
    return string.char(tonumber(hex, 16))
  end))
end

local function convert_charset(data, charset)
  data = tostring(data or "")
  charset = lower(trim(charset or "utf-8"):gsub('"', ""))
  if charset == "" or charset == "utf-8" or charset == "utf8" or charset == "us-ascii" then
    return data
  end

  if charset == "gbk" or charset == "gb2312" or charset == "gb18030" then
    return string.from_gbk(data) or data
  end

  local iconv_mod = require("iconv")
  local cd = iconv_mod.new("UTF-8//IGNORE", charset)
  if not cd then
    return data
  end
  local converted = cd:iconv(data)
  return converted or data
end

local function decode_rfc2231_value(value)
  value = tostring(value or "")
  local charset, encoded = value:match("^([^']*)'[^']*'(.*)$")
  if charset then
    return convert_charset(percent_decode(encoded), charset)
  end
  return percent_decode(value)
end

local function decode_rfc2047_word(charset, mode, text)
  mode = lower(mode)
  local decoded
  if mode == "b" then
    decoded = base64_decode(text)
  else
    decoded = decode_quoted_printable((text or ""):gsub("_", " "))
  end
  return convert_charset(decoded, charset)
end

local function decode_rfc2047(data)
  data = tostring(data or "")
  data = data:gsub("(=%?[^?]+%?[BbQq]%?[^?]*%?=)%s+(=%?[^?]+%?[BbQq]%?[^?]*%?=)", "%1%2")
  return (data:gsub("=%?([^?]+)%?([BbQq])%?([^?]*)%?=", decode_rfc2047_word))
end

local function decode_transfer(data, encoding)
  encoding = lower(encoding)
  if encoding == "base64" then
    return base64_decode(data)
  end
  if encoding == "quoted-printable" then
    return decode_quoted_printable(data)
  end
  return data or ""
end

local function imap_quote(value)
  value = tostring(value or "")
  value = value:gsub("\\", "\\\\"):gsub('"', '\\"'):gsub("\r", ""):gsub("\n", "")
  return '"' .. value .. '"'
end

local function build_xoauth2(email, access_token)
  return base64_encode("user=" .. tostring(email or "") .. "\001auth=Bearer " .. tostring(access_token or "") .. "\001\001")
end

local function strip_bearer(token)
  return trim(tostring(token or "")):gsub("^[Bb][Ee][Aa][Rr][Ee][Rr]%s+", "")
end

local function token_error_from_body(body)
  if not body or body == "" then
    return "empty token response"
  end
  local decoded, decode_err = json.decode(body)
  if type(decoded) ~= "table" then
    return "invalid token response: " .. tostring(decode_err or body)
  end
  local message = decoded.error_description or decoded.error
  if message and message ~= json.null then
    return tostring(message)
  end
  return body
end

local function refresh_access_token(opts)
  local refresh_token = trim(opts.refresh_token or opts.secret)
  local form = http.table_to_form_urlencoded({
    client_id = opts.client_id,
    client_secret = opts.client_secret,
    refresh_token = refresh_token,
    grant_type = "refresh_token",
  })

  local code, _, body = http.post(
    opts.token_endpoint or DEFAULT_TOKEN_ENDPOINT,
    opts.token_timeout or opts.timeout or DEFAULT_TIMEOUT,
    { ["Content-Type"] = "application/x-www-form-urlencoded" },
    form
  )

  if code ~= 200 then
    error("OAuth refresh token failed: HTTP " .. tostring(code) .. " " .. token_error_from_body(body))
  end

  local decoded = json.decode(body)
  if type(decoded) ~= "table" or not decoded.access_token or decoded.access_token == json.null then
    error("OAuth refresh token failed: " .. token_error_from_body(body))
  end

  return strip_bearer(decoded.access_token)
end

local function sanitize_filename(name)
  name = decode_rfc2047(tostring(name or ""))
  name = name:gsub("[%c]", "_"):gsub("[/\\:]+", "_"):gsub("%.%.+", "_")
  name = name:gsub("_+", "_")
  name = trim(name)
  if name == "" or name == "." then
    name = "attachment.bin"
  end
  if #name > 160 then
    local ext = name:match("(%.[^%.]*)$")
    ext = ext and #ext <= 16 and ext or ""
    name = name:sub(1, 160 - #ext) .. ext
  end
  return name
end

local function strip_html(html)
  local text = tostring(html or "")
  text = text:gsub("<br%s*/?>", "\n"):gsub("<BR%s*/?>", "\n")
  text = text:gsub("</p%s*>", "\n"):gsub("</P%s*>", "\n")
  text = text:gsub("<[^>]+>", " ")
  text = text:gsub("&nbsp;", " ")
    :gsub("&lt;", "<")
    :gsub("&gt;", ">")
    :gsub("&amp;", "&")
    :gsub("&quot;", '"')
    :gsub("&#39;", "'")
  return text
end

local function make_preview(body, is_html)
  if is_html then
    body = strip_html(body)
  end
  body = tostring(body or ""):gsub("\239\187\191", "")
  body = normalize_space(body:gsub("\r\n", "\n"):gsub("\r", "\n"))
  if #body > 320 then
    body = body:sub(1, 320) .. "..."
  end
  return body
end

local function parse_headers(raw)
  local headers = {}
  raw = tostring(raw or ""):gsub("\r\n[ \t]+", " "):gsub("\n[ \t]+", " ")
  for line in raw:gmatch("[^\r\n]+") do
    local name, value = line:match("^([^:]+):%s*(.*)$")
    if name then
      headers[lower(name)] = value
    end
  end
  return {
    date = trim(headers.date or ""),
    from = decode_rfc2047(trim(headers.from or "")),
    subject = decode_rfc2047(trim(headers.subject or "")),
  }
end

local function skip_spaces(data, i)
  while i <= #data do
    local ch = data:sub(i, i)
    if ch ~= " " and ch ~= "\t" and ch ~= "\r" and ch ~= "\n" then
      break
    end
    i = i + 1
  end
  return i
end

local parse_imap_value

local function parse_imap_quoted(data, i)
  local out = {}
  i = i + 1
  local escaped = false
  while i <= #data do
    local ch = data:sub(i, i)
    if escaped then
      out[#out + 1] = ch
      escaped = false
    elseif ch == "\\" then
      escaped = true
    elseif ch == '"' then
      return table.concat(out), i + 1
    else
      out[#out + 1] = ch
    end
    i = i + 1
  end
  error("unterminated IMAP quoted string")
end

local function parse_imap_literal(data, i)
  local close_pos = data:find("}\r\n", i, true)
  if not close_pos then
    error("invalid IMAP literal")
  end
  local size = tonumber(data:sub(i + 1, close_pos - 1))
  if not size then
    error("invalid IMAP literal size")
  end
  local start_pos = close_pos + 3
  local end_pos = start_pos + size - 1
  if end_pos > #data then
    error("truncated IMAP literal")
  end
  return data:sub(start_pos, end_pos), end_pos + 1
end

local function parse_imap_atom(data, i)
  local out = {}
  while i <= #data do
    local ch = data:sub(i, i)
    if ch == " " or ch == "\t" or ch == "\r" or ch == "\n" or ch == "(" or ch == ")" then
      break
    end
    if ch == "[" then
      local close_pos = data:find("]", i, true)
      if not close_pos then
        error("unterminated IMAP bracket atom")
      end
      out[#out + 1] = data:sub(i, close_pos)
      i = close_pos + 1
    else
      out[#out + 1] = ch
      i = i + 1
    end
  end
  return table.concat(out), i
end

local function parse_imap_list(data, i)
  local list = {}
  i = i + 1
  while i <= #data do
    i = skip_spaces(data, i)
    local ch = data:sub(i, i)
    if ch == ")" then
      return list, i + 1
    end
    local value
    value, i = parse_imap_value(data, i)
    list[#list + 1] = value
  end
  error("unterminated IMAP list")
end

parse_imap_value = function(data, i)
  i = skip_spaces(data, i or 1)
  local ch = data:sub(i, i)
  if ch == "(" then
    return parse_imap_list(data, i)
  end
  if ch == '"' then
    return parse_imap_quoted(data, i)
  end
  if ch == "{" then
    return parse_imap_literal(data, i)
  end
  return parse_imap_atom(data, i)
end

local function parse_fetch_records(records)
  local messages = {}
  for _, record in ipairs(records or {}) do
    local seq, rest = record:match("^%*%s+(%d+)%s+FETCH%s+(.+)$")
    if seq and rest then
      local ok, parsed = pcall(parse_imap_value, rest, 1)
      if ok and type(parsed) == "table" then
        local msg = { sequence = tonumber(seq), bodies = {} }
        local i = 1
        while i <= #parsed do
          local key = parsed[i]
          local value = parsed[i + 1]
          if type(key) == "string" then
            msg[key] = value
            if key:match("^BODY%[") then
              msg.bodies[key] = value
            end
          end
          i = i + 2
        end
        messages[#messages + 1] = msg
      end
    end
  end
  return messages
end

local function params_to_map(list)
  local map = {}
  if type(list) ~= "table" then
    return map
  end
  local i = 1
  while i <= #list do
    local key = list[i]
    local value = list[i + 1]
    if type(key) == "string" and not is_nil_atom(value) then
      map[lower(key)] = tostring(value)
    end
    i = i + 2
  end
  return map
end

local function mime_param(params, name)
  name = lower(name)
  if params[name] then
    if params[name]:find("^[^']*'[^']*'") then
      return decode_rfc2231_value(params[name])
    end
    return decode_rfc2047(params[name])
  end
  if params[name .. "*"] then
    return decode_rfc2231_value(params[name .. "*"])
  end

  local pieces = {}
  local encoded = false
  for i = 0, 50 do
    local value = params[name .. "*" .. i .. "*"]
    if value then
      encoded = true
      pieces[#pieces + 1] = percent_decode(value)
    else
      value = params[name .. "*" .. i]
      if value then
        pieces[#pieces + 1] = value
      else
        break
      end
    end
  end

  if #pieces == 0 then
    return nil
  end

  local joined = table.concat(pieces)
  if encoded and joined:find("^[^']*'[^']*'") then
    return decode_rfc2231_value(joined)
  end
  if encoded then
    return percent_decode(joined)
  end
  return decode_rfc2047(joined)
end

local function parse_disposition(node, media_type, subtype)
  local index = 9
  if media_type == "text" then
    index = 10
  elseif media_type == "message" and subtype == "rfc822" then
    index = 12
  end

  local disp = node[index]
  if type(disp) ~= "table" then
    return nil, {}
  end
  return lower(disp[1]), params_to_map(disp[2])
end

local function collect_body_parts(node, prefix, out)
  out = out or {}
  if type(node) ~= "table" then
    return out
  end

  if type(node[1]) == "table" then
    local i = 1
    while type(node[i]) == "table" do
      local part_id = prefix and (prefix .. "." .. tostring(i)) or tostring(i)
      collect_body_parts(node[i], part_id, out)
      i = i + 1
    end
    return out
  end

  local media_type = lower(node[1])
  local subtype = lower(node[2])
  local params = params_to_map(node[3])
  local disposition, disposition_params = parse_disposition(node, media_type, subtype)
  local filename = mime_param(disposition_params, "filename") or mime_param(params, "name")

  out[#out + 1] = {
    part = prefix or "1",
    type = media_type,
    subtype = subtype,
    params = params,
    disposition = disposition,
    filename = filename,
    encoding = tostring(node[6] or "7BIT"),
    size = tonumber(node[7]) or 0,
  }
  return out
end

local function choose_preview_part(parts)
  local html_part
  for _, part in ipairs(parts or {}) do
    local can_preview = not part.filename and part.disposition ~= "attachment"
    if can_preview and part.type == "text" and part.subtype == "plain" then
      return part, false
    end
    if can_preview and not html_part and part.type == "text" and part.subtype == "html" then
      html_part = part
    end
  end
  if html_part then
    return html_part, true
  end
  return nil, false
end

local function parse_search_uids(records)
  local uids = {}
  for _, record in ipairs(records or {}) do
    local ids = record:match("^%*%s+SEARCH%s*(.*)$")
    if ids then
      for id in ids:gmatch("%d+") do
        uids[#uids + 1] = tonumber(id)
      end
    end
  end
  return uids
end

local function first_body_value(fetch)
  if not fetch or not fetch.bodies then
    return nil
  end
  for _, value in pairs(fetch.bodies) do
    return value
  end
  return nil
end

local function header_body_value(fetch)
  if not fetch or not fetch.bodies then
    return nil
  end
  for key, value in pairs(fetch.bodies) do
    if key:match("^BODY%[HEADER") then
      return value
    end
  end
  return nil
end

local function ensure_dir(path)
  local ok, err = file.mkdir_p(path)
  if ok == false then
    error("cannot create attachment directory: " .. tostring(err))
  end
end

local function file_exists(path)
  return file.exists(path)
end

local function write_file(path, data)
  local ok, err = file.writes(path, data)
  if ok == false then
    error("cannot write attachment: " .. tostring(err))
  end
end

local function filename_with_suffix(filename, suffix)
  local stem, ext = filename:match("^(.*)(%.[^%.]*)$")
  if not stem or stem == "" or #ext > 16 then
    return filename .. suffix
  end
  return stem .. suffix .. ext
end

local function unique_attachment_path(save_dir, uid, index, filename)
  local path = save_dir .. "/" .. filename
  if not file_exists(path) then
    return path
  end

  local prefixed = tostring(uid) .. "_" .. tostring(index) .. "_" .. filename
  path = save_dir .. "/" .. prefixed
  if not file_exists(path) then
    return path
  end

  for suffix = 2, 1000 do
    path = save_dir .. "/" .. filename_with_suffix(prefixed, "_" .. tostring(suffix))
    if not file_exists(path) then
      return path
    end
  end

  error("cannot find unique attachment path: " .. filename)
end

local Client = {}
Client.__index = Client

function Client.new(opts)
  local socket_mod = assert(require("socket"))
  local ssl_mod = assert(require("ssl"))
  local tcp, tcp_err = socket_mod.tcp()
  if not tcp then
    error("cannot create tcp socket: " .. tostring(tcp_err))
  end

  tcp:settimeout(opts.timeout or DEFAULT_TIMEOUT)
  local ok_connect, connect_err = tcp:connect(opts.host or DEFAULT_HOST, opts.port or DEFAULT_PORT)
  if not ok_connect then
    tcp:close()
    error("cannot connect Gmail IMAP: " .. tostring(connect_err))
  end

  local tls_params = {
    mode = "client",
    protocol = opts.protocol or "tlsv1_2",
    verify = opts.cafile and "peer" or "none",
    options = "all",
  }
  if opts.cafile then
    tls_params.cafile = opts.cafile
  end

  local wrapped, wrap_err = ssl_mod.wrap(tcp, tls_params)
  if not wrapped then
    tcp:close()
    error("cannot wrap tls socket: " .. tostring(wrap_err))
  end
  wrapped:settimeout(opts.timeout or DEFAULT_TIMEOUT)

  local ok_handshake, handshake_err = wrapped:dohandshake()
  if not ok_handshake then
    wrapped:close()
    error("cannot finish tls handshake: " .. tostring(handshake_err))
  end

  local client = setmetatable({
    socket = wrapped,
    tag_index = 0,
    host = opts.host or DEFAULT_HOST,
    port = opts.port or DEFAULT_PORT,
  }, Client)

  client.greeting = client:receive_line()
  if not client.greeting:match("^%*%s+OK") and not client.greeting:match("^%*%s+PREAUTH") then
    client:close()
    error("unexpected IMAP greeting: " .. tostring(client.greeting))
  end
  return client
end

function Client:next_tag()
  self.tag_index = self.tag_index + 1
  return ("A%04d"):format(self.tag_index)
end

function Client:receive_line()
  local line, err, partial = self.socket:receive("*l")
  if not line then
    error("imap receive failed: " .. tostring(err) .. " " .. tostring(partial or ""))
  end
  return line
end

function Client:receive_bytes(size)
  local data, err, partial = self.socket:receive(size)
  if not data then
    error("imap literal receive failed: " .. tostring(err) .. " " .. tostring(partial or ""))
  end
  return data
end

function Client:send_raw(data)
  local start_index = 1
  while start_index <= #data do
    local sent, err, last_index = self.socket:send(data, start_index)
    if not sent then
      error("imap send failed: " .. tostring(err) .. " " .. tostring(last_index or ""))
    end
    if sent < start_index then
      error("imap send failed: partial send made no progress")
    end
    start_index = sent + 1
  end
end

function Client:send_line(line)
  self:send_raw(line .. "\r\n")
end

function Client:read_response(tag)
  local records = {}
  local current
  local tagged

  while true do
    local line = self:receive_line()
    if current and (line:sub(1, 1) == "*" or line:match("^" .. tag .. "%s+")) then
      records[#records + 1] = current
      current = nil
    end

    local literal_size = tonumber(line:match("{(%d+)}$"))
    if literal_size then
      local literal = self:receive_bytes(literal_size)
      current = (current and (current .. "\r\n" .. line) or line) .. "\r\n" .. literal
    else
      local record = current and (current .. "\r\n" .. line) or line
      records[#records + 1] = record
      current = nil
      if line:match("^" .. tag .. "%s+") then
        tagged = line
        break
      end
    end
  end

  return records, tagged
end

function Client:command(command_text)
  local tag = self:next_tag()
  self:send_line(tag .. " " .. command_text)
  local records, tagged = self:read_response(tag)
  local status, message = tagged:match("^" .. tag .. "%s+([A-Z]+)%s*(.*)$")
  if status ~= "OK" then
    error(trim(message) ~= "" and trim(message) or ("IMAP command failed: " .. command_text))
  end
  return records
end

function Client:login(email, password)
  self:command("LOGIN " .. imap_quote(email) .. " " .. imap_quote(password))
end

function Client:authenticate_xoauth2(email, access_token)
  local tag = self:next_tag()
  self:send_line(tag .. " AUTHENTICATE XOAUTH2 " .. build_xoauth2(email, access_token))

  local records = {}
  local challenge
  while true do
    local line = self:receive_line()
    records[#records + 1] = line
    if line:sub(1, 1) == "+" then
      local encoded = trim(line:sub(2))
      challenge = encoded ~= "" and base64_decode(encoded) or ""
      self:send_raw("\r\n")
    elseif line:match("^" .. tag .. "%s+") then
      local status, message = line:match("^" .. tag .. "%s+([A-Z]+)%s*(.*)$")
      if status ~= "OK" then
        local detail = challenge and normalize_space(challenge) or trim(message)
        error("XOAUTH2 authentication failed: " .. tostring(detail))
      end
      return records
    end
  end
end

function Client:authenticate(opts)
  if opts.auth_type == "xoauth2" then
    self:authenticate_xoauth2(opts.email, opts.secret)
  else
    self:login(opts.email, opts.secret)
  end
end

function Client:fetch_body_part(uid, part, max_bytes)
  local section = part or "TEXT"
  local partial = max_bytes and ("<0." .. tostring(max_bytes) .. ">") or ""
  local records = self:command("UID FETCH " .. tostring(uid) .. " (BODY.PEEK[" .. section .. "]" .. partial .. ")")
  local fetches = parse_fetch_records(records)
  return first_body_value(fetches[1]) or ""
end

function Client:close()
  if self.socket then
    pcall(function()
      self.socket:close()
    end)
    self.socket = nil
  end
end

function Client:logout()
  if not self.socket then
    return
  end
  pcall(function()
    self:command("LOGOUT")
  end)
  self:close()
end

local function default_save_dir()
  if XXT_SCRIPTS_PATH then
    return XXT_SCRIPTS_PATH .. "/gmail_attachments"
  end
  return "./gmail_attachments"
end

local function validate_opts(opts)
  if type(opts) ~= "table" then
    error("opts must be a table")
  end
  local normalized = {}
  for key, value in pairs(opts) do
    normalized[key] = value
  end
  opts = normalized
  opts.email = trim(opts.email)
  opts.secret = tostring(opts.secret or "")
  opts.refresh_token = tostring(opts.refresh_token or "")
  opts.client_id = trim(opts.client_id or "")
  opts.client_secret = tostring(opts.client_secret or "")
  opts.auth_type = opts.auth_type or "app_password"
  opts.mailbox = opts.mailbox or "INBOX"
  opts.limit = tonumber(opts.limit) or 5
  opts.timeout = tonumber(opts.timeout) or DEFAULT_TIMEOUT
  opts.save_dir = opts.save_dir or default_save_dir()

  if opts.email == "" then
    error("email is required")
  end
  if opts.auth_type == "xoauth2" then
    opts.secret = strip_bearer(opts.secret)
  end
  if opts.auth_type == "xoauth2_refresh" and opts.refresh_token == "" then
    opts.refresh_token = opts.secret
  end
  if opts.auth_type ~= "xoauth2_refresh" and opts.secret == "" then
    error("password or access token is required")
  end
  if opts.auth_type == "xoauth2_refresh" then
    if trim(opts.refresh_token) == "" then
      error("refresh token is required")
    end
    if opts.client_id == "" then
      error("OAuth client_id is required")
    end
    if opts.client_secret == "" then
      error("OAuth client_secret is required")
    end
  end
  if opts.auth_type ~= "app_password" and opts.auth_type ~= "xoauth2" and opts.auth_type ~= "xoauth2_refresh" then
    error("auth_type must be app_password, xoauth2, or xoauth2_refresh")
  end
  if opts.limit < 1 then
    opts.limit = 1
  elseif opts.limit > 50 then
    opts.limit = 50
  end
  return opts
end

local function clean_error(err)
  local message = tostring(err or "unknown error")
  message = message:gsub("^.-gmail_imap%.lua:%d+:%s*", "")
  return message
end

local function message_from_fetch(client, uid, fetch, save_dir)
  local headers = parse_headers(header_body_value(fetch) or "")
  local bodystructure = fetch and fetch.BODYSTRUCTURE
  local parts = collect_body_parts(bodystructure)
  local preview_part, is_html = choose_preview_part(parts)
  local preview = ""

  if preview_part then
    local raw_preview = client:fetch_body_part(uid, preview_part.part, DEFAULT_PREVIEW_BYTES)
    local decoded = decode_transfer(raw_preview, preview_part.encoding)
    decoded = convert_charset(decoded, preview_part.params.charset or "utf-8")
    preview = make_preview(decoded, is_html)
  else
    local raw_preview = client:fetch_body_part(uid, "TEXT", DEFAULT_PREVIEW_BYTES)
    preview = make_preview(raw_preview, false)
  end

  local attachments = {}
  local save_dir_ready = false
  for _, part in ipairs(parts) do
    if part.filename then
      if not save_dir_ready then
        ensure_dir(save_dir)
        save_dir_ready = true
      end
      local raw = client:fetch_body_part(uid, part.part)
      local content = decode_transfer(raw, part.encoding)
      local filename = sanitize_filename(part.filename)
      local path = unique_attachment_path(save_dir, uid, #attachments + 1, filename)
      write_file(path, content)
      attachments[#attachments + 1] = {
        filename = filename,
        path = path,
        mime_type = part.type .. "/" .. part.subtype,
        size = #content,
        encoding = part.encoding,
      }
    end
  end

  return {
    uid = tonumber(uid),
    date = headers.date,
    from = headers.from,
    subject = headers.subject,
    preview = preview,
    attachments = attachments,
  }
end

function gmail_imap.fetch_recent(opts)
  local client
  local ok, result_or_error = pcall(function()
    opts = validate_opts(opts)
    if opts.auth_type == "xoauth2_refresh" then
      opts.secret = refresh_access_token(opts)
      opts.auth_type = "xoauth2"
    end
    client = Client.new(opts)
    client:command("CAPABILITY")
    client:authenticate(opts)
    client:command("EXAMINE " .. imap_quote(opts.mailbox))

    local search_records = client:command("UID SEARCH ALL")
    local uids = parse_search_uids(search_records)
    local selected = {}
    for i = #uids, 1, -1 do
      selected[#selected + 1] = uids[i]
      if #selected >= opts.limit then
        break
      end
    end

    local result = { messages = {}, mailbox = opts.mailbox, save_dir = opts.save_dir }
    if #selected == 0 then
      client:logout()
      client = nil
      return result
    end

    local uid_set = table.concat(selected, ",")
    local summary_records = client:command(
      "UID FETCH " .. uid_set .. " (UID BODY.PEEK[HEADER.FIELDS (DATE FROM SUBJECT)] BODYSTRUCTURE)"
    )
    local fetches = parse_fetch_records(summary_records)
    local by_uid = {}
    for _, fetch in ipairs(fetches) do
      if fetch.UID then
        by_uid[tostring(fetch.UID)] = fetch
      end
    end

    for _, uid in ipairs(selected) do
      local fetch = by_uid[tostring(uid)]
      if fetch then
        result.messages[#result.messages + 1] = message_from_fetch(client, uid, fetch, opts.save_dir)
      end
    end

    client:logout()
    client = nil
    return result
  end)

  if client then
    client:logout()
  end

  if not ok then
    return nil, clean_error(result_or_error)
  end
  return result_or_error
end

gmail_imap._test = {
  base64_encode = base64_encode,
  base64_decode = base64_decode,
  build_xoauth2 = build_xoauth2,
  collect_body_parts = collect_body_parts,
  decode_quoted_printable = decode_quoted_printable,
  decode_rfc2047 = decode_rfc2047,
  decode_rfc2231_value = decode_rfc2231_value,
  imap_quote = imap_quote,
  parse_fetch_records = parse_fetch_records,
  parse_headers = parse_headers,
  parse_imap_value = parse_imap_value,
  sanitize_filename = sanitize_filename,
  strip_bearer = strip_bearer,
}

return gmail_imap
