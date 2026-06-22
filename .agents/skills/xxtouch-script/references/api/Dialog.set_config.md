# Dialog:set_config

Purpose: Configure the save filename for dialog configuration.

## Signature
```lua
dialog_object = dialog_object:set_config(config_name)
```

## Example
```lua
dialog():set_config('config_name'):show()
```

## Parameters
- config_name
    string, the save name for option configuration on the dialog object.

## Returns
- dialog_object
    Dialog, returns the dialog itself.

## Notes
After the dialog is shown, pressing Submit saves configuration options; the next time it is shown, saved configuration is selected by default.
The configuration is saved as a file under `/private/var/mobile/Media/1ferver/uicfg/<config_name>.xcfg`.
