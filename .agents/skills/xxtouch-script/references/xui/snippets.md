# XUI Snippets

`.snippet` files are used in XUI to open selector queues and are commonly paired with `TitleValue`. A snippet file returns a Lua table. The App executes the selectors in `arguments` in order, then passes the selected values to `generator`.

## File Structure

```lua
return {
    name = "Select Target App";
    description = "Returns the target app Bundle ID";
    arguments = {
        {
            type = "app";
            title = "Select App";
            subtitle = "The script will operate on this app";
            default = xui.get("com.example.demo", "target_app");
        };
    };
    generator = function(bundle_id)
        return bundle_id
    end;
}
```

| Field | Type | Description |
|---|---|---|
|`name`|string|Snippet name|
|`description`|string|Snippet description|
|`arguments`|array|Selector argument list; order determines the `generator` argument order|
|`generator`|function|Returns the value to save or insert|
|`output`|string|Output filename when run standalone|

## Use In XUI

```lua
{
    cell = "TitleValue";
    label = "Target App";
    key = "target_app";
    snippet = "snippets/app.snippet";
};
```

After selection, the `generator` return value is saved to `target_app`. `.snippet` files can call APIs listed in `format.md` under APIs Available Inside XUI.

## Selector Arguments

Common fields:

| Field | Type | Description |
|---|---|---|
|`type`|string|Selector type|
|`title`|string|Selector page title|
|`subtitle`|string|Selector page description|
|`default`|any|Default value; some image/color selectors do not support it|

Selector types:

| `type` | Return Value | Description |
|---|---|---|
|`app`|string|Single app Bundle ID|
|`apps`|string array|Multiple app Bundle IDs, preserving user order|
|`key`|string|Virtual key code, such as `HOME`|
|`loc`|table|`{ latitude = number, longitude = number }`|
|`pos`|array|`{ x, y }`|
|`color`|integer|`0xRRGGBB`|
|`poscolor`|array|`{ x, y, 0xRRGGBB }`|
|`poscolors`|2D array|Multiple `{ x, y, 0xRRGGBB }` groups|
|`rect`|array|`{ left, top, right, bottom }`|

## Common Templates

### Single App

```lua
return {
    name = "Select App";
    arguments = {
        {
            type = "app";
            default = xui.get("com.example.demo", "target_app");
        };
    };
    generator = function(bundle_id)
        return bundle_id
    end;
}
```

### Multi-Point Colors

```lua
return {
    name = "Multi-Point Colors";
    arguments = {
        { type = "poscolors"; title = "Pick Multiple Positions And Colors" };
    };
    generator = function(poscolors)
        local lines = {}
        for _, item in ipairs(poscolors) do
            lines[#lines + 1] = string.format("    { %d, %d, 0x%06x },", item[1], item[2], item[3] & 0x00ffffff)
        end
        return "{\n" .. table.concat(lines, "\n") .. "\n}"
    end;
}
```

### Region

```lua
return {
    name = "Select Region";
    arguments = {
        { type = "rect"; title = "Select Region" };
    };
    generator = function(rect)
        return rect
    end;
}
```

## Standalone Use

When placed under the main `snippets/` directory, snippets are available from the App code editor. After setting `output`, snippets placed under `lua/scripts/` can also run standalone; text returned by `generator` is written to the `output` file in the same directory.
