#!/usr/bin/env python3
"""Convert matrix-dict assist results into dm Lua snippets."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

from xxtouch_assist_common import (
    collect_rect,
    extract_matrix_lines,
    load_json,
    normalize_rect,
    rect_args,
    select_step,
    unwrap_result,
    validated_matrix_lines,
)


def read_input(path: str) -> tuple[Any | None, list[str]]:
    if path == "-":
        text = sys.stdin.read()
    else:
        text = Path(path).read_text(encoding="utf-8")
    try:
        return json.loads(text), []
    except json.JSONDecodeError:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        return None, lines


def rect_from_args(text: str | None) -> dict[str, int] | None:
    if not text:
        return None
    parts = [part for part in text.replace(",", " ").split() if part]
    if len(parts) != 4:
        raise SystemExit("--rect must be formatted as left,top,right,bottom")
    rect = normalize_rect([parts[0], parts[1], parts[2], parts[3]])
    if not rect:
        raise SystemExit("invalid --rect")
    return rect


def result_rect(result: dict[str, Any], rect_key: str | None, override: str | None) -> dict[str, int]:
    rect = rect_from_args(override)
    if rect:
        return rect
    keys = [rect_key] if rect_key else ["metaRect", "rect", "shiftRect"]
    for key in keys:
        try:
            _, rect = collect_rect(result, key)
            return rect
        except SystemExit:
            continue
    return {"left": 0, "top": 0, "right": 0, "bottom": 0}


def dm_header() -> list[str]:
    return ['local dm = require("dm")']


def render_load_dict(lines: list[str], dict_index: int) -> str:
    out = dm_header()
    out.extend(
        [
            f"dm.LoadDict({dict_index}, [[",
            *lines,
            "]])",
            f"dm.UseDict({dict_index})",
        ]
    )
    return "\n".join(out)


def render_find_matrix(lines: list[str], rect: dict[str, int], color_range: str, similarity: str) -> str:
    out = dm_header()
    out.extend(
        [
            "",
            "local matrix = [[",
            *lines,
            "]]",
            f"local found, x, y, word, boxes = dm.FindMatrix({rect_args(rect)}, matrix, {json.dumps(color_range)}, {similarity})",
            "if found then",
            "    nLog('FindMatrix', word, x, y, boxes)",
            "end",
        ]
    )
    return "\n".join(out)


def render_find_str(
    lines: list[str],
    rect: dict[str, int],
    word: str,
    color_range: str,
    similarity: str,
    dict_index: int,
    include_load: bool,
) -> str:
    out = dm_header()
    if include_load and lines:
        out.extend(["", f"dm.LoadDict({dict_index}, [[", *lines, "]])"])
    out.extend(
        [
            f"dm.UseDict({dict_index})",
            f"local found, x, y, boxes = dm.FindStr({rect_args(rect)}, {json.dumps(word)}, {json.dumps(color_range)}, {similarity})",
            "if found then",
            "    touch.tap(x, y)",
            "end",
        ]
    )
    return "\n".join(out)


def render_ocr(lines: list[str], rect: dict[str, int], color_range: str, similarity: str, dict_index: int, include_load: bool) -> str:
    out = dm_header()
    if include_load and lines:
        out.extend(["", f"dm.LoadDict({dict_index}, [[", *lines, "]])"])
    out.extend(
        [
            f"dm.UseDict({dict_index})",
            f"local text, boxes = dm.Ocr({rect_args(rect)}, {json.dumps(color_range)}, {similarity})",
            "nLog('dm OCR', text, boxes)",
        ]
    )
    return "\n".join(out)


def write_output(text: str, output: str | None) -> None:
    if output:
        Path(output).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="Task/result JSON, manifest JSON, plain matrix lines, or - for stdin")
    parser.add_argument("--step", help="Select a manifest steps[].stepId")
    parser.add_argument(
        "--format",
        choices=("lines", "load-dict", "find-matrix", "find-str", "ocr", "json"),
        default="find-matrix",
    )
    parser.add_argument("--rect", help="Override region as left,top,right,bottom")
    parser.add_argument("--rect-key", help="Rectangle field to use, defaults to metaRect then rect then shiftRect")
    parser.add_argument("--word", help="Word for find-str; defaults to result.word")
    parser.add_argument("--color-range", help="Color range text; defaults to result.colorRange or FFFFFF-101010")
    parser.add_argument("--similarity", default="0.98", help="dm similarity, defaults to 0.98")
    parser.add_argument("--dict-index", type=int, default=0, help="dm dictionary index, defaults to 0")
    parser.add_argument("--no-load", action="store_true", help="Do not include dm.LoadDict in find-str/ocr output")
    parser.add_argument("--output", help="Write output to file instead of stdout")
    args = parser.parse_args()

    payload, plain_lines = read_input(args.input)
    result: dict[str, Any] = {}
    if payload is not None:
        selected = select_step(payload, args.step)
        _, result = unwrap_result(selected)
    lines = validated_matrix_lines(plain_lines or extract_matrix_lines(result))
    rect = result_rect(result, args.rect_key, args.rect)
    word = args.word or str(result.get("word") or "")
    color_range = args.color_range or str(result.get("colorRange") or "FFFFFF-101010")

    if args.format == "lines":
        output = "\n".join(lines)
    elif args.format == "load-dict":
        output = render_load_dict(lines, args.dict_index)
    elif args.format == "find-matrix":
        output = render_find_matrix(lines, rect, color_range, args.similarity)
    elif args.format == "find-str":
        if not word:
            raise SystemExit("--word is required when result.word is empty")
        output = render_find_str(lines, rect, word, color_range, args.similarity, args.dict_index, not args.no_load)
    elif args.format == "ocr":
        output = render_ocr(lines, rect, color_range, args.similarity, args.dict_index, not args.no_load)
    else:
        output = json.dumps({"matrixLines": lines, "rect": rect, "word": word, "colorRange": color_range}, ensure_ascii=False, indent=2)

    write_output(output, args.output)


if __name__ == "__main__":
    main()
