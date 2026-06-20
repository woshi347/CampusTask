from datetime import datetime

def create_task(task_id, title, deadline="", priority=1):
    return {
        "id": task_id,
        "title": title,
        "status": "todo",
        "deadline": deadline,
        "priority": priority,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }