# coreml.compile_model

Purpose: Compile CoreML model locally

## Signature
```lua
compiled_model_path, error_message = coreml.compile_model(model_file_path)
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
```

## Parameters
- model_file_path
    string, path to the model to compile. iOS 15 and later support the `.mlpackage` format; iOS 13 and 14 only support the legacy `.mlmodel` format.

    Notes for converting YOLO11 to CoreML

    ```bash
    # This assumes you already have a Python 3.10 environment. Create one yourself if not.
    # This has only been tested with Python 3.10; later versions are unverified.
    # Install ultralytics first. Skip this step if it is already installed.
    pip install ultralytics

    # On iOS 13 or iOS 14, specify format=mlmodel to convert to the legacy mlmodel format.
    yolo export format=mlmodel nms=True model=best.pt

    # On iOS 15 and later, specify format=coreml to convert to an mlpackage model.
    yolo export format=coreml nms=True model=best.pt

    # Use nms=True when relying on XXTouch's built-in object-detection result shape.
    # If you plan to do post-processing yourself on the XXTouch side with
    # coreml.nms / coreml.rotated_nms, you can omit nms=True.
    ```

## Returns
- compiled_model_path
    string | nil. On success, returns the compiled model path. On failure, returns `nil`.

- error_message
    string | nil. On success, returns `nil`; on failure, returns the error message.

## Notes
- iOS versions below 13 are not supported.
- This function compiles a `.mlpackage` or `.mlmodel` model into the `.mlmodelc` format that can be loaded directly on the device.
- `.mlmodelc` files compiled on different device models or system versions may not be interchangeable.

## Training Notes

- For YOLO11 training, use an Ultralytics-supported Python environment. Python 3.10 is the most conservative choice for compatibility with the documented toolchain.
- On NVIDIA machines, install a CUDA-capable PyTorch build that matches the local CUDA Toolkit, then train with a CUDA device such as `device=0`.
- On macOS with Apple Silicon or supported Metal acceleration, train with `device=mps`.
- After training, export to CoreML with `format=mlmodel` for iOS 13/14, or `format=coreml` for iOS 15 and later.
