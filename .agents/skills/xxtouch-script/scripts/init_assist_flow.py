#!/usr/bin/env python3
"""Create a resumable XXTLanControl assist-flow manifest."""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from xxtouch_assist_common import print_json, utc_now, write_json


ASSIST_ROOT = ".tmp/xxtouch-ai/assist"


def slug(value: str) -> str:
    cleaned = "".join(ch if ch.isalnum() or ch in {"-", "_"} else "-" for ch in value.strip())
    cleaned = "-".join(part for part in cleaned.split("-") if part)
    return cleaned or "step"


def load_json_arg(value: str) -> dict[str, Any]:
    path = Path(value)
    if path.is_file():
        data = json.loads(path.read_text(encoding="utf-8"))
    else:
        data = json.loads(value)
    if not isinstance(data, dict):
        raise SystemExit("--step-json must be a JSON object or a file containing one")
    return data


def build_step(args: argparse.Namespace, flow_id: str) -> dict[str, Any] | None:
    if not args.step:
        return None
    step_id = slug(args.step)
    screenshot = args.screenshot or f"{ASSIST_ROOT}/{flow_id}/screens/{step_id}.png"
    backend_screenshot = args.backend_screenshot_path or f"assist/{flow_id}/{step_id}.png"
    return {
        "stepId": step_id,
        "title": args.title or step_id,
        "screenshot": screenshot,
        "backendScreenshotPath": backend_screenshot,
        "assistTaskIds": list(args.task_id or []),
        "why": args.why or "",
        "willUseFor": args.will_use_for or "",
        "status": "pending",
        "result": None,
    }


def run_ignore_helper(project_root: Path) -> dict[str, Any] | None:
    config_path = project_root / ".config"
    if not config_path.is_file():
        return {"skipped": True, "reason": ".config not found"}
    helper = Path(__file__).with_name("ensure_config_ignores.py")
    result = subprocess.run(
        [sys.executable, str(helper), str(project_root)],
        check=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    try:
        payload = json.loads(result.stdout or "{}")
    except json.JSONDecodeError:
        payload = {"stdout": result.stdout.strip()}
    payload["returnCode"] = result.returncode
    if result.stderr.strip():
        payload["stderr"] = result.stderr.strip()
    return payload


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project_root", nargs="?", default=".", help="XXT/XPP project root, defaults to cwd")
    parser.add_argument("--flow", required=True, help="Flow id under .tmp/xxtouch-ai/assist")
    parser.add_argument("--goal", default="", help="Human-readable flow goal")
    parser.add_argument("--step", help="Create one initial step id")
    parser.add_argument("--title", help="Initial step title")
    parser.add_argument("--why", help="Why this step is needed")
    parser.add_argument("--will-use-for", help="How the submitted result will be used")
    parser.add_argument("--screenshot", help="Initial step local screenshot path")
    parser.add_argument("--backend-screenshot-path", help="Initial step backend screenshot path")
    parser.add_argument("--task-id", action="append", help="Initial assist task id, repeatable")
    parser.add_argument("--step-json", action="append", default=[], help="Inline JSON object or JSON file for a step")
    parser.add_argument("--apply", action="store_true", help="Write manifest and create directories")
    parser.add_argument("--overwrite", action="store_true", help="Replace an existing manifest when used with --apply")
    parser.add_argument("--skip-ignore", action="store_true", help="Do not update .config ignores")
    args = parser.parse_args()

    project_root = Path(args.project_root).resolve()
    flow_id = slug(args.flow)
    flow_root = project_root / ASSIST_ROOT / flow_id
    manifest_path = flow_root / "manifest.json"
    steps: list[dict[str, Any]] = []
    first_step = build_step(args, flow_id)
    if first_step:
        steps.append(first_step)
    steps.extend(load_json_arg(value) for value in args.step_json)

    manifest = {
        "flowId": flow_id,
        "goal": args.goal,
        "createdAt": utc_now(),
        "updatedAt": utc_now(),
        "steps": steps,
    }
    summary: dict[str, Any] = {
        "manifest": str(manifest_path),
        "flowRoot": str(flow_root),
        "dryRun": not args.apply,
        "created": False,
        "stepCount": len(steps),
        "manifestData": manifest,
    }

    if args.apply:
        if manifest_path.exists() and not args.overwrite:
            raise SystemExit(f"manifest already exists: {manifest_path}")
        (flow_root / "screens").mkdir(parents=True, exist_ok=True)
        write_json(manifest_path, manifest)
        summary["created"] = True
        if not args.skip_ignore:
            summary["ignoreUpdate"] = run_ignore_helper(project_root)

    print_json(summary)


if __name__ == "__main__":
    main()
