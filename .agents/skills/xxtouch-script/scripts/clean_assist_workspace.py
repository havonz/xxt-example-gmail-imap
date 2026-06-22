#!/usr/bin/env python3
"""Safely clean completed XXTLanControl assist screenshots from .tmp/xxtouch-ai."""

from __future__ import annotations

import argparse
import json
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any


DEFAULT_ASSIST_ROOT = ".tmp/xxtouch-ai/assist"
COMPLETED_STATUSES = {"completed", "done", "consumed", "submitted"}


def load_json(path: Path) -> Any:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as error:
        raise SystemExit(f"invalid JSON in {path}: {error}") from None


def write_json(path: Path, data: Any) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def is_relative_workspace_path(value: Any) -> bool:
    if not isinstance(value, str) or not value.strip():
        return False
    text = value.replace("\\", "/")
    if text.startswith("/") or "://" in text:
        return False
    parts = [part for part in text.split("/") if part not in {"", "."}]
    return ".." not in parts


def resolve_under(path: Path, root: Path) -> Path | None:
    resolved = path.resolve()
    try:
        resolved.relative_to(root.resolve())
    except ValueError:
        return None
    return resolved


def iter_manifest_paths(assist_root: Path, flow: str | None) -> list[Path]:
    if flow:
        manifest = assist_root / flow / "manifest.json"
        return [manifest] if manifest.is_file() else []
    return sorted(assist_root.glob("*/manifest.json"))


def step_is_cleanable(step: dict[str, Any], statuses: set[str], require_result: bool) -> bool:
    status = str(step.get("status", "")).strip().lower()
    if status not in statuses:
        return False
    if require_result and step.get("result") is None:
        return False
    return True


def collect_screenshot_paths(step: dict[str, Any]) -> list[str]:
    values: list[str] = []
    for key in ("screenshot", "localScreenshotPath"):
        value = step.get(key)
        if isinstance(value, str):
            values.append(value)
    return values


def prune_empty_dirs(start: Path, stop: Path) -> list[str]:
    removed: list[str] = []
    current = start
    stop = stop.resolve()
    while current.resolve() != stop and current.exists():
        try:
            current.rmdir()
        except OSError:
            break
        removed.append(str(current))
        current = current.parent
    return removed


def clean_manifest(
    manifest_path: Path,
    project_root: Path,
    assist_root: Path,
    statuses: set[str],
    require_result: bool,
    apply: bool,
    mark_manifest: bool,
    prune_dirs: bool,
) -> dict[str, Any]:
    manifest = load_json(manifest_path)
    if not isinstance(manifest, dict):
        raise SystemExit(f"manifest must be a JSON object: {manifest_path}")
    steps = manifest.get("steps")
    if not isinstance(steps, list):
        return {"manifest": str(manifest_path), "deleted": [], "missing": [], "skipped": ["steps missing"]}

    summary: dict[str, Any] = {"manifest": str(manifest_path), "deleted": [], "missing": [], "skipped": [], "prunedDirs": []}
    manifest_changed = False
    cleaned_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")

    for step in steps:
        if not isinstance(step, dict):
            continue
        if not step_is_cleanable(step, statuses, require_result):
            continue
        for screenshot in collect_screenshot_paths(step):
            if not is_relative_workspace_path(screenshot):
                summary["skipped"].append({"path": screenshot, "reason": "not a relative workspace path"})
                continue
            candidate = project_root / screenshot
            target = resolve_under(candidate, assist_root)
            if target is None:
                summary["skipped"].append({"path": screenshot, "reason": "outside assist workspace"})
                continue
            if not target.exists():
                summary["missing"].append(str(target))
                continue
            if not target.is_file():
                summary["skipped"].append({"path": str(target), "reason": "not a file"})
                continue
            summary["deleted"].append(str(target))
            if apply:
                target.unlink()
                if prune_dirs:
                    summary["prunedDirs"].extend(prune_empty_dirs(target.parent, manifest_path.parent))
                if mark_manifest:
                    step["screenshotCleanedAt"] = cleaned_at
                    step["screenshotCleanedPath"] = screenshot
                    manifest_changed = True

    if apply and mark_manifest and manifest_changed:
        write_json(manifest_path, manifest)
        summary["manifestUpdated"] = True
    else:
        summary["manifestUpdated"] = False
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", nargs="?", default=".", help="XXT/XPP project root, defaults to cwd")
    parser.add_argument("--flow", help="Only clean one flow id under .tmp/xxtouch-ai/assist")
    parser.add_argument("--assist-root", default=DEFAULT_ASSIST_ROOT, help=f"Assist root, defaults to {DEFAULT_ASSIST_ROOT}")
    parser.add_argument(
        "--status",
        action="append",
        default=[],
        help="Clean steps with this status, repeatable. Defaults to completed/done/consumed/submitted",
    )
    parser.add_argument(
        "--allow-without-result",
        action="store_true",
        help="Allow cleaning a matching step even when result is null",
    )
    parser.add_argument("--apply", action="store_true", help="Actually delete files. Without this, only prints a dry run")
    parser.add_argument("--no-mark-manifest", action="store_true", help="Do not write screenshotCleanedAt metadata")
    parser.add_argument("--no-prune-empty-dirs", action="store_true", help="Do not remove empty screenshot directories")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    assist_root = (project_root / args.assist_root).resolve()
    if not assist_root.exists():
        print(json.dumps({"assistRoot": str(assist_root), "dryRun": not args.apply, "manifests": []}, ensure_ascii=False, indent=2))
        return
    if not assist_root.is_dir():
        raise SystemExit(f"assist root is not a directory: {assist_root}")

    statuses = {status.strip().lower() for status in args.status if status.strip()} or COMPLETED_STATUSES
    manifests = iter_manifest_paths(assist_root, args.flow)
    results = [
        clean_manifest(
            manifest_path,
            project_root,
            assist_root,
            statuses,
            require_result=not args.allow_without_result,
            apply=args.apply,
            mark_manifest=not args.no_mark_manifest,
            prune_dirs=not args.no_prune_empty_dirs,
        )
        for manifest_path in manifests
    ]
    print(json.dumps({"assistRoot": str(assist_root), "dryRun": not args.apply, "manifests": results}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    try:
        main()
    except BrokenPipeError:
        sys.exit(1)
    except KeyboardInterrupt:
        sys.exit(130)
