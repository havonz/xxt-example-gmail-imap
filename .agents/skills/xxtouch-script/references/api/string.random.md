# string.random

Purpose: Generate a random string.

## Signature
```lua
random_string = string.random(character_pool [, generated_character_count, bytes_per_character ])
```

## Example
```lua
rs = string.random("qwertyuiopasdfghjklzxcvbnm", 20, 1)
rs = string.random("0123456789abcdef", 20, 1)
```

## Parameters
- character_pool
    string, dictionary used to generate the string.
- generated_character_count
    integer, optional. Number of characters in the generated random string; defaults to 6.
- bytes_per_character
    integer, optional. Length of each character in bytes; defaults to 1.

## Returns
- random_string
    string, the generated random string.

## Notes
Generates a random string. In UTF-8, many CJK characters use 3 bytes per character.
