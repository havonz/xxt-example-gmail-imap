# screen.find_color

Purpose: Multi-point similarity color search

## Signature
```lua
x, y = screen.find_color({
    [find_all = whether_to_search_multiple_results,]
    [max_results = maximum_result_count,]
    [max_miss = maximum_allowed_misses,]
    [csim_algorithm = color_similarity_algorithm,]
    {anchor_x, anchor_y, anchor_color[, anchor_similarity]},
    {offset_x*, offset_y*, offset_color*[, offset_similarity*]},
    {offset_x*, offset_y*, offset_color*[, offset_similarity*]},
    ...
} [, global_similarity, left, top, right, bottom ])
```

## Example
```lua
local x, y = screen.find_color({
    {0, 0, 0xec1c23},
    {12, -3, 0xffffff, 85},
    {5, -18, 0x00adee},
}, 90, 0, 0, 100, 100)
```

## Parameters
- whether_to_search_multiple_results
    boolean, optional. When this field is set to `true`, returns a table of all matched positions in the region, in the format `{{x1, y1}, {x2, y2}, ...}`. Defaults to `false`.
- maximum_result_count
    integer, optional. When `find_all` is set to `true`, this is the maximum number of results to return. It can be set up to `1000`. Defaults to `100`.
- maximum_allowed_misses
    integer, optional. The maximum number of unmatched points allowed. Defaults to `0`, meaning every point must match.
- color_similarity_algorithm
    integer, optional. The color similarity algorithm. Defaults to `0`.
- anchor_x, anchor_y
    integer, the anchor coordinate. This does not constrain color search to this fixed point; it only provides a relative coordinate for offset positions. If offsets are not needed, use `0, 0`.
- anchor_color
    integer, the color of the point to search for.
- anchor_similarity
    integer, optional. The similarity for the anchor point color, in the range `1` to `100`. Defaults to `100`.
- offset_x\*, offset_y\*
    integer, the coordinate of an offset position.
- offset_color\*
    integer, the color that the offset position needs to match.
- offset_similarity\*
    integer, optional. The color similarity for the offset position, in the range `-100` to `100`. Defaults to `100`. A negative similarity means matching a similarity lower than the absolute value.
- global_similarity
    integer, optional. If no per-point similarity is set, every point uses this similarity. Range: `1` to `100`. Defaults to `100`.
- left, top, right, bottom
    integer, optional search region. Defaults to full screen.

## Returns
- x, y
    integer, the anchor coordinate of the matched structure.

## Notes
Searches for a multi-point color structure using similarity matching. The first point is the anchor; subsequent point coordinates are offsets relative to the anchor.
For coordinate, region, similarity algorithm, miss return, and `find_all` conventions, see Visual API Conventions in `references/workflow.md`.
