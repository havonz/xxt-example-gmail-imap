# captcha_recognizer

`captcha_recognizer` is a captcha recognition wrapper based on XXTouch's built-in `onnxruntime`; it currently exposes slider-model capabilities.

Version requirement: XXTouch later than 20260402 is required.

## Require

```lua
local captcha_recognizer = require("captcha_recognizer")
```

Dependencies:

- `require("onnxruntime")`
- `require("image.cv")`
- `require("yolo_backend_common")`

## Model Files

Default lookup:

- `XXT_HOME_PATH.."/models/captcha_recognizer/slider.onnx"`
- `/var/mobile/Media/1ferver/models/captcha_recognizer/slider.onnx`

You can also specify `model_path` or `model_dir`.

## Construction

```lua
local model = captcha_recognizer.new({type = "slider"})
-- Alternatively:
local model2 = captcha_recognizer.Slider({})
```

Constructor options:

- `type = "slider"`
- `model_path = "/path/to/slider.onnx"`
- `model_dir = "/path/to/model_dir"`
- `providers = {"cpu"}` or `{"coreml", "cpu"}`
- `fallback_to_cpu = true/false`
- `coreml_compute_units = "all" | "cpu_only" | "cpu_and_gpu" | "cpu_and_neural_engine"`
- `coreml_enable_on_subgraph = true/false`
- `coreml_require_static_input_shapes = true/false`
- `coreml_create_mlprogram = true/false`

CoreML options are passed through to `onnxruntime.session(...)` unchanged. The default provider is normalized by shared logic; CPU is used when no provider is passed.

## Image Input

Public recognition methods support:

- File paths
- Raw image bytes
- BASE64 strings
- `image_object`

## Module Functions

- `captcha_recognizer.new(opts)`: creates an instance; currently only `type = "slider"` is supported.
- `captcha_recognizer.Slider(opts)`: creates a slider-recognition instance; pass a table when calling directly.
- `captcha_recognizer.version()`: returns the module version.
- `captcha_recognizer.providers()`: returns a copy of the current `onnxruntime.providers()`.

## Instance Methods

### predict(input[, opts])

```lua
local batches = model:predict("/path/to/image.png", {
    confidence = 0.25,
    iou = 0.7,
    input_size = 640,
})
```

Legacy arguments are also supported: `predict(input, conf, iou, imgsz)`.

Returns `{batch}`. Each item in `batch.boxes` is `{x1, y1, x2, y2, score, class_id}`; `batch.masks` contains the corresponding masks.

### identify(input[, opts])

```lua
local box, confidence, preview = model:identify("/path/to/image.png", {
    confidence = 0.5,
    iou = 0.8,
    show = true,
})
```

Legacy arguments are also supported: `identify(input, conf, iou, show)`.

Returns:

- `box`: `{x1, y1, x2, y2}`; empty table when not recognized.
- `confidence`: confidence score; `0.0` when not recognized.
- `preview`: annotated image, returned only when `show = true`.

### identify_offset(input[, opts])

```lua
local offset, confidence = model:identify_offset("/path/to/image.png")
```

Returns the `x1` of the leftmost detection box, commonly used as the horizontal slider offset. Returns `0, 0.0` when not recognized.

### get_model_info()

Returns a copy of model path, input shape, providers, output information, whether CoreML is used, and related metadata.

### close()

Closes the underlying session and marks the instance as closed. Do not continue calling recognition methods afterward.

```lua
model:close()
```

## Shortest Example

```lua
local captcha_recognizer = require("captcha_recognizer")

local model = assert(captcha_recognizer.Slider({
    model_path = XXT_HOME_PATH.."/models/captcha_recognizer/slider.onnx",
}))

local offset, confidence = model:identify_offset(XXT_HOME_PATH.."/res/slider.png")
sys.log("offset", offset, "confidence", confidence)

model:close()
```

## Notes

- Pass `providers = {"coreml", "cpu"}` explicitly when CoreML is needed.
- For debugging, use `identify(..., {show = true})` to get an annotated image; normal runs usually only need coordinates and confidence.
