# ImageObject:cv_find_shapes

Purpose: cv contour search

## Signature
```lua
found_shape_info, visualization_image = image:cv_find_shapes(shape_collection[, shape_search_options])
```

## Example
```lua
local function make_triangle(side_len)
    local h = math.floor(math.sqrt(3) / 2 * side_len)
    return {
        {x = 1, y = h},
        {x = side_len, y = h},
        {x = side_len // 2, y = 1},
    }
end

local function make_rectangle(side_len)
    return {
        {x = 1, y = 1},
        {x = 1, y = side_len},
        {x = side_len, y = side_len},
        {x = side_len, y = 1},
    }
end

local info, visimg = screen.image():cv_find_shapes({make_triangle(45), make_rectangle(40)}, {
    min_area = 2000,
    max_area = 20000,
    diff_threshold = 0.005,
    approx_epsilon = 1,
    closed = true,
    should_visualize = true,
})

nLog(info[1])
nLog(info[2])
dialog():add_image(visimg):show()
```

## Parameters
- shape_collection
    table, vertex information for one or more shapes to search for.

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

  - shape_search_options
    table, optional contour matching options.

    ```Lua
    {
        should_visualize = false | true,  -- Optional. Whether to output a visualization. Defaults to false.
        closed = false | true,            -- Optional. Whether the shape is closed. Defaults to false.
        min_area = number_value,          -- Optional minimum area. Defaults to -1, meaning no limit.
        max_area = number_value,          -- Optional maximum area. Defaults to -1, meaning no limit.
        blur_size = integer_value,        -- Optional blur kernel size in pixels. Must be a positive odd number. Defaults to 3.
        canny_threshold1 = 100,           -- Optional minimum edge threshold. Defaults to 100.
        canny_threshold2 = 200,           -- Optional maximum edge threshold. Defaults to 200.
        diff_threshold = number_value,    -- Optional difference threshold; smaller means more similar. Defaults to 0.001.
        approx_epsilon = integer_value,   -- Optional contour approximation perimeter percentage, used to simplify complex contours. Defaults to 2.
    }
    ```

## Returns
- found_shape_info
    table

    ```Lua
    {
        { -- list of shapes matching shape 1
            { -- first shape matching shape 1
                diff_score = number_value, -- Difference value between this shape and shape 1; smaller means more similar.
                { -- vertex 1 of the first shape matching shape 1
                    ["y"] = number_value,
                    ["x"] = number_value,
                },
                { -- vertex 2 of the first shape matching shape 1
                    ["y"] = number_value,
                    ["x"] = number_value,
                },
                ...
            },
            { -- second shape matching shape 1
                diff_score = number_value, -- Difference value between this shape and shape 1; smaller means more similar.
                { -- vertex 1 of the second shape matching shape 1
                    ["y"] = number_value,
                    ["x"] = number_value,
                },
                { -- vertex 2 of the second shape matching shape 1
                    ["y"] = number_value,
                    ["x"] = number_value,
                },
                ...
            },
            ...
        },
        { -- list of shapes matching shape 2
            { -- first shape matching shape 2
                diff_score = number_value, -- Difference value between this shape and shape 2; smaller means more similar.
                { -- vertex 1 of the first shape matching shape 2
                    ["y"] = number_value,
                    ["x"] = number_value,
                },
                { -- vertex 2 of the first shape matching shape 2
                    ["y"] = number_value,
                    ["x"] = number_value,
                },
                ...
            },
            ...
        },
        ...
    }
    ```

## Notes
Finds one or more shapes in an image.
Standard regular shapes can be generated with functions.
