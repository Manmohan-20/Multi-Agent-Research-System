"""Small, dependency-free helpers for the Streamlit frontend.

Nothing here touches the agent/pipeline logic — it only reshapes the
strings that pipeline.py already produces so the UI can render them
nicely (sources, timestamps, exports).
"""

from __future__ import annotations

import re
from datetime import datetime
from urllib.parse import urlparse
from typing import List, Dict


def parse_sources(search_results_text: str) -> List[Dict[str, str]]:
    """Turn the raw 'Title: ... URL: ... Snippet: ...' blob from web_search
    into a list of {title, url, domain, snippet} dicts for the sources panel.
    """
    if not search_results_text:
        return []

    blocks = [b.strip() for b in search_results_text.split("----") if b.strip()]
    sources = []

    for block in blocks:
        title_match = re.search(r"Title:\s*(.+)", block)
        url_match = re.search(r"URL:\s*(\S+)", block)
        snippet_match = re.search(r"Snippet:\s*(.+)", block, re.DOTALL)

        if not url_match:
            continue

        url = url_match.group(1).strip()
        title = title_match.group(1).strip() if title_match else url
        snippet = snippet_match.group(1).strip() if snippet_match else ""
        domain = urlparse(url).netloc.replace("www.", "")

        sources.append({
            "title": title,
            "url": url,
            "domain": domain or "unknown",
            "snippet": snippet,
        })

    return sources


def extract_all_urls(*texts: str) -> List[str]:
    """Fallback URL extraction across any raw text blobs (search + scrape + report)."""
    urls = []
    seen = set()
    for text in texts:
        if not text:
            continue
        for url in re.findall(r"https?://[^\s\)\]\"'>]+", text):
            clean = url.rstrip(").,;:")
            if clean not in seen:
                seen.add(clean)
                urls.append(clean)
    return urls


def format_duration(seconds: float) -> str:
    if seconds < 1:
        return f"{seconds * 1000:.0f} ms"
    if seconds < 60:
        return f"{seconds:.1f} s"
    minutes, secs = divmod(seconds, 60)
    return f"{int(minutes)}m {secs:.0f}s"


def now_stamp() -> str:
    return datetime.now().strftime("%H:%M:%S")


def today_stamp() -> str:
    return datetime.now().strftime("%b %d, %Y")


def slugify(text: str, max_len: int = 40) -> str:
    slug = re.sub(r"[^a-zA-Z0-9\s-]", "", text).strip().lower()
    slug = re.sub(r"[\s]+", "-", slug)
    return slug[:max_len] or "research-report"


def build_markdown_export(topic: str, report: str, feedback: str, sources: List[Dict[str, str]]) -> str:
    parts = [
        f"# Research Report: {topic}",
        f"*Generated on {today_stamp()}*",
        "",
        "---",
        "",
        report.strip(),
        "",
        "---",
        "",
        "## Critic Review",
        "",
        feedback.strip(),
    ]

    if sources:
        parts += ["", "---", "", "## Sources"]
        for i, s in enumerate(sources, 1):
            parts.append(f"{i}. [{s['title']}]({s['url']}) — {s['domain']}")

    return "\n".join(parts)


def build_txt_export(topic: str, report: str, feedback: str) -> str:
    return (
        f"RESEARCH REPORT: {topic}\n"
        f"Generated on {today_stamp()}\n"
        f"{'=' * 60}\n\n"
        f"{report.strip()}\n\n"
        f"{'=' * 60}\n"
        f"CRITIC REVIEW\n"
        f"{'=' * 60}\n\n"
        f"{feedback.strip()}\n"
    )


def word_count(text: str) -> int:
    return len(text.split()) if text else 0