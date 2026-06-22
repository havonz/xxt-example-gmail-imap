#!/usr/bin/env python3
"""Ensure XXTouch .config ignores local temporary workspace paths."""

from __future__ import annotations

import argparse
import json
import posixpath
import sys
from pathlib import Path
from typing import Any


DEFAULT_ENTRY = ".tmp"


def normalize_ignore_entry(entry: str) -> str:
    replaced = entry.replace("\\", "/").strip()
    while replaced.startswith("./"):
        replaced = replaced[2:]
    replaced = replaced.lstrip("/")
    if not replaced:
        return ""
    normalized = posixpath.normpath(replaced)
    if normalized in {"", "."}:
        return ""
    return normalized.rstrip("/")


def format_ignore_entry(entry: str) -> str:
    normalized = normalize_ignore_entry(entry)
    if not normalized:
        raise SystemExit(f"invalid ignore entry: {entry!r}")
    return f"/{normalized}"


def load_config(config_path: Path) -> dict[str, Any]:
    if not config_path.is_file():
        raise SystemExit(f".config not found: {config_path}")
    try:
        data = json.loads(config_path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise SystemExit(f"invalid .config JSON: {error}") from None
    if not isinstance(data, dict):
        raise SystemExit(".config must be a JSON object")
    return data


def ensure_array(data: dict[str, Any], key: str) -> list[Any]:
    value = data.get(key)
    if value is None:
        data[key] = []
        return data[key]
    if not isinstance(value, list):
        raise SystemExit(f".config.{key} must be an array")
    return value


def append_missing(items: list[Any], entries: list[str]) -> list[str]:
    known = {
        normalized
        for item in items
        if isinstance(item, str)
        for normalized in [normalize_ignore_entry(item)]
        if normalized
    }
    added: list[str] = []
    for entry in entries:
        normalized = normalize_ignore_entry(entry)
        if not normalized or normalized in known:
            continue
        formatted = format_ignore_entry(normalized)
        items.append(formatted)
        known.add(normalized)
        added.append(formatted)
    return added


def write_config(config_path: Path, data: dict[str, Any]) -> None:
    config_path.write_text(json.dumps(data, ensure_ascii=False, indent=4) + "\n", encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", nargs="?", default=".", help="XXT/XPP project root, defaults to cwd")
    parser.add_argument(
        "--entry",
        action="append",
        default=[],
        help=f"Path to ignore, repeatable. Defaults to {DEFAULT_ENTRY!r}",
    )
    parser.add_argument("--no-build", action="store_true", help="Do not update buildIgnores")
    parser.add_argument("--check", action="store_true", help="Exit with code 1 if changes would be needed")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    config_path = project_root / ".config"
    entries = args.entry or [DEFAULT_ENTRY]
    data = load_config(config_path)

    summary: dict[str, Any] = {"config": str(config_path), "changed": False, "added": {}}
    ignores = ensure_array(data, "ignores")
    added_ignores = append_missing(ignores, entries)
    summary["added"]["ignores"] = added_ignores

    if not args.no_build:
        build_ignores = ensure_array(data, "buildIgnores")
        added_build_ignores = append_missing(build_ignores, entries)
        summary["added"]["buildIgnores"] = added_build_ignores

    summary["changed"] = any(summary["added"].values())
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    if args.check:
        if summary["changed"]:
            raise SystemExit(1)
        return
    if summary["changed"]:
        write_config(config_path, data)


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        sys.exit(1)
