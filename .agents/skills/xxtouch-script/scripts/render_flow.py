#!/usr/bin/env python3
"""Render completed assist-flow color steps into XXTouch Lua flow code."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Any

from xxtouch_assist_common import (
    COMPLETED_STATUSES,
    collect_points,
    load_json,
    lua_name,
    lua_string,
    point_line,
    render_tap,
    result_tap,
    unwrap_result,
)


def step_enabled(step: dict[str, Any], statuses: set[str], step_ids: set[str], all_steps: bool) -> bool:
    if step_ids and str(step.get("stepId", "")) not in step_ids:
        return False
    if all_steps:
        return True
    status = str(step.get("status", "")).strip().lower()
    return status in statuses and step.get("result") is not None


def collect_screens(manifest: dict[str, Any], args: argparse.Namespace) -> tuple[list[dict[str, Any]], list[dict[str, str]]]:
    steps = manifest.get("steps")
    if not isinstance(steps, list):
        raise SystemExit("manifest.steps must be an array")
    statuses = {status.strip().lower() for status in args.status if status.strip()} or COMPLETED_STATUSES
    step_ids = set(args.step or [])
    screens: list[dict[str, Any]] = []
    skipped: list[dict[str, str]] = []
    used_names: set[str] = set()
    for step in steps:
        if not isinstance(step, dict) or not step_enabled(step, statuses, step_ids, args.all_steps):
            continue
        meta, result = unwrap_result(step)
        points = collect_points(result, include_records=not args.no_records)
        if not points:
            skipped.append({"stepId": str(step.get("stepId", "")), "reason": "no color points"})
            continue
        base_name = lua_name(None, meta)
        name = base_name
        suffix = 2
        while name in used_names:
            name = f"{base_name}_{suffix}"
            suffix += 1
        used_names.add(name)
        screens.append(
            {
                "name": name,
                "title": str(step.get("title") or step.get("stepId") or ""),
                "points": points,
                "tap": result_tap(result),
            }
        )
    return screens, skipped


def render_xxtdo(manifest: dict[str, Any], screens: list[dict[str, Any]], args: argparse.Namespace) -> str:
    flow_name = args.name or str(manifest.get("flowId") or "assist_flow")
    lines = [
        "local XXTDo = require 'XXTDo'",
        "",
        "XXTDo.runloop {",
        f"    name = {lua_string(flow_name)},",
        f"    csim = {args.similarity},",
        f"    interval_ms = {args.interval_ms},",
        "    log = sys.log,",
        "",
    ]
    for screen in screens:
        lines.extend(
            [
                "    {",
                f"        name = {lua_string(screen['name'])},",
                f"        csim = {args.similarity},",
            ]
        )
        lines.extend(point_line(point, "        ") for point in screen["points"])
        lines.append("        run = function()")
        lines.extend(render_tap(screen["tap"], "            "))
        lines.extend(["        end,", "    },", ""])
    lines.append("}")
    return "\n".join(lines)


def render_plain(manifest: dict[str, Any], screens: list[dict[str, Any]], args: argparse.Namespace) -> str:
    flow_name = lua_name(args.name or str(manifest.get("flowId") or "assist_flow"))
    lines = [f"-- {flow_name}", "screen.init(0)", ""]
    for screen in screens:
        func = f"match_{screen['name']}"
        lines.extend([f"local function {func}()", "    screen.keep()", "    local ok = screen.is_colors({"])
        lines.extend(point_line(point, "        ") for point in screen["points"])
        lines.extend([f"    }}, {args.similarity})", "    screen.unkeep()", "    return ok", "end", ""])

    lines.append("while true do")
    for index, screen in enumerate(screens):
        prefix = "if" if index == 0 else "elseif"
        lines.append(f"    {prefix} match_{screen['name']}() then")
        lines.extend(render_tap(screen["tap"], "        "))
    lines.extend(["    else", f"        sys.msleep({args.interval_ms})", "    end", "end"])
    return "\n".join(lines)


def write_output(text: str, output: str | None) -> None:
    if output:
        Path(output).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", help="Path to .tmp/xxtouch-ai/assist/<flow>/manifest.json")
    parser.add_argument("--mode", choices=("xxtdo", "plain"), default="xxtdo")
    parser.add_argument("--name", help="Flow/runloop name")
    parser.add_argument("--step", action="append", help="Only render this step id, repeatable")
    parser.add_argument("--status", action="append", default=[], help="Renderable status, repeatable")
    parser.add_argument("--all-steps", action="store_true", help="Render matching steps regardless of status")
    parser.add_argument("--similarity", type=int, default=92)
    parser.add_argument("--interval-ms", type=int, default=150)
    parser.add_argument("--no-records", action="store_true", help="Do not merge result.records into points")
    parser.add_argument("--output", help="Write output to file instead of stdout")
    args = parser.parse_args()

    manifest = load_json(args.manifest)
    if not isinstance(manifest, dict):
        raise SystemExit("manifest must be a JSON object")
    screens, skipped = collect_screens(manifest, args)
    if not screens:
        reason = f"; skipped={skipped}" if skipped else ""
        raise SystemExit(f"no renderable color steps found{reason}")

    output = render_xxtdo(manifest, screens, args) if args.mode == "xxtdo" else render_plain(manifest, screens, args)
    write_output(output, args.output)


if __name__ == "__main__":
    main()
