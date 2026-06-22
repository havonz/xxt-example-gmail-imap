# LuaSQLite3

Source: https://lua.sqlite.org/home/doc/tip/doc/lsqlite3.wiki

## Require

```lua
local sqlite3 = require 'sqlite3'
```

Use only when the script must read or write SQLite databases directly. Close database handles explicitly.

Current handbook examples use `require 'sqlite3'`. If older project notes mention `require 'lsqlite3'`, prefer `sqlite3` unless the target script already proves otherwise.

## Topic Slice

- Prepared statements, bind, step, row iteration: `luasqlite3-statements.md`.

## Open And Query

```lua
local sqlite3 = require 'sqlite3'

local db = assert(sqlite3.open(XXT_RES_PATH..'/data.db'))
local rows = {}

db:exec('select id, name from items', function(_, ncols, values, names)
    rows[#rows + 1] = {
        id = values[1],
        name = values[2],
    }
    return sqlite3.OK
end)

db:close()
sys.log(json.encode(rows))
```

## Common APIs

- `sqlite3.open(filename[, flags]) -> db | nil, code, message`
- `sqlite3.open_memory() -> db`
- `db:exec(sql[, callback[, udata]]) -> sqlite3.OK | error_code`
- `db:nrows(sql)` iterates named row tables.
- `db:rows(sql)` iterates array row tables.
- `db:errmsg()` and `db:errcode()` expose the latest database error.
- `db:last_insert_rowid()` returns the last inserted rowid.
- `db:close()` closes the handle.

## Notes

- Prefer parameterized APIs if writing user-provided values; avoid string-concatenated SQL.
- Keep queries narrow; large result sets can block the script.
- Device system databases may require permissions and may change schema between iOS versions.
- Always call `db:close()` when done.
