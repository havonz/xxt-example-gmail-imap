# ImageObject:paddle_ocr

Purpose: Recognize text in an existing ImageObject with Paddle-Lite OCR models.

## Signature

```lua
text, details = image_object:paddle_ocr([model_options])
```

## Options

```lua
local text, details = screen.image():paddle_ocr({
    det_path = XXT_HOME_PATH.."/models/ppocr_ch/det_opt.nb",
    cls_path = XXT_HOME_PATH.."/models/ppocr_ch/cls_opt.nb",
    rec_path = XXT_HOME_PATH.."/models/ppocr_ch/rec_opt.nb",
    config_path = XXT_HOME_PATH.."/models/ppocr_ch/config.txt",
    dict_path = XXT_HOME_PATH.."/models/ppocr_ch/dict.txt",
    downscale = 0.5,
})
```

- Paths should point to Paddle-Lite `.nb` OCR model files and supporting config/dict files.
- `downscale` shrinks the image before inference. Common values: `0.5`, `0.33`; smaller is faster but may miss small text.
- Returns `text, details`; `details` uses the OCR block shape documented in `screen.ocr_text.md`.

## Notes

- For screen-region OCR, use `screen.ocr_text(..., {engine = "paddle", lang = "ppocr_ch"})`.
- Very small images may not work well with Paddle-Lite OCR. Expand the captured region or use Apple Vision when needed.
