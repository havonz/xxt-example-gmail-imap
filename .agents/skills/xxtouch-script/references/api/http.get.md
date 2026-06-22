# http.get

Purpose: GET request

## Signature
```lua
http_status_code, response_headers_json_text, response_body = http.get(URL [, timeout_seconds, request_headers, do_not_escape_url ])

http_status_code, response_headers_json_text, response_body = http.get{
    url = URL;
    timeout = timeout_seconds;
    headers = request_headers;
    params = query_parameters;
    download_file = file_path_for_saving_response_body_after_success;
    progress = progress_callback;
    progress_interval_ms = progress_callback_interval_ms;
}
```

## Example
```lua
local code, headers, body = http.get('https://httpbin.org/get?hello=world', 15, {
    ['User-Agent'] = 'XXTouch';
    ['Cookie'] = 'a=1; b=2';
})

if code == 200 then
    sys.alert(body)
end
```

## Named-Argument Example
```lua
local code, headers, body = http.get{
    url = 'https://httpbin.org/get';
    timeout = 15;
    headers = {
        ['User-Agent'] = 'XXTouch';
    };
    params = {
        hello = 'world';
        greeting = 'hello';
    };
}

if code == 200 then
    sys.alert(body)
end
```

## Save Response Body to File
```lua
local save_path = XXT_HOME_PATH..'/tmp/http-body.txt'
local code, headers, path = http.get{
    url = 'https://httpbin.org/get';
    timeout = 15;
    download_file = save_path;
}

if code == 200 then
    nLog('saved to', path)
end
```

## Parameters
- URL
    string, URL to request. This method applies percent-escaping to the URL by default.
- timeout_seconds
    number, optional request timeout in seconds. Defaults to `10`.
- request_headers
    table, optional outgoing request headers in the form `{field1 = value1, field2 = value2, ...}`. Defaults to `{}`.
- query_parameters
    table, optional outgoing request query parameters in the form `{field1 = value1, field2 = value2, ...}`. Defaults to `{}`.
- file_path_for_saving_response_body_after_success
    string, optional. If set, the response body returned after a successful request is the saved file path.
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
- response_body
    string | nil, content returned when the request completes. If the response body is saved to a file, this value is the file path. Returns `nil` on request timeout.

## Notes
Uses the HTTP/1.1 GET method to request a network resource.
Named-argument calls can save the response body to a file through `download_file`; `http.download` is deprecated, and new code should use `http.get` instead.
This function may yield. Before it returns, other threads may get a chance to run.
If the server protocol version is HTTP/1.0 or HTTP/0.9, use the `httpGet` method instead.
```lua
response_body = httpGet(URL, timeout_seconds)
```
