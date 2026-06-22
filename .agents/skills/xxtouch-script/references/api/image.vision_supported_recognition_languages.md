# image.vision_supported_recognition_languages

Purpose: Query OCR language identifiers supported by Vision.framework on the current system.

## Signature

```lua
languages = image.vision_supported_recognition_languages()
```

## Example

```lua
local languages = image.vision_supported_recognition_languages()
nLog(languages)
```

## Returns

- `languages`
    table, language identifiers such as `"en-US"`, `"zh-Hans"`, and `"ja-JP"`. Actual results depend on the iOS version.

## Notes

- Use this when choosing `lang` for `screen.ocr_text(..., {engine = "apple"})` or `ImageObject:apple_ocr(...)`.
- iOS 13 generally supports English; iOS 14/15 add common European languages and Chinese; iOS 16 adds more languages and automatic detection.
