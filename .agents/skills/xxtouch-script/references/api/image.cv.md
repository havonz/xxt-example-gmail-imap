# image.cv / cv.mat

`image.cv` is XXTouch's OpenCV-style image processing module. It must be loaded explicitly:

```lua
local cv = require("image.cv")
```

Version requirement: XXTouch later than 20260402 is required.

After loading, it returns the `cv` module table and adds a set of `cv_*` methods to `image_object`.

## Use Cases

- Color space conversion, thresholding, filtering, morphology, contours, template matching, and geometric transforms.
- Use `cv.mat` when an `image_object` needs to be converted into an intermediate matrix for processing.
- For simple screenshots, color search, and basic ImageObject operations, prefer existing `screen` / `image_object` APIs.

## image_object and cv.mat

```lua
local img = assert(image.load_file(XXT_HOME_PATH.."/res/input.png"))

local mat = cv.from_image(img, "gray")
local out = mat:canny(80, 160):to_image()
out:save_to_png_file(XXT_HOME_PATH.."/res/edges.png")
```

Common conversions:

```lua
local mat1 = cv.from_image(img)
local mat2 = cv.from_image(img, "bgr")
local mat3 = img:cv_to_mat("gray")

local img2 = cv.to_image(mat1)
local img3 = mat1:to_image({normalize = true})
```

`cv.from_image(src[, color_mode])` supports common `color_mode` values:

- `"bgra"`
- `"bgr"`
- `"gray"` / `"grey"`
- `"rgb"`
- `"rgba"`

`cv.to_image(src[, opts])` converts `cv.mat` back to `image_object`. `opts.normalize = true` is commonly used to normalize floating-point matrices to `0` to `255`.

## Type Checks

```lua
print(cv.is(img))          -- true
print(cv.type(img))        -- image_object

local mat = cv.from_image(img)
print(cv.mat.is(mat))      -- true
print(cv.type(mat))        -- cv.mat
print(cv.version())        -- OpenCV version
```

Note: `image.type(img)` returns `"image"`, and `cv.type(img)` returns `"image_object"`.

## Return Rules

- Most processing functions return `cv.mat` by default, such as `cv.cvt_color`, `cv.resize`, `cv.blur`, `cv.threshold`, and `cv.canny`.
- Many functions support `opts.return_image = true` to return `image_object` directly.
- Drawing functions usually return `image_object` by default when an `image_object` is passed in, such as `cv.rectangle`, `cv.circle`, `cv.line`, `cv.draw_contours`, and `cv.put_text`.
- `opts.inplace = true` mainly makes sense for `cv.mat`, and not all functions support in-place writeback.

## cv.mat Methods

Shape and type:

```lua
print(mat:type())      -- for example, uint8C4
print(mat:depth())     -- for example, uint8
print(mat:channels())  -- for example, 4

local cols, rows = mat:size()
local shape = mat:shape()
print(shape.rows, shape.cols, shape.channels)
```

`mat:size()` returns values in the order `cols, rows`. `mat:shape()` returns `{rows, cols, channels}` and includes fields with the same names.

Common methods:

- `clone()`
- `astype(type_name)`
- `to_image([opts])`
- `cvt_color(code[, opts])`
- `resize(width, height[, opts])`
- `threshold(thresh, maxval, type[, opts])`
- `canny(threshold1, threshold2[, opts])`
- `find_contours([mode][, method][, opts])`
- `match_template(templ[, method][, mask])`
- `min_max_loc([mask])`
- `rectangle(...)` / `circle(...)` / `line(...)` / `draw_contours(...)` / `put_text(...)`

Currently, `cv.mat` also exports: `split`, `extract_channel`, `insert_channel`, `rotate`, `flip`, `transpose`, `warp_perspective`, `warp_affine`, `repeat`, `pyr_down`, `pyr_up`, `get_rect_sub_pix`, `copy_make_border`, `absdiff`, `add`, `subtract`, `multiply`, `divide`, `compare`, `reduce`, `sum`, `norm`, `copy_to`, `set_to`, `adaptive_threshold`, `blur`, `gaussian_blur`, `median_blur`, `bilateral_filter`, `equalize_hist`, `clahe`, `normalize`, `mean`, `mean_std_dev`, `count_non_zero`, `in_range`, `add_weighted`, `bitwise_and`, `bitwise_or`, `bitwise_xor`, `bitwise_not`, `sobel`, `scharr`, `laplacian`, `convert_scale_abs`, `erode`, `dilate`, `morphology_ex`, `remap`, `flood_fill`, `phase_correlate`, `magnitude`, `phase`, `cart_to_polar`, `polar_to_cart`, `connected_components_with_stats`, `find_non_zero`, `moments`, `hu_moments`, `calc_hist`, `compare_hist`, `hough_lines_p`, `hough_circles`, `distance_transform`, `good_features_to_track`, `polylines`, `fill_poly`.

## Color Spaces and Channels

```lua
local gray = cv.cvt_color(img, "bgra2gray")
local hsv = cv.cvt_color(img, "bgr2hsv")
local rgba = cv.cvt_color(hsv, "hsv2rgba")
```

Common conversion codes:

- `bgra2gray`
- `bgr2gray`
- `gray2bgr`
- `gray2bgra`
- `bgr2rgb`
- `bgra2rgba`
- `bgr2hsv` / `hsv2bgr`
- `bgr2lab` / `lab2bgr`
- `bgr2ycrcb` / `ycrcb2bgr`

Channel operations:

```lua
local bgr = cv.from_image(img, "bgr")
local channels = cv.split(bgr)
local merged = cv.merge(channels)
local alpha = cv.extract_channel(cv.from_image(img), 3)
```

## Size and Geometry

```lua
local small = cv.resize(img, 540, 960)
local half = cv.resize(img, 0, 0, {fx = 0.5, fy = 0.5})
local rotated = cv.rotate(small, "90clockwise")
local flipped = cv.flip(rotated, "horizontal")
```

Common interpolation modes: `nearest`, `linear` / `bilinear`, `cubic`, `area`, `lanczos4`.

Perspective and affine:

```lua
local M = cv.get_perspective_transform(src_points, dst_points)
local fixed = cv.warp_perspective(img, M, 300, 200)
```

Common border types: `constant`, `replicate`, `reflect`, `wrap`, `reflect101`, `transparent`.

## Thresholding, Filtering, and Morphology

```lua
local gray = cv.from_image(img, "gray")
local binary, used = cv.threshold(gray, 0, 255, "binary|otsu", {
    return_threshold = true,
})

local kernel = cv.get_structuring_element("rect", 3, 3)
local opened = cv.morphology_ex(binary, "open", kernel)
```

`cv.threshold` types support `binary`, `binary_inv`, `trunc`, `tozero`, and `tozero_inv`. Combinations such as `binary|otsu` and `binary|triangle` are also supported.

Common functions:

- `cv.blur(src, ksize[, opts])`
- `cv.gaussian_blur(src, kx, ky[, sigma_x][, sigma_y][, opts])`
- `cv.median_blur(src, ksize[, opts])`
- `cv.bilateral_filter(src, d, sigma_color, sigma_space)`
- `cv.normalize(src[, opts])`
- `cv.in_range(src, lower, upper)`
- `cv.canny(src, threshold1, threshold2)`
- `cv.erode(src, kernel[, iterations][, opts])`
- `cv.dilate(src, kernel[, iterations][, opts])`
- `cv.morphology_ex(src, op, kernel[, iterations][, opts])`

Morphology `op` supports `open`, `close`, `gradient`, `tophat`, and `blackhat`.

## Contours and Template Matching

```lua
local contours, hierarchy = cv.find_contours(binary, "external", "simple", {
    return_hierarchy = true,
})

local marked = cv.draw_contours(img, contours, 0x00FF00, 2)
```

Common `find_contours` `mode` values: `external`, `list`, `ccomp`, `tree`. Common `method` values: `none`, `simple`, `tc89l1`, `tc89kcos`.

Template matching:

```lua
local response = cv.match_template(big, small, "ccoeff_normed")
local stat = cv.min_max_loc(response)
print(stat.max_val, stat.max_loc.x, stat.max_loc.y)
```

`cv.min_max_loc` returns `min_val`, `max_val`, `min_loc = {x, y}`, and `max_loc = {x, y}`.

## Drawing

```lua
local out = cv.rectangle(img, 100, 100, 300, 260, 0x00FF00, 2)
out = cv.put_text(out, "OK", {x = 20, y = 40}, "simplex", 1.0, 0x00FF00, 2)
```

The `org` parameter of `put_text` is the baseline position of the lower-left corner of the text, not the upper-left corner.

## image_object-centered cv APIs

After loading `image.cv`, these APIs or their corresponding `image_object:cv_*` methods can be used directly:

- `cv.find_image_old(big, templ[, opts])`
- `cv.find_image(big, templ[, opts])`
- `cv.binaryzation(img[, threshold])`
- `cv.binaryzation_copy(img[, threshold])`
- `cv.binarization(img[, threshold])`
- `cv.binarization_copy(img[, threshold])`
- `cv.binarize(img[, threshold])`
- `cv.binarize_copy(img[, threshold])`
- `cv.resize_copy(img, width, height)`
- `cv.stitch_long(images[, opts])`
- `cv.find_polygon(img, opts)`
- `cv.compare_image(img1, img2[, opts])`
- `cv.find_shapes(img, shape_image_or_contours[, opts])`
- `cv.to_shapes(img[, opts])`
- `cv.detect_templates(img, template_images_opts_table)`

```lua
local x1, y1, sim1 = cv.find_image(big, templ, {confidence_threshold = 92})
local x2, y2, sim2 = big:cv_find_image(templ, {confidence_threshold = 92})
```
