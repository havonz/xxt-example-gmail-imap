# key.down / key.up / key.press

Purpose: Keys/chords/key codes

## Signature
```lua
key.down(key_code)
key.up(key_code)
key.press(key_code)
```

## Example
```lua
key.press("HOMEBUTTON")
key.press("LOCK")
key.press("RETURN")

key.down("HOMEBUTTON")
sys.msleep(1000)
key.up("HOMEBUTTON")

key.press("HOMEBUTTON")
key.press("HOMEBUTTON")

key.down("LEFTCOMMAND")
sys.msleep(30)
key.press("V")
sys.msleep(30)
key.up("LEFTCOMMAND")

key.down("LEFTCOMMAND")
sys.msleep(30)
key.press("[")
sys.msleep(30)
key.up("LEFTCOMMAND")

key.down("LEFTCOMMAND")
sys.msleep(30)
key.press("A")
sys.msleep(30)
key.up("LEFTCOMMAND")
sys.msleep(100)
key.press("BACKSPACE")

key.press("VOLUMEUP")
key.press("VOLUMEDOWN")
key.press("SHOW_HIDE_KEYBOARD")

key.down("LOCK")
sys.msleep(100)
key.press("HOMEBUTTON")
sys.msleep(100)
key.up("LOCK")

key.down("LEFTCOMMAND")
sys.msleep(50)
key.press(" ")
sys.msleep(50)
key.up("LEFTCOMMAND")

key.down("LEFTCONTROL")
sys.msleep(50)
key.press("SPACE")
sys.msleep(50)
key.up("LEFTCONTROL")
```

## Parameters
- key_code
    string, see the key code table below. You can also pass an input character directly, such as `"["`, `" "`, or `"A"`.

## Notes
`key.press` automatically presses and releases a key. `key.down` must be paired with `key.up`; otherwise, the key may remain pressed after the script terminates.
iOS shortcuts usually use Command, not Ctrl. Switching input methods commonly uses `LEFTCOMMAND + " "` on iOS 7/8 or `LEFTCONTROL + "SPACE"` on iOS 9+. Prefer named key codes when stability across keyboard layouts is needed.

## Supported Key Codes

Letter keys:
```text
A B C D E F G H I J K L M N O P Q R S T U V W X Y Z
```

Number keys:
```text
1 2 3 4 5 6 7 8 9 0
```

Function keys:
```text
F1 F2 F3 F4 F5 F6 F7 F8 F9 F10 F11 F12
```

Other keys:
```text
RETURN             Return
ESCAPE             ESC
BACKSPACE          Backspace
TAB                Tab
SPACE              Space
HYPHEN             - or _
EQUAL              = or +
BRACKETOPEN        [ or {
BRACKETCLOSE       ] or }
BACKSLASH          \ or |
SEMICOLON          ; or :
QUOTATION          single quote or double quote
ACCENT             ` or ~
COMMA              , or <
DOT                . or >
SLASH              / or ?
CAPSLOCK           Caps Lock
PAUSE
INSERT
HOME               Keyboard Home, not the same as the iOS device Home button
PAGEUP
DELETE
END
PAGEDOWN
RIGHTARROW         Right
LEFTARROW          Left
DOWNARROW          Down
UPARROW            Up
LEFTCONTROL        Left Ctrl
LEFTSHIFT          Left Shift
LEFTALT            Left Alt
LEFTCOMMAND        Left Command
RIGHTCONTROL       Right Ctrl
RIGHTSHIFT         Right Shift
RIGHTALT           Right Alt
RIGHTCOMMAND       Right Command
LOCK               Lock screen / Power key
HOMEBUTTON         iOS device Home button
FORWARD            Multimedia next track
REWIND             Multimedia previous track
FORWARD2           Alternate multimedia next track key
REWIND2            Alternate multimedia previous track key
EJECT
PLAYPAUSE          Multimedia play/pause
MUTE               Mute
VOLUMEUP           Volume +
VOLUMEDOWN         Volume -
SPOTLIGHT          Spotlight
BRIGHTUP           Screen brightness +
BRIGHTDOWN         Screen brightness -
SHOW_HIDE_KEYBOARD Hide/show keyboard
```
