# ImageObject:cv_detect_templates

Purpose: cv multi-template detection

## Signature
```lua
result_collection, visualization_image = image:cv_detect_templates(small_image_template_collection_and_options)
```

## Example
```lua
local img1 = image.load_file(XXT_SCRIPTS_PATH..'/template1.png')
local img2 = image.load_file(XXT_SCRIPTS_PATH..'/template2.png')

local results, visimg = screen.image():cv_detect_templates({
    img1, img2;
    score_thresh = 90,
    detector = 1, -- SIFT; 0 is ORB, 2 is SURF.
    should_visualize = true,
})

nLog(results)
dialog():add_image(visimg):show()
```

## Parameters
- small_image_template_collection_and_options
    optional table. Each sequential element in the table is an ImageObject, and named fields are options.

    ```Lua
    {
        should_visualize = false | true,  -- Optional field. Whether to output a visualization. Defaults to false.
        detector = 0 | 1 | 2,             -- Optional field. Feature detector: 0: ORB, 1: SIFT, 2: SURF. Defaults to 0: ORB.
        score_thresh = number_value,      -- Optional field. Feature point matching score threshold in percent. Defaults to 90.
    }
    ```

## Returns
- result_collection
    table, information collection for template features detected in the image.

    ```Lua
    {
        { -- result 1
            { -- result 1 vertex 1
                ["y"] = number_value,
                ["x"] = number_value,
            },
            { -- result 1 vertex 2
                ["y"] = number_value,
                ["x"] = number_value,
            },
            { -- result 1 vertex 3
                ["y"] = number_value,
                ["x"] = number_value,
            },
            { -- result 1 vertex 4
                ["y"] = number_value,
                ["x"] = number_value,
            },
            confidence = number_value,  -- Combined confidence of all feature points in result 1.
            angle = number_value,       -- Rotation angle.
            index = number_value,       -- Index of the matched template in the small image template collection.
        },
        { -- result 2
            { -- result 2 vertex 1
                ["y"] = number_value,
                ["x"] = number_value,
            },
            { -- result 2 vertex 2
                ["y"] = number_value,
                ["x"] = number_value,
            },
            { -- result 2 vertex 3
                ["y"] = number_value,
                ["x"] = number_value,
            },
            { -- result 2 vertex 4
                ["y"] = number_value,
                ["x"] = number_value,
            },
            confidence = number_value,  -- Combined confidence of all feature points in result 2.
            angle = number_value,       -- Rotation angle.
            index = number_value,       -- Index of the matched template in the small image template collection.
        },
        ...
    }
    ```

## Notes
Detects image features from a collection of small image templates in an image. This can be used for feature detection after deformation or rotation.
Each small image template only matches the best result whose score exceeds `score_thresh`.
`score_thresh` is used to filter feature points; `confidence` in the return value is the combined confidence of all feature points in the template.
