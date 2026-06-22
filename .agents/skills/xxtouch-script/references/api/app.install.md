# app.install / app.uninstall

Purpose: Install/uninstall apps

## Install IPA
```lua
success = app.install(file_path [, force_install ])
```

### Example
```lua
app.install("/var/mobile/1.ipa", true) -- Force overwrite installation, useful for downgrading an app.

if app.install("/var/mobile/1.ipa") then
    -- Installation succeeded.
else
    -- Installation failed.
end
```

### Parameters
- file_path
    string, absolute path to the app installation package in IPA format.
- force_install
    boolean, optional. Whether to force installation. `true` overwrites the existing app regardless of version, which can be used for downgrades. `false` installs only when the IPA version is newer than the installed version; the installation is skipped when the version is the same or older. Defaults to `false`.

### Returns
- success
    boolean, returns `true` if installation succeeds and `false` if it fails.

### Notes
Installs an IPA package in the background.
Stopping the script before installation completes may leave the app partially installed.
Before calling this function, make sure the AppSync plugin has been installed on the target device.

## Uninstall App
```lua
success = app.uninstall(bundle_identifier)
```

### Example
```lua
if app.uninstall("com.tencent.mqq") then
    -- Uninstallation succeeded.
else
    -- Uninstallation failed.
end
```

### Parameters
- bundle_identifier
    string

### Returns
- success
    boolean, returns `true` if uninstallation succeeds and `false` if it fails.

### Notes
Uninstalls an app in the background.
Stopping the script during uninstallation may leave the app partially uninstalled.
