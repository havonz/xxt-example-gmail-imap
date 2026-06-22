# coreml.model.request.object.methods

Purpose: CoreML request object methods

`coreml_model_request_object` is returned by `coreml.new_model_request(...)` / `coreml.session(...)`. It is only responsible for inference, asynchronous results, input/output signatures, and runtime configuration. Text tokenization, image preprocessing, and post-processing should be done in Lua.

## Signature
```lua
result_table, error_message = req:predict(input_mapping_table [, options])
result_table, error_message = req:run(input_mapping_table [, options])
batch_results, error_message = req:predict_batch(input_mapping_table_array [, options])
batch_results, error_message = req:run_batch(input_mapping_table_array [, options])

is_done = req:is_done()
async_results, error_message = req:results([options])

metadata = req:metadata()
name_list = req:input_names()
name_list = req:output_names()
feature_count = req:input_count()
feature_count = req:output_count()
feature_table = req:input_features()
feature_table = req:output_features()
feature_info = req:input_info(name_or_1_based_index)
feature_info = req:output_info(name_or_1_based_index)
label_table = req:class_labels()

is_cpu_only = req:uses_cpu_only()
compute_units = req:compute_units()
req:close()
is_model_request = req:is_model_request()
is_model_request = req:is_session()
```

## Example
```lua
local req = assert(coreml.session(XXT_HOME_PATH.."/models/demo.mlmodelc"))

local out = assert(req:predict({
    input_ids = ids,
}, {
    multi_array_output = "MLMultiArray",
}))

print(out[1])
print(out.text_features)
print(req:output_names())
```

Async:

```lua
assert(req:predict({input_ids = ids}, {
    async = true,
    multi_array_output = "MLMultiArray",
}))

while not req:is_done() do
    sys.msleep(20)
end

local out = assert(req:results())
```

Batch:

```lua
local batch = assert(req:predict_batch({
    {input_ids = ids1},
    {input_ids = ids2},
}, {
    multi_array_output = "MLMultiArray",
}))

print(batch[1].logits)
```

## Inference Parameters
- `inputs`
    Must be a table organized by model input names, for example `{ input_ids = ids, attention_mask = mask }`.

- `opts.async`
    boolean. When `true`, only submits the task and returns `true`; read it later with `is_done()` / `results()`.

- `opts.multi_array_output`
    `"MLMultiArray"` or `"table"`. Controls whether `MLMultiArray` values in outputs are kept as native tensors or converted to Lua tables. Prefer `"MLMultiArray"` in new code.

- `opts.uses_cpu_only`
    boolean, only affects this inference and does not modify the request's default configuration.

## Return Rules
- Synchronous `predict()` / `run()` returns a single-sample result table.
- `predict_batch()` / `run_batch()` returns an array of batch results.
- Results support both numeric indexes and output-name indexes: `out[1]`, `out.logits`.
- The order of `output_names()` is consistent with the numeric index order in the synchronous inference result table.
- If the task is not complete, asynchronous `results()` returns `nil, "not yet"`. If no readable result exists, it returns `nil, "unknown"`.

## Input/Output Signatures
- `input_names()` / `output_names()` returns arrays of names sorted lexicographically.
- `input_features()` / `output_features()` returns feature description tables indexed by name.
- `input_info(name_or_index)` / `output_info(name_or_index)` accepts a name or a 1-based index.
- Common fields in feature info:
    - `name`
    - `type`
    - `optional`
    - `shape`, common only for `multi_array`
    - `data_type`, common only for `multi_array`

## Runtime Configuration
- `metadata()` returns model metadata.
- `uses_cpu_only()` returns the default CPUOnly configuration recorded at creation.
- `compute_units()` returns the lowercase string recorded at creation. If `uses_cpu_only = true` was used at creation, returns `"cpu_only"`.
- Common `compute_units` values: `"all"`, `"cpu_only"`, `"cpu"`, `"cpu_and_gpu"`, `"gpu"`, `"cpu_and_neural_engine"`, `"ane"`, `"neural_engine"`.

## Notes
- `predict_batch()` / `run_batch()` depends on the system's batch inference capability.
- `class_labels()` reads the category labels declared by the model.
- Do not continue calling other methods after `close()`.
- For the new generic predictor, keep output tensors as `MLMultiArray` and call `to_table()` only after post-processing or during debugging.
