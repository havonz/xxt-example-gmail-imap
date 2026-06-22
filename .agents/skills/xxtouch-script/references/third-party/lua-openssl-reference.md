# lua-openssl Offline Reference

Sources:
- https://zhaozg.github.io/lua-openssl/index.html
- https://zhaozg.github.io/lua-openssl/modules/digest.html
- https://zhaozg.github.io/lua-openssl/modules/hmac.html
- https://zhaozg.github.io/lua-openssl/modules/cipher.html
- https://zhaozg.github.io/lua-openssl/modules/pkey.html
- https://zhaozg.github.io/lua-openssl/modules/x509.html

Use this file before browsing. It is a compact offline map for the lua-openssl APIs most useful in XXTouch scripts.

## Require And Module Map

```lua
local openssl = require 'openssl'

local digest = openssl.digest
local hmac = openssl.hmac
local cipher = openssl.cipher
local pkey = openssl.pkey
local x509 = openssl.x509
```

Common modules exposed by upstream docs:

| Area | Module | Use |
| --- | --- | --- |
| Hash | `openssl.digest` | SHA/MD digest objects and streaming digest contexts. |
| HMAC | `openssl.hmac` | Message authentication code, one-shot or streaming. |
| Cipher | `openssl.cipher` | EVP symmetric encryption/decryption. |
| Key | `openssl.pkey` | Load keys, sign/verify, encrypt/decrypt, derive. |
| Certificate | `openssl.x509` | Read, export, parse and verify certificates. |
| CSR/CRL | `openssl.x509.req`, `openssl.x509.crl` | Certificate request and revocation list objects. |
| PKCS | `openssl.pkcs12`, `openssl.pkcs7` | PFX/P12 and PKCS#7 containers. |
| TLS | `openssl.ssl` | Low-level TLS contexts; prefer `http`/`lcurl` for HTTP. |
| ASN.1 / OID | `openssl.asn1`, `openssl.x509.name` | Certificate names and structured crypto data. |
| Provider | `openssl.provider` | OpenSSL 3 provider loading/querying. |
| Misc | `openssl.random`, `openssl.hex`, `openssl.base64` | Random bytes and binary encoding helpers. |

## Digest

```lua
local openssl = require 'openssl'

local hex = openssl.digest.digest('sha256', 'message')
local raw = openssl.digest.digest('sha256', 'message', true)
```

Streaming:

```lua
local ctx = openssl.digest.new('sha256')
ctx:update('part-a')
ctx:update('part-b')
local hex = openssl.hex(ctx:final())
```

Useful shapes:

```lua
local md, err = openssl.digest.get('sha256')
local ctx = openssl.digest.new('sha256')
ctx:update(data)
local raw = ctx:final()
local hex = openssl.hex(raw)

-- OpenSSL 3 provider-aware builds may expose:
local fetched, fetch_err = openssl.digest.fetch('SHA256', {provider = 'default'})
```

## HMAC

One-shot:

```lua
local openssl = require 'openssl'

local hex = openssl.hmac.hmac('sha256', 'message', 'secret')
local raw = openssl.hmac.hmac('sha256', 'message', 'secret', true)
```

Streaming:

```lua
local ctx = openssl.hmac.new('sha256', 'secret')
ctx:update('part-a')
ctx:update('part-b')
local hex = ctx:final()
local raw = ctx:final(nil, true)
```

Shapes:

```lua
ctx = openssl.hmac.new(alg, key[, engine])
ok = ctx:update(msg)
result = ctx:final([last[, raw]])
size = ctx:size()
```

## Cipher

Prefer modern authenticated modes when the protocol allows them. Do not invent key/IV formats.

Quick CBC example:

```lua
local openssl = require 'openssl'

local key = string.rep('\0', 32) -- AES-256 key length
local iv = string.rep('\0', 16)
local encrypted = openssl.cipher.encrypt('aes-256-cbc', 'plaintext', key, iv, true)
local decrypted = openssl.cipher.decrypt('aes-256-cbc', encrypted, key, iv, true)
```

Streaming context:

```lua
local ctx = openssl.cipher.new('aes-256-cbc', true, key, iv, true)
local out = {}
out[#out + 1] = ctx:update(chunk1)
out[#out + 1] = ctx:update(chunk2)
out[#out + 1] = ctx:final()
local ciphertext = table.concat(out)
```

Useful shapes:

```lua
algs = openssl.cipher.list([alias])
cipher_obj, err = openssl.cipher.get(alg)
cipher_obj, err = openssl.cipher.fetch(alg[, options])
encrypted = openssl.cipher.encrypt(alg, input, key[, iv[, pad[, engine]]])
decrypted = openssl.cipher.decrypt(alg, input, key[, iv[, pad[, engine]]])
ctx, err = openssl.cipher.new(alg, encrypt[, key[, iv[, pad[, engine]]]])
ctx = openssl.cipher.encrypt_new(alg, key[, iv[, engine[, pad]]])
ctx = openssl.cipher.decrypt_new(alg, key[, iv[, engine[, pad]]])
part = ctx:update(data[, isAAD])
tail = ctx:final()
info = ctx:info()
ctx:padding(boolean)
ctx:ctrl(type, arg)
```

## Public And Private Keys

Exact key-loading helpers vary by key format. Prefer existing project code if present.

Sign and verify:

```lua
local openssl = require 'openssl'

local private_pem = file.reads(XXT_RES_PATH..'/private.pem')
local public_pem = file.reads(XXT_RES_PATH..'/public.pem')
local private = assert(openssl.pkey.read(private_pem, true))
local public = assert(openssl.pkey.read(public_pem, false))

local signature = assert(private:sign('message', 'sha256'))
local ok = public:verify('message', signature, 'sha256')
```

Useful shapes from upstream docs:

```lua
key = openssl.pkey.read(pem_or_der[, private[, format[, passphrase]]])
signature = key:sign(data[, md_alg[, userId]])
ok = key:verify(data, signature[, md_alg[, userId]])
encrypted = key:encrypt(data)
decrypted = key:decrypt(data)
shared = key:derive(private_key, peer_key[, engine])
sealed, encrypted_key, iv = key:seal(data[, cipher_alg])
opened = key:open(encrypted_key, iv[, cipher_alg])
```

Notes:

- Use `sha256` unless the protocol or test vector requires another digest.
- PEM/DER, private/public, padding, and SM2 user ID must match the external protocol.
- Always verify with a known test vector before deploying crypto changes.

## X.509 Certificates

Read and inspect:

```lua
local openssl = require 'openssl'

local cert_pem = assert(file.reads(XXT_RES_PATH..'/cert.pem'))
local cert = assert(openssl.x509.read(cert_pem, 'pem'))
local parsed = cert:parse()
sys.log(parsed.subject, parsed.issuer)
```

Common shapes:

```lua
cert = openssl.x509.read(input[, format])
pem = cert:export(['pem'|'der'])
info = cert:parse([default])
pubkey = cert:pubkey()
name = cert:subject()
name = cert:issuer([asobject])
digest = cert:digest([md_alg])
ok = cert:check(cacerts, untrusted[, purpose])
ok = cert:check(pkey)
ok = cert:check_host(host)
ok = cert:check_email(email)
ok = cert:check_ip_asc(ip)
message = openssl.x509.verify_cert_error_string(code)
```

## Random And Encoding

```lua
local openssl = require 'openssl'

local bytes = openssl.random(32)
local hex = openssl.hex(bytes)
```

Use `openssl.random(length)` for keys, IVs, nonces, and tokens. Do not use `math.random` for cryptographic values.

## Operational Rules

- Prefer XXTouch built-ins for simple hash/HMAC and HTTP/TLS.
- For crypto interop, ask for sample input/output or test vectors.
- Decide binary-vs-hex/base64 at module boundaries and keep it explicit.
- Do not log secrets, private keys, bearer tokens, raw P12 content, or decrypted payloads.
- Keep this code in a small helper module and expose task-level functions, not OpenSSL internals.
