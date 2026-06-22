# file line operations

Purpose: Read/write/insert/delete/count text lines.

## Signature
```lua
line_content, error_message = file.get_line(file_path, line_number)
line_array, error_message = file.get_lines(file_path)
write_success, error_message = file.set_line(file_path, line_number, content_to_write)
write_success, error_message = file.set_lines(file_path, line_array)
write_success, error_message = file.insert_line(file_path, line_number, content_to_insert)
write_success, error_message = file.insert_lines(file_path, line_number, line_array)
success, removed_line_content_or_error_message = file.remove_line(file_path, line_number)
line_count = file.line_count(file_path)
```

## Example
```lua
local path = "/var/mobile/1.txt"
file.set_lines(path, {"first", "second"})
file.insert_line(path, 0, "tail")
file.set_line(path, -1, "last")

local first = file.get_line(path, 1)
local lines = file.get_lines(path)
local ok, removed = file.remove_line(path, 2)
local count = file.line_count(path)
```

## Parameters
- file_path
    string, absolute file path.
- line_number
    integer, specified line number. `0` means last line + 1; negative numbers mean line numbers counted from the end.
- content_to_write, content_to_insert
    string. `insert_line` inserts before the specified line.
- line_array
    array table. `set_lines` overwrites the whole file, and `insert_lines` inserts before the specified line.

## Returns
- line_content
    string or nil. Returns an empty string when there are not enough lines, and nil when the file does not exist.
- line_array
    array table or nil. Empty files return 0 lines; nonexistent files return nil.
- write_success, success
    boolean.
- removed_line_content_or_error_message
    `remove_line` returns the removed line on success and an error message on failure.
- line_count
    integer or nil. Empty files return 0; nonexistent files return nil.
- error_message
    string, returned on failure.

## Notes
These functions automatically remove a UTF-8 BOM at the beginning of the file. `set_line` / `insert_line` fill missing lines with empty lines when the line count is insufficient. Line number `0` appends to the end of the file. After `remove_line` deletes a line, following lines move forward. Write functions create nonexistent files; if the directory does not exist, they return false.
