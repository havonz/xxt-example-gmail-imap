# lunix

Source: https://xxtouch.app/assets/files/lunix-a491331e03b45cb97fcf546b9dcb2eb4.pdf

## Require

```lua
local unix = require 'unix'
```

Use for Unix ownership and permission operations when XXTouch `sys.lchown_r`, `sys.lchmod_r`, or `sys.lchownmod_r` do not fit.

## Change Ownership And Mode

```lua
local unix = require 'unix'

local target = XXT_HOME_PATH..'/1ferver.conf'
unix.chown(target, 501, 501)
unix.chmod(target, 0x1a4) -- octal 0644
```

## Recursive XXTouch Alternative

```lua
-- Prefer these when changing a whole tree under an owned path.
sys.lchown_r(XXT_HOME_PATH..'/some-dir', 501, 501)
sys.lchmod_r(XXT_HOME_PATH..'/some-dir', 0x1ed) -- octal 0755
sys.lchownmod_r(XXT_HOME_PATH..'/some-dir', 501, 501, 0x1ed)
```

## Return Handling

```lua
local unix = require 'unix'

local ok, err = unix.chmod(XXT_HOME_PATH..'/1ferver.conf', 0x1a4)
if ok == nil then
    return nil, err
end
```

## Notes

- Permission changes can break scripts or app data. Use only on paths the script owns or the user explicitly names.
- Prefer symbolic explanation in comments when using numeric modes.
- Avoid hardcoded `/var/mobile/Media/1ferver`; use `XXT_HOME_PATH`.
- Numeric modes in these examples are hexadecimal representations of common octal permissions: `0x1a4` is `0644`, `0x1ed` is `0755`.
