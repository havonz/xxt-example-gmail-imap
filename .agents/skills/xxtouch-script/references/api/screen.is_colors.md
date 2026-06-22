# screen.is_colors

Purpose: Screen multi-point color match

## Signature
```lua
matched = screen.is_colors({
    [max_miss = maximum_allowed_misses,]
    [xy_tolerance = coordinate_tolerance,]
    [csim_algorithm = color_similarity_algorithm,]
    {x*, y*, color*},
    {x*, y*, color*},
    ...
}[, color_similarity])
```

## Example
```lua
if screen.is_colors({
    {509, 488, 0xec1c23},
    {514, 470, 0x00adee},
    {508, 478, 0xffc823},
}, 90) then
    sys.alert("Matched!")
else
    sys.alert("Not matched!")
end
```

## Parameters
- maximum_allowed_misses
    integer, optional. The maximum number of unmatched points allowed. Defaults to `0`, meaning every point must match.
- coordinate_tolerance
    integer, optional. The allowed coordinate offset. Points exceeding this value are treated as misses. Defaults to `0`, requiring exact coordinate matching.
- color_similarity_algorithm
    integer, optional. Specifies the color similarity algorithm. Defaults to `0`.
- x\*, y\*
    integer, the coordinate of one point.
- color\*
    integer, the color value that one point needs to match.
- color_similarity
    integer, optional. The required color similarity, in the range `1` to `100`. Defaults to `100`.

## Returns
- matched
    boolean, returns `true` if all point colors match; otherwise returns `false`.

## Notes
Matches colors at multiple points on the screen.
For coordinate and similarity algorithm conventions, see Visual API Conventions in `references/workflow.md`.
