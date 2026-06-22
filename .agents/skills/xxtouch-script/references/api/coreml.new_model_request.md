# coreml.new_model_request

Purpose: CoreML generic predictor

## Signature
```lua
model_request_object, error_message = coreml.new_model_request(compiled_model_path)

model_request_object, error_message = coreml.new_model_request({
    compiled_model_path = compiled_model_path,
    uses_cpu_only = whether_to_use_cpu_only,
    compute_units = compute_unit_configuration,
})

model_request_object, error_message = coreml.session(...)
is_model_request = coreml.is_model_request(value)
is_model_request = coreml.is_session(value)
```

## Example
```lua
local compiled_model_path = XXT_HOME_PATH.."/models/demo_text.mlmodelc"

local req, err = coreml.new_model_request({
    compiled_model_path = compiled_model_path,
    uses_cpu_only = false,
    compute_units = "all",
})
if not req then
    error(err)
end

local out = assert(req:predict({
    input_ids = ids,
}))

print(req:input_names())
print(req:output_names())
print(out[1])
```

## Parameters
- `compiled_model_path`
    string, path to the compiled `.mlmodelc` model directory.

- `uses_cpu_only`
    boolean, optional. Whether inference uses only the CPU by default. Default: `false`.

- `compute_units`
    string, optional. Takes effect on iOS 12+. Supports the following values:
    - `"all"`
    - `"cpu_only"` or `"cpu"`
    - `"cpu_and_gpu"` or `"gpu"`
    - `"cpu_and_neural_engine"`, `"ane"`, or `"neural_engine"` (iOS 16+)

    When `uses_cpu_only = true`, CPUOnly configuration is forcibly preferred.

## Returns
- model_request_object
    model request object; returns `nil` if creation fails.

- error_message
    string. Returns `nil` on successful creation; on failure, returns the error message.

## Notes
- `coreml.session(...)` is an alias for `coreml.new_model_request(...)`.
- `coreml.is_session()` and `coreml.is_model_request()` are synonymous APIs, suitable for argument validation in general wrappers.
- Basic capabilities support iOS 11+.
- `compute_units` related configuration depends on iOS 12+.
- If the model declares an image feature and you want to pass an `image_object` directly to this generic request as input, iOS 13+ is required.
- Inputs must be passed as an input-name mapping table, for example `{ input_ids = ids }`.
- Input values support numbers, strings, booleans, dictionaries, `MLMultiArray`, and `image` objects when the model declares an image feature.
- This object only handles model inference. It does not handle image preprocessing or text tokenization; prepare those steps in Lua.
- The same predictor object can call `predict()` / `run()` repeatedly, so it is suitable for caching and reuse instead of being recreated for every inference.
- If an older device or certain model is unstable on the default backend, set `uses_cpu_only = true` at creation.
