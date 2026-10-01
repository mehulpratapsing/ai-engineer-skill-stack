"""Check curated primary references and optionally open one deduplicated GitHub issue."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timezone
from html.parser import HTMLParser
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCES_PATH = ROOT / "references" / "monitored-sources.json"
LOCK_PATH = ROOT / "references" / "monitored-sources.lock.json"
MAX_BYTES = 12 * 1024 * 1024
TIMEOUT_SECONDS = 30
ISSUE_TITLE = "Primary reference sources changed — review required"
ALLOWED_HOSTS = {
    "mcp-specification": "modelcontextprotocol.io",
    "nist-genai-profile": "www.nist.gov",
    "owasp-llm-top-10-2026": "genai.owasp.org",
    "opentelemetry-genai-semconv": "raw.githubusercontent.com",
}


class VisibleText(HTMLParser):
    """Collect visible page text while skipping common chrome and script content."""

    SKIP_TAGS = {"aside", "footer", "head", "header", "nav", "noscript", "script", "style", "svg"}

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.skip_stack: list[str] = []
        self.parts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        tag = tag.lower()
        if tag in self.SKIP_TAGS:
            self.skip_stack.append(tag)

    def handle_startendtag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        return

    def handle_endtag(self, tag: str) -> None:
        tag = tag.lower()
        if tag in self.skip_stack:
            index = len(self.skip_stack) - 1 - self.skip_stack[::-1].index(tag)
            del self.skip_stack[index:]

    def handle_data(self, data: str) -> None:
        if not self.skip_stack:
            value = re.sub(r"\s+", " ", data).strip()
            if value:
                self.parts.append(value)


def normalized_content(body: bytes, content_type: str) -> bytes:
    if "text/html" in content_type.lower():
        parser = VisibleText()
        parser.feed(body.decode("utf-8", errors="replace"))
        text = "\n".join(parser.parts)
    else:
        text = body.decode("utf-8-sig", errors="replace")
        text = text.replace("\r\n", "\n").replace("\r", "\n")
        text = "\n".join(line.strip() for line in text.splitlines())
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text).strip()
    if len(text) < 200:
        raise ValueError("source returned too little readable content to verify")
    return text.encode("utf-8")


def fetch_source(source: dict[str, str]) -> dict[str, str]:
    url = source["url"]
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or not parsed.hostname:
        raise ValueError(f"{source['id']}: source URL must use HTTPS")
    expected_host = ALLOWED_HOSTS.get(source["id"])
    if not expected_host or parsed.hostname.lower() != expected_host:
        raise ValueError(f"{source['id']}: host is not on the monitor's fixed primary-source allowlist")
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": "ai-engineer-skill-stack-source-monitor/1.0 (+https://github.com/mehulpratapsing/ai-engineer-skill-stack)",
            "Accept": "text/html, text/plain, application/xhtml+xml;q=0.9, */*;q=0.1",
        },
    )
    with urllib.request.urlopen(request, timeout=TIMEOUT_SECONDS) as response:
        final_url = urllib.parse.urlparse(response.geturl())
        if final_url.scheme != "https" or final_url.hostname != expected_host:
            raise ValueError(f"{source['id']}: source redirected away from its allowlisted HTTPS host")
        body = response.read(MAX_BYTES + 1)
        if len(body) > MAX_BYTES:
            raise ValueError(f"{source['id']}: source exceeds the {MAX_BYTES}-byte safety limit")
        content = normalized_content(body, response.headers.get("Content-Type", ""))
    return {
        "id": source["id"],
        "name": source["name"],
        "url": url,
        "sha256": hashlib.sha256(content).hexdigest(),
    }


def load_sources() -> list[dict[str, str]]:
    data = json.loads(SOURCES_PATH.read_text(encoding="utf-8"))
    sources = data.get("sources")
    if not isinstance(sources, list) or not sources:
        raise ValueError("monitored-sources.json must define a non-empty sources list")
    ids = [source.get("id") for source in sources]
    if len(set(ids)) != len(ids) or any(not isinstance(value, str) or not value for value in ids):
        raise ValueError("source IDs must be unique, non-empty strings")
    for source in sources:
        if not all(isinstance(source.get(key), str) and source[key] for key in ("id", "name", "url")):
            raise ValueError("each source needs non-empty id, name, and url fields")
    return sources


def open_github_issue(changed: list[tuple[dict[str, str], str, str]]) -> str:
    token = os.environ.get("GITHUB_TOKEN")
    repository = os.environ.get("GITHUB_REPOSITORY")
    if not token or not repository or not re.fullmatch(r"[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+", repository):
        return "No issue opened: GITHUB_TOKEN and GITHUB_REPOSITORY are needed in CI."

    api = f"https://api.github.com/repos/{repository}/issues"
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {token}",
        "User-Agent": "ai-engineer-skill-stack-source-monitor/1.0",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    list_request = urllib.request.Request(api + "?state=open&per_page=100", headers=headers)
    with urllib.request.urlopen(list_request, timeout=TIMEOUT_SECONDS) as response:
        open_issues = json.loads(response.read().decode("utf-8"))
    for issue in open_issues:
        if issue.get("title") == ISSUE_TITLE and "pull_request" not in issue:
            return f"Existing tracking issue: {issue.get('html_url', '(URL unavailable)')}"

    rows = ["| Source | Previous SHA-256 | Current SHA-256 |", "|---|---|---|"]
    for source, previous_hash, current_hash in changed:
        rows.append(f"| [{source['name']}]({source['url']}) | `{previous_hash}` | `{current_hash}` |")
    run_url = os.environ.get("GITHUB_SERVER_URL", "https://github.com") + "/" + repository + "/actions/runs/" + os.environ.get("GITHUB_RUN_ID", "")
    body = (
        "The scheduled source monitor found content changes in one or more tracked primary references.\n\n"
        "Review each upstream source and decide whether any skill guidance needs an update. A changed page is a review signal, not proof that a recommendation changed. "
        "Do not refresh the lock file until a maintainer has reviewed the sources.\n\n"
        + "\n".join(rows)
        + f"\n\n[Workflow run]({run_url})"
    )
    payload = json.dumps({"title": ISSUE_TITLE, "body": body}).encode("utf-8")
    create_request = urllib.request.Request(api, data=payload, headers={**headers, "Content-Type": "application/json"}, method="POST")
    with urllib.request.urlopen(create_request, timeout=TIMEOUT_SECONDS) as response:
        issue = json.loads(response.read().decode("utf-8"))
    return f"Opened review issue: {issue.get('html_url', '(URL unavailable)')}"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    group = parser.add_mutually_exclusive_group()
    group.add_argument("--check", action="store_true", help="compare current sources with the reviewed baseline")
    group.add_argument("--update-baseline", action="store_true", help="replace the baseline after a human source review")
    args = parser.parse_args()

    sources = load_sources()
    try:
        current = [fetch_source(source) for source in sources]
    except (OSError, ValueError, urllib.error.URLError) as error:
        print(f"ERROR: source check could not complete: {error}", file=sys.stderr)
        return 2

    if args.update_baseline:
        baseline = {"reviewed_at": date.today().isoformat(), "sources": current}
        LOCK_PATH.write_bytes((json.dumps(baseline, indent=2) + "\n").encode("utf-8"))
        print(f"Updated reviewed baseline for {len(current)} sources at {baseline['reviewed_at']}.")
        return 0

    if not LOCK_PATH.is_file():
        print("ERROR: reviewed baseline is missing; review the sources, then run with --update-baseline.", file=sys.stderr)
        return 2
    baseline_data = json.loads(LOCK_PATH.read_text(encoding="utf-8"))
    baseline = {item["id"]: item for item in baseline_data.get("sources", [])}
    changed: list[tuple[dict[str, str], str, str]] = []
    for item in current:
        previous = baseline.get(item["id"])
        if previous is None:
            changed.append((item, "(not present)", item["sha256"]))
        elif previous.get("url") != item["url"] or previous.get("sha256") != item["sha256"]:
            changed.append((item, previous.get("sha256", "(missing)"), item["sha256"]))
    removed = sorted(set(baseline) - {item["id"] for item in current})
    if removed:
        print(f"ERROR: source IDs removed from configuration: {', '.join(removed)}", file=sys.stderr)
        return 2

    if changed:
        print(f"Detected changes in {len(changed)} of {len(current)} monitored sources:")
        for item, old_hash, new_hash in changed:
            print(f"- {item['name']} ({item['url']}): {old_hash} -> {new_hash}")
        try:
            print(open_github_issue(changed))
        except (OSError, urllib.error.URLError, json.JSONDecodeError) as error:
            print(f"ERROR: changes were detected, but the GitHub issue could not be opened: {error}", file=sys.stderr)
        return 1

    print(f"Verified {len(current)} monitored primary sources; no content changes since {baseline_data.get('reviewed_at', 'baseline review')}.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
