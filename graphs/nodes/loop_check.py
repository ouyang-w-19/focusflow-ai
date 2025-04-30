# /graphs/nodes/loop_check.py

def is_finished(state: dict) -> bool:
    """
    Decide whether to continue the tool/LLM loop
    or exit to final response.

    Returns:
        - True: if no pending tool calls (ready to respond)
        - False: if new tool calls were created by last LLM step
    """

    # If the last LLM output created new tool calls, keep looping
    if state.get("tool_calls"):
        return False

    # If a tool execution raised an error, stop looping (optional design choice)
    if state.get("tool_error"):
        return True

    # Otherwise, assume done and ready to generate final response
    return True
