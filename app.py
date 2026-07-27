"""
Nexus Research — premium Streamlit frontend for the multi-agent
research pipeline defined in tools.py / agents.py / pipeline.py.

Backend logic is untouched: this file only orchestrates the UI,
drives the pipeline in a background thread so the app stays
responsive, and renders results.
"""

import os
import time
import threading
import queue as queue_module
from datetime import datetime

import streamlit as st

import styles
import components as ui
from utils import (
    parse_sources, extract_all_urls, format_duration,
    build_markdown_export, build_txt_export, slugify, word_count,
)
from pipeline import run_research_pipeline, PipelineError

# --------------------------------------------------------------------------
# Page config — must be the first Streamlit call
# --------------------------------------------------------------------------
st.set_page_config(
    page_title="Nexus Research",
    page_icon="🧭",
    layout="wide",
    initial_sidebar_state="expanded",
)
styles.inject(st)

STEP_KEYS = [s["key"] for s in ui.STEPS]

# --------------------------------------------------------------------------
# Session state
# --------------------------------------------------------------------------
defaults = {
    "history": [],
    "thread": None,
    "stop_event": None,
    "queue": None,
    "running": False,
    "step_status": {k: "idle" for k in STEP_KEYS},
    "logs": [],
    "current_topic": "",
    "current_result": None,
    "current_error": None,
    "session_start": time.time(),
    "total_reports": 0,
    "total_searches": 0,
    "total_scrapes": 0,
    "topic_input": "",
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value


# --------------------------------------------------------------------------
# Background worker
# --------------------------------------------------------------------------
def _worker(topic: str, q: "queue_module.Queue", stop_event: threading.Event):
    def on_step(step, status, detail):
        if stop_event.is_set():
            raise PipelineError(step, "Stopped by user.")
        q.put(("step", step, status, detail))

    try:
        result = run_research_pipeline(topic, on_step=on_step)
        q.put(("done", result))
    except PipelineError as e:
        q.put(("error", e.stage, e.message))
    except Exception as e:
        q.put(("error", "unknown", f"Unexpected error: {e}"))


def start_research(topic: str):
    topic = topic.strip()
    if len(topic) < 3:
        st.session_state.current_error = ("validation", "Enter a topic with at least 3 characters.")
        return

    st.session_state.running = True
    st.session_state.current_topic = topic
    st.session_state.current_result = None
    st.session_state.current_error = None
    st.session_state.step_status = {k: "idle" for k in STEP_KEYS}
    st.session_state.logs = []

    q = queue_module.Queue()
    stop_event = threading.Event()
    thread = threading.Thread(target=_worker, args=(topic, q, stop_event), daemon=True)

    st.session_state.queue = q
    st.session_state.stop_event = stop_event
    st.session_state.thread = thread
    thread.start()


def stop_research():
    if st.session_state.stop_event:
        st.session_state.stop_event.set()
    ui_log("Stop requested — finishing the current stage, then halting.")


def clear_session():
    st.session_state.current_topic = ""
    st.session_state.current_result = None
    st.session_state.current_error = None
    st.session_state.step_status = {k: "idle" for k in STEP_KEYS}
    st.session_state.logs = []
    st.session_state.topic_input = ""


def ui_log(message: str):
    st.session_state.logs.append(message)


def drain_queue():
    q = st.session_state.queue
    if q is None:
        return
    while True:
        try:
            msg = q.get_nowait()
        except queue_module.Empty:
            break

        if msg[0] == "step":
            _, step, status, detail = msg
            st.session_state.step_status[step] = status
            label = next(s["label"] for s in ui.STEPS if s["key"] == step)
            if status == "running":
                ui_log(f"{label} started…")
            elif status == "done":
                ui_log(f"{label} completed.")
                if step == "search":
                    st.session_state.total_searches += 1
                if step == "scrape":
                    st.session_state.total_scrapes += 1

        elif msg[0] == "done":
            result = msg[1]
            sources = parse_sources(result.get("search_results", ""))
            if not sources:
                # fall back to any URLs found anywhere in the research text
                sources = [
                    {"title": u, "url": u, "domain": u.split("/")[2] if "//" in u else u, "snippet": ""}
                    for u in extract_all_urls(result.get("search_results", ""), result.get("scraped_content", ""))
                ]
            record = {
                "id": slugify(st.session_state.current_topic) + "-" + datetime.now().strftime("%H%M%S"),
                "topic": st.session_state.current_topic,
                "report": result.get("report", ""),
                "feedback": result.get("feedback", ""),
                "sources": sources,
                "timings": result.get("timings", {}),
                "timestamp": datetime.now(),
            }
            st.session_state.current_result = record
            st.session_state.history.insert(0, record)
            st.session_state.total_reports += 1
            st.session_state.running = False
            ui_log("Report finalized successfully.")

        elif msg[0] == "error":
            _, stage, message = msg
            st.session_state.current_error = (stage, message)
            st.session_state.running = False
            ui_log(f"Error during {stage}: {message}")


# --------------------------------------------------------------------------
# Sidebar
# --------------------------------------------------------------------------
with st.sidebar:
    st.markdown("### 🧭 Nexus Research")
    st.caption("A multi-agent research system: a search agent, a reader agent, "
               "a writer, and a critic collaborate on every report.")

    st.link_button("⭐ View on GitHub", "https://github.com", use_container_width=True)

    st.markdown("---")
    with st.expander("⚙️ Settings & model", expanded=False):
        st.markdown("**Model:** `mistral-small-2506`")
        st.markdown("**Theme:** Dark glass")
        st.markdown("**Provider:** Mistral AI via LangChain")

    with st.expander("🩺 System status", expanded=False):
        mistral_ok = bool(os.getenv("MISTRAL_API_KEY"))
        tavily_ok = bool(os.getenv("TAVILY_API_KEY"))
        c1, c2 = st.columns(2)
        with c1:
            st.markdown("Mistral key")
            ui.render_badge("Connected" if mistral_ok else "Missing", "done" if mistral_ok else "error")
        with c2:
            st.markdown("Tavily key")
            ui.render_badge("Connected" if tavily_ok else "Missing", "done" if tavily_ok else "error")

    st.markdown("---")
    st.markdown("**Research statistics**")
    session_minutes = (time.time() - st.session_state.session_start) / 60
    ui.render_stat_grid([
        {"value": st.session_state.total_reports, "label": "Reports"},
        {"value": st.session_state.total_searches, "label": "Searches"},
        {"value": st.session_state.total_scrapes, "label": "Pages read"},
        {"value": f"{session_minutes:.0f}m", "label": "Session"},
    ])

    st.markdown("---")
    with st.expander("ℹ️ About"):
        st.write(
            "Nexus Research pairs four LangChain agents — search, read, write, "
            "critique — into one pipeline, wrapped in a Streamlit interface "
            "built for clarity during a long-running research task."
        )

    st.markdown("---")
    st.markdown("**Session controls**")
    sc1, sc2 = st.columns(2)
    with sc1:
        if st.button("🗑️ Clear history", use_container_width=True, disabled=not st.session_state.history):
            st.session_state.history = []
            st.session_state.total_reports = 0
            st.rerun()
    with sc2:
        if st.button("♻️ Reset session", use_container_width=True):
            for key, value in defaults.items():
                st.session_state[key] = value
            st.rerun()


# --------------------------------------------------------------------------
# Hero + input
# --------------------------------------------------------------------------
ui.render_hero()

with st.container():
    st.markdown('<div class="nx-panel">', unsafe_allow_html=True)

    with st.form(key="research_form", clear_on_submit=False):
        topic = st.text_input(
            "Research topic",
            key="topic_input",
            placeholder="e.g. The impact of small modular reactors on grid decarbonization",
            label_visibility="collapsed",
            disabled=st.session_state.running,
        )
        b1, b2, b3 = st.columns([2, 1, 1])
        with b1:
            start_clicked = st.form_submit_button(
                "🚀 Start Research", use_container_width=True, type="primary",
                disabled=st.session_state.running,
            )
        with b2:
            stop_clicked = st.form_submit_button(
                "⏹ Stop", use_container_width=True, disabled=not st.session_state.running,
            )
        with b3:
            clear_clicked = st.form_submit_button(
                "🧹 Clear", use_container_width=True, disabled=st.session_state.running,
            )

    st.markdown('</div>', unsafe_allow_html=True)

if start_clicked:
    start_research(topic)
    st.rerun()

if stop_clicked:
    stop_research()

if clear_clicked:
    clear_session()
    st.rerun()

if st.session_state.current_error and st.session_state.current_error[0] == "validation":
    st.warning(st.session_state.current_error[1])


# --------------------------------------------------------------------------
# Progress section
# --------------------------------------------------------------------------
if st.session_state.running or any(v != "idle" for v in st.session_state.step_status.values()):
    st.markdown('<div class="nx-panel">', unsafe_allow_html=True)
    st.markdown("#### Execution")
    ui.render_trail(st.session_state.step_status)

    if st.session_state.running:
        st.progress(
            sum(1 for v in st.session_state.step_status.values() if v == "done") / len(STEP_KEYS),
            text="Working…",
        )

    with st.expander("📜 Live log", expanded=st.session_state.running):
        if st.session_state.logs:
            for line in st.session_state.logs[-30:]:
                ui.render_log_line(line)
        else:
            st.caption("No activity yet.")
    st.markdown('</div>', unsafe_allow_html=True)

# Drain queue + keep polling while a job is running
if st.session_state.running:
    drain_queue()
    if st.session_state.running:
        time.sleep(0.6)
        st.rerun()
    else:
        st.rerun()

# Surface pipeline errors
if st.session_state.current_error and st.session_state.current_error[0] != "validation":
    stage, message = st.session_state.current_error
    st.error(f"**{stage.title()} stage failed.** {message}\n\nTry again, or try a more specific topic — "
              "network hiccups and rate limits are the most common cause.")


# --------------------------------------------------------------------------
# Results section
# --------------------------------------------------------------------------
result = st.session_state.current_result

st.markdown("#### Results")
st.markdown('<div class="nx-panel">', unsafe_allow_html=True)

if not result:
    ui.render_empty("🧭", "No research yet", "Enter a topic above and start your first research run.")
else:
    top_stats = [
        {"value": word_count(result["report"]), "label": "Words"},
        {"value": len(result["sources"]), "label": "Sources"},
        {"value": format_duration(sum(result["timings"].values())) if result["timings"] else "—", "label": "Total time"},
        {"value": result["timestamp"].strftime("%H:%M"), "label": "Generated"},
    ]
    ui.render_stat_grid(top_stats)
    st.markdown("<br>", unsafe_allow_html=True)

    tab_report, tab_critic, tab_sources = st.tabs(["📄 Report", "🧠 Critic Review", "🔗 Sources"])

    with tab_report:
        st.markdown(result["report"])
        with st.expander("📋 Copy report (plain text)"):
            st.code(result["report"], language="markdown")

    with tab_critic:
        st.markdown(result["feedback"])

    with tab_sources:
        ui.render_sources(result["sources"])

    st.markdown("<br>", unsafe_allow_html=True)
    d1, d2, d3 = st.columns(3)
    md_export = build_markdown_export(result["topic"], result["report"], result["feedback"], result["sources"])
    txt_export = build_txt_export(result["topic"], result["report"], result["feedback"])
    fname = slugify(result["topic"])

    with d1:
        st.download_button("⬇️ Download Markdown", md_export, file_name=f"{fname}.md",
                            mime="text/markdown", use_container_width=True)
    with d2:
        st.download_button("⬇️ Download TXT", txt_export, file_name=f"{fname}.txt",
                            mime="text/plain", use_container_width=True)
    with d3:
        st.download_button("⬇️ Download History (JSON)",
                            str([{"topic": h["topic"], "report": h["report"]} for h in st.session_state.history]),
                            file_name="research_history.json", mime="application/json",
                            use_container_width=True, disabled=not st.session_state.history)

st.markdown('</div>', unsafe_allow_html=True)


# --------------------------------------------------------------------------
# History
# --------------------------------------------------------------------------
if st.session_state.history:
    st.markdown("#### Session history")
    st.markdown('<div class="nx-panel">', unsafe_allow_html=True)
    search_term = st.text_input("Search history", placeholder="Filter past reports by keyword…",
                                 label_visibility="collapsed")
    visible = [
        h for h in st.session_state.history
        if search_term.lower() in h["topic"].lower()
    ] if search_term else st.session_state.history

    for h in visible[:15]:
        with st.expander(f"{h['topic']}  ·  {h['timestamp'].strftime('%b %d, %H:%M')}"):
            st.markdown(h["report"])
            if st.button("Reopen as current report", key=f"reopen-{h['id']}"):
                st.session_state.current_result = h
                st.rerun()
    st.markdown('</div>', unsafe_allow_html=True)


ui.render_footer()