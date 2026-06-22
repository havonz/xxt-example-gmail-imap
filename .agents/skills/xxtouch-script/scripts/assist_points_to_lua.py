#!/usr/bin/env python3
"""Convert XXTLanControl assist-task color results into Lua snippets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from xxtouch_assist_common import (
    collect_points,
    load_json,
    lua_name,
    lua_string,
    point_line,
    result_tap,
    select_step,
    unwrap_result,
)


def render_points(points: list[dict[str, Any]]) -> str:
    lines = ["{"]
    lines.extend(point_line(point, "    ") for point in points)
    lines.append("}")
    return "\n".join(lines)


def render_is_colors(points: list[dict[str, Any]], similarity: int) -> str:
    lines = ["screen.keep()", "local ok = screen.is_colors({"]
    lines.extend(point_line(point, "    ") for point in points)
    lines.extend([f"}}, {similarity})", "screen.unkeep()"])
    return "\n".join(lines)


def render_tap(tap: dict[str, int] | None) -> str:
    if not tap:
        return "-- TODO: add touch.tap(x, y)"
    return f"touch.tap({tap['x']}, {tap['y']})\nsys.msleep(300)"


def render_xxtdo_screen(points: list[dict[str, Any]], name: str, similarity: int, tap: dict[str, int] | None) -> str:
    lines = [
        "{",
        f"    name = {lua_string(name)},",
        f"    csim = {similarity},",
    ]
    lines.extend(point_line(point, "    ") for point in points)
    lines.append("    run = function()")
    if tap:
        lines.append(f"        touch.tap({tap['x']}, {tap['y']})")
        lines.append("        sys.msleep(300)")
    else:
        lines.append("        -- TODO: add next action")
    lines.extend(["    end,", "}"])
    return "\n".join(lines)


def write_output(text: str, output: str | None) -> None:
    if output:
        Path(output).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="JSON file path, or - for stdin")
    parser.add_argument("--step", help="Select a manifest steps[].stepId")
    parser.add_argument("--format", choices=("points", "is-colors", "xxtdo-screen", "tap", "json"), default="points")
    parser.add_argument("--name", help="Screen name for xxtdo-screen output")
    parser.add_argument("--similarity", type=int, default=90)
    parser.add_argument("--tap", help="Override tap point as x,y")
    parser.add_argument("--no-records", action="store_true", help="Do not merge result.records into points")
    parser.add_argument("--output", help="Write output to file instead of stdout")
    args = parser.parse_args()

    selected = select_step(load_json(args.input), args.step)
    meta, result = unwrap_result(selected)
    points = collect_points(result, include_records=not args.no_records)
    tap = result_tap(result, args.tap)

    if args.format in {"points", "is-colors", "xxtdo-screen"} and not points:
        raise SystemExit("no color points found in result")

    if args.format == "points":
        output = render_points(points)
    elif args.format == "is-colors":
        output = render_is_colors(points, args.similarity)
    elif args.format == "xxtdo-screen":
        output = render_xxtdo_screen(points, lua_name(args.name, meta), args.similarity, tap)
    elif args.format == "tap":
        output = render_tap(tap)
    else:
        output = json.dumps({"points": points, "tap": tap}, ensure_ascii=False, indent=2)

    write_output(output, args.output)


if __name__ == "__main__":
    main()
