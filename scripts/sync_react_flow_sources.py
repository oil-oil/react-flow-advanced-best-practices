#!/usr/bin/env python3
"""Sync official React Flow advanced docs and recent React package releases.

This script intentionally uses only official sources:
- reactflow.dev
- github.com/xyflow/xyflow releases via GitHub API
"""

from __future__ import annotations

import argparse
import json
import re
from dataclasses import dataclass
from datetime import datetime, timezone
from html import unescape
from pathlib import Path
from typing import Iterable, List
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen

SITEMAP_URL = "https://reactflow.dev/sitemap.xml"
GITHUB_RELEASES_API = "https://api.github.com/repos/xyflow/xyflow/releases?per_page=30"

MANDATORY_URLS = [
    "https://reactflow.dev/learn/advanced-use/performance",
    "https://reactflow.dev/learn/advanced-use/computing-flows",
    "https://reactflow.dev/learn/advanced-use/ssr-ssg-configuration",
    "https://reactflow.dev/learn/advanced-use/multiplayer",
    "https://reactflow.dev/learn/advanced-use/whiteboard",
    "https://reactflow.dev/learn/layouting/layouting",
    "https://reactflow.dev/learn/layouting/sub-flows",
    "https://reactflow.dev/learn/troubleshooting/migrate-to-v12",
    "https://reactflow.dev/api-reference/hooks/use-react-flow",
    "https://reactflow.dev/api-reference/hooks/use-store",
    "https://reactflow.dev/api-reference/hooks/use-node-connections",
    "https://reactflow.dev/api-reference/hooks/use-nodes-data",
    "https://reactflow.dev/api-reference/hooks/use-handle-connections",
    "https://reactflow.dev/api-reference/types/react-flow-instance",
    "https://reactflow.dev/api-reference/types/z-index-mode",
]


@dataclass
class PageInfo:
    url: str
    title: str
    updated_human: str
    updated_iso: str
    headings: List[str]


def fetch_text(url: str, timeout: int) -> str:
    req = Request(url, headers={"User-Agent": "codex-react-flow-skill/1.0"})
    with urlopen(req, timeout=timeout) as resp:
        charset = resp.headers.get_content_charset() or "utf-8"
        return resp.read().decode(charset, "ignore")


def strip_tags(text: str) -> str:
    text = re.sub(r"<[^>]+>", "", text)
    text = unescape(text)
    text = re.sub(r"\s+", " ", text).strip()
    return text


def dedupe_preserve_order(items: Iterable[str]) -> List[str]:
    seen = set()
    out: List[str] = []
    for item in items:
        if not item or item in seen:
            continue
        seen.add(item)
        out.append(item)
    return out


def extract_page_info(url: str, html_text: str, max_headings: int) -> PageInfo:
    title_match = re.search(r"<title>(.*?)</title>", html_text, re.IGNORECASE | re.DOTALL)
    title = strip_tags(title_match.group(1)) if title_match else url

    time_match = re.search(
        r"Last updated on<!-- -->\s*<time[^>]*dateTime=\"([^\"]+)\"[^>]*>([^<]+)</time>",
        html_text,
        re.IGNORECASE,
    )
    if time_match:
        updated_iso = time_match.group(1)
        updated_human = strip_tags(time_match.group(2))
    else:
        updated_iso = ""
        updated_human = "n/a"

    headings: List[str] = []
    for level in (2, 3):
        for match in re.finditer(
            rf"<h{level}[^>]*>(.*?)</h{level}>",
            html_text,
            re.IGNORECASE | re.DOTALL,
        ):
            heading = strip_tags(match.group(1))
            if heading:
                headings.append(heading)

    return PageInfo(
        url=url,
        title=title,
        updated_human=updated_human,
        updated_iso=updated_iso,
        headings=dedupe_preserve_order(headings)[:max_headings],
    )


def fetch_react_releases(timeout: int, max_releases: int) -> List[dict]:
    text = fetch_text(GITHUB_RELEASES_API, timeout)
    data = json.loads(text)
    react_releases = [r for r in data if r.get("tag_name", "").startswith("@xyflow/react@")]

    out = []
    for rel in react_releases[:max_releases]:
        body = rel.get("body") or ""
        bullet_lines = []
        for line in body.splitlines():
            line = line.strip()
            if not line.startswith("-"):
                continue
            cleaned = re.sub(r"\s+", " ", line)
            cleaned = cleaned.lstrip("- ").strip()
            bullet_lines.append(cleaned)
        out.append(
            {
                "tag": rel.get("tag_name", ""),
                "name": rel.get("name", ""),
                "published_at": rel.get("published_at", ""),
                "url": rel.get("html_url", ""),
                "highlights": bullet_lines[:8],
            }
        )
    return out


def discover_advanced_urls(timeout: int) -> List[str]:
    xml_text = fetch_text(SITEMAP_URL, timeout)
    urls = re.findall(r"<loc>(.*?)</loc>", xml_text)
    advanced = [u for u in urls if "/learn/advanced-use/" in u]
    return sorted(set(advanced))


def build_markdown(
    generated_at: str,
    advanced_urls: List[str],
    pages: List[PageInfo],
    releases: List[dict],
) -> str:
    lines: List[str] = []
    lines.append("# React Flow Official Snapshot")
    lines.append("")
    lines.append(f"Generated at (UTC): {generated_at}")
    lines.append("Sources: reactflow.dev docs + GitHub releases for @xyflow/react")
    lines.append("")

    lines.append("## Advanced docs discovered from sitemap")
    for url in advanced_urls:
        lines.append(f"- {url}")
    lines.append("")

    lines.append("## Mandatory pages snapshot")
    for page in pages:
        lines.append(f"### {page.title}")
        lines.append(f"- URL: {page.url}")
        lines.append(f"- Last updated: {page.updated_human}")
        if page.updated_iso:
            lines.append(f"- Last updated (ISO): {page.updated_iso}")
        if page.headings:
            lines.append("- Key headings:")
            for h in page.headings:
                lines.append(f"  - {h}")
        lines.append("")

    lines.append("## Recent @xyflow/react releases")
    if not releases:
        lines.append("- No release data returned.")
    for rel in releases:
        lines.append(f"### {rel['tag']}")
        lines.append(f"- Published: {rel['published_at']}")
        lines.append(f"- URL: {rel['url']}")
        if rel["highlights"]:
            lines.append("- Highlights:")
            for item in rel["highlights"]:
                lines.append(f"  - {item}")
        lines.append("")

    return "\n".join(lines).rstrip() + "\n"


def main() -> int:
    script_dir = Path(__file__).resolve().parent
    skill_dir = script_dir.parent
    default_md = skill_dir / "references" / "react-flow-latest-snapshot.md"
    default_json = skill_dir / "references" / "react-flow-latest-snapshot.json"

    parser = argparse.ArgumentParser(description="Sync React Flow advanced docs and releases.")
    parser.add_argument("--output-md", default=str(default_md), help="Path to markdown snapshot output")
    parser.add_argument("--output-json", default=str(default_json), help="Path to JSON snapshot output")
    parser.add_argument("--timeout", type=int, default=25, help="HTTP timeout seconds")
    parser.add_argument("--max-headings", type=int, default=10, help="Max h2/h3 headings per page")
    parser.add_argument("--max-releases", type=int, default=4, help="Max recent @xyflow/react releases")
    args = parser.parse_args()

    generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    errors: List[str] = []

    try:
        advanced_urls = discover_advanced_urls(args.timeout)
    except (HTTPError, URLError, TimeoutError) as exc:
        advanced_urls = []
        errors.append(f"Failed to load sitemap: {exc}")

    pages: List[PageInfo] = []
    for url in MANDATORY_URLS:
        try:
            html_text = fetch_text(url, args.timeout)
            pages.append(extract_page_info(url, html_text, args.max_headings))
        except (HTTPError, URLError, TimeoutError) as exc:
            errors.append(f"Failed to load {url}: {exc}")

    try:
        releases = fetch_react_releases(args.timeout, args.max_releases)
    except (HTTPError, URLError, TimeoutError, json.JSONDecodeError) as exc:
        releases = []
        errors.append(f"Failed to load releases: {exc}")

    json_payload = {
        "generated_at_utc": generated_at,
        "advanced_urls": advanced_urls,
        "mandatory_urls": MANDATORY_URLS,
        "pages": [
            {
                "url": p.url,
                "title": p.title,
                "updated_human": p.updated_human,
                "updated_iso": p.updated_iso,
                "headings": p.headings,
            }
            for p in pages
        ],
        "releases": releases,
        "errors": errors,
    }

    md_text = build_markdown(generated_at, advanced_urls, pages, releases)
    if errors:
        md_text += "\n## Fetch errors\n"
        for err in errors:
            md_text += f"- {err}\n"

    md_path = Path(args.output_md)
    json_path = Path(args.output_json)
    md_path.parent.mkdir(parents=True, exist_ok=True)
    json_path.parent.mkdir(parents=True, exist_ok=True)

    md_path.write_text(md_text, encoding="utf-8")
    json_path.write_text(json.dumps(json_payload, indent=2, ensure_ascii=True) + "\n", encoding="utf-8")

    print(f"Wrote markdown snapshot: {md_path}")
    print(f"Wrote JSON snapshot: {json_path}")
    if errors:
        print("Completed with fetch errors:")
        for err in errors:
            print(f"- {err}")
        return 2

    print(f"Fetched {len(pages)} pages and {len(releases)} releases.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
