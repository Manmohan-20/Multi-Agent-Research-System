"""Design tokens + global CSS for the Nexus Research UI.

Token system
------------
Color:
    --bg            #050506   pure-black canvas
    --bg-panel      #0d0d10   panel surface
    --bg-glass      rgba(255,255,255,0.035)  glass fill
    --border        rgba(255,255,255,0.08)
    --border-soft   rgba(255,255,255,0.05)
    --text-1        #ECECF1   primary text
    --text-2        #9A9AA7   secondary text
    --text-3        #5C5C66   tertiary / placeholder
    --violet        #7B5CFA   primary accent (search / active)
    --violet-dim    #7B5CFA22
    --cyan          #35D0C0   secondary accent (success / read)
    --amber         #FFB454   tertiary accent (write / warning)
    --red           #FF6B6B   error

Type:
    Display  "Space Grotesk"  — headings, wordmark, step labels
    Body     "Inter"          — paragraphs, UI copy
    Mono     "JetBrains Mono" — logs, urls, stats, code

Signature element: the "research trail" — a horizontal chain of nodes
(Search -> Read -> Write -> Critique) connected by a line that fills
with a gradient as each agent hands off to the next. It's the one
animated, bold element; everything else stays quiet.
"""

CSS = """
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@400;500;600;700&family=Inter:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">

<style>
:root {
    --bg: #050506;
    --bg-panel: #0d0d10;
    --bg-glass: rgba(255,255,255,0.035);
    --border: rgba(255,255,255,0.08);
    --border-soft: rgba(255,255,255,0.05);
    --text-1: #ECECF1;
    --text-2: #9A9AA7;
    --text-3: #5C5C66;
    --violet: #7B5CFA;
    --violet-dim: rgba(123,92,250,0.14);
    --cyan: #35D0C0;
    --cyan-dim: rgba(53,208,192,0.14);
    --amber: #FFB454;
    --amber-dim: rgba(255,180,84,0.14);
    --red: #FF6B6B;
    --red-dim: rgba(255,107,107,0.14);
    --radius: 16px;
    --radius-sm: 10px;
}

/* ---------- base canvas ---------- */
.stApp {
    background:
        radial-gradient(circle at 15% 0%, rgba(123,92,250,0.10) 0%, transparent 45%),
        radial-gradient(circle at 85% 15%, rgba(53,208,192,0.06) 0%, transparent 40%),
        var(--bg);
    color: var(--text-1);
    font-family: 'Inter', sans-serif;
}

[data-testid="stHeader"] {
    background: transparent;
    z-index: 999990;
}
/* Hide only the "Deploy" button and status widget — keep the toolbar
   itself (and the sidebar collapse arrow that lives inside it) working. */
[data-testid="stAppDeployButton"] { display: none; }
[data-testid="stStatusWidget"] { display: none; }
footer { visibility: hidden; }

/* The sidebar show/hide controls must never be hidden or buried behind
   the glass panels (backdrop-filter creates its own stacking context). */
[data-testid="stExpandSidebarButton"],
[data-testid="stSidebarCollapseButton"] {
    display: flex !important;
    visibility: visible !important;
    opacity: 1 !important;
    pointer-events: auto !important;
    z-index: 999999 !important;
}
[data-testid="stSidebar"] {
    z-index: 999980;
}

.block-container {
    padding-top: 2.2rem;
    padding-bottom: 4rem;
    max-width: 920px;
}

h1, h2, h3, h4 {
    font-family: 'Space Grotesk', sans-serif !important;
    color: var(--text-1) !important;
    letter-spacing: -0.01em;
}

p, span, li, label, div { color: var(--text-1); }
.muted { color: var(--text-2) !important; }
code, pre, .mono { font-family: 'JetBrains Mono', monospace !important; }

/* ---------- sidebar ---------- */
[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0a0a0c 0%, #050506 100%);
    border-right: 1px solid var(--border-soft);
}
[data-testid="stSidebar"] * { color: var(--text-1); }
[data-testid="stSidebar"] .stMarkdown p { color: var(--text-2); }

/* ---------- hero ---------- */
.nx-hero {
    text-align: center;
    padding: 1.6rem 0 0.4rem 0;
}
.nx-hero .nx-eyebrow {
    display: inline-flex;
    align-items: center;
    gap: 8px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: var(--cyan);
    background: var(--cyan-dim);
    border: 1px solid rgba(53,208,192,0.25);
    padding: 5px 14px;
    border-radius: 999px;
    margin-bottom: 1.1rem;
}
.nx-hero .nx-dot {
    width: 6px; height: 6px; border-radius: 50%;
    background: var(--cyan);
    box-shadow: 0 0 8px var(--cyan);
    animation: nx-pulse 2s ease-in-out infinite;
}
.nx-hero h1 {
    font-size: 2.7rem;
    font-weight: 700;
    margin: 0;
    background: linear-gradient(120deg, #FFFFFF 30%, #B8AFFF 65%, var(--cyan) 100%);
    -webkit-background-clip: text;
    background-clip: text;
    -webkit-text-fill-color: transparent;
}
.nx-hero .nx-sub {
    color: var(--text-2);
    font-size: 1.02rem;
    margin-top: 0.6rem;
    font-weight: 400;
}
@keyframes nx-pulse {
    0%, 100% { opacity: 1; }
    50% { opacity: 0.35; }
}

/* ---------- glass panel ---------- */
.nx-panel {
    background: var(--bg-glass);
    border: 1px solid var(--border);
    border-radius: var(--radius);
    padding: 1.4rem 1.5rem;
    backdrop-filter: blur(18px);
    -webkit-backdrop-filter: blur(18px);
    box-shadow: 0 8px 32px rgba(0,0,0,0.35);
    margin-bottom: 1.1rem;
}
.nx-panel-tight { padding: 1rem 1.2rem; }

/* ---------- text input ---------- */
[data-testid="stTextInput"] input, [data-testid="stTextArea"] textarea {
    background: var(--bg-glass) !important;
    border: 1px solid var(--border) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-1) !important;
    font-family: 'Inter', sans-serif !important;
    font-size: 1rem !important;
    padding: 0.85rem 1rem !important;
}
[data-testid="stTextInput"] input:focus, [data-testid="stTextArea"] textarea:focus {
    border-color: var(--violet) !important;
    box-shadow: 0 0 0 3px var(--violet-dim) !important;
}
[data-testid="stTextInput"] input::placeholder { color: var(--text-3) !important; }

/* ---------- buttons ---------- */
.stButton button, .stDownloadButton button {
    background: var(--bg-glass);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    color: var(--text-1);
    font-family: 'Inter', sans-serif;
    font-weight: 500;
    padding: 0.55rem 1.1rem;
    transition: all 0.15s ease;
}
.stButton button:hover, .stDownloadButton button:hover {
    border-color: var(--violet);
    background: var(--violet-dim);
    color: var(--text-1);
    transform: translateY(-1px);
}
.stButton button:active { transform: translateY(0px); }

div[data-testid="stFormSubmitButton"] button,
button[kind="primary"] {
    background: linear-gradient(120deg, var(--violet), #9B7BFF) !important;
    border: none !important;
    color: white !important;
    font-weight: 600 !important;
    box-shadow: 0 4px 20px var(--violet-dim);
}
div[data-testid="stFormSubmitButton"] button:hover, button[kind="primary"]:hover {
    box-shadow: 0 6px 26px rgba(123,92,250,0.4);
    transform: translateY(-1px);
}

/* ---------- badges ---------- */
.nx-badge {
    display: inline-flex;
    align-items: center;
    gap: 6px;
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    padding: 3px 10px;
    border-radius: 999px;
    font-weight: 500;
    letter-spacing: 0.02em;
}
.nx-badge-idle   { background: rgba(255,255,255,0.06); color: var(--text-2); border: 1px solid var(--border); }
.nx-badge-run    { background: var(--violet-dim); color: #C4B5FF; border: 1px solid rgba(123,92,250,0.35); }
.nx-badge-done   { background: var(--cyan-dim); color: var(--cyan); border: 1px solid rgba(53,208,192,0.35); }
.nx-badge-error  { background: var(--red-dim); color: var(--red); border: 1px solid rgba(255,107,107,0.35); }
.nx-badge-warn   { background: var(--amber-dim); color: var(--amber); border: 1px solid rgba(255,180,84,0.35); }

/* ---------- research trail (signature element) ---------- */
.nx-trail { display: flex; align-items: flex-start; justify-content: space-between; margin: 0.6rem 0 0.3rem 0; }
.nx-trail-node { display: flex; flex-direction: column; align-items: center; flex: 1; position: relative; }
.nx-trail-circle {
    width: 38px; height: 38px; border-radius: 50%;
    display: flex; align-items: center; justify-content: center;
    font-size: 1.05rem;
    background: var(--bg-glass);
    border: 1.5px solid var(--border);
    z-index: 2;
    transition: all 0.3s ease;
}
.nx-trail-circle.done {
    border-color: var(--cyan);
    background: var(--cyan-dim);
    box-shadow: 0 0 16px rgba(53,208,192,0.35);
}
.nx-trail-circle.run {
    border-color: var(--violet);
    background: var(--violet-dim);
    box-shadow: 0 0 16px rgba(123,92,250,0.4);
    animation: nx-glow 1.4s ease-in-out infinite;
}
.nx-trail-circle.error {
    border-color: var(--red);
    background: var(--red-dim);
}
@keyframes nx-glow {
    0%, 100% { box-shadow: 0 0 10px rgba(123,92,250,0.3); }
    50% { box-shadow: 0 0 22px rgba(123,92,250,0.6); }
}
.nx-trail-label { font-size: 0.78rem; color: var(--text-2); margin-top: 8px; font-weight: 500; text-align: center; }
.nx-trail-label.active { color: var(--text-1); }
.nx-trail-line {
    position: absolute;
    top: 19px; left: 50%; width: 100%; height: 2px;
    background: var(--border-soft);
    z-index: 1;
}
.nx-trail-line-fill {
    height: 100%;
    background: linear-gradient(90deg, var(--cyan), var(--violet));
    transition: width 0.5s ease;
}
.nx-trail-node:last-child .nx-trail-line { display: none; }

/* ---------- source card ---------- */
.nx-source {
    background: var(--bg-glass);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 0.9rem 1.1rem;
    margin-bottom: 0.6rem;
    transition: border-color 0.15s ease;
}
.nx-source:hover { border-color: var(--violet); }
.nx-source-title { font-weight: 600; font-size: 0.95rem; color: var(--text-1); }
.nx-source-domain {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.72rem;
    color: var(--cyan);
    margin-left: 6px;
}
.nx-source-snippet { color: var(--text-2); font-size: 0.85rem; margin-top: 4px; line-height: 1.5; }
.nx-source-link { font-size: 0.78rem; color: var(--text-3); text-decoration: none; }

/* ---------- stat tile ---------- */
.nx-stat-grid { display: grid; grid-template-columns: 1fr 1fr; gap: 0.7rem; }
.nx-stat {
    background: var(--bg-glass);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
    padding: 0.75rem 0.9rem;
}
.nx-stat-value { font-family: 'Space Grotesk', sans-serif; font-size: 1.4rem; font-weight: 700; color: var(--text-1); }
.nx-stat-label { font-size: 0.72rem; color: var(--text-2); text-transform: uppercase; letter-spacing: 0.05em; }

/* ---------- empty state ---------- */
.nx-empty {
    text-align: center;
    padding: 3rem 1rem;
    color: var(--text-2);
}
.nx-empty .nx-empty-icon { font-size: 2.4rem; margin-bottom: 0.8rem; opacity: 0.8; }
.nx-empty .nx-empty-title { color: var(--text-1); font-family: 'Space Grotesk', sans-serif; font-size: 1.1rem; font-weight: 600; margin-bottom: 0.3rem; }

/* ---------- log line ---------- */
.nx-log {
    font-family: 'JetBrains Mono', monospace;
    font-size: 0.78rem;
    color: var(--text-2);
    padding: 3px 0;
    border-bottom: 1px solid var(--border-soft);
}
.nx-log .nx-log-time { color: var(--text-3); margin-right: 8px; }

/* ---------- misc ---------- */
hr { border-color: var(--border-soft) !important; }
[data-testid="stExpander"] {
    background: var(--bg-glass);
    border: 1px solid var(--border);
    border-radius: var(--radius-sm);
}
[data-testid="stMetricValue"] { color: var(--text-1); font-family: 'Space Grotesk', sans-serif; }
.stProgress > div > div { background: linear-gradient(90deg, var(--violet), var(--cyan)) !important; }
[data-testid="stChatMessage"] { background: var(--bg-glass); border: 1px solid var(--border); border-radius: var(--radius-sm); }

.nx-footer {
    text-align: center;
    padding-top: 2rem;
    color: var(--text-3);
    font-size: 0.8rem;
    border-top: 1px solid var(--border-soft);
    margin-top: 2.5rem;
}
.nx-footer a { color: var(--text-2); text-decoration: none; }
.nx-footer a:hover { color: var(--cyan); }
</style>
"""


def inject(st):
    st.markdown(CSS, unsafe_allow_html=True)