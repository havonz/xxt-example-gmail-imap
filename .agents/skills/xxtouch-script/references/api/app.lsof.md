# app.lsof

Purpose: App open files

## Signature
```lua
file_list, error_message = app.lsof(bundle_identifier_or_pid)
```

## Example
```lua
nLog(app.lsof('com.apple.Preferences'))
```

## Parameters
- bundle_identifier
    string
- pid
    integer, the process ID of the app to inspect.

## Returns
- file_list
    table | nil

    ```lua
    {
        opensockets = {
            {
                fd = integer_value,
                kind = "TCP" | "IN",
                ["local"] = {
                    address = string_value,
                    port = integer_value,
                },
                ["remote"] = {
                    address = string_value,
                    port = integer_value,
                },
            },
            ...
        },
        openfiles = {
            {
                fd = integer_value,
                path = string_value,
            },
            ...
        },
    }
    ```

- error_message
    string | nil, returns the error message on failure.

## Notes
Lists the file descriptors and socket descriptors opened by the specified app.
