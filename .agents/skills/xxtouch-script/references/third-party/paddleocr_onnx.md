# paddleocr_onnx

`paddleocr_onnx` is a text detection/recognition wrapper based on XXTouch's built-in `onnxruntime`, `image.cv`, and PaddleOCR ONNX models.

Version requirement: XXTouch later than 20260402 is required.

## Require

```lua
local paddleocr = require("paddleocr_onnx")
```

Dependencies:

- `require("onnxruntime")`
- `require("image.cv")`
- `require("yolo_backend_common")`

## Model Files

Expected files:

- `det.onnx`: text detection model, optional; when missing, only single-line images can be recognized.
- `rec.onnx`: text recognition model, required.
- `dict.txt`: character dictionary, required.

Default lookup:

- `XXT_HOME_PATH.."/models/paddleocr_onnx"`
- `/var/mobile/Media/1ferver/models/paddleocr_onnx`

You can also pass these separately:

- `det_model_path`
- `rec_model_path`
- `dict_path`
- `det_model_dir`
- `rec_model_dir`
- `model_dir`

## Construction

```lua
local ocr = paddleocr.new({
    model_dir = XXT_HOME_PATH.."/models/paddleocr_onnx/chinese",
})
```

Constructor options:

- `det_model_path = "/path/to/det.onnx"`
- `rec_model_path = "/path/to/rec.onnx"`
- `dict_path = "/path/to/dict.txt"`
- `det_model_dir = "/path/to/det_dir"`
- `rec_model_dir = "/path/to/rec_dir"`
- `model_dir = "/path/to/model_dir"`
- `providers = {"cpu"}` or `{"coreml", "cpu"}`
- `fallback_to_cpu = true/false`
- `threads = integer`
- `max_side_len = integer`
- `det_db_thresh = number`
- `det_db_box_thresh = number`
- `det_db_unclip_ratio = number`
- `det_db_use_dilate = true/false`
- `det_use_polygon_score = true/false`
- `rec_batch = true/false`
- `rec_batch_size = integer`
- `rec_batch_min_size = integer`
- `rec_bucket_width = true/false`
- `rec_bucket_width_stride = integer`
- `use_space_char = true/false`
- `coreml_compute_units = "all" | "cpu_only" | "cpu_and_gpu" | "cpu_and_neural_engine"`
- `coreml_enable_on_subgraph = true/false`
- `coreml_require_static_input_shapes = true/false`
- `coreml_create_mlprogram = true/false`

CoreML options are passed through to `onnxruntime.session(...)` unchanged.

## Image Input

Public recognition methods support:

- File paths
- Raw image bytes
- BASE64 strings
- `image_object`

## Full-Image Recognition

```lua
local result = ocr:recognize("/path/to/image.png", {
    return_stats = true,
})

print(result.text)
for i = 1, #result.lines do
    local line = result.lines[i]
    print(line.text, line.confidence, line.x, line.y, line.w, line.h)
end
```

`recognize(input[, opts])` first detects text boxes, then crops and recognizes them. Returns:

- `text`: text joined by line.
- `lines`: recognized line array.
- `stats`: returned only when `return_stats = true`; includes DET count and REC batch-processing statistics.

Each line contains at least:

- `text`
- `confidence`
- `det_confidence`
- `box`: four-point coordinate array.
- `x`, `y`, `w`, `h`

## Single-Line Recognition

```lua
local line = ocr:recognize_line("/path/to/text-line.png")
print(line.text, line.confidence)

local text = ocr:recognize_line("/path/to/text-line.png", {
    return_text_only = true,
})
```

`classification(input[, opts])` calls `recognize_line` with `return_text_only = true` by default, making it suitable for captchas or pre-cropped text lines.

## Detection

```lua
local boxes = ocr:detect("/path/to/image.png")
for i = 1, #boxes do
    local item = boxes[i]
    print(item.confidence, item.x, item.y, item.w, item.h)
end
```

`det(input)` is an alias of `detect(input)`. It requires configured `det.onnx`. Returns an array; each item contains:

- `box`: four-point coordinate array.
- `confidence`
- `x`, `y`, `w`, `h`

## Module Functions

- `paddleocr_onnx.new(opts)`
- `paddleocr_onnx.create(opts)`: alias of `new`.
- `paddleocr_onnx.open(opts)`: alias of `new`.

## Instance Methods

- `recognize_line(input[, opts])`
- `recognize(input[, opts])`
- `classification(input[, opts])`
- `ocr(input[, opts])`
- `detect(input)`
- `det(input)`
- `get_model_info()`
- `close()`

`get_model_info()` returns a copy of `rec`, `det`, `dict_path`, detection configuration, and recognition configuration.

## Shortest Example

```lua
local paddleocr = require("paddleocr_onnx")

local ocr = assert(paddleocr.new({
    det_model_path = XXT_HOME_PATH.."/models/paddleocr_onnx/chinese/det.onnx",
    rec_model_path = XXT_HOME_PATH.."/models/paddleocr_onnx/chinese/rec.onnx",
    dict_path = XXT_HOME_PATH.."/models/paddleocr_onnx/chinese/dict.txt",
    providers = {"cpu"},
}))

local result = ocr:recognize(XXT_HOME_PATH.."/res/page.png")
sys.log(result.text)

ocr:close()
```

## Notes

- `rec.onnx` and `dict.txt` are required. When `det.onnx` is missing, do not call `recognize` or `detect`; use only `recognize_line` / `classification`.
- Pass `providers = {"coreml", "cpu"}` explicitly when CoreML is needed.
- Call `close()` after using an instance to release DET/REC sessions.
