from datetime import datetime

def create_task(task_id, title):
    return {
        "id": task_id,
        "title": title,
        "status": "todo",
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }