"""Render functions used by app.py. Each function writes directly to the
Streamlit app via st.markdown/st.* — nothing here touches pipeline logic.
"""

import re
from typing import List, Dict, Optional
import streamlit as st
from utils import format_duration, now_stamp

STEPS = [
    {"key": "search", "label": "Searching", "icon": "🔎"},
    {"key": "scrape", "label": "Reading", "icon": "📄"},
    {"key": "write", "label": "Writing", "icon": "✍️"},
    {"key": "critic", "label": "Reviewing", "icon": "🧠"},
]


def _md(html: str):
    """st.markdown(html, unsafe_allow_html=True), but strips leading
    whitespace from every line first.

    Streamlit renders unsafe_allow_html content through a Markdown parser.
    Markdown treats a line indented 4+ spaces as the start of an *indented
    code block*, so HTML built inside an indented Python function (the
    natural way to write it) gets displayed as literal text instead of
    being rendered — that's what was showing up on screen. Stripping
    per-line indentation avoids that without changing the HTML itself.
    """
    st.markdown(re.sub(r"(?m)^[ \t]+", "", html.strip()), unsafe_allow_html=True)


def render_hero():
    _md("""
        <div class="nx-hero">
            <span class="nx-eyebrow"><span class="nx-dot"></span>Multi-Agent Research System</span>
            <h1>Nexus Research</h1>
            <p class="nx-sub">Four agents, one report. Search, read, write and critique — end to end.</p>
        </div>
        """)


def render_trail(status: Dict[str, str]):
    """status: {step_key: 'idle' | 'running' | 'done' | 'error'}"""
    nodes_html = []
    for i, step in enumerate(STEPS):
        s = status.get(step["key"], "idle")
        circle_class = {"idle": "", "running": "run", "done": "done", "error": "error"}[s]
        icon = "✓" if s == "done" else ("✕" if s == "error" else step["icon"])
        label_class = "active" if s in ("running", "done") else ""

        fill_width = "0%"
        if s == "done":
            fill_width = "100%"
        elif s == "running":
            fill_width = "50%"

        line_html = (
            f'<div class="nx-trail-line"><div class="nx-trail-line-fill" style="width:{fill_width}"></div></div>'
            if i < len(STEPS) - 1 else ""
        )

        nodes_html.append(f"""
            <div class="nx-trail-node">
                {line_html}
                <div class="nx-trail-circle {circle_class}">{icon}</div>
                <div class="nx-trail-label {label_class}">{step['label']}</div>
            </div>
        """)

    _md(f'<div class="nx-trail">{"".join(nodes_html)}</div>')


def render_badge(text: str, kind: str = "idle"):
    _md(f'<span class="nx-badge nx-badge-{kind}">{text}</span>')


def render_sources(sources: List[Dict[str, str]]):
    if not sources:
        render_empty("🗂️", "No sources yet", "Run a research query to collect sources here.")
        return

    for i, s in enumerate(sources, 1):
        _md(f"""
            <div class="nx-source">
                <div><span class="nx-source-title">{i}. {s['title']}</span>
                <span class="nx-source-domain">{s['domain']}</span></div>
                <div class="nx-source-snippet">{s['snippet']}</div>
                <a class="nx-source-link" href="{s['url']}" target="_blank">{s['url']}</a>
            </div>
            """)


def render_empty(icon: str, title: str, subtitle: str):
    _md(f"""
        <div class="nx-empty">
            <div class="nx-empty-icon">{icon}</div>
            <div class="nx-empty-title">{title}</div>
            <div class="muted">{subtitle}</div>
        </div>
        """)


def render_stat_grid(stats: List[Dict[str, str]]):
    tiles = "".join(
        f"""<div class="nx-stat">
                <div class="nx-stat-value">{s['value']}</div>
                <div class="nx-stat-label">{s['label']}</div>
            </div>"""
        for s in stats
    )
    _md(f'<div class="nx-stat-grid">{tiles}</div>')


def render_log_line(text: str):
    _md(f'<div class="nx-log"><span class="nx-log-time">{now_stamp()}</span>{text}</div>')


def render_footer():
    _md("""
        <div class="nx-footer">
            Made with ❤️ using Streamlit &nbsp;·&nbsp;
            <a href="https://github.com/Manmohan-20/Multi-Agent-Research-System" target="_blank">GitHub Repository</a> &nbsp;·&nbsp;
            v1.0.0 &nbsp;·&nbsp; MIT License
        </div>
        """)