# LPeg Captures Slice

Source: https://www.inf.puc-rio.br/~roberto/lpeg/

Captures turn successful matches into returned values. Avoid side effects inside capture functions because LPeg does not guarantee how often all captures are evaluated.

## Common Captures

```lua
local lpeg = require 'lpeg'

local C = lpeg.C      -- captured substring
local Ct = lpeg.Ct    -- table capture
local Cg = lpeg.Cg    -- named group inside table captures
local Cc = lpeg.Cc    -- constant capture
local Cs = lpeg.Cs    -- substitution capture
local Cp = lpeg.Cp    -- current position
```

## Named Fields

```lua
local lpeg = require 'lpeg'

local P, R, C, Cg, Ct = lpeg.P, lpeg.R, lpeg.C, lpeg.Cg, lpeg.Ct
local digit = R('09')
local word = C((R('az', 'AZ') + P('_')) ^ 1)
local number = C(digit ^ 1) / tonumber

local item = Ct(
    Cg(word, 'name') * P('=') * Cg(number, 'value')
)

local row = lpeg.match(item, 'count=12')
sys.log(row.name, row.value)
```

## Split-Like Capture

```lua
local lpeg = require 'lpeg'

local P, C, Ct = lpeg.P, lpeg.C, lpeg.Ct
local comma = P(',')
local field = C((1 - comma) ^ 0)
local csv = Ct(field * (comma * field) ^ 0)

local values = lpeg.match(csv, 'a,b,c')
```

## Notes

- `lpeg.C(p)` captures the matched substring for `p`.
- `lpeg.Ct(p)` returns one table containing captures inside `p`.
- `p / function` transforms capture values; return transformed values.
- `lpeg.Cp()` is useful for source positions and parsers.
