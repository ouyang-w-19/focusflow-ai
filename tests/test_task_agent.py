from agents.task_agent import TaskAgent
from config import OLLAMA_HOST

if __name__ == "__main__":
    agent = TaskAgent()
    goal = "Prepare for a job interview"
    subtasks = agent.plan(goal)
    
    print("🧠 Goal Breakdown:\n")
    print(subtasks)
