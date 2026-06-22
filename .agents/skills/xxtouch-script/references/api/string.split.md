# string.split

Purpose: Split a string by delimiter rules.

## Signature
```lua
split_text_array = string.split(text_to_split, delimiter)
```

## Example
```lua
-- Split account and password.
local t = string.split('lfue6841214----123456', '----')
sys.alert('Account: '..t[1])

-- Extract the verification code between two # characters.
t = string.split('Hello, your code is #4937# and is valid for 15 minutes.', '#')
sys.alert('Code: '..t[2])

-- Extract middle text with two different delimiters.
t = string.split('Hello, your code is 4937 and is valid for 15 minutes.', 'code is ')
t = string.split(t[2], ' and is valid')
sys.alert('Code: '..t[1])
```

## Common Wrapper
```lua
function str_middle(str, sep1, sep2)
    local t = string.split(str, sep1)
    if not sep2 or sep1 == sep2 then
        return t[2]
    end
    if not t[2] then
        return nil
    end
    return string.split(t[2], sep2)[1]
end

local code = str_middle('Hello, your code is 4937 and is valid for 15 minutes.', 'code is ', ' and is valid')
sys.alert(code) -- 4937

local code2 = str_middle('Hello, your code is #8346# and is valid for 15 minutes.', '#')
sys.alert(code2) -- 8346
```

## Path Handling Example
```lua
local path = '/private/var/mobile/Media/1ferver/lua/scripts/1.lua.xxt'

local function str_strip_dirname(path)
    local parts = string.split(path, '/')
    return parts[#parts]
end

local function str_strip_filename(path)
    local parts = string.split(path, '/')
    parts[#parts] = nil
    return table.concat(parts, '/')
end

local function str_strip_extension(path)
    local parts = string.split(path, '/')
    local filename_parts = string.split(parts[#parts], '.')
    parts[#parts] = filename_parts[1]
    return table.concat(parts, '/')
end

local function str_get_extension(path)
    local parts = string.split(path, '/')
    local filename_parts = string.split(parts[#parts], '.')
    table.remove(filename_parts, 1)
    return table.concat(filename_parts, '.')
end

sys.alert(str_strip_dirname(path))    -- 1.lua.xxt
sys.alert(str_strip_filename(path))   -- /private/var/mobile/Media/1ferver/lua/scripts
sys.alert(str_strip_extension(path))  -- /private/var/mobile/Media/1ferver/lua/scripts/1
sys.alert(str_get_extension(path))    -- lua.xxt
```

## Parameters
- text_to_split
    string, the string to split.
- delimiter
    string, delimiter.

## Returns
- split_text_array
    table, split string fragments arranged in order.

## Notes
Splits a string by delimiter rules.
Keywords: string split, text split, text slicing, text segmentation.
Do not use `string.split` to split UTF-8 text character by character; use `utf8.codes` / `utf8.char` instead.
