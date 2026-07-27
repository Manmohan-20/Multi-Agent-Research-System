<div align="center">

# 🧭 Nexus Research

### A Multi-Agent GenAI Research System

*Four autonomous LLM agents — Search, Read, Write, Critique — collaborating end-to-end to turn a single topic into a polished, sourced research report.*

![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=flat&logo=python&logoColor=white)
![LangChain](https://img.shields.io/badge/LangChain-Agents-1C3C3C?style=flat&logo=langchain&logoColor=white)
![Mistral AI](https://img.shields.io/badge/Mistral%20AI-LLM-FF7000?style=flat)
![Streamlit](https://img.shields.io/badge/Streamlit-Frontend-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green?style=flat)

</div>

---

## 🧠 What this is

**Nexus Research** is a multi-agent GenAI application: instead of one LLM call answering a question from memory, a coordinated team of agents actively **searches the live web, reads real sources, writes a structured report, and critiques its own output** — the same workflow a human researcher follows, automated end to end and wrapped in a premium, production-style Streamlit interface.

It's built to demonstrate practical, working knowledge of:
- **Agentic AI system design** — multiple specialized agents with distinct tools, orchestrated as a pipeline rather than one monolithic prompt
- **Tool-using LLMs** — agents that call real functions (web search, web scraping) and reason over the results
- **LLM-as-a-judge / self-critique loops** — a dedicated critic agent scores and reviews the writer's output
- **Production-grade frontend engineering around an AI backend** — background execution, live progress, structured error handling, and a fully custom design system

---

## 🤖 How the agents work together

```
   ┌─────────────┐     ┌─────────────┐     ┌─────────────┐     ┌─────────────┐
   │   🔎 SEARCH  │ ──▶ │   📄 READ    │ ──▶ │   ✍️ WRITE   │ ──▶ │  🧠 CRITIQUE │
   │    Agent     │     │    Agent     │     │    Chain     │     │    Chain     │
   └─────────────┘     └─────────────┘     └─────────────┘     └─────────────┘
   Tavily web search    Scrapes the top     Drafts a structured   Scores the report,
   → titles, URLs,      result for deep     report: intro, key    lists strengths &
   snippets             page content        findings, sources     areas to improve
```

1. **Search Agent** (LangChain agent + Tavily tool) — finds recent, reliable sources for the given topic and returns titles, URLs, and snippets.
2. **Reader Agent** (LangChain agent + BeautifulSoup scraping tool) — picks the most relevant result and scrapes it for deeper, unstructured page content.
3. **Writer Chain** (prompt → Mistral LLM → output parser) — synthesizes the search results and scraped content into a structured report: Introduction, Key Findings, Conclusion, Sources.
4. **Critic Chain** (prompt → Mistral LLM → output parser) — independently reviews the report and returns a strict score out of 10, strengths, and areas to improve — a self-critique / LLM-as-a-judge step.

Each stage's output feeds the next, and the whole run is orchestrated by a single pipeline function with per-stage error handling and live progress callbacks.

---

## ✨ Features

### Core AI pipeline
- 🔎 Real-time web search via **Tavily**
- 📄 Live web scraping of source pages with **BeautifulSoup**
- ✍️ Structured report generation with a dedicated writer prompt chain
- 🧠 Automated critique / scoring of the generated report (LLM-as-a-judge)
- ⚙️ Powered by **Mistral AI** (`mistral-small`) through **LangChain**
- 🧩 Modular agent architecture — each agent has exactly one tool and one job

### Frontend / product experience
- 🎨 Custom dark **glassmorphism** design system — no default Streamlit look
- 🧵 **Background execution** — agents run in a worker thread so the UI never freezes
- 📊 A live **"research trail"** — an animated, connected node tracker showing which agent is active in real time
- ⏹ Best-effort **Stop** control for long-running research jobs
- 📋 Tabbed results: **Report**, **Critic Review**, **Sources**
- 🔗 A structured **sources panel** — title, domain, snippet, and clickable link per source
- ⬇️ Export the report as **Markdown** or **TXT**, with a one-click **copy** block
- 🕒 **Session history** with keyword search and one-click reopen of past reports
- 📈 Sidebar research statistics — searches run, pages read, reports generated, session duration
- 🩺 Live system status checks for required API keys
- 🛡️ Friendly, human-readable error handling for network failures, scraping failures, empty queries, and API errors — no raw Python tracebacks reach the UI

---

## 🛠️ Tech stack

| Layer | Technology |
|---|---|
| LLM | Mistral AI (`mistral-small-2506`) |
| Agent framework | LangChain (`create_agent`, tool-calling agents) |
| Orchestration | Custom Python pipeline with callback-based progress hooks |
| Web search tool | Tavily API |
| Web scraping tool | Requests + BeautifulSoup4 |
| Concurrency | Python `threading` + `queue` for non-blocking UI execution |
| Frontend | Streamlit, custom CSS (glassmorphism, Space Grotesk / Inter / JetBrains Mono) |
| Config | `python-dotenv` |

---

## 📁 Project structure

```
nexus-research/
├── app.py              # Streamlit entry point — UI orchestration only
├── components.py        # Reusable render functions (hero, trail, sources, stats…)
├── styles.py             # Design tokens + global CSS, injected once
├── utils.py               # Parsing / formatting / export helpers (no UI, no agents)
├── pipeline.py            # Orchestration: search → read → write → critique
├── agents.py               # Agent + chain definitions, LLM config, prompts
├── tools.py                 # web_search (Tavily) and scrape_url (BeautifulSoup) tools
├── requirements.txt
├── .env.example
└── README.md
```

The AI backend (`tools.py`, `agents.py`, `pipeline.py`) is fully decoupled from the UI — `python pipeline.py` runs the whole research pipeline standalone from the terminal, no Streamlit required.

---

## 🚀 Getting started

### 1. Clone and install

```bash
git clone https://github.com/<your-username>/nexus-research.git
cd nexus-research
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Add your API keys

```bash
cp .env.example .env
```

```env
MISTRAL_API_KEY=your_mistral_api_key_here
TAVILY_API_KEY=your_tavily_api_key_here
```

- Mistral AI key → https://console.mistral.ai
- Tavily key → https://tavily.com

### 3. Run it

```bash
streamlit run app.py
```

Or run the raw agent pipeline from the CLI:

```bash
python pipeline.py
```

---

## 🧭 Usage

1. Enter a research topic (e.g. *"The impact of small modular reactors on grid decarbonization"*).
2. Click **Start Research** and watch the research trail move through Search → Read → Write → Critique in real time.
3. Review the generated **Report**, the **Critic's** score and feedback, and the full list of **Sources**.
4. Export the report as Markdown/TXT, or revisit it later from **Session history**.

---

## 📄 License

MIT — see [LICENSE](LICENSE) for details.

---

<div align="center">

Built as a hands-on exploration of agentic GenAI systems — multi-agent orchestration, tool use, and self-critique — wrapped in a production-quality interface.

</div>