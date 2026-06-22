#!/usr/bin/env python3
"""Install the bundled XXTDo.lua framework into an XXT/XPP project."""

from __future__ import annotations

import argparse
import filecmp
import json
import shutil
from pathlib import Path
from typing import Any

from xxtouch_assist_common import print_json


def load_config_type(root: Path) -> str | None:
    path = root / ".config"
    if not path.is_file():
        return None
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return None
    if not isinstance(data, dict):
        return None
    value = str(data.get("type") or "").strip().lower()
    return value if value in {"xxt", "xpp"} else None


def detect_project_type(root: Path, override: str | None) -> str:
    if override:
        return override
    config_type = load_config_type(root)
    if config_type:
        return config_type
    if (root / "Info.lua").is_file():
        return "xpp"
    if (root / "lua" / "scripts" / "main.lua").is_file():
        return "xxt"
    raise SystemExit("cannot infer project type; pass --type xxt or --type xpp")


def framework_source() -> Path:
    path = Path(__file__).resolve().parents[1] / "assets" / "frameworks" / "XXTDo.lua"
    if not path.is_file():
        raise SystemExit(f"bundled XXTDo.lua not found: {path}")
    return path


def target_path(root: Path, project_type: str, override: str | None) -> Path:
    if override:
        return root / override
    if project_type == "xpp":
        return root / "XXTDo.lua"
    legacy = root / "lua" / "scripts" / "XXTDo.lua"
    if legacy.is_file():
        return legacy
    return root / "lua" / "XXTDo.lua"


def same_file_content(source: Path, target: Path) -> bool:
    return target.is_file() and filecmp.cmp(source, target, shallow=False)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", nargs="?", default=".", help="XXT/XPP project root, defaults to cwd")
    parser.add_argument("--type", choices=("xxt", "xpp"), help="Project type override")
    parser.add_argument("--target", help="Project-relative target path override")
    parser.add_argument("--check", action="store_true", help="Exit 1 when XXTDo.lua is missing or differs")
    parser.add_argument("--apply", action="store_true", help="Copy XXTDo.lua into the project")
    parser.add_argument("--force", action="store_true", help="Overwrite an existing different target when used with --apply")
    args = parser.parse_args()

    root = Path(args.project_root).resolve()
    project_type = detect_project_type(root, args.type)
    source = framework_source()
    target = target_path(root, project_type, args.target)
    exists = target.is_file()
    up_to_date = same_file_content(source, target)
    summary: dict[str, Any] = {
        "projectRoot": str(root),
        "projectType": project_type,
        "source": str(source),
        "target": str(target),
        "exists": exists,
        "upToDate": up_to_date,
        "dryRun": not args.apply,
        "changed": False,
    }

    if args.check:
        print_json(summary)
        if not up_to_date:
            raise SystemExit(1)
        return

    if args.apply:
        if exists and not up_to_date and not args.force:
            raise SystemExit(f"target exists and differs; pass --force to overwrite: {target}")
        if not up_to_date:
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
            summary["changed"] = True
            summary["exists"] = True
            summary["upToDate"] = True

    print_json(summary)


if __name__ == "__main__":
    main()
