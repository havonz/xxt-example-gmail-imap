# sys.input_text

Purpose: Input text

## Signature
```lua
sys.input_text(text_content [, press_return_after_input ])
```

## Example
```lua
sys.input_text("hello") -- Input "hello" into the text box where the current cursor is located.

sys.input_text("hello", true) -- Input "hello" in a chat/search text box and press Return to trigger send or search.
```

## Parameters
- text_content
    string, text to input. Since 20250625, `"\b"` (Backspace) is supported.
- press_return_after_input
    boolean, whether to press the Return key on the keyboard after input finishes, such as for send or search. Defaults to `false`.

## Notes
Inputs text in a text-input area of the foreground app.
The function works by first writing the text to the pasteboard, then invoking the paste shortcut, command + v, to paste the text.
Calling this function affects the shared pasteboard. Back up important pasteboard data before calling it.
If the system shared pasteboard is damaged, text input with this function fails. In other words, if the device cannot copy and paste text normally, this function cannot be used either.
Known plugin conflict with this function: Background Manager.
If it does not work, `key.send_text` may help.
