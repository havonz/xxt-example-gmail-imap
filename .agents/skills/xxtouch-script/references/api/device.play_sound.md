# device.play_sound

Purpose: Play sound in background

## Signature
```lua
device.play_sound(sound_file_path)
```

## Example
```lua
device.play_sound("/var/mobile/song.mp3")
sys.msleep(205 * 1000) -- Wait 205 seconds (3 minutes 25 seconds).
```

## Parameters
- sound_file_path
    string, the absolute path to the sound file. Supports `mp3`, `wav`, and `aac` audio formats.

## Notes
Plays a sound in the background.
This function does not affect script execution, and the sound stops automatically when the script stops. To play the complete sound, make sure the script delays its exit.
