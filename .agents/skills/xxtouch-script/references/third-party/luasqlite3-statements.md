# LuaSQLite3 Statement Slice

Source: https://lua.sqlite.org/home/doc/tip/doc/lsqlite3.wiki

Use prepared statements for repeated queries or user-provided values. XXTouch handbook examples import `sqlite3`; upstream lsqlite3 docs use the same API shape with `lsqlite3`.

## Prepared Query

```lua
local sqlite3 = require 'sqlite3'

local db = assert(sqlite3.open(XXT_RES_PATH..'/data.db'))
local stmt = assert(db:prepare('select id, name from items where id > ? order by id'))
stmt:bind_values(10)

local rows = {}
for row in stmt:nrows() do
    rows[#rows + 1] = row
end

stmt:finalize()
db:close()
```

## Insert With Bind

```lua
local sqlite3 = require 'sqlite3'

local db = assert(sqlite3.open(XXT_RES_PATH..'/data.db'))
assert(db:exec('create table if not exists items(id integer primary key, name text)') == sqlite3.OK)

local stmt = assert(db:prepare('insert into items(name) values(?)'))
stmt:bind_values('demo')
local rc = stmt:step()
stmt:finalize()

local id = db:last_insert_rowid()
db:close()

if rc ~= sqlite3.DONE then
    return nil, 'insert failed'
end
```

## Transaction For Multiple Writes

```lua
local sqlite3 = require 'sqlite3'

local db = assert(sqlite3.open(XXT_HOME_PATH..'/items.db'))
assert(db:exec('create table if not exists items(id integer primary key, name text)') == sqlite3.OK)
assert(db:exec('begin immediate') == sqlite3.OK)

local ok, err = pcall(function()
    local stmt = assert(db:prepare('insert into items(name) values(?)'))
    for _, name in ipairs({'a', 'b', 'c'}) do
        stmt:bind_values(name)
        assert(stmt:step() == sqlite3.DONE)
        stmt:reset()
    end
    stmt:finalize()
end)

if ok then
    db:exec('commit')
else
    db:exec('rollback')
end
db:close()

if not ok then
    return nil, err
end
```

## Named Bind

```lua
local stmt = assert(db:prepare('select id from items where name = :name'))
stmt:bind_names{[':name'] = 'demo'}
local row = stmt:nrows()()
stmt:finalize()
```

## Useful Statement APIs

- `db:prepare(sql) -> stmt`
- `stmt:bind(n, value)` or `stmt:bind_values(...)`
- `stmt:bind_names{ [':name'] = value }`
- `stmt:step() -> sqlite3.ROW | sqlite3.DONE | error_code`
- `stmt:nrows()` iterates named row tables.
- `stmt:rows()` iterates array row tables.
- `stmt:get_value(n)` uses zero-based column indexes.
- `stmt:reset()` reuses the statement with current bindings.
- `stmt:finalize()` closes the statement.

## Notes

- Finalize statements before closing the database.
- Use binds instead of concatenating user-provided values into SQL.
- Wrap multiple writes in a transaction when performance matters.
- On `sqlite3.BUSY`, retry only when the surrounding transaction rules are clear.
- Call `stmt:reset()` before reusing a statement after `stmt:step()`.
