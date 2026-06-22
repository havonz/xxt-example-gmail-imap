#!/usr/bin/env python3
"""Inspect an XXT/XPP project and report script-development conventions."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Any

from xxtouch_assist_common import parse_key_values, print_json


def rel(path: Path, root: Path) -> str:
    try:
        return path.resolve().relative_to(root.resolve()).as_posix()
    except ValueError:
        return str(path)


def load_config(root: Path) -> tuple[dict[str, Any] | None, str | None]:
    path = root / ".config"
    if not path.is_file():
        return None, None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        return None, f"invalid .config JSON: {error}"
    if not isinstance(data, dict):
        return None, ".config must be a JSON object"
    return data, None


def load_info_fields(root: Path) -> dict[str, str]:
    path = root / "Info.lua"
    if not path.is_file():
        return {}
    return parse_key_values(path.read_text(encoding="utf-8", errors="replace"))


def list_xui_files(root: Path) -> list[str]:
    out: list[str] = []
    for pattern in ("*.xui", "*.xuic"):
        for path in root.rglob(pattern):
            if any(part in {".tmp", ".git", "node_modules"} for part in path.parts):
                continue
            out.append(rel(path, root))
    return sorted(out)


def detect_project_type(root: Path, config: dict[str, Any] | None, info_fields: dict[str, str]) -> tuple[str, str]:
    config_type = str((config or {}).get("type") or "").strip().lower()
    if config_type in {"xxt", "xpp"}:
        return config_type, ".config.type"
    if (root / "Info.lua").is_file() or info_fields:
        return "xpp", "Info.lua"
    if (root / "lua" / "scripts" / "main.lua").is_file():
        return "xxt", "lua/scripts/main.lua"
    return "unknown", "layout"


def xxtdo_info(root: Path, project_type: str) -> dict[str, Any]:
    if project_type == "xpp":
        candidates = [root / "XXTDo.lua"]
        recommended = "XXTDo.lua"
    else:
        candidates = [root / "lua" / "XXTDo.lua", root / "lua" / "scripts" / "XXTDo.lua"]
        recommended = "lua/XXTDo.lua"
    existing = [rel(path, root) for path in candidates if path.is_file()]
    return {"available": bool(existing), "existing": existing, "recommended": recommended}


def diagnostics(root: Path, project_type: str, config_error: str | None, entry: str | None, xui_files: list[str]) -> list[dict[str, str]]:
    out: list[dict[str, str]] = []
    if config_error:
        out.append({"level": "error", "message": config_error})
    if not (root / ".config").is_file():
        out.append({"level": "warning", "message": ".config not found"})
    if project_type == "unknown":
        out.append({"level": "warning", "message": "project type could not be inferred"})
    if entry and not (root / entry).is_file():
        out.append({"level": "warning", "message": f"entry script does not exist: {entry}"})
    if project_type == "xxt":
        if (root / "Info.lua").exists():
            out.append({"level": "warning", "message": "XXT project contains Info.lua"})
        if xui_files:
            out.append({"level": "warning", "message": "XXT project contains XUI files"})
    if project_type == "xpp" and (root / "lua" / "scripts" / "main.lua").is_file():
        out.append({"level": "info", "message": "XPP project also contains lua/scripts/main.lua; use Info.lua.Executable"})
    return out


def inspect_project(root: Path) -> dict[str, Any]:
    root = root.resolve()
    config, config_error = load_config(root)
    info_fields = load_info_fields(root)
    project_type, detected_by = detect_project_type(root, config, info_fields)
    xui_files = list_xui_files(root)

    if project_type == "xxt":
        entry = "lua/scripts/main.lua"
        resource_strategy = "XXT_RES_PATH"
        main_interface = None
    elif project_type == "xpp":
        entry = info_fields.get("Executable") or "main.lua"
        resource_strategy = "xpp.resource_path('res/name.ext')"
        main_interface = info_fields.get("MainInterfaceFile")
    else:
        entry = None
        resource_strategy = None
        main_interface = info_fields.get("MainInterfaceFile")

    return {
        "projectRoot": str(root),
        "projectType": project_type,
        "detectedBy": detected_by,
        "config": {
            "path": str(root / ".config"),
            "type": (config or {}).get("type") if isinstance(config, dict) else None,
            "bid": (config or {}).get("bid") if isinstance(config, dict) else None,
            "name": (config or {}).get("name") if isinstance(config, dict) else None,
        },
        "infoLua": {
            "path": str(root / "Info.lua"),
            "exists": (root / "Info.lua").is_file(),
            "fields": info_fields,
        },
        "entry": entry,
        "entryExists": bool(entry and (root / entry).is_file()),
        "resourceStrategy": resource_strategy,
        "mainInterfaceFile": main_interface,
        "xuiFiles": xui_files,
        "xxtdo": xxtdo_info(root, project_type),
        "diagnostics": diagnostics(root, project_type, config_error, entry, xui_files),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", nargs="?", default=".", help="XXT/XPP project root, defaults to cwd")
    parser.add_argument("--compact", action="store_true", help="Print compact JSON")
    args = parser.parse_args()

    print_json(inspect_project(Path(args.project_root)), compact=args.compact)


if __name__ == "__main__":
    main()
