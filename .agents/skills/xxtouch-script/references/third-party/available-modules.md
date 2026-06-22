# Available Third-Party Require Names

This is a capability map, not a full API reference. Open the linked local note before using a module.

| Library | Require | Local note | Notes |
| --- | --- | --- |
| LuaSocket | `require "socket"` | `luasocket.md` | TCP/UDP sockets and DNS. Prefer `http` for normal HTTP requests. |
| LuaSocket HTTP | `require "socket.http"` | `luasocket-http-ftp.md` | Legacy HTTP client with LTN12 sinks/sources. No HTTPS by itself. |
| LuaSocket FTP | `require "socket.ftp"` | `luasocket-http-ftp.md` | Legacy FTP client. Prefer XXTouch `ftp` for normal transfers. |
| LuaSocket URL | `require "socket.url"` | `luasocket-dns-url.md` | URL parse/build/escape helpers. |
| LTN12 | `require "ltn12"` | `luasocket-http-ftp.md` | Source/sink/pump helpers used by LuaSocket protocols. |
| MIME | `require "mime"` | `luasocket-http-ftp.md` | Base64 and MIME helpers often used with LuaSocket. |
| LuaSSL | `require "ssl"` | `luassl.md` | TLS support for socket workflows. Prefer high-level HTTP clients. |
| lua-openssl | `require "openssl"` | `lua-openssl.md`, `lua-openssl-reference.md` | OpenSSL bindings; use only for explicit crypto/TLS tasks. |
| LPeg | `require "lpeg"` | `lpeg.md`, `lpeg-patterns.md`, `lpeg-captures.md` | Pattern grammar parsing. |
| SLAXML | `require "slaxml"` or `require "slaxdom"` | `slaxml.md` | XML streaming parse, DOM parse, and XML serialization. |
| lyaml | `require "lyaml"` | `lyaml.md` | YAML load/dump. Prefer JSON/plist unless YAML is required. |
| LuaFileSystem | `require "lfs"` | `luafilesystem.md`, `luafilesystem-*.md` | Directory iteration, file attributes, current directory. Prefer `file` for simple file operations. |
| XXTouch UI element API | `require "ui_element"` | `ui_element.md` | Element query and action automation. Prefer this for semantic UI operations; prefer `touch` for fixed-position taps. |
| LuaCJSON | `require "cjson"` or `require "cjson.safe"` | `luacjson.md`, `luacjson-options.md` | JSON codec. Prefer global `json` unless `cjson` behavior is specifically needed. |
| lua-iconv | `require "iconv"` | `luaiconv.md` | Encoding conversion. |
| LuaSQLite3 | `require "sqlite3"` | `luasqlite3.md`, `luasqlite3-statements.md` | SQLite database access. Prefer current handbook examples over old `lsqlite3` mentions. |
| lcurl | `require "lcurl"` or `require "curl.safe"` | `lcurl.md`, `lcurl-easy.md` | libcurl wrapper. Prefer global `http`/`ftp` for ordinary transfers. |
| lunix | `require "unix"` | `lunix.md` | Unix file ownership and permission helpers. |
| lua-posix | `require "posix"` | `lua-posix.md` | POSIX bindings. Use only when documented XXTouch APIs are insufficient. |
| cffi-lua | `require "ffi"` | `cffi-lua.md`, `cffi-lua-reference.md` | FFI access. High risk; avoid unless explicitly requested. |
| lobjc | `require "objc"` | `lobjc.md`, `lobjc-objc-bridge.md` | Objective-C bridge. Prefer `fork_dostring` for risky isolated calls. |
| lua-ev | `require "ev"` | `lua-ev.md` | Event loop library. |
| lua-archive | `require "archive"` | `lua-archive.md` | Archive handling. Prefer `file.zip` / `file.unzip` for ZIP. |
| lua-path | `require "path"` | `lua-path.md` | Path manipulation. |
| lua-zip | `require "zip"` | `lua-zip.md` | ZIP handling. XXTouch alias differs from upstream `brimworks.zip`; prefer `file.zip` / `file.unzip`. |
| lua-websockets | `require "websocket"` | `lua-websockets.md` | WebSocket client/server workflows. |
| captcha-recognizer wrapper | `require "captcha_recognizer"` | `captcha_recognizer.md` | Slider captcha recognition via ONNX Runtime; depends on model files under `models/captcha_recognizer`. |
| ddddocr wrapper | `require "ddddocr"` | `ddddocr.md` | OCR, detection, and slider helpers via ONNX Runtime and `image.cv`. |
| PaddleOCR ONNX wrapper | `require "paddleocr_onnx"` | `paddleocr_onnx.md` | PaddleOCR text detection/recognition with `det.onnx`, `rec.onnx`, and `dict.txt`. |
| YOLO ONNX wrapper | `require "yolo_onnx"` | `yolo_onnx.md` | YOLO detect/classify/OBB through ONNX Runtime; profile support for seg/pose/track. |
| YOLO CoreML wrapper | `require "yolo_coreml"` | `yolo_coreml.md` | YOLO detect/classify/OBB through CoreML; supports cached model compilation. |
