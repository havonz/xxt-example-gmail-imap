# http.head

Purpose: HEAD request

## Signature
```lua
http_status_code, response_headers_json_text = http.head(URL [, timeout_seconds, request_headers, do_not_escape_url ])

http_status_code, response_headers_json_text = http.head{
    url = URL;
    timeout = timeout_seconds;
    headers = request_headers;
    params = query_parameters;
    progress = progress_callback;
    progress_interval_ms = progress_callback_interval_ms;
}
```

## Example
```lua
local c, h = http.head("https://www.xxtouch.app/test.txt")
if c==200 then -- If the returned status code is HTTP_OK.
    sys.alert(h) -- Output the requested header information.
end
```

## Parameters
- URL
    string, URL to request. This method escapes the URL by default.
- timeout_seconds
    number, optional request timeout in seconds. Defaults to `10`.
- request_headers
    table, optional outgoing request headers in the form `{field1 = value1, field2 = value2, ...}`. Defaults to `{}`.
- query_parameters
    table, optional outgoing request query parameters in the form `{field1 = value1, field2 = value2, ...}`. Defaults to `{}`.
- progress_callback
    function, optional. Supported by named-argument calls after 20260402. During the request, `function(info) end` is called. The `info` structure is described in "Progress Callback".
- progress_callback_interval_ms
    integer, optional. Supported by named-argument calls after 20260402. Controls the callback interval of `progress`, in milliseconds.
- do_not_escape_url
    boolean, optional. `true` means request the URL directly without escaping it. Defaults to `false`.
    Use this when the URL is escaped manually.

## Progress Callback
The `info` parameter of the `progress` callback has this structure:

```lua
{
    count_of_bytes_sent = 0;
    count_of_bytes_expected_to_send = 100;
    count_of_bytes_received = 0;
    count_of_bytes_expected_to_receive = 100;
}
```

## Returns
- http_status_code
    integer, HTTP status code for this request. Returns `-1` on request timeout.
- response_headers_json_text
    string | nil, response headers in JSON form returned when the request completes. Returns `nil` on request timeout.

## Notes
Uses the HTTP/1.1 HEAD method to request header information for a network resource.
HEAD usually gets the same response headers as a GET request, but HEAD does not return the actual body content.
This function may yield. Before it returns, other threads may get a chance to run.
