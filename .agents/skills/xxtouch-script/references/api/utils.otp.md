# utils.totp_next / utils.hotp_counter / utils.hotp_next

Purpose: Generate TOTP/HOTP one-time passwords

Version requirement: XXTouch later than 20260107 is required.

## Signature
```lua
code, err = utils.totp_next(timestamp, url[, secret])
code, err = utils.hotp_counter(counter, url[, secret])
code, err = utils.hotp_next(url[, secret])
```

## Examples
```lua
local totp_url = "otpauth://totp/Demo:alice?secret=JBSWY3DPEHPK3PXP&issuer=Demo&digits=6&period=30&algorithm=SHA1"

local totp_code, totp_err = utils.totp_next(-1, totp_url)
if totp_code then
    nLog(totp_code)
else
    nLog(totp_err)
end

local hotp_url = "otpauth://hotp/Demo:alice?secret=JBSWY3DPEHPK3PXP&issuer=Demo&digits=6&algorithm=SHA1"

local code1, err1 = utils.hotp_counter(1, hotp_url)
local code2, err2 = utils.hotp_next(hotp_url)
```

## TOTP
`utils.totp_next(timestamp, url[, secret])` generates a time-based one-time password.

### Parameters
- timestamp
    integer, Unix timestamp in seconds. Pass `-1` to use the current time.
- url
    string, TOTP URL in the `otpauth://totp/...` format.
- secret
    string, optional Base32 secret. When provided, it is used instead of the secret in `url`.

### Returns
- code
    string, generated one-time password.
- err
    string, error message when generation fails.

## HOTP with a specified counter
`utils.hotp_counter(counter, url[, secret])` generates a counter-based one-time password using the specified counter.

### Parameters
- counter
    integer, HOTP counter.
- url
    string, HOTP URL in the `otpauth://hotp/...` format.
- secret
    string, optional Base32 secret. When provided, it is used instead of the secret in `url`.

### Returns
- code
    string, generated one-time password.
- err
    string, error message when generation fails.

## HOTP next code
`utils.hotp_next(url[, secret])` generates the next counter-based one-time password for the URL.

Use `utils.hotp_counter(counter, url[, secret])` when the script needs to control the counter explicitly.

### Parameters
- url
    string, HOTP URL in the `otpauth://hotp/...` format.
- secret
    string, optional Base32 secret. When provided, it is used instead of the secret in `url`.

### Returns
- code
    string, generated one-time password.
- err
    string, error message when generation fails.

## URL fields
- `secret`
    Base32 secret.
- `digits`
    OTP code length. Common value: `6`.
- `algorithm`
    HMAC algorithm. Supported values: `SHA1`, `SHA256`, `SHA512`.
- `period`
    TOTP period in seconds. Common value: `30`. TOTP only.

## Errors
On failure, these functions return `nil, err`.

Common errors:
- `invalid otpauth totp url`
- `invalid otpauth hotp url`
- `missing secret`
- `invalid base32 secret`

