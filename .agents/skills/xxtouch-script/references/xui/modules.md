# XUI Modules

This file organizes component fields by `cell` name. Example snippets are intended to be used inside the root table's `items = { ... }`.

## Component Selection Table

| `cell` | Purpose | Saved Value Type | Key Fields |
|---|---|---|---|
|`Group`|Section title and footer|Not saved|`label`, `footerText`|
|`Switch`|Switch control|Boolean or `trueValue` / `falseValue`|`key`, `default`|
|`TextField`|Single-line text|String|`key`, `placeholder`, `keyboard`, `alignment`|
|`Textarea`|Multi-line text|String|`key`, `maxLength`, `keyboard`|
|`StaticText`|Static text|Not saved|`label`, `selectable`, `alignment`|
|`TitleValue`|Key-value display or snippet entry|Any|`value` or `key` + `snippet`|
|`Option`|Subpage single-choice list|Primitive type|`key`, `options`|
|`MultipleOption`|Subpage multi-choice list|Array|`key`, `options`, `maxCount`|
|`OrderedOption`|Subpage ordered multi-choice list|Array|`key`, `options`, `minCount`, `maxCount`|
|`Segment`|Segmented single choice for a small option set|Primitive type|`key`, `options`|
|`Radio`|Inline single-choice tags|Primitive type|`key`, `options`, `numPerLine`|
|`Checkbox`|Inline multi-choice tags|Array|`key`, `options`, `minCount`, `maxCount`|
|`Slider`|Numeric slider|Number|`key`, `min`, `max`, `step`|
|`Stepper`|Numeric stepper|Number|`key`, `min`, `max`, `step`|
|`DateTime`|Date, time, or interval|Integer or string|`key`, `mode`, `format`|
|`EditableList`|Editable string list|String array|`key`, `maxCount`, `validationRegex`|
|`File`|File or directory picker|Absolute path string|`key`, `initialPath`, `allowedExtensions`|
|`Button`|Execute an action|Action return value or not saved|`action`; fill `args` according to the action|
|`Link`|Open a subpage, file, or webpage|Not saved|`url`|
|`Image`|Static image|Not saved|`path`, `height`|
|`AnimatedImage`|GIF or online image|Not saved|`path`, `height`|
|`About`|About block|Not saved|`label`, `value`, `icon`|

## Shared Enums

| Field | Allowed Values |
|---|---|
|`alignment`|`Left`, `Center`, `Right`, `Natural`, `Justified`|
|`keyboard`|`Default`, `Alphabet`, `ASCIICapable`, `NumbersAndPunctuation`, `URL`, `NumberPad`, `PhonePad`, `NamePhonePad`, `EmailAddress`, `DecimalPad`|
|`clearButtonMode`|`Never`, `Always`, `WhileEditing`, `UnlessEditing`|
|`autoCapitalization`|`None`, `Sentences`, `Words`, `AllCharacters`|
|`autoCorrection`|`Default`, `No`, `Yes`|

## Option Structure

`Option` / `MultipleOption` / `OrderedOption` / `Segment` / `Radio` / `Checkbox` share the same option structure:

| Field | Type | Description |
|---|---|---|
|`title`|string|Displayed title; localizable|
|`value`|primitive type|Saved value; uses `title` when omitted|
|`icon`|string|Option icon; supported by list-style options|
|`shortTitle`|string|Short title shown on the right side of the parent entry; supported only by `Option`|

Prefer table-form options instead of relying on string shorthand, so default values are not coupled to display text.

```lua
options = {
    { title = "Slow"; value = "slow" };
    { title = "Standard"; value = "normal"; shortTitle = "Standard" };
    { title = "Fast"; value = "fast" };
}
```

## Group

Fields: `label` and `footerText`; both are localizable. The first component in a list should usually be `Group`; if it is not, XUI automatically inserts an empty group.

```lua
{
    cell = "Group";
    label = "Basic Settings";
    footerText = "These settings are read when the script starts.";
};
```

## Switch

Fields:

| Field | Type | Default | Description |
|---|---|---|---|
|`negate`|boolean|`false`|Saved value is the opposite of the switch state|
|`trueValue`|primitive type|`true`|Value saved when the switch is on|
|`falseValue`|primitive type|`false`|Value saved when the switch is off|

Theme keys: `offTintColor`, `onTintColor`, `thumbTintColor`.

```lua
{
    cell = "Switch";
    label = "Enable Auto Run";
    key = "auto_run";
    default = true;
};
```

## TextField

Fields:

| Field | Type | Default | Description |
|---|---|---|---|
|`alignment`|string|`Left`|Text alignment|
|`keyboard`|string|`Default`|Keyboard type|
|`placeholder`|string|`""`|Placeholder text; localizable|
|`isSecure`|boolean|`false`|Password-style input|
|`clearButtonMode`|string|`Never`|Clear button display policy|
|`maxLength`|integer|`INT_MAX`|Maximum length|
|`validationRegex`|string|`nil`|Validation before saving|
|`prompt`|string|`nil`|When non-empty, tapping opens a popup input; localizable|
|`message`|string|`nil`|Popup description; localizable|
|`okTitle`|string|`"OK"`|Popup confirmation button; localizable|
|`cancelTitle`|string|`"Cancel"`|Popup cancel button; localizable|

`icon` is not supported. When `label` exists, it is usually paired with `alignment = "Right"`. Theme keys: `textColor`, `caretColor`, `placeholderColor`.

```lua
{
    cell = "TextField";
    label = "Account";
    key = "username";
    default = "";
    placeholder = "Enter account";
    alignment = "Right";
    validationRegex = "^[0-9A-Za-z_]+$";
};
```

## Textarea

Fields:

| Field | Type | Default | Description |
|---|---|---|---|
|`maxLength`|integer|`INT_MAX`|Maximum length|
|`keyboard`|string|`Default`|Keyboard type|
|`autoCapitalization`|string|`None`|Auto-capitalization policy|
|`autoCorrection`|string|`Default`|Auto-correction policy|

Theme keys: `textColor`, `caretColor`, `placeholderColor`.

```lua
{
    cell = "Textarea";
    label = "Notes";
    key = "note";
    default = "";
    maxLength = 200;
};
```

## StaticText

Fields:

| Field | Type | Default | Description |
|---|---|---|---|
|`label`|string|required|Displayed text|
|`alignment`|string|`Left`|Text alignment|
|`selectable`|boolean|`false`|Whether copying is allowed|

```lua
{
    cell = "StaticText";
    label = "Saved configuration takes effect the next time the script runs.";
    selectable = true;
};
```

## TitleValue

Fields:

| Field | Type | Default | Description |
|---|---|---|---|
|`value`|primitive type|`nil`|Value displayed on the right|
|`snippet`|string|`nil`|`.snippet` file path|

After `key` + `snippet` is set, tapping the component opens the selector queue and saves the `generator` return value to that `key`. Swiping left can clear the saved value, but it will not overwrite a `value` hardcoded in the XUI file.

```lua
{
    cell = "TitleValue";
    label = "Target App";
    key = "target_app";
    snippet = "snippets/app.snippet";
};
```

## Option / MultipleOption / OrderedOption

Fields:

| Component | Field | Default | Description |
|---|---|---|---|
|`Option`|`options`|required|Single-choice list|
|`Option`|`footerText`|`""`|List footer; localizable|
|`Option`|`popoverMode`|`false`|Popover style|
|`MultipleOption`|`options`|required|Multi-choice list|
|`MultipleOption`|`footerText`|`""`|List footer; localizable|
|`MultipleOption`|`maxCount`|`INT_MAX`|Maximum number of selected items|
|`MultipleOption`|`popoverMode`|`false`|Popover style|
|`OrderedOption`|`options`|required|Ordered multi-choice list|
|`OrderedOption`|`footerText`|`""`|List footer; localizable|
|`OrderedOption`|`minCount`|`0`|Minimum number of selected items|
|`OrderedOption`|`maxCount`|`INT_MAX`|Maximum number of selected items|
|`OrderedOption`|`popoverMode`|`false`|Popover style|

```lua
{
    cell = "Option";
    label = "Run Mode";
    key = "mode";
    default = "normal";
    options = {
        { title = "Slow"; value = "slow"; shortTitle = "Slow" };
        { title = "Standard"; value = "normal"; shortTitle = "Standard" };
        { title = "Fast"; value = "fast"; shortTitle = "Fast" };
    };
};
{
    cell = "MultipleOption";
    label = "Enabled Features";
    key = "features";
    default = { "log" };
    maxCount = 2;
    options = {
        { title = "Logs"; value = "log" };
        { title = "Screenshots"; value = "screenshot" };
        { title = "Notifications"; value = "notify" };
    };
};
```

## Segment / Radio / Checkbox

`Segment` is suitable for a small set of mutually exclusive options. `Radio` / `Checkbox` use an inline tag style.

Fields:

| Component | Field | Default | Description |
|---|---|---|---|
|`Segment`|`options`|required|Single-choice segment items|
|`Radio`|`options`|required|Single-choice tag items|
|`Radio`|`numPerLine`|iPhone `2`, iPad `4`|Number per line, maximum `12`|
|`Checkbox`|`options`|required|Multi-choice tag items|
|`Checkbox`|`numPerLine`|iPhone `2`, iPad `4`|Number per line, maximum `12`|
|`Checkbox`|`minCount`|`0`|Minimum number of selected items|
|`Checkbox`|`maxCount`|`INT_MAX`|Maximum number of selected items|

`Radio` saves a single value; `Checkbox` saves an array. Theme keys: `tagTextColor`, `tagSelectedTextColor`, `tagBackgroundColor`, `tagSelectedBackgroundColor`, `tagBorderColor`, `tagSelectedBorderColor`.

```lua
{
    cell = "Segment";
    label = "Speed";
    key = "speed";
    default = "normal";
    options = {
        { title = "Slow"; value = "slow" };
        { title = "Normal"; value = "normal" };
        { title = "Fast"; value = "fast" };
    };
};
{
    cell = "Checkbox";
    key = "channels";
    default = { "toast" };
    maxCount = 2;
    options = {
        { title = "Alert"; value = "alert" };
        { title = "Toast"; value = "toast" };
        { title = "Log"; value = "log" };
    };
};
```

## Slider / Stepper

Fields:

| Component | Field | Default | Description |
|---|---|---|---|
|`Slider`|`min`|`0.0`|Minimum value|
|`Slider`|`max`|`1.0`|Maximum value|
|`Slider`|`step`|`0`|Snap step; `0` means no snapping|
|`Slider`|`showValue`|`false`|Show the current value|
|`Stepper`|`min`|`1`|Minimum value|
|`Stepper`|`max`|`100`|Maximum value|
|`Stepper`|`step`|`1`|Step size|
|`Stepper`|`isInteger`|`false`|Display as integer|
|`Stepper`|`autoRepeat`|`true`|Continuously adjust while long-pressed|

`Slider` theme keys: `tintColor`, `thumbColor`.

```lua
{
    cell = "Slider";
    label = "Delay";
    key = "delay";
    default = 0.5;
    min = 0;
    max = 3;
    step = 0.1;
    showValue = true;
};
```

## DateTime

Fields:

| Field | Type | Default | Description |
|---|---|---|---|
|`min`|number|`0`|Minimum interval value|
|`max`|number|`FLOAT_MAX`|Maximum interval value|
|`minuteInterval`|integer|`1`|Minute step|
|`mode`|string|`datetime`|`datetime`, `date`, `time`, `interval`|
|`format`|string|`nil`|When non-empty, saves a formatted string|

Without `format`, the saved value is a Unix timestamp or interval seconds. With `format`, the saved value is a formatted string. `label` / `icon` are not supported; put explanatory text in a preceding `Group` when needed.

```lua
{
    cell = "DateTime";
    key = "start_at";
    mode = "datetime";
    minuteInterval = 5;
};
```

## EditableList

Fields:

| Field | Type | Default | Description |
|---|---|---|---|
|`footerText`|string|`""`|List footer; localizable|
|`itemFooterText`|string|`""`|New-item footer; localizable|
|`maxCount`|integer|`INT_MAX`|Maximum number of items|
|`validationRegex`|string|`nil`|Validate each item before saving|

Theme keys: `textColor`, `caretColor`, `placeholderColor`.

```lua
{
    cell = "EditableList";
    label = "Allowlist";
    key = "allow_list";
    default = {};
    validationRegex = "^[0-9A-Za-z_.-]+$";
};
```

## File

Fields:

| Field | Type | Default | Description |
|---|---|---|---|
|`initialPath`|string|XPP root directory|Picker initial directory, relative to the script package|
|`allowedExtensions`|string array|`{}`|Allowed file extensions|
|`label`|string|`""`|Title when nothing is selected; localizable|
|`footerText`|string|`""`|Description when nothing is selected; localizable|
|`isFile`|boolean|`true`|When `false`, selects a directory|

Saves the full absolute path of the selected file or directory. Swiping left can clear the configuration value. Theme keys: `labelColor`, `valueColor`.

```lua
{
    cell = "File";
    key = "data_file";
    initialPath = "res";
    allowedExtensions = { "json"; "txt" };
    label = "Select Data File";
};
```

## Button

Fields:

| Field | Type | Default | Description |
|---|---|---|---|
|`action`|string|required|Action identifier|
|`args`|table|as required by the action|Action arguments; actions without arguments can omit it or use `{}`|
|`alignment`|string|`Left`|Button text alignment|

The return value after the action completes is saved into the component's configuration item. Set `key` when it must be saved; omit `key` when it does not need to be saved.

| `action` | `args` | Return Value |
|---|---|---|
|`Reload:`|No arguments|None|
|`RunCommand:`|`{ command = "..." }`|Integer exit status|
|`LaunchScript:`|`{ path = "sub/task.lua" }`|None|
|`OpenURL:`|`{ url = "https://example.com" }`|None|
|`ScanQRCode:`|No arguments|QR code string|
|`SendMail:`|`subject`, `toRecipients`, optional `ccRecipients`, `bccRecipients`, `attachments`|None|
|`Null:`|No arguments|None|

`RunCommand:` executes a system command; prefer narrower actions unless the user explicitly needs it.

```lua
{
    cell = "Button";
    label = "Open Help";
    action = "OpenURL:";
    args = {
        url = "https://example.com/help";
    };
};
```

## Link

Field: `url` is required. It can open a relative package-path file, a `.xui` / `.xuic` subpage, or a web URL. When linking to another XUI file, the subpage can set its own `theme`.

```lua
{
    cell = "Link";
    label = "Advanced Settings";
    url = "sub/advanced.xui";
};
```

## Image / AnimatedImage

Fields: `path` is required, and `height` is required. `Image` is for local static images; `AnimatedImage` supports GIF and http/https images and caches them.

```lua
{
    cell = "Image";
    path = "res/logo.png";
    height = 128;
};
```

## About

Field: `icon`. Common fields `label` / `value` display the title and subtitle respectively. Theme keys: `tintColor`, `labelColor`.

```lua
{
    cell = "About";
    icon = "appicon.png";
    label = "Demo\nv1.0.0";
    value = "Example Script Package";
};
```
