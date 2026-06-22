# LPeg

Source: https://www.inf.puc-rio.br/~roberto/lpeg/

## Require

```lua
local lpeg = require 'lpeg'
```

Use LPeg for grammar-style parsing when Lua patterns are too weak. For simple string matching, prefer Lua string APIs.

## Topic Slices

- Pattern constructors and operators: `lpeg-patterns.md`.
- Captures and table captures: `lpeg-captures.md`.

## Minimal Pattern

```lua
local lpeg = require 'lpeg'

local digit = lpeg.R('09')
local digits = digit ^ 1
local matched = lpeg.match(digits, '123abc')
sys.log(matched) -- first unmatched position
```

## Notes

- LPeg patterns are not Lua string patterns.
- `lpeg.match` is anchored at the start position unless the pattern consumes leading input.
- Keep grammars small and named; complex inline expressions are hard to maintain.
- Prefer plain Lua parsing for one-off simple formats.
