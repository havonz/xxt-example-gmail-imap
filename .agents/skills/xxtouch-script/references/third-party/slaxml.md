# SLAXML

Use when an XXTouch script must parse or serialize XML. Prefer `plist` for plist files and `json` for JSON; use SLAXML only for real XML.

## Require
```lua
local SLAXML = require 'slaxml'  -- SAX/event parser
local SLAXDOM = require 'slaxdom' -- DOM parse + XML serialization
```

## DOM Round Trip
```lua
local xml = assert(file.reads(path))
local doc = SLAXDOM:dom(xml, { stripWhitespace = true })
-- modify doc.root / node.kids / node.attr
local out = SLAXDOM:xml(doc, { indent = 2, sort = true })
assert(file.writes(path, out))
```

DOM nodes commonly expose `type`, `name`, `kids`, `attr`, `root`, and text node `value`. Use `SLAXDOM:dom(xml, { simple = true })` when parent links and convenience indexes are not needed.

## Streaming Parse
```lua
local parser = SLAXML:parser({
    startElement = function(name, nsURI, nsPrefix) end,
    attribute = function(name, value, nsURI, nsPrefix) end,
    closeElement = function(name, nsURI) end,
    text = function(text, cdata) end,
})
parser:parse(xml, { stripWhitespace = true })
```

Use streaming callbacks for large XML or when only a few fields are needed. Use DOM for edit-and-write workflows.
