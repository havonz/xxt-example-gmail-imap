# utils.launch_args

Purpose: Script launch arguments

## Signature
```lua
launch_arguments_table = utils.launch_args()
```

## Example
```lua
sys.alert(table.deep_dump(utils.launch_args()))

-- Get the current script file path. Note: a script does not always have a file path.
sys.alert("Current script path: "..tostring(utils.launch_args().path))
```

## Returns
- launch_arguments_table
    table, returns a parameter table describing this launch. You can print the structure with `table.deep_dump`.

## Notes
Gets the current script launch arguments. Recommended for use with Activator-triggered scripts.
