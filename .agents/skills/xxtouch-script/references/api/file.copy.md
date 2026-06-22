# file.copy

Purpose: Copy file/directory.

## Signature
```lua
success, error_message = file.copy(source_path, destination_path [, mode])
```

## Example
```lua
ok, err = file.copy(XXT_SCRIPTS_PATH..'/1.zip', XXT_SCRIPTS_PATH..'/2.zip')
if not ok then
    sys.alert('Copy failed: '..err)
end
```

## Parameters
- source_path
    string, absolute file path.
- destination_path
    string, absolute file path.
- mode 20250914+
    string, optional copy mode. Values:
    - Empty string or omitted: default mode (`no-clobber`), returns failure when the destination already exists.
    - `"overwrite"` or `"o"`: overwrite mode, directly replaces the existing destination. The existing destination is removed.
    - `"merge"` or `"m"`: merge mode (directories only), preserves files already present in the destination.
    - `"overwrite-merge"` or `"om"`/`"mo"`: overwrite-merge mode, merges directories and overwrites same-name files.

## Returns
- success
    boolean, returns true on success and false on failure.
- error_message
    string, error message on failure.

## Notes
Copies a file or directory from `source_path` to `destination_path`.
Keywords: copy file, copy directory, copy folder.
