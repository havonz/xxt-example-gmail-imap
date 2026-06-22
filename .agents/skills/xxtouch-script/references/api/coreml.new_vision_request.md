# coreml.new_vision_request

Purpose: CoreML vision predictor

## Signature
```lua
vision_request_object, error_message = coreml.new_vision_request(compiled_model_path)

vision_request_object, error_message = coreml.new_vision_request({
    compiled_model_path = compiled_model_path,
    uses_cpu_only = whether_to_use_cpu_only,
    compute_units = compute_unit_configuration,
    image_crop_and_scale_option = crop_and_scale_mode,
})
```

## Example
```lua
local compiled_model_path = XXT_HOME_PATH..'/models/yolo11m.mlmodelc'

local request, err = coreml.new_vision_request({
    compiled_model_path = compiled_model_path,
    compute_units = 'all',
    image_crop_and_scale_option = 0,
})
if not request then
    error(err)
end

local results = assert(request:predict(screen.image(), {
    multi_array_output = 'MLMultiArray',
}))
nLog(results)
```

## Parameters
- compiled_model_path
    string, currently supports two model types: image classification and object detection.

- uses_cpu_only
    boolean, optional. Whether inference uses only the CPU by default. Default: `false`.

- compute_units
    string, optional. Takes effect on iOS 12+. Supports the following values:
    - `"all"`
    - `"cpu_only"` or `"cpu"`
    - `"cpu_and_gpu"` or `"gpu"`
    - `"cpu_and_neural_engine"`, `"ane"`, or `"neural_engine"` (iOS 16+)

- image_crop_and_scale_option
    integer, optional. Crop and scale mode for vision inference.

## Returns
- vision_request_object
    vision request object; returns `nil` if creation fails.

- error_message
    string. `nil` on successful creation; on failure, returns the error message.

## Notes
- iOS versions below 13 are not supported.
- This function loads a compiled `.mlmodelc` model and returns a context for image inference.
- Suitable for CoreML vision models that use images as input.
- If the model input itself is a generic `image` / `MLMultiArray` feature, also consider using [coreml.new_model_request](coreml.new_model_request.md).
- In addition to `:predict()` / `:run()`, this object also supports query methods such as `:results()`, `:is_done()`, `:compute_units()`, `:image_crop_and_scale_option()`, and `:class_labels()`.
