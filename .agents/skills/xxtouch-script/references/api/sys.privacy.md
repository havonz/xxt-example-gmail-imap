# sys.privacy

Purpose: Read/set system privacy switches

Version requirement: XXTouch later than 20260529 is required.

## Signature
```lua
allow = sys.user_tracking()
success = sys.set_user_tracking(allow)

allow = sys.personalized_advertising()
success = sys.set_personalized_advertising(allow)

enabled = sys.location_services()
success = sys.set_location_services(enabled)
```

## Example
```lua
local allowTracking = sys.user_tracking()
if allowTracking ~= nil then
    sys.set_user_tracking(false)
    sys.set_user_tracking(allowTracking)
end

local allowAds = sys.personalized_advertising()
if allowAds ~= nil then
    sys.set_personalized_advertising(allowAds)
end

local locationEnabled = sys.location_services()
if locationEnabled ~= nil then
    sys.set_location_services(locationEnabled)
end
```

## Parameters
- allow
    boolean. For user tracking, `true` means apps may request tracking permission. For personalized advertising, `true` means personalized ads are allowed.
- enabled
    boolean. `true` enables system Location Services.

## Returns
- allow
    boolean | nil. Returns `nil` if the current setting cannot be read.
- enabled
    boolean | nil. Returns `nil` if the current setting cannot be read.
- success
    boolean, whether the setting operation was accepted.
