# ImageObject:apple_ocr

Purpose: Recognize text in an existing ImageObject with iOS Vision.framework.

## Signature

```lua
text, details = image_object:apple_ocr([lang_options])
```

## Options

```lua
local img = screen.image()
local text, details = img:apple_ocr({
    lang = "zh-Hans",
    level = "accurate",
    correction = true,
})
nLog(text, details)
```

- `lang`: Vision language identifier. On iOS 16+, `"auto_detection"` lets Vision detect language.
- `level`: `"accurate"` or `"fast"`; default favors accuracy.
- `custom_words`: newline-separated custom terms.
- `correction`: boolean.

Returns `text, details`; `details` uses the OCR block shape documented in `screen.ocr_text.md`.

## Notes

- Requires iOS 13 or later.
- To recognize a screen region directly, prefer `screen.ocr_text(..., {engine = "apple", lang = "..."})`.
- Use `image.vision_supported_recognition_languages()` to query Vision OCR languages supported by the current system.
