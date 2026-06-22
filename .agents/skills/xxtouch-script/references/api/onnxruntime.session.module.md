# onnxruntime.session.module

Purpose: ONNX Runtime session module

Version requirement: XXTouch later than 20260402 is required.

## Signature
```lua
local ort = require("onnxruntime")

session, error_message = ort.session(model_path [, options])
session, error_message = ort.session_from_bytes(model_bytes [, options])
output_table, error_message = session:run(inputs [, output_names [, run_options]])
output_table, error_message = session:run_into(inputs, outputs [, run_options])
output_table, error_message = session:run_with_iobinding(binding [, run_options])
run_options = ort.run_options([options])
```

## Basic Example
```lua
local ort = require("onnxruntime")

local session = assert(ort.session(XXT_HOME_PATH.."/models/demo/model.onnx", {
    providers = {"coreml", "cpu"},
    fallback_to_cpu = true,
    coreml_compute_units = "all",
}))

local x = assert(ort.tensor("float32", {1, 2}, {1.0, 2.0}))
local bias = assert(ort.tensor("float32", {1, 2}, {0.5, -0.5}))

local outputs = assert(session:run({
    x = x,
    bias = bias,
}, {"y"}))

print(outputs.y:to_table()[1])
```

## Runtime Configuration
```lua
assert(ort.configure({
    log_severity_level = 2,
    log_id = "my-runtime",
    use_global_thread_pools = false,
    global_intra_op_num_threads = 0,
    global_inter_op_num_threads = 0,
}))
```

Rules:
- `configure()` must be called before creating any session.
- Calling it after an active session already exists raises an error.
- Supported fields: `log_severity_level`, `log_id`, `use_global_thread_pools`, `global_intra_op_num_threads`, `global_inter_op_num_threads`.

## Create Session
```lua
session, error_message = ort.session(model_path [, options])
session, error_message = ort.session_from_bytes(model_bytes [, options])
```

Common options:
- `providers` or `provider`: a single string or an array of strings. Currently handles `"cpu"` and `"coreml"` natively, and also accepts `CPUExecutionProvider` and `CoreMLExecutionProvider`.
- `fallback_to_cpu`: boolean, default `true`.
- `intra_op_num_threads`
- `inter_op_num_threads`
- `log_id`
- `session_log_severity_level`
- `session_log_verbosity_level`
- `optimized_model_path`
- `profile_file_prefix`
- `free_dimension_overrides`
- `config_entries`
- `graph_optimization_level`: `"disable"`, `"basic"`, `"extended"`, `"all"`
- `execution_mode`: `"sequential"`, `"parallel"`
- `deterministic_compute`
- `disable_per_session_threads`
- `enable_cpu_mem_arena`
- `enable_mem_pattern`
- `custom_op_libraries`

Additional notes:
- `free_dimension_overrides` is an array where each item looks like `{ by = "name"|"denotation", key = "...", value = integer }`.
- `config_entries` must be a table of string keys to string values.
- `custom_op_libraries` can be a single path, an array of paths, a handle returned by `load_custom_op_library()`, or a mixed array.
- When `providers` is not explicitly specified or the list is empty, the CPU provider is added.
- `providers = {"coreml", "cpu"}` means CoreML first, then CPU.
- When `"coreml"` is included and `fallback_to_cpu = true`, it can fall back to CPU after CoreML provider initialization fails.

CoreML provider options:
- `coreml_compute_units`: recommended values are `"all"`, `"cpu_only"`, `"cpu_and_gpu"`, `"cpu_and_neural_engine"`; aliases such as `CPUOnly`, `CPUAndGPU`, `CPUAndNeuralEngine`, and `MLComputeUnits...` are accepted for compatibility.
- `coreml_create_mlprogram`
- `coreml_require_static_input_shapes`
- `coreml_enable_on_subgraph`
- `coreml_flags`
- `coreml_use_cpu_only`
- `coreml_use_cpu_and_gpu`
- `coreml_only_enable_device_with_ane`

Rules:
- `coreml_flags`, `coreml_use_cpu_only`, `coreml_use_cpu_and_gpu`, and `coreml_only_enable_device_with_ane` are compatibility fields for the old style.
- New and old fields can be mixed, but session creation errors if they conflict with each other.
- `coreml_only_enable_device_with_ane` cannot be used together with mutually exclusive configurations such as `coreml_compute_units = "cpu_only"` / `"cpu_and_gpu"`.

## Session Object Methods
Basic information:
- `session:input_names()`
- `session:output_names()`
- `session:overridable_initializer_names()`
- `session:input_count()`
- `session:output_count()`
- `session:overridable_initializer_count()`

Type information:
- `session:input_info(name_or_index)`
- `session:output_info(name_or_index)`
- `session:overridable_initializer_info(name_or_index)`

Common fields in type information:
- `name`
- `onnx_type`
- `is_sparse`
- `data_type`
- `type`
- `has_shape`
- `shape`
- `symbolic_shape`
- `element`
- `key_type`
- `value`

Description:
- tensor / sparse tensor contains `data_type`, `shape`, and `symbolic_shape`.
- sequence / optional contains nested `element`.
- map contains `key_type` and nested `value`.
- `name_or_index` can be a name or a 1-based index.

Memory information:
- `session:memory_info_for_inputs()`
- `session:memory_info_for_outputs()`

Return values can be accessed by order or by name. Each item usually contains `name`, `id`, `mem_type`, `allocator_type`, `device_type`, `device_mem_type`, and `vendor_id`.

Metadata and Lifecycle:
- `session:metadata()`
- `session:close()`
- `session:end_profiling()`
- `session:profiling_start_time_ns()`
- `session:set_ep_dynamic_options(opts)`
- `session:register_custom_op_library(path_or_handle)`

Description:
- `end_profiling()` returns the profiling output file path.
- `set_ep_dynamic_options()` converts table key/value pairs to strings before passing them to ORT.
- `register_custom_op_library()` rebuilds the internal session based on the current session options.
- `path_or_handle` can be a path or a handle returned by `load_custom_op_library()`.

## Run Inference
```lua
output_table, error_message = session:run(inputs [, output_names [, run_options]])
output_table, error_message = session:run_into(inputs, outputs [, run_options])
output_table, error_message = session:run_with_iobinding(binding [, run_options])
```

Input Rules:
- `inputs` can be an ordered array or a dictionary organized by input names.
- Ordered arrays are matched by model input order and can also continue overriding overridable initializers.
- In dictionary form, keys must match input names or overridable initializer names.
- Optional inputs can be omitted, or passed as `onnxruntime.optional(nil, type_info)`.

Output Rules:
- The return value is a table.
- The same output can be accessed by numeric index or by output name: `outputs[1]`, `outputs.logits`.
- If `run_into()` reuses an existing tensor for an output, the corresponding item in the returned table is the original object itself.

## Run Options
```lua
run_options = ort.run_options({
    tag = "session-run",
    log_severity_level = 2,
    log_verbosity_level = 1,
})
```

Fields:
- `tag`
- `log_severity_level`
- `log_verbosity_level`

Object methods:
- `run_options:tag([value])`
- `run_options:log_severity_level([value])`
- `run_options:log_verbosity_level([value])`
- `run_options:terminate()`
- `run_options:reset_terminate()`

## IOBinding
```lua
binding, error_message = session:create_io_binding()
binding:bind_input(name, value)
binding:bind_output(name [, spec_or_tensor])
output_table, error_message = session:run_with_iobinding(binding, run_options)
```

Rules:
- `bind_input()` does not accept empty optional values.
- `bind_output("y")`: binds to CPU memory and retrieves it later with `get_outputs()`.
- `bind_output("y", existing_tensor)`: writes directly into an existing tensor.
- `bind_output("y", {type = "float32", shape = {1, 2}})`: creates and returns an output tensor.
- `bind_output("y", {mode = "device"})`: binds device output.

Other methods:
- `binding:clear_inputs()`
- `binding:clear_outputs()`
- `binding:synchronize_inputs()`
- `binding:synchronize_outputs()`
- `binding:get_outputs()`
