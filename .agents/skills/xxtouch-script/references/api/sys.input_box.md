# sys.input_box

Purpose: Input prompt

## Signature
```lua
input_content = sys.input_box(description)
input_content = sys.input_box(title, description)
input_content = sys.input_box(title, description, input_box_count)
input_content, choice = sys.input_box(title, description, text_field_prompt, text_field_default_value, default_button_title, button1_title, button2_title, input_box_count)
input_content1, input_content2, choice = sys.input_box(title, description, text_field_prompt_list, text_field_default_value_list, default_button_title, button1_title, button2_title, input_box_count)
```

## Example
```lua
input_content = sys.input_box("Description")

input_content = sys.input_box("Title", "This is the description")

input_content = sys.input_box("Title", "This is the description", 0)
```

## Notes
Shows a system input dialog with up to 3 buttons and 2 text boxes, blocking all threads while waiting for the return value.
The title defaults to `"Script Alert"`.
