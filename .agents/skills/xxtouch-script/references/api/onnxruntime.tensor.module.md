# onnxruntime.tensor.module

Purpose: ONNX Runtime tensor module

Version requirement: XXTouch later than 20260402 is required.

## Signature
```lua
local ort = require("onnxruntime")

tensor, error_message = ort.tensor(type, shape[, data])
tensor, error_message = ort.tensor_from_bytes(type, shape, bytes)
tensor, preprocessing_info = ort.tensor_from_image(image, opts)
batch_tensor, preprocessing_info_array = ort.tensor_from_images(images, opts)
image_object, error_message = ort.image_from_tensor(tensor, opts)

result_tensor = tensor:slice(dim, start, stop[, step])
result_tensor = tensor:softmax([axis])
topk_result = tensor:topk(k[, axis])
lua_table = tensor:to_table()
```

## Example
```lua
local ort = require("onnxruntime")

local tensor = assert(ort.tensor("float32", {2, 3}, {
    1, 9, 3,
    8, 2, 7,
}))

local sliced = assert(tensor:slice(2, 2, 3))
print(sliced:to_table()[1]) -- 9

local topk = assert(tensor:topk(2, 2))
print(topk.values:to_table()[1])  -- 9
print(topk.indices:to_table()[1]) -- 2
```

Image to tensor:

```lua
local x, meta = assert(ort.tensor_from_image(screen.image(), {
    width = 224,
    height = 224,
    layout = "nchw",
    channel_order = "rgb",
    data_type = "float32",
    scale = 1 / 255,
    mean = {0.485, 0.456, 0.406},
    std = {0.229, 0.224, 0.225},
    resize_mode = "letterbox",
}))
```

## Creation
```lua
tensor, error_message = ort.tensor(type, shape[, data])
tensor, error_message = ort.tensor_from_bytes(type, shape, bytes)
```

Rules:
- `type` is the element type name.
- `shape` is the shape array.
- `data` can be omitted; when omitted, creates an empty tensor.
- Numeric tensors can be passed a scalar, meaning the whole tensor is filled with the same value.
- `string` tensors can be passed a single string, meaning the whole tensor is filled with the same string.
- `tensor_from_bytes()` only supports numeric types and `bool`; byte length must exactly match `shape` and `type`.

## Image and OpenCV Conversion
```lua
tensor, error_message = ort.tensor_from_cv_mat(mat, opts)
tensor, error_message = ort.tensor_from_quad(mat, quad, opts)
batch_tensor, error_message = ort.tensor_from_quads(mat, quads, opts)
tensor, preprocessing_info = ort.tensor_from_image(image, opts)
batch_tensor, preprocessing_info_array = ort.tensor_from_images({img1, img2}, opts)
image_object, error_message = ort.image_from_tensor(tensor, opts)
```

Common `tensor_from_image()` options:
- `width` / `height`
- `layout`: `"nchw"`, `"nhwc"`, `"chw"`, `"hwc"`
- `channel_order`: `"rgb"`, `"bgr"`, `"gray"`, `"grey"`, `"grayscale"`
- `data_type`
- `scale`
- `mean`
- `std`
- `resize_mode`: `"stretch"`, `"letterbox"`, `"center_crop"`
- `letterbox_mode`: supports `"top_left"`; other cases are handled as centered padding
- `pad_color`
- `interpolation`: `"bilinear"`, `"nearest"`
- `alpha_mode`: `"ignore"`, `"white"`, `"black"`, `"premultiply"`
- `crop = {x, y, width, height}`
- `add_batch`

Preprocessing info fields:
- `src_width` / `src_height`
- `crop_x` / `crop_y` / `crop_width` / `crop_height`
- `dst_width` / `dst_height`
- `resized_width` / `resized_height`
- `layout`
- `channel_order`
- `resize_mode`
- `scale_x` / `scale_y` / `ratio`
- `offset_x` / `offset_y`
- `pad_left` / `pad_top` / `pad_right` / `pad_bottom`

Common `image_from_tensor()` options:
- `layout`
- `channel_order`
- `batch_index`: 1-based, default 1
- `scale`
- `mean`
- `std`
- `clamp`
- `value_range`: `"0_255"` or `"0_1"`

Limits:
- `image_from_tensor()` only supports 2D / 3D / 4D tensors, and only channel counts `1` or `3`.
- `tensor_from_cv_mat()` / `tensor_from_quad()` / `tensor_from_quads()` require `require("image.cv")` first.
- `quad` can be passed directly as four points, or as a table with a `points` field.
- Extra common fields in `opts` for `tensor_from_quad()`: `content_width`, `content_height`, `border_type`.
- `tensor_from_quads()` requires `quads` to be a non-empty array. Each item can override the global `content_width` / `content_height`.

## Tensor Object Methods
Basic information:
- `tensor:shape()`
- `tensor:rank()`
- `tensor:size()`
- `tensor:type()`
- `tensor:to_table()`
- `tensor:bytes()`

Rules:
- `to_table()` expands the contents into a Lua table.
- `bytes()` only supports numeric and `bool` tensors.

Read, Write, and Copy:
- `tensor:get(index1[, index2, ...])`
- `tensor:set(index1[, index2, ...], value)`
- `tensor:fill(value_or_table)`
- `tensor:clone()`
- `tensor:copy_from_bytes(raw_bytes)`
- `tensor:to(type)`

Rules:
- `get()` / `set()` use 1-based indexes.
- When `fill()` receives a scalar, it fills the whole tensor; when it receives a table, the number of elements must match exactly.
- `copy_from_bytes()` only supports numeric types and `bool`; byte length must match exactly.
- `tensor:to("string")` currently only supports `string -> string`.

Shape and index:
- `tensor:reshape(shape)`
- `tensor:transpose([axes])`
- `tensor:flatten([start_dim[, end_dim]])`
- `tensor:squeeze([dim])`
- `tensor:unsqueeze(dim)`
- `tensor:slice(dim, start, stop[, step])`
- `tensor:select(dim, index)`
- `tensor:gather(dim, indices)`

Rules:
- `start` and `stop` for `slice()` are both 1-based and include the stop position.
- `step` for `slice()` must be a positive integer.
- `select()` removes the selected dimension.
- `indices` for `gather()` can be a Lua array or a tensor with shape `[N]`; indexes are also 1-based.
- These methods return new tensors.

Numeric Operations:
- `tensor:add(other)`
- `tensor:sub(other)`
- `tensor:mul(other)`
- `tensor:div(other)`
- `tensor:clamp(min, max)`
- `tensor:sigmoid()`
- `tensor:exp()`
- `tensor:matmul(other)`
- `tensor:dot(other)`

Rules:
- `other` can be a scalar or a tensor with the same shape.
- `matmul()` currently supports rank-1 / rank-2 tensor combinations.
- Return values of `sigmoid()` / `exp()` / `matmul()` are promoted to floating-point result types.
- `string` tensors are not supported.

Reduction, Sorting, and Probability:
- `tensor:argmax([axis])`
- `tensor:sum([axis])`
- `tensor:mean([axis])`
- `tensor:max([axis])`
- `tensor:min([axis])`
- `tensor:softmax([axis])`
- `tensor:normalize([axis])`
- `tensor:sort([axis[, descending]])`
- `tensor:topk(k[, axis])`

Rules:
- `argmax()` without an axis returns a single 1-based index.
- `argmax(axis)` returns an `int64` tensor, and indexes are also 1-based.
- `sort()` returns `{ values = tensor, indices = tensor }`.
- `topk()` returns `{ values = tensor, indices = tensor }`.
- Indexes returned by `sort()` / `topk()` are 1-based.

OpenCV:
- `tensor:to_cv_mat([opts])`

```lua
mat, error_message = tensor:to_cv_mat({
    layout = "hwc",
    channel_order = "rgb",
    coreml_data_type = "uint8",
})
```

Requires `require("image.cv")` first. Some tensor types cannot be mapped directly to `cv.mat`; pass `coreml_data_type` explicitly in that case.

## Module-Level Numeric Helpers
- `ort.clamp(tensor, min, max)`
- `ort.sigmoid(tensor)`
- `ort.exp(tensor)`
- `ort.where(condition, x, y)`
- `ort.matmul(lhs, rhs)`
- `ort.concat(tensors[, axis])`
- `ort.stack(tensors[, axis])`

Description:
- `clamp()`, `sigmoid()`, `exp()`, and `matmul()` share implementations with the corresponding `tensor:` methods.
- `where()` supports mixing scalars / booleans / tensors and computes according to broadcasting rules.

## Detection and Post-Processing
NMS:
- `ort.nms(boxes, scores[, opts])`
- `ort.rotated_nms(boxes, scores[, opts])`

`nms()` options:
- `iou_threshold`
- `score_threshold`
- `top_k`
- `class_aware`
- `class_ids`

Rules:
- `nms()` returns an `int64` tensor with 1-based indexes.
- `boxes` for `rotated_nms()` must be `[N, 5]`; `scores` can be a Lua array or an `[N]` / `[N, 1]` tensor.

Geometry:
- `ort.box_points(rotated_boxes)`
- `ort.xywh_to_xyxy(boxes)`
- `ort.xyxy_to_xywh(boxes)`
- `ort.rotated_iou(box1, box2)`

Rules:
- Input shape for `box_points()` can be `[5]`, `[1, 5]`, or `[N, 5]`. A single box returns a Lua point table; multiple boxes return an array of point tables.

Decoding and Records:
- `ort.create_decoder(schema)`
- `ort.decode_yolo(output[, opts])`
- `ort.decode_yolo_obb(output[, opts])`
- `ort.decode_matrix_candidates(output, schema[, opts])`
- `ort.decode_dense_detection(output, opts)`
- `ort.records_from_boxes(boxes, scores, class_ids[, keep_indices])`
- `ort.obb_records_from_rows(rows, scores, class_ids[, angles[, keep_indices[, opts]]])`
- `ort.points_to_records(points[, opts])`

Rules:
- Decoder objects support `:decode(output[, opts])`, `:task()`, and `:schema()`.
- Common return values of `decode_matrix_candidates()`: `boxes`, `scores`, `class_ids`, `keep_indices`, `selected_rows`, `angles`.
- `decode_dense_detection()` returns `boxes`, `scores`, and `labels`.
- `decode_dense_detection()` input supports `[R, C]` or `[N, R, C]`.
- `decode_dense_detection()` requires a non-empty positive integer `opts.strides`, and also requires `decode_width` and `decode_height`.
- `decode_dense_detection()` currently only supports `box_encoding = "grid_center_log_wh"`.
- `records_from_boxes()` outputs Lua records. Common fields: `box`, `score`, `class_id`, `row_index`, `x1`, `y1`, `x2`, `y2`, `width`, `height`, `cx`, `cy`.
- `opts` for `obb_records_from_rows()` supports `x_index`, `y_index`, `width_index`, and `height_index`.
- `points_to_records()` supports `point_count` / `keypoint_count` and `point_dim` / `keypoint_dim`.

Mask:
- `ort.threshold_masks(masks, threshold)`
- `ort.crop_masks_by_boxes(masks, boxes)`
- `ort.resize_masks(masks, width, height[, opts])`
- `ort.mask_iou(lhs_mask, rhs_mask[, opts])`
- `ort.mask_to_polygon(mask[, opts])`
- `ort.proto_masks(proto, coeffs, boxes, image_width, image_height[, opts])`
- `ort.project_masks(proto, coeffs, boxes, image_width, image_height[, opts])`

Rules:
- `threshold_masks()` returns Lua mask tables; each mask contains `width`, `height`, `bits`, `pixel_count`, and `bounds`.
- `resize_masks()` currently only supports `opts.interpolation = "nearest"`.
- `mask_to_polygon()` supports `opts.epsilon` / `opts.approx_epsilon`.
- `proto_masks()` returns a list of Lua mask tables, not a tensor.
- `project_masks()` is an alias for `proto_masks()`.
- `mask_iou()` can pass `compare_size = true`, or explicitly pass `width` / `height`.

Keypoints and Tracking:
- `ort.reshape_keypoints(points[, keypoint_count[, keypoint_dim|opts]])`
- `ort.scale_boxes(boxes, transform)`
- `ort.clip_boxes(boxes, clip_width, clip_height)`
- `ort.scale_points(points, transform[, opts])`
- `ort.scale_keypoints(points, transform[, opts])`
- `ort.clip_keypoints(points, clip_width, clip_height[, opts])`
- `ort.tracker([opts])`

Rules:
- `reshape_keypoints()` supports reshaping between `[N, K*D]` and `[N, K, D]`.
- `scale_points()` defaults to a normal point layout; `scale_keypoints()` defaults to a keypoint layout.
- Common fields in `transform` align with image preprocessing metadata: `scale_x`, `scale_y`, `pad_left`, `pad_top`.
- Tracker objects support `:update(detections[, timestamp])`, `:reset()`, `:state()`, and `:close()`. Common configuration: `iou_threshold`, `max_age`, `min_hits`.

Tracker Object methods:
- `tracker:update(detections[, timestamp])`
- `tracker:reset()`
- `tracker:state()`
- `tracker:close()`

Text and Logits:
- `ort.ctc_greedy_decode(logits[, opts])`
- `ort.sample_logits(logits[, opts])`

Rules:
- `ctc_greedy_decode()` input supports `[T, C]` or `[N, T, C]`.
- `ctc_greedy_decode()` supports `blank_index`, `merge_repeated`, `apply_softmax`, `return_probabilities`, and `charset`.
- `ctc_greedy_decode()` always returns `indices`; `text` is available only when `charset` is passed; `confidence` is available only when `apply_softmax` or `return_probabilities` is enabled; `probabilities` and `probability_confidence` are available only when `return_probabilities` is enabled.
- `sample_logits()` supports `argmax`, `temperature`, `top_k`, `top_p`, `min_p`, and `seed`.
- For 1D logits, `sample_logits()` returns a single 1-based index; for multi-row logits, it returns an `int64` tensor.
