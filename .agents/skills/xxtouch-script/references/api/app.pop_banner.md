# app.pop_banner

Purpose: App notification

## Signature
```lua
app.pop_banner(bundle_identifier, title, content)
```

## Example
```lua
app.pop_banner('com.tencent.mqq', 'QQ', 'You have a new message')
```

## Parameters
- bundle_identifier
    string
- title
    string, the notification title.
- content
    string, the notification content.

## Notes
Requires a full jailbreak environment and the basic dependency `libbulletin` installed from Cydia or Sileo.
