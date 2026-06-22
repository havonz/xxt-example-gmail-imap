# ddddocr

`ddddocr` is a ddddocr wrapper based on XXTouch's built-in `onnxruntime` and `image.cv`; it supports OCR, DET, and slider assistance.

Version requirement: XXTouch later than 20260402 is required.

## Require

```lua
local ddddocr = require("ddddocr")
```

Dependencies:

- `require("onnxruntime")`
- `require("image.cv")`
- `require("yolo_backend_common")`

## Model Files

Default lookup:

- `XXT_HOME_PATH.."/models/ddddocr"`
- `/var/mobile/Media/1ferver/models/ddddocr`

Common files:

- `common_old.onnx`
- `common_old.json`
- `common.onnx`
- `common.json`
- `common_det.onnx`

You can also specify `model_dir`, `import_onnx_path`, and `charsets_path`.

## Construction

```lua
local ocr = ddddocr.new({
    ocr = true,
    show_ad = false,
})

local det = ddddocr.new({
    det = true,
    show_ad = false,
})
```

Constructor options:

- `ocr = true/false`
- `det = true/false`
- `old = true/false`
- `beta = true/false`
- `show_ad = true/false`
- `model_dir = "/path/to/model_dir"`
- `import_onnx_path = "/path/to/model.onnx"`
- `charsets_path = "/path/to/model.json"`
- `providers = {"cpu"}` or `{"coreml", "cpu"}`
- `fallback_to_cpu = true/false`
- `coreml_compute_units = "all" | "cpu_only" | "cpu_and_gpu" | "cpu_and_neural_engine"`
- `coreml_enable_on_subgraph = true/false`
- `coreml_require_static_input_shapes = true/false`
- `coreml_create_mlprogram = true/false`

When `det = true`, a detection instance is created; otherwise an OCR instance is created by default. If `ocr = false` and no custom OCR model is provided, an instance used only for slider assistance is created.

## Image Input

Public recognition methods support:

- File paths
- Raw image bytes
- BASE64 strings
- `image_object`

## OCR

```lua
local text = ocr:classification("/path/to/captcha.png")
```

`classification(input[, opts])` is an alias of `ocr(input[, opts])`. It returns text by default.

Options:

- `png_fix = true`
- `color_filter_colors = {"red", "blue"}`
- `color_filter_custom_ranges = {{{h_min, s_min, v_min}, {h_max, s_max, v_max}}}`
- `probability = true`
- `charset_range = "0123456789"`

Output with probabilities:

```lua
local result = ocr:classification("/path/to/captcha.png", {
    probability = true,
})
print(result.text, result.confidence)
```

When `probability = true`, returns `{text, confidence, probabilities, charset}`.

Persistently restrict the charset:

```lua
ocr:set_ranges("0123456789")
local charset = ocr:get_charset()
```

Color presets:

```lua
local names = ddddocr.available_colors()
```

Current presets include black, blue, cyan, gray, green, orange, purple, red, white, and yellow.

## DET

```lua
local boxes = det:det("/path/to/image.png")
for i = 1, #boxes do
    local box = boxes[i]
    print(box[1], box[2], box[3], box[4])
end
```

`detect(input)` and `detection(input)` are both aliases of `det(input)`. Returns an array of boxes; each item is `{x1, y1, x2, y2}`.

## Slider Assistance

Supported at both module and instance level:

```lua
local result = ddddocr.slide_match(target_img, background_img)
print(result.target_x, result.target_y, result.confidence)

local simple = ddddocr.slide_match(target_img, background_img, true)
local diff = ddddocr.slide_comparison(target_img, background_img)
```

Returns:

- `target = {center_x, center_y}`
- `target_x`
- `target_y`
- `confidence`

`slide_comparison` requires both images to have the same size.

## Module Functions

- `ddddocr.new(opts)`
- `ddddocr.available_colors()`
- `ddddocr.slide_match(target, background[, simple_target])`
- `ddddocr.slide_comparison(target, background)`
- `ddddocr.version()`

## Instance Methods

- `ocr(input[, opts])`
- `classification(input[, opts])`
- `det(input)`
- `detect(input)`
- `detection(input)`
- `slide_match(target, background[, simple_target])`
- `slide_comparison(target, background)`
- `set_ranges(value)`
- `get_charset()`
- `get_model_info()`
- `close()`

`get_model_info()` returns a copy of model path, input shape, providers, output information, mode, and related metadata.

## Shortest Example

```lua
local ddddocr = require("ddddocr")

local ocr = assert(ddddocr.new({
    ocr = true,
    show_ad = false,
    model_dir = XXT_HOME_PATH.."/models/ddddocr",
}))

local text = ocr:classification(XXT_HOME_PATH.."/res/captcha.png", {
    charset_range = "0123456789",
})
sys.log("text", text)

ocr:close()
```

## Notes

- Pass `providers = {"coreml", "cpu"}` explicitly when CoreML is needed.
- OCR and DET are different instance modes. Detection instances cannot call text recognition, and OCR instances cannot call object detection.
- Call `close()` after using an instance to release the session.
