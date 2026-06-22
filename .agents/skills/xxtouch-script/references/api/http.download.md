# http.download

Purpose: HTTP file download (deprecated; prefer http.get)

> `http.download` is deprecated. New code should use `http.get{ download_file = path }` instead. Use the `progress` and `progress_interval_ms` named parameters of `http.get` when progress is needed.

## Signature
```lua
download_success, download_info = http.download(URL, local_file_path [, connection_timeout_seconds, resume_mode, chunk_callback, buffer_size ])
```

## Example
```lua
local code, headers, path = http.get{
    url = "https://example.com/1.zip";
    download_file = "/var/mobile/1.zip";
}
if code == 200 then
    sys.alert("Download completed: "..path)
end
```

## Legacy Usage: Resume and Progress
```lua
local done, info = http.download("https://example.com/1.zip", "/var/mobile/1.zip", 10, true, function(binfo)
    local percent = math.floor(((binfo.start_pos + binfo.size_download) / binfo.resource_size) * 100)
    sys.toast("Download progress "..percent.."%")
end, 4096 * 1024)

if (done) then
    if (info.start_pos + info.size_download < info.resource_size) then
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

## Parameters
- URL
    string, remote file URL.
- local_file_path
    string, local path where the file should be saved.
- connection_timeout_seconds
    number, optional connection timeout in seconds. Defaults to `10`.
- resume_mode
    boolean, optional. Whether resume support is needed. `true` means yes, `false` means no. Defaults to `false`.
- chunk_callback
    function, optional chunk callback. The function is called once after each chunk is downloaded. Defaults to an empty function.
    The first argument of the chunk callback is the current download information. Returning `true` from the callback interrupts this download.
- buffer_size
    integer, optional buffer size in bytes. Defaults to automatic optimal configuration.

## Returns
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

## Notes
This function is deprecated. New code should use `http.get{ download_file = path }`.
The legacy interface supports large file downloads. Stopping the script during transfer may be slow.
This function may yield. Before it returns, other threads may get a chance to run.
If `Requested range was not delivered by the server` is returned, the server may not support resuming. Set the resume parameter to `false`.
