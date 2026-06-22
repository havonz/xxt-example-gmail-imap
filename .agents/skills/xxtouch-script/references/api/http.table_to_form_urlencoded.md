# http.table_to_form_urlencoded

Purpose: URL-encoded form encoding

## Signature
```lua
encoded_form_text = http.table_to_form_urlencoded(table_to_encode)
```

## Example
```lua
form = http.table_to_form_urlencoded{
    num = 1,
    str = 'hello',
    arr = {12, 34, 'ok'},
}

nLog(form) -- arr%5B0%5D=12&arr%5B1%5D=34&arr%5B2%5D=ok&str=hello&num=1

c, h, r = http.get('https://httpbin.org/get?'..form, 10, {}, true) -- Submit the form through GET query. The URL is escaped automatically by default unless the final argument is true.
nLog(r)

c, h, r = http.post('https://httpbin.org/post', 10, {}, form) -- Submit the form through POST.
nLog(r)
```

## Parameters
- table_to_encode
    table

## Returns
- encoded_form_text
    string
