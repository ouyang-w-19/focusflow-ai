# /graphs/types.py
from typing import TypedDict, Optional, List

class GraphState(TypedDict, total=False):   #  total=False → keys are optional
    thread_id: str
    turns: List[dict]
    user_msg: str
    agent_route: Optional[str]
    intent: Optional[str]
    tool_calls: Optional[list]
    tool_result: Optional[dict]
    assistant_response: Optional[str]
    tool_error: Optional[str]
    system_prompt: Optional[str]
    conversation: Optional[str]
