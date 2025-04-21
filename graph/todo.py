import requests


def get_task_lists(user_id, access_token):
    """
    Fetches all Microsoft To Do task lists for a given user.

    Args:
        user_id (str): The user's Microsoft Graph ID
        access_token (str): OAuth 2.0 bearer token

    Returns:
        list[dict]: A list of task list objects, or empty list if none
    """
    url = f"https://graph.microsoft.com/v1.0/users/{user_id}/todo/lists"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    response = requests.get(url, headers=headers)

    if response.status_code == 200:
        task_lists = response.json().get("value", [])
        print(f"📂 Found {len(task_lists)} task list(s).")
        for task_list in task_lists:
            print(f"- {task_list['displayName']} (ID: {task_list['id']})")
        return task_lists
    else:
        print("❌ Failed to retrieve task lists.")
        print("🔎 Error:", response.status_code, response.json())
        return []


def create_default_task_list(user_id, access_token):
    """
    Creates a new task list named 'FocusFlow Tasks' for a given user.

    Args:
        user_id (str): The user's Microsoft Graph ID
        access_token (str): OAuth 2.0 bearer token

    Returns:
        str or None: ID of the newly created task list, or None if failed
    """
    url = f"https://graph.microsoft.com/v1.0/users/{user_id}/todo/lists"
    headers = {
        "Authorization": f"Bearer {access_token}",
        "Content-Type": "application/json"
    }
    payload = {"displayName": "FocusFlow Tasks"}
    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 201:
        print("✅ Default task list created.")
        return response.json()["id"]
    else:
        print("❌ Failed to create task list:", response.json())
        return None