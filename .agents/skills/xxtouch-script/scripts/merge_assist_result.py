#!/usr/bin/env python3
"""Merge a submitted XXTLanControl assist-task result into a flow manifest."""

from __future__ import annotations

import argparse
import copy
from pathlib import Path
from typing import Any

from xxtouch_assist_common import load_json, print_json, utc_now, write_json


def as_dict(value: Any, label: str) -> dict[str, Any]:
    if not isinstance(value, dict):
        raise SystemExit(f"{label} must be a JSON object")
    return value


def task_object(payload: dict[str, Any]) -> dict[str, Any]:
    for key in ("task", "assistTask"):
        if isinstance(payload.get(key), dict):
            return payload[key]
    return payload


def submitted_result(payload: dict[str, Any]) -> dict[str, Any]:
    task = task_object(payload)
    if isinstance(task.get("result"), dict):
        return task["result"]
    if isinstance(payload.get("result"), dict):
        return payload["result"]
    return payload


def task_id(payload: dict[str, Any], override: str | None) -> str | None:
    if override:
        return override
    task = task_object(payload)
    for key in ("id", "taskId", "assistTaskId"):
        value = task.get(key)
        if value is not None and str(value).strip():
            return str(value)
    return None


def infer_step_id(payload: dict[str, Any], override: str | None) -> str | None:
    if override:
        return override
    task = task_object(payload)
    for source in (task.get("input"), payload.get("input"), submitted_result(payload)):
        if isinstance(source, dict):
            value = source.get("stepId") or source.get("step_id")
            if value is not None and str(value).strip():
                return str(value)
    return None


def find_step(manifest: dict[str, Any], step_id: str) -> dict[str, Any]:
    steps = manifest.get("steps")
    if not isinstance(steps, list):
        raise SystemExit("manifest.steps must be an array")
    for step in steps:
        if isinstance(step, dict) and str(step.get("stepId", "")) == step_id:
            return step
    raise SystemExit(f"step not found: {step_id}")


def append_task_id(step: dict[str, Any], value: str | None) -> None:
    if not value:
        return
    current = step.get("assistTaskIds")
    if not isinstance(current, list):
        current = []
        step["assistTaskIds"] = current
    if value not in [str(item) for item in current]:
        current.append(value)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("manifest", help="Path to .tmp/xxtouch-ai/assist/<flow>/manifest.json")
    parser.add_argument("input", help="Submitted task/result JSON path, or - for stdin")
    parser.add_argument("--step", help="Manifest steps[].stepId; inferred from task.input.stepId when omitted")
    parser.add_argument("--task-id", help="Assist task id override")
    parser.add_argument("--status", default="submitted", help="Step status after merge, defaults to submitted")
    parser.add_argument("--apply", action="store_true", help="Write the updated manifest")
    args = parser.parse_args()

    manifest_path = Path(args.manifest)
    manifest = as_dict(load_json(str(manifest_path)), "manifest")
    payload = as_dict(load_json(args.input), "input")
    result = submitted_result(payload)
    if not isinstance(result, dict):
        raise SystemExit("submitted result must be a JSON object")

    step_id = infer_step_id(payload, args.step)
    if not step_id:
        raise SystemExit("--step is required when the task payload has no input.stepId")

    updated = copy.deepcopy(manifest)
    step = find_step(updated, step_id)
    append_task_id(step, task_id(payload, args.task_id))
    step["status"] = args.status
    step["result"] = result
    step["updatedAt"] = utc_now()
    updated["updatedAt"] = utc_now()

    summary = {
        "manifest": str(manifest_path),
        "dryRun": not args.apply,
        "stepId": step_id,
        "status": args.status,
        "taskId": task_id(payload, args.task_id),
        "updatedStep": step,
    }
    if args.apply:
        write_json(manifest_path, updated)
        summary["written"] = True
    else:
        summary["manifestData"] = updated
        summary["written"] = False

    print_json(summary)


if __name__ == "__main__":
    main()
