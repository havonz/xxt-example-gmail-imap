# jbroot / rootfs

Purpose: Convert system root/jailbreak root paths

## System Root to Jailbreak Root
```lua
jailbreak_root_path = jbroot(system_root_path)
```

### Example
```lua
nLog(jbroot('/')) -- /var/containers/Bundle/Application/.jbroot-XXXXXXXXXXXXXXXX/
```

### Parameters
- system_root_path
    string, path under the system root

### Returns
- jailbreak_root_path
    string, the jailbreak root path corresponding to the `system_root_path` argument

## Jailbreak Root to System Root
```lua
system_root_path = rootfs(jailbreak_root_path)
```

### Example
```lua
nLog(rootfs('/var/containers/Bundle/Application/.jbroot-XXXXXXXXXXXXXXXX/')) -- /
```

### Parameters
- jailbreak_root_path
    string, path under the jailbreak root

### Returns
- system_root_path
    string, the system root path corresponding to the `jailbreak_root_path` argument

## Notes
In roothide and rootless versions of XXTouch, `jbroot` maps a path under the system root to the absolute path with the same name under the jailbreak root, and `rootfs` maps a path under the jailbreak root back to the corresponding system root path.
In rootful or TrollStore versions of XXTouch, both functions return the passed argument unchanged.
