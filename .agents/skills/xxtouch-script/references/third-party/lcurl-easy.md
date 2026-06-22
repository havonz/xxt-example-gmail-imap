# lcurl Easy Slice

Source: https://lua-curl.github.io/lcurl/modules/lcurl.html

Use `curl.safe` for request execution when the script needs custom curl options. Prefer XXTouch `http` for ordinary requests.

## GET With Body And Status

```lua
local curl = require 'curl.safe'

local chunks = {}
local easy = curl.easy()
local ok, err = pcall(function()
    easy
        :setopt(curl.OPT_URL, 'https://example.com/api')
        :setopt(curl.OPT_CONNECTTIMEOUT, 10)
        :setopt(curl.OPT_TIMEOUT, 30)
        :setopt_writefunction(function(chunk)
            chunks[#chunks + 1] = chunk
            return true
        end)
        :perform()
end)

local status = easy:getinfo(curl.INFO_RESPONSE_CODE)
easy:close()

if not ok then
    return nil, err
end
return table.concat(chunks), status
```

## POST Raw Body

```lua
local curl = require 'curl.safe'

local body = json.encode({ok = true})
local response = {}
local easy = curl.easy()
easy
    :setopt(curl.OPT_URL, 'https://example.com/api')
    :setopt(curl.OPT_POST, true)
    :setopt(curl.OPT_HTTPHEADER, {'Content-Type: application/json'})
    :setopt_postfields(body)
    :setopt_writefunction(function(chunk)
        response[#response + 1] = chunk
        return true
    end)
    :perform()
easy:close()
```

## Download To File

```lua
local curl = require 'curl.safe'

local out = assert(io.open(XXT_HOME_PATH..'/download.bin', 'wb'))
local easy = curl.easy()
local ok, err = pcall(function()
    easy
        :setopt(curl.OPT_URL, 'https://example.com/file.bin')
        :setopt(curl.OPT_FOLLOWLOCATION, true)
        :setopt(curl.OPT_CONNECTTIMEOUT, 10)
        :setopt(curl.OPT_TIMEOUT, 60)
        :setopt_writefunction(function(chunk)
            out:write(chunk)
            return true
        end)
        :perform()
end)

local status = easy:getinfo(curl.INFO_RESPONSE_CODE)
easy:close()
out:close()

if not ok then
    return nil, err
end
if status < 200 or status >= 300 then
    return nil, 'http status '..tostring(status)
end
```

## Custom Headers

```lua
easy:setopt(curl.OPT_HTTPHEADER, {
    'Accept: application/json',
    'Authorization: Bearer '..token,
})
```

## Multipart Form

```lua
local curl = require 'curl.safe'

local form = curl.form()
form:add_content('name', 'value')
form:add_file('upload', XXT_RES_PATH..'/image.png', 'image/png')

local easy = curl.easy()
easy
    :setopt(curl.OPT_URL, 'https://example.com/upload')
    :setopt_httppost(form)
    :perform()
easy:close()
form:free()
```

## Useful APIs

- `curl.easy([options])` creates an easy handle.
- `easy:setopt(opt, value)` or `easy:setopt{ url = ..., [curl.OPT_VERBOSE] = true }`.
- `easy:setopt_writefunction(fn)` receives response chunks.
- `easy:setopt_readfunction(fn)` supplies upload data.
- `easy:getinfo(curl.INFO_RESPONSE_CODE)` reads status.
- `easy:escape(text)` and `easy:unescape(text)` percent encode/decode.
- `easy:close()` ends the handle.
- `curl.OPT_FOLLOWLOCATION` follows redirects; enable it only when expected.

## Notes

- Always close easy handles; free forms if created.
- Writer callbacks should return `true`, the full byte count, or nothing to continue.
- Do not log headers containing tokens.
- For ordinary downloads, prefer XXTouch `http.get` with `download_file`; use lcurl when you need curl-specific options.
