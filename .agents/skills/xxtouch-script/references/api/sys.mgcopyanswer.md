# sys.mgcopyanswer

Purpose: Query system value

## Signature
```lua
answer = sys.mgcopyanswer(question)
```

## Example
```lua
sys.alert("Device serial number: "..sys.mgcopyanswer("SerialNumber"))
sys.alert("Device IMEI: "..sys.mgcopyanswer("InternationalMobileEquipmentIdentity"))
sys.alert("Device MEID: "..sys.mgcopyanswer("MobileEquipmentIdentifier"))
sys.alert(string.format('Device ECID: %016X', sys.mgcopyanswer('UniqueChipID')))

local infos = sys.mgcopyanswer('CarrierBundleInfoArray')
if type(infos) == 'table' and #infos > 0 then
    local info = infos[1]
    if type(info.InternationalMobileSubscriberIdentity) == 'string' then
        sys.alert("Carrier IMSI: "..info.InternationalMobileSubscriberIdentity)
    else
        sys.alert("Unable to read carrier IMSI. Make sure the SIM card is inserted correctly.")
    end
    if type(info.IntegratedCircuitCardIdentity) == 'string' then
        sys.alert("Carrier ICCID: "..info.IntegratedCircuitCardIdentity)
    else
        sys.alert("Unable to read carrier ICCID. Make sure the SIM card is inserted correctly.")
    end
else
    sys.alert("Unable to read carrier information. Make sure the SIM card is inserted correctly.")
end

local phone_number = sys.mgcopyanswer('PhoneNumber')
if sys.mgcopyanswer('SIMTrayStatus') == 'kCTSIMSupportSIMTrayInsertedWithSIM' and type(phone_number) == 'string' then
    sys.alert("Phone number: "..phone_number)
else
    sys.alert("Unable to read phone number. Make sure the SIM card is inserted correctly.")
end
```

## Parameters
- question
    string, question name. For some question names, see `MobileGestalt.h`.

## Returns
- answer
    string | table | number | integer | boolean | nil, the system response. Returns `nil` if the question is unsupported.

## Notes
Gets certain system information through the underlying MGCopyAnswer.
Keywords: get system information, read device information, device identifiers, read phone number.
