# device.network_switches

Purpose: Network switches

## Signature
```lua
device.turn_on_wifi()
device.turn_off_wifi()

device.turn_on_data()
device.turn_off_data()

device.turn_on_bluetooth()
device.turn_off_bluetooth()

device.turn_on_airplane()
device.turn_off_airplane()

switch_state, status_description = device.is_vpn_on()
device.turn_on_vpn()
device.turn_off_vpn()
```

## Example
```lua
device.turn_off_wifi()
device.turn_on_data()

local vpn_on = device.is_vpn_on()
if not vpn_on then
    device.turn_on_vpn()
end
```

## Returns
- switch_state
    boolean, returns `true` when the VPN switch is on, either connecting or connected successfully; otherwise returns `false`.
- status_description
    string | nil, when the VPN switch state is `true`, returns a string describing the current VPN connection state.

## Notes
Turning on Airplane Mode disconnects all wireless network connections. Turning it off restores wireless network connections.
`device.turn_on_vpn()` only attempts to connect the VPN currently selected by the system. It has no effect when no VPN is selected.
`device.turn_on_vpn()` and `device.turn_off_vpn()` have limited stability. Prefer `vpnconf` for more complex VPN tasks.
When the VPN is connecting but not yet connected successfully, the switch state returned by `device.is_vpn_on()` is also `true`.
