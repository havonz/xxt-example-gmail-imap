# utils.add_contacts / utils.remove_all_contacts

Purpose: Add/clear contacts

## Add Contacts
```lua
success = utils.add_contacts({
    {
        firstName = "FirstName1",
        lastName = "LastName1",
        phoneNumbers = {
            "contact1_phone1",
            "contact1_phone2",
        },
        emails = {
            "contact1_email1",
            "contact1_email2",
        },
    },
    ...
})
```

### Example
```lua
utils.add_contacts({
    {
        firstName = "John",
        lastName = "Doe",
        phoneNumbers = {"13800001111", "13800002222"},
        emails = {"john@example.com", "john.doe@example.com"},
    },
})
```

### Parameters
- firstName
    string, contact first name.
- lastName
    string, contact last name.
- phoneNumbers
    table, this person's phone number list.
- emails
    table, this person's email list.

### Returns
- success
    boolean, returns `true` if adding succeeds, or `false` if it fails.

## Remove All Contacts
```lua
success = utils.remove_all_contacts()
```

### Example
```lua
utils.remove_all_contacts()
```

### Returns
- success
    boolean, returns `true` if deletion succeeds, or `false` if it fails.

## Notes
Adding or deleting contacts can take a long time when there are many contacts.
