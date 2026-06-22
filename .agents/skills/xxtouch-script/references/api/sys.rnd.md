# sys.rnd

Purpose: Random number

## Signature
```lua
random_number = sys.rnd()
```

## Example
```lua
math.randomseed(sys.rnd()) -- Initialize the random seed with a true random number.
local r = math.random(1, 100) -- Generate a random number in the range 1 to 100.
```

## Returns
- random_number
    integer, a random number in the range `0` to `4294967295`.

## Notes
Generates a true random number.
