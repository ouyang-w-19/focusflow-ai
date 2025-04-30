# /cli/main.py
from graphs.main_graph import build_main_graph
from memory.checkpointer import get_checkpointer


def main() -> None:
    # ── build graph & bind persistent memory ───────────────────────────────
    graph = build_main_graph()                     # CompiledStateGraph → Runnable
    checkpointer = get_checkpointer()              # your SQLite wrapper

    engine = graph.with_config({                   # attach once
        "checkpointer": checkpointer,
        "recency_window": 8,                       # keep if your graph reads it
    })

    thread_id = "focusflow-local-user"
    cfg = {"configurable": {"thread_id": thread_id}}

    print("🧠 FocusFlow AI CLI\nType /exit to quit.\n")

    while True:
        user_msg = input("You: ").strip()
        if user_msg.lower() == "/exit":
            print("Goodbye! 👋")
            break

        # Run the graph
        result = engine.invoke({"user_msg": user_msg}, cfg)
        print("AI:", result.get("assistant_response", "[no response]"))


if __name__ == "__main__":
    main()
