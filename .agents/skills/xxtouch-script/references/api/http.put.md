# http.put

Purpose: PUT request

## Signature
```lua
http_status_code, response_headers_json_text, response_body = http.put(URL [, timeout_seconds, request_headers, request_body_data, do_not_escape_url ])

http_status_code, response_headers_json_text, response_body = http.put{
    url = URL;
    timeout = timeout_seconds;
    headers = request_headers;
    params = query_parameters;

    -- Request body parameters are mutually exclusive. Priority: multipart > data > json > upload_file.
    multipart = request_body_multipart_form;
    data = request_body_data;
    json = request_body_json;
    upload_file = request_body_upload_file_path;

    download_file = file_path_for_saving_response_body_after_success;
    progress = progress_callback;
    progress_interval_ms = progress_callback_interval_ms;
}
```

## Example
```lua
local code, headers, body = http.put('https://httpbin.org/put?hello=world', 15, {
    ['User-Agent'] = 'XXTouch';
}, 'data to send')

if code == 200 then
    sys.alert(body)
end
```

## Named-Argument Example
```lua
local code, headers, body = http.put{
    url = 'https://httpbin.org/put';
    timeout = 15;
    headers = {
        ['User-Agent'] = 'XXTouch';
    };
    params = {
        hello = 'world';
    };
    data = {
        name = 'alice';
        email = 'alice@example.com';
    };
}

if code == 200 then
    sys.alert(body)
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
- request_body_data
    string, optional content sent with PUT. Defaults to an empty string.
    Since 20250625, if this is a table, it is encoded and sent as `application/x-www-form-urlencoded`.
- request_body_multipart_form
    table, optional multipart form data sent with PUT, in the form `{field1 = value1, field2 = value2, ...}`. Defaults to `{}`.
- request_body_json
    table, optional data encoded and sent as `application/json`.
- request_body_upload_file_path
    string, optional. Sends file data directly as the request body.
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
Uses the HTTP/1.1 PUT method to send data over the network. Its usage is the same as POST.
This function may yield. Before it returns, other threads may get a chance to run.
