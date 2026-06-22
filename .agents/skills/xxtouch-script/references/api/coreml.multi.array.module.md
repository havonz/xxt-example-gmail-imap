# coreml.multi.array.module

Purpose: MLMultiArray tensor module

## Signature
```lua
tensor, error_message = coreml.tensor({shape = shape_array, data_type = data_type})
tensor, error_message = coreml.tensor_from_table(data_table, options)
tensor, metadata = coreml.tensor_from_image(image_object, options)
batch_tensor, metadata_array = coreml.tensor_from_images(image_array, options)
image_object, error_message = coreml.image_from_tensor(tensor, options)

result_tensor = tensor:reshape(shape)
result_tensor = tensor:slice(dim, start, stop [, step])
result_tensor = tensor:softmax([axis])
topk_result = tensor:topk(k [, axis])
```

## Common Examples
```lua
local arr = assert(coreml.tensor({
    shape = {2, 3},
    data_type = "float32",
}))

local filled = assert(coreml.tensor_from_table({
    {1, 2, 3},
    {4, 5, 6},
}, {
    shape = {2, 3},
    data_type = "float32",
}))

local logits = assert(filled:softmax(2))
local topk = assert(logits:topk(2, 2))
print(topk.indices:to_table()[1])
```

Image to tensor:

```lua
local tensor, meta = assert(coreml.tensor_from_image(screen.image(), {
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

## Creation and Conversion
```lua
tensor, error_message = coreml.new_multi_array({
    shape = shape_array,
    data_type = data_type,
})
tensor, error_message = coreml.tensor(options)

tensor, error_message = coreml.multi_array_from_table(data_table, {
    shape = shape_array,
    data_type = data_type,
})
tensor, error_message = coreml.tensor_from_table(data_table, options)
```

Rules:
- `shape` must match the total amount of data, for example `{1, 3, 224, 224}`.
- `data_type` can be `"int32"`, `"float32"`, `"float16"`, or `"double"`; `"float64"` is an alias for `"double"`.
- `coreml.tensor()` is an alias for `coreml.new_multi_array()`.
- `coreml.tensor_from_table()` is an alias for `coreml.multi_array_from_table()`.

## Image and OpenCV Conversion
```lua
tensor, metadata = coreml.tensor_from_image(image_object, options)
batch_tensor, metadata_array = coreml.tensor_from_images({img1, img2}, options)
image_object, error_message = coreml.image_from_tensor(tensor, options)

tensor, error_message = coreml.tensor_from_cv_mat(mat, options)
tensor, error_message = coreml.tensor_from_quad(mat, quad, options)
batch_tensor, error_message = coreml.tensor_from_quads(mat, quads, options)
```

Common `tensor_from_image()` options:
- `width` / `height`
- `layout`: `"nchw"`, `"nhwc"`
- `channel_order`: `"rgb"`, `"bgr"`, `"gray"`, `"grey"`, `"grayscale"`
- `data_type`
- `scale`
- `mean`
- `std`
- `resize_mode`: `"stretch"`, `"letterbox"`, `"center_crop"`
- `letterbox_mode`: `"center"`, `"top_left"`; `"topleft"` is also treated as `"top_left"`
- `pad_color`
- `interpolation`: `"bilinear"`, `"nearest"`
- `alpha_mode`: `"ignore"`, `"white"`, `"black"`, `"premultiply"`
- `crop = {x, y, width, height}`

Common metadata fields:
- `src_width` / `src_height`
- `crop_x` / `crop_y` / `crop_width` / `crop_height`
- `dst_width` / `dst_height`
- `resized_width` / `resized_height`
- `scale_x` / `scale_y` / `ratio`
- `pad_left` / `pad_top` / `pad_right` / `pad_bottom`
- `resize_mode` / `letterbox_mode`
- `offset_x` / `offset_y`

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
- `coreml.image_to_multi_array()` is the old name and is currently an alias for `tensor_from_image()`.
- `coreml.multi_array_from_quad()` / `coreml.multi_array_from_quads()` are aliases for the corresponding `tensor_from_*` functions.

Quadrilateral crop:
- `quad` can be passed directly as four points, or as a table with a `points` field.
- Extra common fields in `opts` for `tensor_from_quad()`: `content_width`, `content_height`, `border_type`.
- `tensor_from_quads()` requires `quads` to be a non-empty array. Each item can override the global `content_width` / `content_height`.
- Batch results are automatically combined into a batch with `stack()` or `concat()` according to rank, suitable for OCR multi-box processing.

## ONNXRuntime Bridge
```lua
local ort = require("onnxruntime")

tensor, error_message = coreml.multi_array_from_ort_tensor(ORT_tensor[, "float32"])
ORT_tensor, error_message = array:to_ort_tensor(["int64"])
```

These APIs do not exist by default; they are injected only after executing `require("onnxruntime")`. Conversion uses native copies and does not go through Lua tables. `string` tensors cannot be converted to `MLMultiArray`.

## Type Checks
```lua
is_tensor = coreml.is_multi_array(value)
is_tensor = coreml.is_tensor(value)
```

`is_tensor()` is an alias for `is_multi_array()`.

## Module-Level Tensor Helpers
Basics:
- `coreml.concat(arrays, axis)`
- `coreml.stack(arrays, axis)`
- `coreml.gather(array, dim, indices)`
- `coreml.take(array, indices[, dim])`
- `coreml.gather_rows(array, indices)`
- `coreml.clamp(array, min, max)`
- `coreml.sigmoid(array)`
- `coreml.exp(array)`
- `coreml.where(condition, x, y)`
- `coreml.matmul(lhs, rhs)`

Rules:
- `take()` defaults to taking values along dimension 1.
- `gather_rows()` is an alias for `take(array, indices, 1)`.
- `where()` supports mixing scalars and `MLMultiArray` and produces results according to broadcasting rules.
- `matmul()` currently supports rank-1 / rank-2 input combinations.

Detection Geometry:
- `coreml.nms(boxes, scores[, opts])`
- `coreml.box_points(rotated_boxes)`
- `coreml.xywh_to_xyxy(boxes)`
- `coreml.xyxy_to_xywh(boxes)`
- `coreml.rotated_iou(lhs, rhs)`
- `coreml.rotated_nms(boxes, scores[, opts])`

Rules:
- `boxes` for `nms()` is `[N, 4]`, and `scores` is `[N]` or `[N, C]`.
- `boxes` for `rotated_nms()` is `[N, 5]`; `scores` currently uses a Lua number array.
- `nms()` / `rotated_nms()` returns an `MLMultiArray` containing 1-based indices.

Decoding and Records:
- `coreml.create_decoder(schema)`
- `coreml.decode_yolo(output[, opts])`
- `coreml.decode_yolo_obb(output[, opts])`
- `coreml.decode_matrix_candidates(output, schema[, opts])`
- `coreml.decode_dense_detection(output, opts)`
- `coreml.records_from_boxes(boxes, scores, class_ids[, keep_indices])`
- `coreml.obb_records_from_rows(rows, scores, class_ids[, angles[, keep_indices[, opts]]])`
- `coreml.points_to_records(points[, opts])`

Rules:
- `create_decoder()` returns an object supporting `:decode()`, `:task()`, and `:schema()`.
- `decode_dense_detection()` returns `{ boxes, scores, labels }`; for batch input, it returns an array of batch results.
- `decode_dense_detection()` requires `opts.strides` to be a non-empty positive integer array, and also requires `decode_width` and `decode_height`.
- `decode_dense_detection()` currently only supports `box_encoding = "grid_center_log_wh"`.

Mask, Keypoints, and Tracking:
- `coreml.threshold_masks(masks, threshold)`
- `coreml.crop_masks_by_boxes(masks, boxes)`
- `coreml.resize_masks(masks, width, height[, opts])`
- `coreml.mask_iou(lhs_mask, rhs_mask[, opts])`
- `coreml.mask_to_polygon(mask[, opts])`
- `coreml.proto_masks(proto, coeffs, boxes, image_width, image_height[, opts])`
- `coreml.project_masks(proto, coeffs, boxes, image_width, image_height[, opts])`
- `coreml.db_postprocess(score_map[, opts])`
- `coreml.tracker([opts])`
- `coreml.reshape_keypoints(points[, keypoint_count[, keypoint_dim|opts]])`
- `coreml.scale_boxes(boxes, transform)`
- `coreml.clip_boxes(boxes, clip_width, clip_height)`
- `coreml.scale_points(points, transform[, opts])`
- `coreml.scale_keypoints(points, transform[, opts])`
- `coreml.clip_keypoints(points, clip_width, clip_height[, opts])`
- `coreml.ctc_greedy_decode(logits[, opts])`
- `coreml.sample_logits(logits[, opts])`

Rules:
- `project_masks()` is an alias for `proto_masks()`.
- `mask_iou()` can pass `compare_size = true`, or explicitly pass `width` / `height` to align sizes.
- `db_postprocess()` input supports `[H, W]`, `[C, H, W]`, or `[N, C, H, W]`; returned items contain `score`, `points`, and `box`.
- `tracker()` returns an object supporting `:update()`, `:reset()`, `:state()`, and `:close()`.
- `ctc_greedy_decode()` input supports `[T, C]` or `[N, T, C]`, and always returns `indices`; `text` is available only when `charset` is passed.
- `sample_logits()` supports `argmax`, `temperature`, `top_k`, `top_p`, `min_p`, and `seed`; 1D input returns a single 1-based index, and batch input returns an index tensor.

Tracker Object Methods:
- `tracker:update(detections[, timestamp])`
- `tracker:reset()`
- `tracker:state()`
- `tracker:close()`

## Basic Object Methods
Queries:
- `array:shape()`
- `array:data_type()`
- `array:count()`
- `array:strides()`
- `array:to_table()`
- `array:to_cv_mat([opts])`

Shape and Indexing:
- `array:astype(data_type)`
- `array:clone()`
- `array:reshape(shape)`
- `array:transpose(axes)`
- `array:slice(dim, start, stop[, step])`
- `array:select(dim, index)`
- `array:squeeze([dim])`
- `array:unsqueeze(dim)`
- `array:flatten([start_dim[, end_dim]])`

Rules:
- `reshape()`, `transpose()`, `squeeze()`, `unsqueeze()`, and `flatten()` return views by default and do not copy underlying data.
- `reshape()` / `flatten()` errors on non-contiguous layouts; call `clone()` first if needed.
- `slice()` and `select()` return new contiguous tensors, not views.
- `slice()` / `select()` / `gather()` / `take()` all use 1-based index semantics.

Numeric:
- `array:gather(dim, indices)`
- `array:take(indices[, dim])`
- `array:l2_norm()`
- `array:dot(other)`
- `array:max([axis])`
- `array:min([axis])`
- `array:add(other)`
- `array:sub(other)`
- `array:mul(other)`
- `array:div(other)`
- `array:clamp(min, max)`
- `array:sigmoid()`
- `array:exp()`
- `array:matmul(other)`
- `array:scale(number)`

Reduction and Sorting:
- `array:sum([axis])`
- `array:mean([axis])`
- `array:softmax([axis])`
- `array:normalize([axis])`
- `array:argmax([axis])`
- `array:topk(k[, axis])`
- `array:sort([axis[, descending]])`

Rules:
- `add/sub/mul/div` supports scalars and limited broadcasting.
- `sigmoid()`, `exp()`, and `matmul()` results are promoted to floating-point output.
- `argmax()` without an axis returns the 1-based linear index of the maximum value in the entire array.
- `argmax(axis)` returns an `MLMultiArray` containing indices.
- `topk()` returns `{ values = tensor, indices = tensor }`.
- `sort()` returns a new sorted `MLMultiArray` and does not additionally return an index table.

Geometry Object Methods:
- `array:clip_boxes(clip_width, clip_height)`
- `array:xywh_to_xyxy()`
- `array:xyxy_to_xywh()`
- `array:reshape_keypoints([keypoint_count[, keypoint_dim|opts]])`
- `array:scale_points(transform[, opts])`
- `array:clip_keypoints(clip_width, clip_height[, opts])`

These methods share implementations with module functions of the same names; the current array is simply used as the first argument.

## Usage Guidance
- The new generic CoreML inference treats `MLMultiArray` as a first-class data type by default. Do not call `to_table()` too early.
- Keep batch operations on tensor objects when possible. Convert to Lua tables only for debugging, small-data output, or compatibility with old code.
- Configure image preprocessing rules explicitly through `tensor_from_image()` to avoid hard-coding model preprocessing in post-processing.
- Explicitly call `clone()` when an independent copy or contiguous layout is needed.
