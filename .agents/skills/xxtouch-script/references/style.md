# XXTouch Lua Style

## Coding Rules

- Use Lua 5.3 syntax.
- XXTouch built-ins are globals; do not require `app`, `sys`, `screen`, `touch`, `image`, `file`, `json`, `http`, `dialog`, `device`, or similar modules.
- Do not name local variables after built-in modules.
- Prefer small functions around actions and screen checks.
- Prefer explicit wait points after UI-changing actions: `sys.msleep(ms)`.
- Keep similarity thresholds conservative. For image matching, avoid values below 90 unless the user explicitly accepts false positives.
- For color matching, choose stable points surrounded by similar colors and use multiple points where possible.

## Validation

- If XXTLanControl MCP tools are available, test scripts on a selected device when the task involves runtime behavior.
- For quick syntax/runtime checks, send a focused snippet or run the target entry script.
- Collect realtime logs when debugging `nLog`, `sys.log`, or runtime errors.
