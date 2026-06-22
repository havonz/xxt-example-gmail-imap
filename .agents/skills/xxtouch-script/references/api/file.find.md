# file.find

Purpose: Find file/directory.

## Signature
```lua
file_list = file.find(match_pattern)
```

## Example
```lua
-- Simple wildcard mode. Only supports the three basic wildcards: * ? [...]
-- * matches any characters of any length, including length 0.
-- ? matches one arbitrary character.
-- [...] matches one arbitrary character inside the brackets. For example, [abc]haha.txt matches ahaha.txt, bhaha.txt, and chaha.txt.
-- [!...] matches one arbitrary character outside the brackets. For example, [!abc]haha.txt does not match ahaha.txt, bhaha.txt, or chaha.txt, but can match another single character such as xhaha.txt.
local results = file.find("/private/var/mobile/Containers/Shared/AppGroup/*/Library/Preferences/*.plist")

-- Precise Lua pattern matching mode.
-- Precise matching uses Lua table segments to build the match pattern. Strings are literal checks, and pattern matching can use boolean-returning functions to decide whether the current segment is valid.
local results = file.find{ -- <--- Note the braces here.
    "/private/var/mobile/Containers/Shared/AppGroup/", -- Plain strings do not need pattern matching.
    function(s) return s:match("^[A-F0-9]+%-[A-F0-9]+%-[A-F0-9]+%-[A-F0-9]+%-[A-F0-9]+$") end, -- Use a function to match the current segment.
    "/Library/Preferences/",
    function(s) return s:match("%.plist$") end, -- Use a function to match the current segment.
}
-- Precise Lua pattern matching mode can also wrap a single string in braces to create a simple pattern-matching function.
local results = file.find{ -- <--- Note the braces here.
    "/private/var/mobile/Containers/Shared/AppGroup/", -- Plain strings do not need pattern matching.
    {"^[A-F0-9]+%-[A-F0-9]+%-[A-F0-9]+%-[A-F0-9]+%-[A-F0-9]+$"}, -- A table wrapping one string marks this segment as needing pattern matching.
    "/Library/Preferences/", -- Plain strings do not need pattern matching.
    {"%.plist$"}, -- A table wrapping one string marks this segment as needing pattern matching.
}
```

## Parameters
- match_pattern
    table or string.

## Returns
- file_list
    table, list of found filenames.

## Notes
Searches files or directories with wildcard mode or Lua precise matching and returns the matched filename list.
If `match_pattern` is a string, wildcard matching is used. Wildcard matching supports only `*`, `?`, and `[...]`.
If `match_pattern` is a table, Lua precise matching is used.
