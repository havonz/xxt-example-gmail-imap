"""Shared helpers for host-side XXTouch assist scripts."""

from __future__ import annotations

import json
import re
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


COMPLETED_STATUSES = {"completed", "done", "consumed", "submitted"}


def utc_now() -> str:
    return datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def load_json(path: str) -> Any:
    if path == "-":
        return json.load(sys.stdin)
    with open(path, "r", encoding="utf-8") as handle:
        return json.load(handle)


def write_json(path: Path, data: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def print_json(data: Any, compact: bool = False) -> None:
    if compact:
        print(json.dumps(data, ensure_ascii=False, separators=(",", ":")))
    else:
        print(json.dumps(data, ensure_ascii=False, indent=2))


def select_step(payload: Any, step_id: str | None) -> Any:
    if not step_id:
        return payload
    if not isinstance(payload, dict):
        raise SystemExit("--step requires a manifest object")
    for step in payload.get("steps", []):
        if isinstance(step, dict) and str(step.get("stepId", "")) == step_id:
            return step
    raise SystemExit(f"step not found: {step_id}")


def unwrap_result(payload: Any) -> tuple[dict[str, Any], dict[str, Any]]:
    if not isinstance(payload, dict):
        raise SystemExit("input must be a JSON object")
    meta = payload
    data = payload
    if isinstance(data.get("task"), dict):
        meta = data["task"]
        data = data["task"]
    if isinstance(data.get("assistTask"), dict):
        meta = data["assistTask"]
        data = data["assistTask"]
    if isinstance(data.get("result"), dict):
        data = data["result"]
    return meta, data


def as_int(value: Any, field: str) -> int:
    try:
        return int(round(float(value)))
    except (TypeError, ValueError):
        raise ValueError(f"invalid {field}: {value!r}") from None


def normalize_color(value: Any) -> str:
    if isinstance(value, int):
        if value <= 0xFFFFFF:
            return f"0x{value:06X}"
        return f"0x{value:X}"
    text = str(value or "").strip()
    if not text:
        raise ValueError("missing color")
    text = re.sub(r"^(?:0x|#)", "", text, flags=re.IGNORECASE)
    text = re.sub(r"[^0-9a-fA-F]", "", text).upper()
    if len(text) == 3:
        text = "".join(ch * 2 for ch in text)
    if not text:
        raise ValueError("invalid color")
    if len(text) > 8:
        text = text[-8:]
    return f"0x{text}"


def normalize_point(item: Any) -> dict[str, Any] | None:
    if isinstance(item, (list, tuple)) and len(item) >= 3:
        point = {"x": item[0], "y": item[1], "color": item[2]}
        if len(item) >= 4:
            point["similarity"] = item[3]
    elif isinstance(item, dict):
        point = item
    else:
        return None

    try:
        out: dict[str, Any] = {
            "x": as_int(point.get("x"), "x"),
            "y": as_int(point.get("y"), "y"),
            "color": normalize_color(point.get("color", point.get("hex", point.get("rgb")))),
        }
        sim = point.get("similarity", point.get("sim", point.get("csim")))
        if sim is not None and str(sim).strip() != "":
            out["similarity"] = as_int(sim, "similarity")
        return out
    except ValueError:
        return None


def collect_points(result: dict[str, Any], include_records: bool = True) -> list[dict[str, Any]]:
    raw_points: list[Any] = []
    for key in ("points", "statePoints", "colorPoints", "colors", "group"):
        value = result.get(key)
        if isinstance(value, list):
            raw_points.extend(value)
    if include_records and isinstance(result.get("records"), list):
        raw_points.extend(result["records"])

    points: list[dict[str, Any]] = []
    seen: set[tuple[int, int, str]] = set()
    for item in raw_points:
        point = normalize_point(item)
        if not point:
            continue
        key = (point["x"], point["y"], point["color"])
        if key in seen:
            continue
        seen.add(key)
        points.append(point)
    return points


def parse_tap(text: str | None) -> dict[str, int] | None:
    if not text:
        return None
    parts = re.split(r"[,:\s]+", text.strip())
    if len(parts) < 2:
        raise SystemExit("--tap must be formatted as x,y")
    return {"x": as_int(parts[0], "tap x"), "y": as_int(parts[1], "tap y")}


def result_tap(result: dict[str, Any], override: str | None = None) -> dict[str, int] | None:
    explicit = parse_tap(override)
    if explicit:
        return explicit
    for key in ("actionPoint", "tap", "action"):
        value = result.get(key)
        if isinstance(value, dict) and "x" in value and "y" in value:
            return {"x": as_int(value["x"], "tap x"), "y": as_int(value["y"], "tap y")}
        if isinstance(value, (list, tuple)) and len(value) >= 2:
            return {"x": as_int(value[0], "tap x"), "y": as_int(value[1], "tap y")}
    return None


def normalize_rect(value: Any) -> dict[str, int] | None:
    if value is None:
        return None
    if isinstance(value, (list, tuple)) and len(value) >= 4:
        value = {"left": value[0], "top": value[1], "right": value[2], "bottom": value[3]}
    if not isinstance(value, dict):
        return None

    try:
        if all(key in value for key in ("left", "top", "right", "bottom")):
            rect = {
                "left": as_int(value["left"], "left"),
                "top": as_int(value["top"], "top"),
                "right": as_int(value["right"], "right"),
                "bottom": as_int(value["bottom"], "bottom"),
            }
        elif all(key in value for key in ("x", "y", "w", "h")):
            left = as_int(value["x"], "x")
            top = as_int(value["y"], "y")
            rect = {
                "left": left,
                "top": top,
                "right": left + as_int(value["w"], "w"),
                "bottom": top + as_int(value["h"], "h"),
            }
        elif all(key in value for key in ("x1", "y1", "x2", "y2")):
            rect = {
                "left": as_int(value["x1"], "x1"),
                "top": as_int(value["y1"], "y1"),
                "right": as_int(value["x2"], "x2"),
                "bottom": as_int(value["y2"], "y2"),
            }
        else:
            return None
    except ValueError:
        return None

    if rect["right"] < rect["left"] or rect["bottom"] < rect["top"]:
        raise ValueError(f"invalid rect: {rect}")
    return rect


def collect_rect(result: dict[str, Any], key: str | None = None) -> tuple[str, dict[str, int]]:
    keys = [key] if key else ["rect", "metaRect", "shiftRect", "selection", "region", "bounds"]
    for candidate_key in keys:
        if not candidate_key:
            continue
        try:
            rect = normalize_rect(result.get(candidate_key))
        except ValueError as error:
            raise SystemExit(str(error)) from None
        if rect:
            return candidate_key, rect
    raise SystemExit(f"no rectangle found{f' for {key}' if key else ''}")


def rect_args(rect: dict[str, int]) -> str:
    return f"{rect['left']}, {rect['top']}, {rect['right']}, {rect['bottom']}"


def lua_string(text: str) -> str:
    return "'" + text.replace("\\", "\\\\").replace("'", "\\'") + "'"


def lua_name(value: str | None, meta: dict[str, Any] | None = None) -> str:
    meta = meta or {}
    raw = value or str(meta.get("stepId") or meta.get("title") or meta.get("id") or "screen")
    name = re.sub(r"[^0-9A-Za-z_]+", "_", raw.strip()).strip("_")
    if not name:
        return "screen"
    if name[0].isdigit():
        name = "_" + name
    return name


def point_line(point: dict[str, Any], indent: str = "    ") -> str:
    values = [str(point["x"]), str(point["y"]), point["color"]]
    if "similarity" in point:
        values.append(str(point["similarity"]))
    return f"{indent}{{{', '.join(values)}}},"


def render_tap(tap: dict[str, int] | None, indent: str = "") -> list[str]:
    if not tap:
        return [f"{indent}-- TODO: add next action"]
    return [f"{indent}touch.tap({tap['x']}, {tap['y']})", f"{indent}sys.msleep(300)"]


def extract_matrix_lines(result: dict[str, Any]) -> list[str]:
    raw_values: list[Any] = []
    for key in ("matrixLines", "matrixList", "matrix", "currentLine", "matrixLine", "dict", "dictText"):
        value = result.get(key)
        if value:
            raw_values.append(value)
    snippets = result.get("snippets")
    if isinstance(snippets, dict):
        for value in snippets.values():
            if isinstance(value, str) and "$" in value:
                raw_values.append(value)

    lines: list[str] = []
    for value in raw_values:
        if isinstance(value, list):
            candidates = value
        else:
            candidates = str(value).splitlines()
        for candidate in candidates:
            text = str(candidate).strip()
            if text and "$" in text and text not in lines:
                lines.append(text)
    return lines


def validate_matrix_line(line: str) -> None:
    parts = line.split("$")
    if len(parts) not in {4, 5}:
        raise ValueError(f"invalid matrix line segment count: {line}")
    if not parts[0] or not parts[1]:
        raise ValueError(f"invalid matrix line content: {line}")
    if len(parts) == 4 and "." not in parts[3]:
        raise ValueError(f"invalid matrix line size segment: {line}")


def validated_matrix_lines(lines: list[str]) -> list[str]:
    if not lines:
        raise SystemExit("no matrix lines found")
    for line in lines:
        try:
            validate_matrix_line(line)
        except ValueError as error:
            raise SystemExit(str(error)) from None
    return lines


def parse_key_values(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for match in re.finditer(r"([A-Za-z_][A-Za-z0-9_]*)\s*=\s*(['\"])(.*?)\2", text, re.S):
        out[match.group(1)] = match.group(3)
    return out
