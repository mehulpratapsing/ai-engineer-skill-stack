"""Validate skill metadata and packaged file checksums using only the standard library."""

from __future__ import annotations

import hashlib
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_PATH = ROOT / "MANIFEST.json"


def fail(message: str) -> None:
    print(f"ERROR: {message}", file=sys.stderr)
    raise SystemExit(1)


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    expected_skills = manifest.get("skills")
    if (
        not isinstance(expected_skills, list)
        or not expected_skills
        or len(expected_skills) != len(set(expected_skills))
    ):
        fail("manifest must list a non-empty set of unique skills")

    skill_root = ROOT / ".agents" / "skills"
    actual_skills = sorted(
        directory.name
        for directory in skill_root.iterdir()
        if directory.is_dir() and (directory / "SKILL.md").is_file()
    )
    if actual_skills != sorted(expected_skills):
        fail(f"skill folders do not match manifest: {actual_skills}")

    for skill_name in actual_skills:
        skill_file = skill_root / skill_name / "SKILL.md"
        text = skill_file.read_text(encoding="utf-8")
        match = re.match(r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)", text, re.S)
        if not match:
            fail(f"{skill_file.relative_to(ROOT)} has no YAML frontmatter")
        name_match = re.search(r"^name:\s*([^\s#]+)\s*$", match.group(1), re.M)
        if not name_match or name_match.group(1) != skill_name:
            fail(f"{skill_file.relative_to(ROOT)} frontmatter name does not match folder")
        license_match = re.search(r"^license:\s*([^\s#]+)\s*$", match.group(1), re.M)
        if not license_match or license_match.group(1) != "Apache-2.0":
            fail(f"{skill_file.relative_to(ROOT)} must declare Apache-2.0")

    expected_hashes = manifest.get("sha256", {})
    actual_files = {
        path.relative_to(ROOT).as_posix(): path
        for path in ROOT.rglob("*")
        if path.is_file()
        and path.name != "MANIFEST.json"
        and ".git" not in path.relative_to(ROOT).parts
        and "__pycache__" not in path.relative_to(ROOT).parts
    }
    if set(actual_files) != set(expected_hashes):
        missing = sorted(set(actual_files) - set(expected_hashes))
        stale = sorted(set(expected_hashes) - set(actual_files))
        fail(f"manifest file list differs; missing hashes={missing}, stale entries={stale}")

    for relative_path, path in actual_files.items():
        actual_hash = hashlib.sha256(path.read_bytes()).hexdigest()
        if expected_hashes[relative_path] != actual_hash:
            fail(f"SHA-256 mismatch: {relative_path}")

    print(f"Validated {len(actual_skills)} skills and {len(actual_files)} packaged file checksums.")


if __name__ == "__main__":
    main()
