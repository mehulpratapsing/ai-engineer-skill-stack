"""Run the paired synthetic benchmark with OpenCode in isolated temporary projects.

This command makes one model request per task and condition (20 requests for the full suite).
Use --dry-run to validate the suite and schedule without contacting a model provider.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import random
import shutil
import subprocess
import sys
import tempfile
import uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
TASKS_PATH = ROOT / "benchmarks" / "tasks.json"
SKILLS_PATH = ROOT / ".agents" / "skills"


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def safe_component(value: str) -> str:
    return "".join(char for char in value if char.isalnum() or char in "._-")


def run_checked(command: list[str], cwd: Path | None = None) -> str:
    result = subprocess.run(command, cwd=cwd, capture_output=True, text=True, check=False)
    if result.returncode:
        detail = result.stderr.strip() or result.stdout.strip() or f"exit code {result.returncode}"
        raise RuntimeError(f"command failed ({command[0]}): {detail}")
    return result.stdout.strip()


def isolated_environment(temp_home: Path) -> dict[str, str]:
    env = os.environ.copy()
    for key, value in {
        "HOME": temp_home,
        "USERPROFILE": temp_home,
        "APPDATA": temp_home / "AppData" / "Roaming",
        "LOCALAPPDATA": temp_home / "AppData" / "Local",
        "XDG_CONFIG_HOME": temp_home / ".config",
        "XDG_DATA_HOME": temp_home / ".local" / "share",
        "XDG_CACHE_HOME": temp_home / ".cache",
        "OPENCODE_CONFIG_DIR": temp_home / "opencode-config",
    }.items():
        env[key] = str(value)
    env.pop("OPENCODE_CONFIG", None)
    env.pop("OPENCODE_CONFIG_CONTENT", None)
    return env


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--model", required=True, help="explicit provider/model ID (for example provider/model-name)")
    parser.add_argument("--agent", default="plan", help="same OpenCode agent for both conditions (default: plan)")
    parser.add_argument("--seed", type=int, default=20261002, help="seed used only to randomize pair order")
    parser.add_argument("--timeout", type=int, default=300, help="per-request timeout in seconds")
    parser.add_argument("--dry-run", action="store_true", help="validate prompts and show schedule without model calls")
    parser.add_argument("--output", type=Path, help="new output directory; defaults under benchmarks/results")
    args = parser.parse_args()

    tasks_doc = json.loads(TASKS_PATH.read_text(encoding="utf-8"))
    tasks = tasks_doc.get("tasks")
    if not isinstance(tasks, list) or not tasks or len({task.get("id") for task in tasks}) != len(tasks):
        print("ERROR: benchmark task IDs must be a non-empty unique list", file=sys.stderr)
        return 2
    if not SKILLS_PATH.is_dir() or not any(SKILLS_PATH.glob("*/SKILL.md")):
        print("ERROR: canonical skill directory is missing or empty", file=sys.stderr)
        return 2

    opencode = shutil.which("opencode")
    if not opencode:
        print("ERROR: OpenCode CLI was not found on PATH", file=sys.stderr)
        return 2
    version = run_checked([opencode, "--version"])
    run_id = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ") + "-" + uuid.uuid4().hex[:8]
    output = args.output or ROOT / "benchmarks" / "results" / run_id
    output = output.resolve()
    results_root = (ROOT / "benchmarks" / "results").resolve()
    if not output.is_relative_to(results_root):
        print("ERROR: output must be inside benchmarks/results", file=sys.stderr)
        return 2
    if output.exists():
        print(f"ERROR: output directory already exists: {output}", file=sys.stderr)
        return 2

    rng = random.Random(args.seed)
    schedule: list[dict[str, str]] = []
    for task in tasks:
        order = ["baseline", "stack"]
        rng.shuffle(order)
        schedule.append({"task_id": task["id"], "prompt_sha256": sha256(task["prompt"].encode()), "order": order})

    metadata = {
        "suite": tasks_doc.get("suite"),
        "status": "dry-run; no model calls made" if args.dry_run else "in progress",
        "run_id": run_id,
        "started_at": utc_now(),
        "agent_product": "OpenCode",
        "agent_version": version,
        "agent": args.agent,
        "model": args.model,
        "temperature": "provider default; not overridden by runner",
        "tool_policy": "isolated temporary repository; plan agent; run events captured as raw JSONL",
        "schedule_seed": args.seed,
        "schedule": schedule,
        "requests_planned": len(tasks) * 2,
    }
    if args.dry_run:
        print(json.dumps(metadata, indent=2))
        return 0

    output.mkdir(parents=True)
    (output / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    try:
        with tempfile.TemporaryDirectory(prefix="ai-skill-benchmark-") as temp_name:
            temp_root = Path(temp_name)
            temp_home = temp_root / "isolated-home"
            temp_home.mkdir()
            env = isolated_environment(temp_home)
            for task, run_order in zip(tasks, schedule, strict=True):
                for condition in run_order["order"]:
                    trial = temp_root / safe_component(task["id"]) / condition
                    trial.mkdir(parents=True)
                    run_checked(["git", "init", "--quiet"], cwd=trial)
                    if condition == "stack":
                        shutil.copytree(SKILLS_PATH, trial / ".agents" / "skills")
                    command = [
                        opencode,
                        "run",
                        "--format",
                        "json",
                        "--model",
                        args.model,
                        "--agent",
                        args.agent,
                        "--dir",
                        str(trial),
                        task["prompt"],
                    ]
                    started = utc_now()
                    print(f"Running {task['id']} ({condition})...", flush=True)
                    try:
                        result = subprocess.run(
                            command,
                            cwd=trial,
                            env=env,
                            capture_output=True,
                            timeout=args.timeout,
                            check=False,
                        )
                    except subprocess.TimeoutExpired as error:
                        stdout = error.stdout or b""
                        stderr = error.stderr or b""
                        suffix = "timeout"
                        return_code = 124
                    else:
                        stdout = result.stdout
                        stderr = result.stderr
                        suffix = "complete" if result.returncode == 0 else "error"
                        return_code = result.returncode
                    folder = output / safe_component(task["id"])
                    folder.mkdir(exist_ok=True)
                    stem = condition
                    (folder / f"{stem}.jsonl").write_bytes(stdout)
                    (folder / f"{stem}.stderr.txt").write_bytes(stderr)
                    call_metadata = {
                        "task_id": task["id"],
                        "condition": condition,
                        "started_at": started,
                        "finished_at": utc_now(),
                        "prompt_sha256": run_order["prompt_sha256"],
                        "return_code": return_code,
                        "status": suffix,
                        "stdout_sha256": sha256(stdout),
                        "stderr_sha256": sha256(stderr),
                    }
                    (folder / f"{stem}.metadata.json").write_text(json.dumps(call_metadata, indent=2) + "\n", encoding="utf-8")
                    if return_code != 0:
                        metadata["status"] = "incomplete; inspect captured error and rerun the full pair deliberately"
                        metadata["finished_at"] = utc_now()
                        (output / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
                        print(f"ERROR: {task['id']} ({condition}) returned {return_code}; captured output at {folder}", file=sys.stderr)
                        return 1
    except (OSError, RuntimeError) as error:
        metadata["status"] = "incomplete; runner error"
        metadata["error"] = str(error)
        metadata["finished_at"] = utc_now()
        (output / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
        print(f"ERROR: {error}", file=sys.stderr)
        return 1

    metadata["status"] = "complete; unscored"
    metadata["finished_at"] = utc_now()
    (output / "metadata.json").write_text(json.dumps(metadata, indent=2) + "\n", encoding="utf-8")
    print(f"Captured {len(tasks) * 2} model outputs in {output}")
    print("Score outputs blind with benchmarks/README.md; do not publish only favorable pairs.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
