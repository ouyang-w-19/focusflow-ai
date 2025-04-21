# File: tests/test_todo_functions.py

from dotenv import load_dotenv
from auth.ms_graph_auth import get_access_token
from graph.todo import get_task_lists, create_default_task_list
import os

# Load environment variables
load_dotenv()

# Read user ID and get token
user_id = os.getenv("USER_ID")
access_token = get_access_token()

def test_get_task_lists():
    print("\n🔍 Testing get_task_lists()...")
    task_lists = get_task_lists(user_id, access_token)
    assert isinstance(task_lists, list), "Expected a list"
    print("✅ test_get_task_lists passed.")

def test_create_default_task_list():
    print("\n🛠️ Testing create_default_task_list()...")
    list_id = create_default_task_list(user_id, access_token)
    assert list_id is None or isinstance(list_id, str), "Expected a string or None"
    if list_id:
        print(f"✅ test_create_default_task_list created list: {list_id}")
    else:
        print("ℹ️ test_create_default_task_list skipped (list may already exist).")

if __name__ == "__main__":
    test_get_task_lists()
    test_create_default_task_list()
