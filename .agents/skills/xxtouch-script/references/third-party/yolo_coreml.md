# yolo_coreml

`yolo_coreml` is a YOLO wrapper based on XXTouch's built-in `coreml` module; it supports detect, classify, and obb, and can extend seg, pose, and track through profiles.

Version requirement: XXTouch later than 20260402 is required.

## Require

```lua
local yolo_coreml = require("yolo_coreml")
```

Dependencies:

- global `coreml`
- `require("path")`
- `require("yolo_tracker")`
- `require("yolo_profile_runtime")`
- `require("yolo_backend_common")`

## Model Files

Instance construction requires `compiled_model_path` to point to `.mlmodelc`.

```lua
local compiled = assert(yolo_coreml.compile_model_cached(
    XXT_HOME_PATH.."/models/yolo_coreml/yolo11n.mlpackage"
))
```

Default label-file lookup checks:

- `model_dir`
- the compiled model's directory
- `XXT_HOME_PATH.."/models/yolo_coreml"`
- `/var/mobile/Media/1ferver/models/yolo_coreml`

## Construction

```lua
local model = yolo_coreml.new({
    compiled_model_path = compiled,
    task = "detect",
})
```

Constructor options:

- `compiled_model_path = "/path/to/model.mlmodelc"`
- `model_dir = "/path/to/model_dir"`
- `task = "detect" | "classify" | "obb"`
- `class_names = {"a", "b"}` or `"/path/to/classes.txt"` or `"coco80"` / `"imagenet1000"` / `"dota15"`
- `uses_cpu_only = true/false`
- `input_width = integer`
- `input_height = integer`
- `confidence = number`
- `iou = number`
- `max_det = integer`
- `class_ids = {0, 1, 2}`
- `class_aware = true/false`
- `class_agnostic = true/false`
- `resize_mode = "stretch" | "letterbox"`
- `letterbox_mode = "center" | "top_left"`
- `pad_color = 0x727272`
- `profile = table`
- `tracker = table`

Compatible with CoreML image input and multi-array input. Image-input models such as `yolov8n*.mlpackage` use the image preprocessing path by default.

## Image Input

Public inference methods support:

- File paths
- Raw image bytes
- BASE64 strings
- `image_object`

## Module Functions

- `yolo_coreml.supported_tasks()`: returns `{"detect", "seg", "pose", "obb", "track", "classify"}`.
- `yolo_coreml.new(opts)`: creates an instance.
- `yolo_coreml.create(opts)` / `open(opts)`: aliases of `new`.
- `yolo_coreml.compile_model_cached(model_path)`: compiles `.mlpackage` / `.mlmodel` to `.mlmodelc` in the same directory; returns directly when the cache is fresh.
- `yolo_coreml.clear_compiled_model_cache(model_path)`: deletes the corresponding `.mlmodelc` cache and returns the number of cleaned items.
- `yolo_coreml.tracker(opts)`: creates a tracker.

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
local yolo_coreml = require("yolo_coreml")

local compiled = assert(yolo_coreml.compile_model_cached(
    XXT_HOME_PATH.."/models/yolo_coreml/yolo11n.mlpackage"
))

local model = assert(yolo_coreml.new({
    compiled_model_path = compiled,
    class_names = "coco80",
}))

local detections = assert(model:detect(XXT_HOME_PATH.."/res/bus.jpg"))
for i = 1, #detections do
    local det = detections[i]
    sys.log(det.label, det.score, det.x1, det.y1, det.x2, det.y2)
end

model:close()
```

## Notes

- `compiled_model_path` must be an existing `.mlmodelc`.
- When using `compile_model_cached`, pass `.mlpackage` or `.mlmodel`, not `.mlmodelc`.
- Call `close()` after using an instance to release the CoreML request, decoder, and tracker.
