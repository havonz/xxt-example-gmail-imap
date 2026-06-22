# utils.date

Purpose: Time format/RFC conversion

## Signature
```lua
timestamp = utils.date_from_format(format, date[, options])
timestamp = utils.date_from_rfc1123(rfc1123)
timestamp = utils.date_from_rfc3339(rfc3339)
date = utils.date_to_format(format, timestamp[, options])
rfc1123 = utils.date_to_rfc1123(timestamp)
rfc3339 = utils.date_to_rfc3339(timestamp)
```

## Example
```lua
local ts = utils.date_from_format("EEE, dd MMM yyyy HH:mm:ss ZZZZ", "Mon, 09 Jun 2025 17:40:00 GMT", {
    tz = "GMT",
    locale = "en-US",
})
nLog(utils.date_to_format("EEE, dd MMM yyyy HH:mm:ss ZZZZ", ts, {tz = "PST", locale = "zh-CN"}))
nLog(utils.date_to_format("EEE, dd MMM yyyy HH:mm:ss ZZZZ", 1749490800, {tz = "PST", locale = "en-US"}))
nLog(utils.date_from_rfc1123("Mon, 09 Jun 2025 17:40:00 GMT"))
nLog(utils.date_from_rfc3339("2025-06-09T17:40:00.000Z"))
nLog(utils.date_to_rfc1123(ts))
nLog(utils.date_to_rfc1123(os.time()))
nLog(utils.date_to_rfc3339(ts))
nLog(utils.date_to_rfc3339(os.time()))
```

## Format Placeholders
| Category | Placeholder | Meaning |
| --- | --- | --- |
| Year | `yyyy` / `yy` | 4-digit / 2-digit year |
| Month | `MMMM` / `MMM` | Full month name / abbreviation |
| Month | `MM` / `M` | 2-digit / 1-2 digit month |
| Day | `dd` / `d` | 2-digit / 1-2 digit day |
| Weekday | `EEEE` | Full weekday name |
| Weekday | `E` / `EE` / `EEE` | Weekday abbreviation |
| Weekday | `e` / `ee` | Localized weekday number |
| Hour | `HH` / `H` | 24-hour clock |
| Hour | `hh` / `h` | 12-hour clock |
| AM/PM | `a` | AM / PM |
| Minute | `mm` / `m` | 2-digit / 1-2 digit minute |
| Second | `ss` | 2-digit second |
| Millisecond | `S` / `SS` / `SSS` | Fractional second digits |
| Time zone | `zzzz` | Full time zone name |
| Time zone | `zzz` / `z` | Time zone abbreviation |
| Time zone | `ZZZZZ` | ISO 8601 offset, such as `-07:00` |
| Time zone | `Z` / `ZZ` / `ZZZ` | RFC 822 offset, such as `-0700` |

## Parameters
- format
    string, time format.
- date
    string, time string to parse.
- timestamp
    number, timestamp.
- rfc1123, rfc3339
    string, RFC 1123 / RFC 3339 time text.
- options
    table, optional. `tz` is the time zone and defaults to the system time zone; `locale` is the localization and defaults to the current device locale.

## Returns
- timestamp
    number, timestamp.
- date, rfc1123, rfc3339
    string, formatted time text.
