# coreml.module

Purpose: CoreML module overview

## Usage
```lua
-- coreml is a built-in global module and does not need require.
local req = assert(coreml.session(XXT_HOME_PATH.."/models/demo.mlmodelc"))
```

## Main Capabilities
- Generic model inference: `coreml.new_model_request()` / `coreml.session()`
- Vision image inference: `coreml.new_vision_request()`
- `MLMultiArray` creation, conversion, tensor operations, and post-processing: see `coreml.multi.array.module.md`
- Text tokenization: see `coreml.tokenizer.module.md`
- Post-processing helpers for detection, OBB, mask, keypoint, tracker, CTC, logits sampling, and more

## Common Entry Points
```lua
compiled_path = coreml.compile_model(model_path)
req = coreml.new_model_request(compiled_path)
vision_req = coreml.new_vision_request(compiled_path)

tensor = coreml.tensor({shape = {1, 3, 224, 224}, data_type = "float32"})
tensor = coreml.tensor_from_table(data, {shape = {1, 3}, data_type = "float32"})
tensor, meta = coreml.tensor_from_image(img, opts)

tokenizer = coreml.new_text_tokenizer(opts)
```

## Aliases
- `coreml.session(...)` = `coreml.new_model_request(...)`
- `coreml.tensor(...)` = `coreml.new_multi_array(...)`
- `coreml.tensor_from_table(...)` = `coreml.multi_array_from_table(...)`
- `coreml.image_to_multi_array(...)` = `coreml.tensor_from_image(...)`
- `coreml.multi_array_from_quad(...)` = `coreml.tensor_from_quad(...)`
- `coreml.multi_array_from_quads(...)` = `coreml.tensor_from_quads(...)`
- `coreml.project_masks(...)` = `coreml.proto_masks(...)`

## ONNXRuntime Integration
After executing `require("onnxruntime")`, native-copy bridges are injected into `coreml`:

```lua
local ort = require("onnxruntime")

local ma = assert(coreml.multi_array_from_ort_tensor(ort_tensor, "float32"))
local ort_tensor = assert(ma:to_ort_tensor("int64"))
```

These conversions do not go through Lua tables and are suitable for passing tensors between models.

## Selection Guidance
- Image classification/detection where the input is `image`: prefer `new_vision_request()`.
- Text, embeddings, multiple inputs, multiple outputs, or inputs containing tokens or `MLMultiArray`: use `new_model_request()` / `session()`.
- When preprocessing must be explicitly controlled: first use `tensor_from_image()` to generate an `MLMultiArray`, then pass it to the generic request.
- Use `to_table()` only when debugging output content; keep native `MLMultiArray` for production post-processing.
