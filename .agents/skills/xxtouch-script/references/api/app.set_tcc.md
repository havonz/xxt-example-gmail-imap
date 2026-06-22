# app.set_tcc

Purpose: App TCC permissions

## Signature
```lua
success, previous_state_value = app.set_tcc(bundle_identifier, service_identifier, state_value)
```

## Example
```lua
app.set_tcc("com.apple.SafariViewService", "kTCCServicePasteboard", 2)
```

## Parameters
- bundle_identifier
    string
- service_identifier
    string

    ```lua
    kTCCServiceAccessibility
    kTCCServiceAddressBook
    kTCCServiceAppleEvents
    kTCCServiceCalendar
    kTCCServiceCamera
    kTCCServiceContactsFull
    kTCCServiceContactsLimited
    kTCCServiceDeveloperTool
    kTCCServiceFacebook
    kTCCServiceLinkedIn
    kTCCServiceListenEvent
    kTCCServiceLiverpool
    kTCCServiceLocation
    kTCCServiceMediaLibrary
    kTCCServiceMicrophone
    kTCCServiceMotion
    kTCCServicePhotos
    kTCCServicePhotosAdd
    kTCCServicePostEvent
    kTCCServiceReminders
    kTCCServiceScreenCapture
    kTCCServiceShareKit
    kTCCServiceSinaWeibo
    kTCCServiceSiri
    kTCCServiceSpeechRecognition
    kTCCServiceSystemPolicyAllFiles
    kTCCServiceSystemPolicyDesktopFolder
    kTCCServiceSystemPolicyDeveloperFiles
    kTCCServiceSystemPolicyDocumentsFolder
    kTCCServiceSystemPolicyDownloadsFolder
    kTCCServiceSystemPolicyNetworkVolumes
    kTCCServiceSystemPolicyRemovableVolumes
    kTCCServiceSystemPolicySysAdminFiles
    kTCCServiceTencentWeibo
    kTCCServiceTwitter
    kTCCServiceUbiquity
    kTCCServiceWillow
    kTCCServicePasteboard
    ```

- state_value
    integer, set `state_value` to `-1` to delete the TCC permission for the app identified by `bundle_identifier`.

## Returns
- success
    boolean
- previous_state_value
    integer, `-1` means the app did not previously have this permission entry.
