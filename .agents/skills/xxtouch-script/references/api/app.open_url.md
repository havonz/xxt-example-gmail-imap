# app.open_url

Purpose: Open URL

## Signature
```lua
ok = app.open_url(URL)
```

## Example
```lua
app.open_url("https://www.google.com") -- Open the Google homepage with Safari.

app.open_url("prefs:root=SAFARI&path=CLEAR_HISTORY_AND_DATA") -- Jump to Settings -> Safari -> Clear History and Website Data.
```

## Jailbreak Fallback
```lua
local function sh_escape(path)
    return (string.gsub(path, "([ \\()<>'\"`#&*;?~$|])", "\\%1"))
end

os.execute('uiopen '..sh_escape('https://www.google.com'))
os.execute('uiopen '..sh_escape('prefs:root=SAFARI&path=CLEAR_HISTORY_AND_DATA'))
```

## Parameters
- URL
    string, the URL to open. URL schemes for related apps can also be opened.

## Returns
- ok
    boolean, whether the URL was opened successfully.

## Notes
Opens a URL in the foreground. URL schemes for related apps can also be opened.
For some URLs, jumping with this API may not produce the expected result. In a jailbreak environment, use the `uiopen` command instead.
