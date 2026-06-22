# LPeg Pattern Slice

Source: https://www.inf.puc-rio.br/~roberto/lpeg/

LPeg matches are anchored: `lpeg.match(p, subject)` tries at the current start position, not anywhere in the string unless the pattern accounts for skipped input.

## Constructors And Operators

```lua
local lpeg = require 'lpeg'

local P = lpeg.P      -- literal string, exact length, table grammar, EOF with -1
local S = lpeg.S      -- set of characters
local R = lpeg.R      -- character range, e.g. R('09')

local digit = R('09')
local alpha = R('az', 'AZ')
local space = S(' \t\r\n') ^ 0
local ident = (alpha + P('_')) * (alpha + digit + P('_')) ^ 0
```

Operators:

- `p1 * p2`: sequence.
- `p1 + p2`: ordered choice.
- `p ^ n`: at least `n` repetitions.
- `p ^ -n`: at most `n` repetitions.
- `p1 - p2`: match `p1` only when `p2` does not match.
- `-p`: negative lookahead.
- `#p`: positive lookahead.

## Match Anywhere

```lua
local lpeg = require 'lpeg'

local target = lpeg.P('token')
local anywhere = (1 - target) ^ 0 * target
local pos = lpeg.match(anywhere, 'abc token xyz')
```

## Full String Match

```lua
local EOF = -lpeg.P(1)
local integer = lpeg.R('09') ^ 1
local ok = lpeg.match(integer * EOF, '123') ~= nil
```

## Notes

- Keep pattern pieces named; complex inline LPeg is hard to review.
- Use Lua string functions for simple contains/prefix/suffix tasks.
- Raise `lpeg.setmaxstack(max)` only after simplifying recursive or backtracking-heavy patterns.
