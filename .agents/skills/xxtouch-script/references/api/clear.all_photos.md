# clear.all_photos

Purpose: Clear local photo library

## Signature
```lua
clear.all_photos()
```

## Notes
Clears all local photos from the photo library. This does not affect iCloud Photo Stream.
This function may take a very long time. Forcibly stopping the script while it is running will make stopping slow, because the script must be forcibly terminated.
Warning: the effect of calling this function is irreversible.
