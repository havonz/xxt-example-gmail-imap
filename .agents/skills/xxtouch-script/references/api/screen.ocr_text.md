# screen.ocr_text

Purpose: Recognize text in screen region

## Signature
```lua
recognized_text, result_details = screen.ocr_text(left, top, right, bottom [, engine_options, binarization_options ])
```

## Example
```lua
txt, info = screen.ocr_text(187, 882, 298, 914, "en-US")
sys.toast("OCR result: "..txt:atrim())

txt, info = screen.ocr_text(187, 882, 298, 914, "zh-Hans")
sys.toast("OCR result: "..txt:atrim())

txt, info = screen.ocr_text(187, 882, 298, 914, {
    engine = "apple",
    lang = "zh-Hans",
}, "9D5D39-0F1F26,D3D3D2-2C2C2D")
sys.toast("OCR result: "..txt:atrim())

txt, info = screen.ocr_text(0, 0, 0, 0, {
    engine = "paddle",
    lang = "ppocr_ch",
})
sys.toast("OCR result: "..txt:atrim())
```

## Legacy Tesseract Example
```lua
local txt = screen.ocr_text(187, 882, 298, 914)
sys.toast("OCR result: "..txt:atrim())

local txt2 = screen.ocr_text(465, 241, 505, 269, "eng", "9D5D39-0F1F26,D3D3D2-2C2C2D")
sys.toast("OCR result: "..txt2:atrim())

local txt3 = screen.ocr_text(187, 882, 298, 914, {
    lang = "eng",
    white_list = "1234567890",
}, "9D5D39-0F1F26,D3D3D2-2C2C2D")
sys.toast("OCR result: "..txt3:atrim())
```

## Parameters
- left, top, right, bottom
    integer, the screen region. Pass `0, 0, 0, 0` for full screen.
- engine_options
    optional table used to select the recognition language and recognition engine.

    ```lua
    {
        engine = "apple" | "paddle" | "tesseract",
        lang = "zh-Hans",
    }
    ```

    ```lua
    { -- iOS 13
        [1] = "en-US",
    }

    { -- iOS 14~15
        [1] = "en-US",
        [2] = "fr-FR",
        [3] = "it-IT",
        [4] = "de-DE",
        [5] = "es-ES",
        [6] = "pt-BR",
        [7] = "zh-Hans",
        [8] = "zh-Hant",
    }

    { -- iOS 16
        [ 1] = "en-US",
        [ 2] = "fr-FR",
        [ 3] = "it-IT",
        [ 4] = "de-DE",
        [ 5] = "es-ES",
        [ 6] = "pt-BR",
        [ 7] = "zh-Hans",
        [ 8] = "zh-Hant",
        [ 9] = "yue-Hans",
        [10] = "yue-Hant",
        [11] = "ko-KR",
        [12] = "ja-JP",
        [13] = "ru-RU",
        [14] = "uk-UA",
    }
    ```

- binarization_options
    boolean, `true` enables automatic binarization.
    number, binarization threshold.
    table, custom binarization color tolerance. See manual image binarization.
    string, custom binarization color tolerance. See manual image binarization.
    By default no binarization is applied before OCR.

## Returns
- recognized_text
    string, the recognized text.
- result_details
    table

    ```lua
    {
        {
            ["y"] = number_value,
            ["x"] = number_value,
            ["w"] = number_value,
            ["h"] = number_value,
            ["confidence"] = number_value(0.0 ~ 100.0),
            ["text"] = string_value,
        },
        ...
    }
    ```

## Notes
For coordinate and region conventions, see Visual API Conventions in `references/workflow.md`.
Apple Vision: `en-US` requires iOS 13+, and `zh-Hans` requires iOS 14+.
For forward compatibility, when no recognition engine is specified, the deprecated `tesseract` engine is used for text recognition by default.
Apple and PaddleLite recognition engines are supported in XXTouch 1.3.8 and later.
Languages supported by Apple Vision can be queried with `image.vision_supported_recognition_languages()`.
Legacy tesseract is suitable as a fallback for recognizing English letters and digits. For Chinese or other languages, prepare the corresponding trained data under `XXT_TESSDATA_PATH`.
PaddleLite uses `lang` to specify the model directory. For example, `ppocr_ch` corresponds to `XXT_HOME_PATH.."/models/ppocr_ch"`, and model files are `*.nb`.

PaddleLite model downloads:
- [Simplified Chinese standard model (requires decompression)](https://xxtouch.lanzout.com/iL57a38ww71e)
- [Simplified Chinese full model (requires decompression)](https://xxtouch.lanzout.com/iiQYx38ww6fc)
- [Traditional Chinese recognition model (requires decompression)](https://xxtouch.lanzout.com/iNNpU38wyb3c)
- [English letters and digits recognition model (requires decompression)](https://xxtouch.lanzout.com/iiKtE3994q8f)
- [Japanese recognition model (requires decompression)](https://xxtouch.lanzout.com/iYXfK3boux0h)
- [Korean recognition model (requires decompression)](https://xxtouch.lanzout.com/ieCCH3bouxda)

You can also download the corresponding model from the [PaddleOCR model list](https://gitee.com/paddlepaddle/PaddleOCR/blob/release/2.4/doc/doc_ch/models_list.md), convert it to `det_opt.nb`, `cls_opt.nb`, and `rec_opt.nb`, and use it together with [`dict.txt`](https://gitee.com/paddlepaddle/PaddleOCR/tree/release/2.4/ppocr/utils/dict).
