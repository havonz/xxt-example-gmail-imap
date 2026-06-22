# file.move

Purpose: Move file/directory.

## Signature
```lua
success, error_message = file.move(source_path, destination_path [, mode])
```

## Example
```lua
ok, err = file.move(XXT_SCRIPTS_PATH..'/1.zip', XXT_SCRIPTS_PATH..'/2.zip')
if not ok then
    sys.alert('Move failed: '..err)
end
```

## Parameters
- source_path
    string, absolute file path.
- destination_path
    string, absolute file path.
- mode 20250914+
    string, optional move mode. Values:
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
Moves a file or directory from `source_path` to `destination_path`; renaming within the same path is a rename.
Keywords: rename file, rename directory, rename folder, move file, move directory, move folder.
