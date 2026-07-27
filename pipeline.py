import time
from agents import build_reader_agent, build_search_agent, writer_chain, critic_chain


class PipelineError(Exception):
    """Raised when a pipeline stage fails in a way the caller should surface to the user."""

    def __init__(self, stage: str, message: str):
        self.stage = stage
        self.message = message
        super().__init__(f"[{stage}] {message}")


def _notify(on_step, step: str, status: str, detail: str = ""):
    """Fire the optional progress callback. Safe no-op if on_step is None."""
    if on_step is not None:
        on_step(step, status, detail)


def run_research_pipeline(topic: str, on_step=None) -> dict:
    """
    Executes the full multi-agent research pipeline.

    on_step: optional callable(step: str, status: str, detail: str) invoked at
    the start/end of each stage. status is one of "running", "done", "error".
    Passing None preserves the original print-only CLI behavior.
    """

    state = {"topic": topic, "timings": {}}

    # step 1 - search agent working
    print("\n" + " =" * 50)
    print("step 1 - search agent is working ...")
    print("=" * 50)

    _notify(on_step, "search", "running")
    t0 = time.time()
    try:
        search_agent = build_search_agent()
        search_result = search_agent.invoke({
            "messages": [("user", f"Find recent, reliable and detailed information about: {topic}")]
        })
        state["search_results"] = search_result['messages'][-1].content
    except Exception as e:
        _notify(on_step, "search", "error", str(e))
        raise PipelineError("search", f"The search agent failed: {e}") from e
    state["timings"]["search"] = time.time() - t0
    _notify(on_step, "search", "done", state["search_results"])

    print("\n search result ", state['search_results'])

    # step 2 - reader agent
    print("\n" + " =" * 50)
    print("step 2 - Reader agent is scraping top resources ...")
    print("=" * 50)

    _notify(on_step, "scrape", "running")
    t0 = time.time()
    try:
        reader_agent = build_reader_agent()
        reader_result = reader_agent.invoke({
            "messages": [("user",
                f"Based on the following search results about '{topic}', "
                f"pick the most relevant URL and scrape it for deeper content.\n\n"
                f"Search Results:\n{state['search_results'][:800]}"
            )]
        })
        state['scraped_content'] = reader_result['messages'][-1].content
    except Exception as e:
        _notify(on_step, "scrape", "error", str(e))
        raise PipelineError("scrape", f"The reader agent failed: {e}") from e
    state["timings"]["scrape"] = time.time() - t0
    _notify(on_step, "scrape", "done", state["scraped_content"])

    print("\nscraped content: \n", state['scraped_content'])

    # step 3 - writer chain

    print("\n" + " =" * 50)
    print("step 3 - Writer is drafting the report ...")
    print("=" * 50)

    _notify(on_step, "write", "running")
    t0 = time.time()
    research_combined = (
        f"SEARCH RESULTS : \n {state['search_results']} \n\n"
        f"DETAILED SCRAPED CONTENT : \n {state['scraped_content']}"
    )

    try:
        state["report"] = writer_chain.invoke({
            "topic": topic,
            "research": research_combined
        })
    except Exception as e:
        _notify(on_step, "write", "error", str(e))
        raise PipelineError("write", f"The writer failed to draft the report: {e}") from e
    state["timings"]["write"] = time.time() - t0
    _notify(on_step, "write", "done", state["report"])

    print("\n Final Report\n", state['report'])

    # critic report

    print("\n" + " =" * 50)
    print("step 4 - critic is reviewing the report ")
    print("=" * 50)

    _notify(on_step, "critic", "running")
    t0 = time.time()
    try:
        state["feedback"] = critic_chain.invoke({
            "report": state['report']
        })
    except Exception as e:
        _notify(on_step, "critic", "error", str(e))
        raise PipelineError("critic", f"The critic failed to review the report: {e}") from e
    state["timings"]["critic"] = time.time() - t0
    _notify(on_step, "critic", "done", state["feedback"])

    print("\n critic report \n", state['feedback'])

    return state


if __name__ == "__main__":
    topic = input("\n Enter a research topic : ")
    run_research_pipeline(topic)