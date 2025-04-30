# /tests/test_cli_flow.py
import pytest

from graphs.main_graph import build_main_graph
from memory.checkpointer import get_checkpointer


@pytest.fixture
def engine(tmp_path):
    """
    Fresh LangGraph runnable with a temporary SQLite DB for each test
    (one DB per pytest tmp directory).
    """
    temp_db = tmp_path / "focus_test.db"
    checkpointer = get_checkpointer(path=str(temp_db))

    graph = build_main_graph()                 # compiled Runnable
    # Bind the checkpointer once; other options (stream, recursion_limit …)
    # could be added in the same dict.
    return graph.with_config({"checkpointer": checkpointer})


def _cfg(thread_id: str) -> dict:
    """Convenience helper to build a RunnableConfig for each invoke."""
    return {"configurable": {"thread_id": thread_id}}


def test_plan_creation_flow(engine):
    thread_id = "test-thread-001"

    # Step 1: user asks to create a plan
    r1 = engine.invoke(
        {"user_msg": "I want to launch a personal blog before summer."},
        _cfg(thread_id),
    )
    assert "deadline" in r1["assistant_response"].lower() \
        or "target date" in r1["assistant_response"].lower()

    # Step 2–4: user fills the missing fields
    engine.invoke({"user_msg": "Before June 1st"}, _cfg(thread_id))
    engine.invoke({"user_msg": "High priority"},    _cfg(thread_id))
    r_final = engine.invoke(
        {"user_msg": "Pick niche, write articles, build website, launch."},
        _cfg(thread_id),
    )
    final_reply = r_final["assistant_response"].lower()
    assert "plan" in final_reply or "tasks" in final_reply


def test_schedule_day_flow(engine):
    thread_id = "test-thread-002"
    r = engine.invoke(
        {"user_msg": "Can you schedule my day? I have 5 hours free."},
        _cfg(thread_id),
    )
    assert "schedule" in r["assistant_response"].lower() \
        or "tasks" in r["assistant_response"].lower()


def test_error_handling(engine):
    thread_id = "test-thread-003"
    r = engine.invoke(
        {"user_msg": "Use the flying unicorn tool please."},
        _cfg(thread_id),
    )
    reply = r["assistant_response"].lower()
    assert any(kw in reply for kw in ("didn’t understand",
                                      "didn't understand",
                                      "issue",
                                      "clarify"))
