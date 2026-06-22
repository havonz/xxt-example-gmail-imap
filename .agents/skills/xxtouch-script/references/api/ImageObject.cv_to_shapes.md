# ImageObject:cv_to_shapes

Purpose: cv convert to contours

## Signature
```lua
shape_collection, visualization_image = image:cv_to_shapes([contour_matching_options])
```

## Example
```lua
local img = image.load_file(XXT_SCRIPTS_PATH..'/1.png')
local shapes, visimg = img:cv_to_shapes({
    blur_size = 3,
    approx_epsilon = 2,
    closed = true,
    should_visualize = true,
})

nLog(shapes)
dialog():add_image(visimg):show()
```

## Parameters
- contour_matching_options
    optional table.

    ```Lua
    {
        should_visualize = false | true,  -- Optional. Whether to output a visualization. Defaults to false.
        closed = false | true,            -- Optional. Whether the shape is closed. Defaults to false.
        blur_size = integer_value,        -- Optional blur kernel size in pixels. Must be a positive odd number. Defaults to 3.
        canny_threshold1 = 100,           -- Optional minimum edge threshold. Defaults to 100.
        canny_threshold2 = 200,           -- Optional maximum edge threshold. Defaults to 200.
        approx_epsilon = integer_value,   -- Optional contour approximation perimeter percentage, used to simplify complex contours. Defaults to 2.
    }
    ```

## Returns
- shape_collection
    table, vertex information for shapes in the image.

    ```Lua
    {
        { -- shape 1
            { -- shape 1 vertex 1
                ["y"] = number_value,
                ["x"] = number_value,
            },
            { -- shape 1 vertex 2
                ["y"] = number_value,
                ["x"] = number_value,
            },
            ...
        },
        { -- shape 2
            { -- shape 2 vertex 1
                ["y"] = number_value,
                ["x"] = number_value,
            },
            { -- shape 2 vertex 2
                ["y"] = number_value,
                ["x"] = number_value,
            },
            ...
        },
        ...
    }
    ```

  - visualization_image
    ImageObject, when `options.should_visualize` is `true`, this return value is the visualization result as an ImageObject.

## Notes
Converts contours in the image into shape vertex information.
Images to be converted into shapes should not be too complex; closed shapes with clear contours are best.
