"""Refresh MANIFEST.json version metadata and SHA-256 entries."""

from __future__ import annotations

import argparse
import hashlib
import json
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "MANIFEST.json"


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--version", help="set the package version before a release")
    args = parser.parse_args()

    data = json.loads(MANIFEST.read_text(encoding="utf-8"))
    if args.version:
        data["version"] = args.version
    data.setdefault("license", "Apache-2.0")
    data["distribution_reviewed"] = date.today().isoformat()
    data["sha256"] = {
        path.relative_to(ROOT).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(ROOT.rglob("*"))
        if path.is_file()
        and path.name != "MANIFEST.json"
        and ".git" not in path.relative_to(ROOT).parts
        and "__pycache__" not in path.relative_to(ROOT).parts
    }
    MANIFEST.write_bytes((json.dumps(data, indent=2) + "\n").encode("utf-8"))


if __name__ == "__main__":
    main()
