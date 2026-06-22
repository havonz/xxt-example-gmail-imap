# onnxruntime.module

Purpose: ONNX Runtime module overview

Version requirement: XXTouch later than 20260402 is required.

## Usage
```lua
local ort = require("onnxruntime")
```

`onnxruntime` is an on-demand module. After `require("onnxruntime")` succeeds, CoreML bridges are also injected:

```lua
coreml.multi_array_from_ort_tensor(tensor[, data_type])
multi_array:to_ort_tensor([data_type])
```

## Common Flow
```lua
local ort = require("onnxruntime")

local session = assert(ort.session(XXT_HOME_PATH.."/models/model.onnx", {
    providers = {"coreml", "cpu"},
    fallback_to_cpu = true,
    coreml_compute_units = "all",
}))

local input = assert(ort.tensor("float32", {1, 3}, {1, 2, 3}))
local out = assert(session:run({input = input}, {"logits"}))
local logits = out.logits
```

## Module-Level Functions
Runtime:
- `onnxruntime.version()`
- `onnxruntime.providers()`
- `onnxruntime.configure(opts)`

Session:
- `onnxruntime.session(model_path[, opts])`
- `onnxruntime.session_from_bytes(model_bytes[, opts])`
- `onnxruntime.run_options([opts])`
- `onnxruntime.load_custom_op_library(path)`

Tensors and Images:
- `onnxruntime.tensor(type, shape[, data])`
- `onnxruntime.tensor_from_bytes(type, shape, bytes)`
- `onnxruntime.tensor_from_cv_mat(mat[, opts])`
- `onnxruntime.tensor_from_quad(mat, quad[, opts])`
- `onnxruntime.tensor_from_quads(mat, quads[, opts])`
- `onnxruntime.tensor_from_image(image[, opts])`
- `onnxruntime.tensor_from_images(images[, opts])`
- `onnxruntime.image_from_tensor(tensor[, opts])`

Numeric and Concatenation:
- `onnxruntime.clamp(tensor, min, max)`
- `onnxruntime.sigmoid(tensor)`
- `onnxruntime.exp(tensor)`
- `onnxruntime.where(condition, x, y)`
- `onnxruntime.matmul(lhs, rhs)`
- `onnxruntime.concat(tensors[, axis])`
- `onnxruntime.stack(tensors[, axis])`

Detection and Post-Processing:
- `onnxruntime.nms(boxes, scores[, opts])`
- `onnxruntime.box_points(rotated_boxes)`
- `onnxruntime.xywh_to_xyxy(boxes)`
- `onnxruntime.xyxy_to_xywh(boxes)`
- `onnxruntime.rotated_iou(lhs_box, rhs_box)`
- `onnxruntime.rotated_nms(boxes, scores[, opts])`
- `onnxruntime.create_decoder(schema)`
- `onnxruntime.decode_yolo(output[, opts])`
- `onnxruntime.decode_yolo_obb(output[, opts])`
- `onnxruntime.decode_matrix_candidates(output, schema[, opts])`
- `onnxruntime.decode_dense_detection(output, opts)`
- `onnxruntime.records_from_boxes(boxes, scores, class_ids[, keep_indices])`
- `onnxruntime.obb_records_from_rows(rows, scores, class_ids[, angles[, keep_indices[, opts]]])`
- `onnxruntime.points_to_records(points[, opts])`
- `onnxruntime.threshold_masks(masks, threshold)`
- `onnxruntime.crop_masks_by_boxes(masks, boxes)`
- `onnxruntime.resize_masks(masks, width, height[, opts])`
- `onnxruntime.mask_iou(lhs_mask, rhs_mask[, opts])`
- `onnxruntime.mask_to_polygon(mask[, opts])`
- `onnxruntime.proto_masks(proto, coeffs, boxes, image_width, image_height[, opts])`
- `onnxruntime.project_masks(proto, coeffs, boxes, image_width, image_height[, opts])`
- `onnxruntime.db_postprocess(score_map[, opts])`
- `onnxruntime.tracker([opts])`
- `onnxruntime.reshape_keypoints(points[, keypoint_count[, keypoint_dim|opts]])`
- `onnxruntime.scale_boxes(boxes, transform)`
- `onnxruntime.clip_boxes(boxes, clip_width, clip_height)`
- `onnxruntime.scale_points(points, transform[, opts])`
- `onnxruntime.scale_keypoints(points, transform[, opts])`
- `onnxruntime.clip_keypoints(points, clip_width, clip_height[, opts])`
- `onnxruntime.ctc_greedy_decode(logits[, opts])`
- `onnxruntime.sample_logits(logits[, opts])`

Structured Values:
- `onnxruntime.value(value)`
- `onnxruntime.optional(value, type_info)`
- `onnxruntime.sequence(items)`
- `onnxruntime.map(key_type, value_type, pairs)`
- `onnxruntime.sparse_tensor(type, dense_shape, indices, values)`
- `onnxruntime.sparse_tensor_from_dense(tensor)`

## Data Types
Tensor element types supported:
- `"float32"` / `"float"`
- `"float16"`
- `"bfloat16"`
- `"uint8"` / `"uint16"` / `"uint32"` / `"uint64"`
- `"int8"` / `"int16"` / `"int32"` / `"int64"`
- `"double"` / `"float64"`
- `"bool"`
- `"string"`

Limits:
- `tensor_from_bytes()`, `tensor:copy_from_bytes()`, and `tensor:bytes()` only support numeric types and `bool`; `string` is not supported.
- `tensor:to("string")` currently only supports `string -> string`.

## Provider
```lua
local providers = ort.providers()
```

Provider strings handled natively in session options:
- `"cpu"`
- `"coreml"`

Aliases such as `CPUExecutionProvider` and `CoreMLExecutionProvider` are also accepted. When no provider is specified, CPU is added. `providers = {"coreml", "cpu"}` means CoreML is preferred, then CPU.

## Structured Value Rules
- `onnxruntime.value(x)`: returns an ORT value unchanged; treats Lua tables as sequences; wraps scalars as tensors.
- `onnxruntime.optional(nil, type_info)`: represents an empty optional. `type_info` is required and can be a string or a value returned by `session:input_info()`.
- `onnxruntime.map(key_type, value_type, pairs)`: `key_type` only supports `"string"` or `"int64"`.
- `onnxruntime.sparse_tensor(...)`: currently only supports numeric / `bool` sparse tensors, constructed in COO format. `indices` can be a flat array or a coordinate array.
- `onnxruntime.sparse_tensor_from_dense(tensor)`: does not support `string` tensors.

Object methods:
- `value:type()` / `value:has_value()` / `value:get()`
- `sequence:length()` / `sequence:get(i)` / `sequence:items()`
- `map:get(key)` / `map:set(key, value)` / `map:keys()` / `map:pairs()`
- `sparse_tensor:dense_shape()` / `sparse_tensor:values()` / `sparse_tensor:indices()` / `sparse_tensor:format()` / `sparse_tensor:to_dense()`

## Selection Guidance
- General text / embedding / detection ONNX models: `session()` + `tensor()` / tokenizer output.
- Image models: use `tensor_from_image()` and explicitly specify `layout`, `channel_order`, `scale`, `mean`, and `std`.
- OCR quadrilateral crops: call `require("image.cv")` first, then use `tensor_from_quad()` or `tensor_from_quads()`.
- If model output will continue through post-processing, prefer keeping it as a tensor; call `to_table()` only when debugging small data.
