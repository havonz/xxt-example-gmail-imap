# vpnconf.create / vpnconf.delete / vpnconf.list / vpnconf.select / vpnconf.connect / vpnconf.disconnect / vpnconf.status

Purpose: VPN configuration/connection management

## Create VPN Configuration
```lua
success = vpnconf.create(config_table)
```

### Example
```lua
local success = vpnconf.create{
    dispName = "DemoVPN",
    VPNType = "L2TP",
    server = "vpn.example.com",
    authorization = "your_account",
    password = "your_password",
    secret = "your_shared_secret",
    encrypLevel = 1,
    group = "",
    VPNSendAllTraffic = 1,
}
```

### Parameters
- config_table
    table, describes the VPN configuration to create
    - `dispName`: VPN display name
    - `VPNType`: `"PPTP"`, `"L2TP"`, or `"IPSec"`
    - `server`: server address
    - `authorization`: account
    - `password`: password
    - `secret`: secret, optional for PPTP
    - `encrypLevel`: encryption level, default `1`
    - `group`: group name, default `""`
    - `VPNSendAllTraffic`: whether to send all traffic, default `1`

### Returns
- success
    boolean. Returns true on successful creation, false on failure. Creation failure is usually caused by incomplete or incorrect parameters.

### Notes
Creating IKEv2 configurations is not supported.

## Delete VPN Configuration
```lua
success = vpnconf.delete(display_name_or_vpn_id)
```

### Example
```lua
local success = vpnconf.delete("DemoVPN")
```

### Delete All VPN Configurations
```lua
local vpnlist = vpnconf.list()
if vpnlist then
    for _, v in ipairs(vpnlist) do
        if vpnconf.delete(v.VPNID) then
            sys.log("Deleted successfully: "..v.dispName.."("..v.VPNID..")")
        else
            sys.log("Failed to delete: "..v.dispName.."("..v.VPNID..")")
        end
    end
    sys.alert("Operation complete")
else
    sys.alert("Failed to get VPN list")
end
```

### Parameters
- display_name_or_vpn_id
    string. When multiple VPNs have the same display name, which one is deleted is not guaranteed. Pass the VPNID if exact deletion is needed.

### Returns
- success
    boolean. Returns true on operation success and false on failure. Failure is usually because the specified configuration does not exist.

## Get VPN List
```lua
vpn_list = vpnconf.list()
```

### Returns
- vpn_list
    table or nil. On success, returns an ordered table of current system VPNs. On failure, returns nil.

    ```lua
    {
        {dispName = display_name_1, VPNID = VPNID1},
        {dispName = display_name_2, VPNID = VPNID2},
        ...
    }
    ```

## Select VPN Configuration
```lua
success = vpnconf.select(display_name_or_vpn_id)
```

### Parameters
- display_name_or_vpn_id
    string. When multiple VPNs have the same display name, which one is selected is not guaranteed. Pass the VPNID if exact selection is needed.

### Returns
- success
    boolean. Returns true on operation success and false on failure. Failure is usually because the specified configuration does not exist.

## Connect Current VPN
```lua
success = vpnconf.connect()
```

### Returns
- success
    boolean. Returns true when the operation is started successfully (not when the connection is established), and false on operation failure. Failure is usually because no configuration is selected.

## Disconnect Current VPN
```lua
success = vpnconf.disconnect()
```

### Returns
- success
    boolean. Returns true when the operation is started successfully (not when disconnection is complete), and false on operation failure. Failure is usually because no configuration is selected.

## Get Current VPN Status
```lua
status = vpnconf.status()
```

### Returns
- status
    table or nil. On operation success, returns a status description table. Returns nil when no VPN is selected.

    ```lua
    {
        text = current_status_text_description,
        connected = whether_connected_successfully,
    }
    ```

## Notes
VPNID can be obtained through `vpnconf.list`. After successfully creating a VPN, you usually need to call `vpnconf.select` to select it before calling `vpnconf.connect`.
