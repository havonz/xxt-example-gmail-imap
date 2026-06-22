# ImageObject:ocr_text

Purpose: Image OCR

## Signature
```lua
recognized_text, result_details = image:ocr_text([ engine_options, binarization_options ])
```

## Example
```lua
local img = image.load_file(XXT_SCRIPTS_PATH..'/1.png')

txt, info = img:ocr_text("en-US")
sys.toast("OCR result: "..txt:atrim())

txt, info = img:ocr_text("zh-Hans")
sys.toast("OCR result: "..txt:atrim())

txt, info = img:ocr_text({
    engine = "apple",
    lang = "zh-Hans",
}, "9D5D39-0F1F26,D3D3D2-2C2C2D")
sys.toast("OCR result: "..txt:atrim())

txt, info = img:ocr_text({
    engine = "paddle",
    lang = "ppocr_ch",
})
sys.toast("OCR result: "..txt:atrim())
```

## Legacy Tesseract Example
```lua
local img = image.load_file(XXT_SCRIPTS_PATH..'/1.png')

local txt = img:ocr_text()
sys.toast("OCR result: "..txt:atrim())

local txt2 = img:ocr_text("eng", "9D5D39-0F1F26,D3D3D2-2C2C2D")
sys.toast("OCR result: "..txt2:atrim())

local txt3 = img:ocr_text({
    lang = "eng",
    white_list = "1234567890",
}, "9D5D39-0F1F26,D3D3D2-2C2C2D")
sys.toast("OCR result: "..txt3:atrim())
```

## Notes
Recognizes text in an image. Except that no screen region parameters are needed, engine options, binarization options, and return details are the same as `references/api/screen.ocr_text.md`.
For direct engine-specific image OCR calls, see `references/api/ImageObject.apple_ocr.md` and `references/api/ImageObject.paddle_ocr.md`.
