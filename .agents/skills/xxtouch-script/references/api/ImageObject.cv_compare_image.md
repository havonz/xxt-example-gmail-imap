# ImageObject:cv_compare_image

Purpose: cv image comparison

## Signature
```lua
difference_shape_collection, visualization_image = image:cv_compare_image(another_image[, image_comparison_options])
```

## Example
```lua
local img1 = image.load_file(XXT_SCRIPTS_PATH..'/1.png')
local img2 = image.load_file(XXT_SCRIPTS_PATH..'/2.png')

local shapes, visimg = img1:cv_compare_image(img2, {
    should_visualize = true,
    approx_epsilon = 2,
})

nLog(shapes)
dialog():add_image(visimg):show()
```

## Parameters
- another_image
    ImageObject, the comparison image to compare against.

- image_comparison_options
    table

    ```Lua
    {
        should_visualize = false | true,  -- Optional. Whether to output a visualization. Defaults to false.
        approx_epsilon = integer_value,   -- Optional contour approximation perimeter percentage, used to simplify complex contours. Defaults to 2.
    }
    ```

## Returns
- difference_shape_collection
    table, shapes of differences between the two images.

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
Compares this image with another image and returns shape vertex information for the differing regions.
The two images must have the same size.
