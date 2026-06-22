#!/usr/bin/env python3
"""Convert assist-task rectangle results into Lua snippets."""

from __future__ import annotations

import argparse
import json
from pathlib import Path

from xxtouch_assist_common import collect_rect, load_json, rect_args, select_step, unwrap_result


def render_table(rect: dict[str, int]) -> str:
    return "\n".join(
        [
            "{",
            f"    left = {rect['left']},",
            f"    top = {rect['top']},",
            f"    right = {rect['right']},",
            f"    bottom = {rect['bottom']},",
            "}",
        ]
    )


def render_ocr(rect: dict[str, int], engine: str | None, color_range: str | None) -> str:
    args = rect_args(rect)
    if engine and color_range:
        return f"local text, info = screen.ocr_text({args}, {json.dumps(engine)}, {json.dumps(color_range)})"
    if engine:
        return f"local text, info = screen.ocr_text({args}, {json.dumps(engine)})"
    return f"local text, info = screen.ocr_text({args})"


def render_find_image(rect: dict[str, int], image_var: str, confidence: int) -> str:
    return f"local x, y = screen.find_image({image_var}, {confidence}, {rect_args(rect)})"


def render_crop(rect: dict[str, int], image_var: str, output_var: str) -> str:
    return f"local {output_var} = {image_var}:crop({rect_args(rect)})"


def render_xxtdo_field(rect: dict[str, int], field_name: str) -> str:
    return f"{field_name} = {{{rect_args(rect)}}},"


def write_output(text: str, output: str | None) -> None:
    if output:
        Path(output).write_text(text + "\n", encoding="utf-8")
    else:
        print(text)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input", help="JSON file path, or - for stdin")
    parser.add_argument("--step", help="Select a manifest steps[].stepId")
    parser.add_argument("--rect-key", help="Rectangle field to use, e.g. metaRect or shiftRect")
    parser.add_argument(
        "--format",
        choices=("args", "table", "json", "ocr", "find-image", "crop", "xxtdo-field"),
        default="args",
    )
    parser.add_argument("--engine", help="Optional OCR engine/lang argument for --format ocr")
    parser.add_argument("--color-range", help="Optional binary color range for --format ocr")
    parser.add_argument("--image-var", default="img", help="Image variable for find-image/crop")
    parser.add_argument("--output-var", default="cropped", help="Output variable for crop")
    parser.add_argument("--confidence", type=int, default=95, help="Image confidence for find-image")
    parser.add_argument("--field-name", default="rect", help="Field name for xxtdo-field")
    parser.add_argument("--output", help="Write output to file instead of stdout")
    args = parser.parse_args()

    selected = select_step(load_json(args.input), args.step)
    _, result = unwrap_result(selected)
    key, rect = collect_rect(result, args.rect_key)

    if args.format == "args":
        output = rect_args(rect)
    elif args.format == "table":
        output = render_table(rect)
    elif args.format == "json":
        output = json.dumps({"key": key, "rect": rect}, ensure_ascii=False, indent=2)
    elif args.format == "ocr":
        output = render_ocr(rect, args.engine, args.color_range)
    elif args.format == "find-image":
        output = render_find_image(rect, args.image_var, args.confidence)
    elif args.format == "crop":
        output = render_crop(rect, args.image_var, args.output_var)
    else:
        output = render_xxtdo_field(rect, args.field_name)

    write_output(output, args.output)


if __name__ == "__main__":
    main()
