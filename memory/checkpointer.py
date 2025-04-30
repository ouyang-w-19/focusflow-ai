# memory/checkpointer.py
import os
import sqlite3
from contextlib import closing           # optional, for tidy closing

try:
    from langgraph.checkpoint.sqlite import SqliteSaver
except ModuleNotFoundError:
    from langgraph.checkpoint.memory import MemorySaver as SqliteSaver

DEFAULT_PATH = os.path.expanduser("~/data/focus.db")

def get_checkpointer(path: str = DEFAULT_PATH):
    """
    Return a LangGraph-compatible checkpointer.
    Uses durable SqliteSaver if available, otherwise in-memory saver.
    """
    if SqliteSaver.__name__ == "MemorySaver":
        return SqliteSaver()             # in-memory fallback

    os.makedirs(os.path.dirname(path), exist_ok=True)

    # open connection; SqliteSaver will take care of WAL, tables, thread-safety
    conn = sqlite3.connect(str(path), check_same_thread=False)
    return SqliteSaver(conn)
