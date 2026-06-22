# file.zip / file.unzip

Purpose: Create and extract ZIP archives.

## Create ZIP Archive
```lua
success, error_message = file.zip(zip_path, file_list [, password])
```

### Example
```lua
local ok, err = file.zip(XXT_SCRIPTS_PATH.."/project.zip", XXT_SCRIPTS_PATH.."/project")
if not ok then
    sys.alert("ZIP creation failed: "..err)
else
    sys.alert("ZIP created: "..XXT_SCRIPTS_PATH.."/project.zip")
end

local ok, err = file.zip(XXT_SCRIPTS_PATH.."/out.zip", {
    { XXT_SCRIPTS_PATH.."/data/readme.txt",  "docs/readme.txt" },
    { XXT_SCRIPTS_PATH.."/assets/logo.png",  "assets/images/logo.png" },
}, "123456")
if not ok then
    sys.alert("ZIP creation failed: "..err)
else
    sys.alert("ZIP created: "..XXT_SCRIPTS_PATH.."/out.zip")
end
```

### Parameters
- zip_path
    string, path where the zip file should be created.
- file_list
    table or string.
    - When a table: each item is a two-element table `{ source_file_path, archive_path }`, where `archive_path` is the relative path written inside the zip.
    - When a string: directory path whose contents are packed into the zip.
- password
    string, optional. If provided, creates an encrypted zip.

### Returns
- success
    boolean, returns true on success and false on failure.
- error_message
    string, error message on failure.

### Notes
Compresses files or directories into a zip file.
When `file_list` is a table, each entry's relative path inside the zip can be controlled precisely. When it is a string, that directory's contents are packed as a whole.

## Extract ZIP Archive
```lua
success, error_message = file.unzip(zip_path, output_path [, password])
```

### Example
```lua
local ok, err = file.unzip(XXT_SCRIPTS_PATH.."/project.zip", XXT_SCRIPTS_PATH.."/project")
if not ok then
    sys.alert("ZIP extraction failed: "..err)
end

local ok, err = file.unzip(XXT_SCRIPTS_PATH.."/archive.zip", XXT_SCRIPTS_PATH.."/unzipped", "123456")
if not ok then
    sys.alert("ZIP extraction failed: "..err)
else
    sys.alert("ZIP extracted: "..XXT_SCRIPTS_PATH.."/unzipped")
end
```

### Parameters
- zip_path
    string, absolute path to the zip file to extract.
- output_path
    string, target directory for extracted output.
- password
    string, optional. Required if the zip has a password.

### Returns
- success
    boolean, returns true on success and false on failure.
- error_message
    string, error message on failure.

### Notes
Extracted files are assigned permissions 0755, owner 501, and group 501.
