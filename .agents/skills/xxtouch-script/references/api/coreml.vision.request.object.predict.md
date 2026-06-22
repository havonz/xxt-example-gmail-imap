# coreml.vision.request.object:predict

Purpose: CoreML image prediction

## Signature
```lua
results, error_message = vision_request_object:predict(image_to_predict)

submitted, error_message = vision_request_object:predict(image_to_predict, {
    async = whether_async,
    multi_array_output = "table" or "MLMultiArray",
    uses_cpu_only = whether_to_use_cpu_only_for_this_run,
})
```

## Example
```lua
compiled_model_path = XXT_HOME_PATH..'/models/yolo11m.mlmodelc' -- Where the compiled model is stored.

file.remove(compiled_model_path) -- Recompile every time during testing. Comment this out after the model is stable.

if not file.exists(compiled_model_path) then -- Compile one if no compiled model exists yet.
    local tmp_path, err = coreml.compile_model(XXT_HOME_PATH..'/models/yolo11m.mlpackage') -- Compile the model.
    if not tmp_path then
        error(err)
    end
    file.move(tmp_path, compiled_model_path, 'mo') -- Move the compiled model to the specified location.
end

vnrequest, err = coreml.new_vision_request(compiled_model_path) -- Create a predictor from the model.
if not vnrequest then
    error(err)
end

rets = vnrequest:predict(screen.image()) -- Use the predictor to infer the image.
nLog(rets)
```

## Parameters
- image_to_predict
    ImageObject, image argument to run inference on

- async
    boolean, optional. When `true`, submits inference asynchronously. Default: `false`.

- multi_array_output
    string, optional. When `MLMultiArray` feature values are returned, specifies whether to return `"table"` or `"MLMultiArray"`. Default: `"table"`.

- uses_cpu_only
    boolean, optional. Only affects this inference. When `true`, this inference uses only the CPU.

## Returns
- results
    table

    ```lua
    {
        {
            ["y"] = number_value,
            ["x"] = number_value,
            ["w"] = number_value,
            ["h"] = number_value,
            ["confidence"] = number_value(0.0 ~ 100.0),
            ["name"] = string_value,
        },
        ...
    }
    ```

    ```lua
    {
        {
            ["confidence"] = number_value(0.0 ~ 100.0),
            ["name"] = string_value,
        },
        ...
    }
    ```

    ```lua
    {
        ...
    }
    ```

## Notes
- iOS versions below 13 are not supported.
- Uses an image inference context to run inference on an image and return prediction results.
- If the model returns `MLMultiArray` feature values, use `multi_array_output = "MLMultiArray"` to keep native tensor objects for further post-processing.
- `:run()` is an alias for `:predict()`. After asynchronous submission, use `:is_done()` and `:results()` to read results.
- The vision request object also supports methods such as `:metadata()`, `:compute_units()`, `:image_crop_and_scale_option()`, `:class_labels()`, and `:is_vision_request()`.
