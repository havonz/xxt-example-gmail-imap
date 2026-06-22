# yolo_onnx

`yolo_onnx` is a YOLO wrapper based on XXTouch's built-in `onnxruntime`; it supports detect, classify, and obb, and can extend seg, pose, and track through profiles.

Version requirement: XXTouch later than 20260402 is required.

## Require

```lua
local yolo_onnx = require("yolo_onnx")
```

Dependencies:

- `require("onnxruntime")`
- `require("yolo_tracker")`
- `require("yolo_profile_runtime")`
- `require("yolo_backend_common")`

## Model Files

Default lookup:

- `XXT_HOME_PATH.."/models/yolo_onnx/model.onnx"`
- `/var/mobile/Media/1ferver/models/yolo_onnx/model.onnx`

You can also specify `model_path` or `model_dir`.

Label-file lookup checks the model directory, `model_dir`, and the default model root. `class_names` supports tables, file paths, and preset names.

## Construction

```lua
local detector = yolo_onnx.new({
    model_path = XXT_HOME_PATH.."/models/yolo_onnx/yolo11n.onnx",
    task = "detect",
})
```

Constructor options:

- `model_path = "/path/to/model.onnx"`
- `model_dir = "/path/to/model_dir"`
- `task = "detect" | "classify" | "obb"`
- `class_names = {"a", "b"}` or `"/path/to/classes.txt"` or `"coco80"` / `"imagenet1000"` / `"dota15"`
- `providers = {"cpu"}` or `{"coreml", "cpu"}`
- `fallback_to_cpu = true/false`
- `threads = integer`
- `input_width = integer`
- `input_height = integer`
- `confidence = number`
- `iou = number`
- `max_det = integer`
- `class_ids = {0, 1, 2}`
- `class_agnostic = true/false`
- `profile = table`
- `tracker = table`
- `coreml_compute_units = "all" | "cpu_only" | "cpu_and_gpu" | "cpu_and_neural_engine"`
- `coreml_enable_on_subgraph = true/false`
- `coreml_require_static_input_shapes = true/false`
- `coreml_create_mlprogram = true/false`

CoreML options are passed through to `onnxruntime.session(...)` unchanged.

## Image Input

Public inference methods support:

- File paths
- Raw image bytes
- BASE64 strings
- `image_object`

## Module Functions

- `yolo_onnx.supported_tasks()`: returns `{"detect", "seg", "pose", "obb", "track", "classify"}`.
- `yolo_onnx.new(opts)`: creates an instance.
- `yolo_onnx.create(opts)` / `open(opts)`: aliases of `new`.
- `yolo_onnx.tracker(opts)`: creates a tracker.

## Instance Methods

- `run(input[, opts])`: automatically dispatches by the instance task or profile.
- `detect(input[, conf][, iou][, opts])`
- `predict(input[, conf][, iou][, opts])`: alias of `run`.
- `classify(input[, opts])`
- `segment(input[, conf][, iou][, opts])`
- `pose(input[, conf][, iou][, opts])`
- `track(input[, conf][, iou][, opts])`
- `detect_obb(input[, conf][, iou][, opts])`
- `obb(input[, conf][, iou][, opts])`
- `get_model_info()`
- `close()`

## Return Values

Detect returns an array of detections. Each item usually contains:

- `box = {x1, y1, x2, y2}`
- `x1`, `y1`, `x2`, `y2`
- `width`, `height`, `cx`, `cy`
- `score`
- `class_id`
- `label`: present when `class_names` can be resolved.

Classify returns:

- `class_id`
- `score`
- `label`
- `classes`
- `logits`: present only when `return_logits = true`.

OBB return items also contain:

- `cx`, `cy`, `w`, `h`, `theta`
- `points`
- enclosing `box` and `x1/y1/x2/y2`

Seg, pose, and track require suitable profiles. Seg adds `mask`, pose adds `keypoints`, and track returns detections updated by the tracker.

## Shortest Example

```lua
local yolo_onnx = require("yolo_onnx")

local detector = assert(yolo_onnx.new({
    model_path = XXT_HOME_PATH.."/models/yolo_onnx/yolo11n.onnx",
    class_names = "coco80",
    providers = {"cpu"},
}))

local detections = assert(detector:detect(XXT_HOME_PATH.."/res/bus.jpg"))
for i = 1, #detections do
    local det = detections[i]
    sys.log(det.label, det.score, det.x1, det.y1, det.x2, det.y2)
end

detector:close()
```

Classification example:

```lua
local classifier = assert(yolo_onnx.new({
    model_path = XXT_HOME_PATH.."/models/yolo_onnx/yolo11n-cls.onnx",
    task = "classify",
    class_names = "imagenet1000",
}))

local result = assert(classifier:classify(XXT_HOME_PATH.."/res/bus.jpg", {
    return_logits = true,
}))
sys.log(result.class_id, result.label, result.score)

classifier:close()
```

## Notes

- Pass `providers = {"coreml", "cpu"}` explicitly when CoreML is needed.
- The default is `task = "detect"`; classification and OBB models must pass `task` explicitly.
- Call `close()` after using an instance to release the session, decoder, and tracker.
