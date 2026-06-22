# sys.free_disk_space

Purpose: Free storage

## Signature
```lua
free_space = sys.free_disk_space([mount_point])
```

## Example
```lua
sys.alert(
    'Current remaining system space\n'..sys.free_disk_space('/')..'MB\n\n'..
    'Current remaining user space\n'..sys.free_disk_space('/var')..'MB'
)
```

## Parameters
- mount_point
    string, valid default values are `"/var"` or `"/"`, representing user space and system space respectively. Other values may exist when external storage such as a memory card is present.

## Returns
- free_space
    number, current unused storage space of the device, in MB.
