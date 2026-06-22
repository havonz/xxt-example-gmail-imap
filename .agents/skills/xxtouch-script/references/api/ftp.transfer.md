# ftp.download / ftp.upload

Purpose: FTP upload/download

## Download File
```lua
download_success, download_info = ftp.download(URL, local_file_path [, connection_timeout_seconds, resume_mode, chunk_callback, buffer_size ])
```

### Example
```lua
local done, info = ftp.download("ftp://user:p%40ss@example.com/files/1.zip", "/var/mobile/1.zip")
if done then
    if info.start_pos + info.size_download < info.resource_size then
        sys.alert("Download interrupted, downloaded "..info.size_download.." bytes")
    else
        sys.alert("Download completed")
    end
else
    sys.alert("Connection failed: "..info)
end
```

### Resume and Progress
```lua
local done, info = ftp.download("ftp://user:password@example.com/files/1.zip", "/var/mobile/1.zip", 10, true, function(binfo)
    local percent = math.floor(((binfo.start_pos + binfo.size_download) / binfo.resource_size) * 100)
    sys.toast("Download progress "..percent.."%")
end, 4096 * 1024)

if done then
    if info.start_pos + info.size_download < info.resource_size then
        sys.alert(
            "Download interrupted\nDownloaded this time: "..info.size_download.." bytes"
            .."\nStarted from byte "..info.start_pos
            .."\nAverage speed: "..math.floor(info.speed_download/1024).." kB/s"
            .."\nRemaining: "..(info.resource_size - (info.start_pos + info.size_download)).." bytes"
        )
    else
        sys.alert(
            "Download completed\nDownloaded this time: "..info.size_download.." bytes"
            .."\nStarted from byte "..info.start_pos
            .."\nAverage speed: "..math.floor(info.speed_download/1024).." kB/s"
        )
    end
else
    sys.alert("Connection failed: "..info)
end
```

### Parameters
- URL
    string, remote file URL. Account and password are included in this parameter.
- local_file_path
    string, local path where the file should be saved.
- connection_timeout_seconds
    number, optional connection timeout in seconds. Defaults to `10`.
- resume_mode
    boolean, optional. Whether resume support is needed. `true` means yes, `false` means no. Defaults to `false`.
- chunk_callback
    function, optional. Called once after each chunk is downloaded. The first argument is the current download information. Returning `true` from the callback interrupts this download.
- buffer_size
    integer, optional buffer size in bytes. Defaults to automatic optimal configuration.

### Returns
- download_success
    boolean, whether the connection succeeded.
- download_info
    table | string, if the connection succeeds, returns a table with download information; otherwise returns a text description of the connection failure reason.

    ```lua
    {
        resource_size = total_remote_resource_bytes,
        start_pos = start_position_of_this_download,
        size_download = bytes_downloaded_this_time,
        speed_download = download_speed_this_time, -- bytes/second
    }
    ```

## Upload File
```lua
upload_success, upload_info = ftp.upload(local_file_path, URL [, connection_timeout_seconds, resume_mode, chunk_callback, buffer_size ])
```

### Example
```lua
local done, info = ftp.upload("/var/mobile/1.zip", "ftp://user:p%40ss@example.com/files/1.zip")
if done then
    if info.start_pos + info.size_upload < info.resource_size then
        sys.alert("Upload interrupted, uploaded "..info.size_upload.." bytes")
    else
        sys.alert("Upload completed")
    end
else
    sys.alert("Connection failed: "..info)
end
```

### Resume and Progress
```lua
local done, info = ftp.upload("/var/mobile/1.zip", "ftp://user:password@example.com/files/1.zip", 10, true, function(binfo)
    local percent = math.floor(((binfo.start_pos + binfo.size_upload) / binfo.resource_size) * 100)
    sys.toast("Upload progress "..percent.."%")
end, 4096 * 1024)

if done then
    if info.start_pos + info.size_upload < info.resource_size then
        sys.alert(
            "Upload interrupted\nUploaded this time: "..info.size_upload.." bytes"
            .."\nStarted from byte "..info.start_pos
            .."\nAverage speed: "..math.floor(info.speed_upload/1024).." kB/s"
            .."\nRemaining: "..(info.resource_size - (info.start_pos + info.size_upload)).." bytes"
        )
    else
        sys.alert(
            "Upload completed\nUploaded this time: "..info.size_upload.." bytes"
            .."\nStarted from byte "..info.start_pos
            .."\nAverage speed: "..math.floor(info.speed_upload/1024).." kB/s"
        )
    end
else
    sys.alert("Connection failed: "..info)
end
```

### Parameters
- local_file_path
    string, local file path.
- URL
    string, remote URL to upload to. Account and password are included in this parameter.
- connection_timeout_seconds
    number, optional connection timeout in seconds. Defaults to `10`.
- resume_mode
    boolean, optional. Whether resume support is needed. `true` means yes, `false` means no. Defaults to `false`.
- chunk_callback
    function, optional. Called once after each chunk is uploaded. The first argument is the current upload information. Returning `true` from the callback interrupts this upload.
- buffer_size
    integer, optional buffer size in bytes. Defaults to automatic optimal configuration.

### Returns
- upload_success
    boolean, whether the connection succeeded.
- upload_info
    table | string, if the connection succeeds, returns a table with upload information; otherwise returns a text description of the connection failure reason.

    ```lua
    {
        resource_size = total_local_file_bytes,
        start_pos = start_position_of_this_upload,
        size_upload = bytes_uploaded_this_time,
        speed_upload = upload_speed_this_time, -- bytes/second
    }
    ```

## Notes
URL format: `ftp://[account:password@]address[:port]/path`. In the account or password, write `@`, `:`, and `/` as `%40`, `%3A`, and `%2F` respectively.
This function is suitable for large file transfers. Stopping the script during transfer may be slow.
This function may yield. Before it returns, other threads may get a chance to run.
If `Requested range was not delivered by the server` is returned, the server may not support resuming. Set the resume parameter to `false`.
