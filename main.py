import json
import sys
from datetime import datetime

FILE = "tasks.json"


def load_tasks():
    try:
        with open(FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except:
        return []


def save_tasks(tasks):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def add_task(title):
    tasks = load_tasks()

    task = {
        "id": len(tasks) + 1,
        "title": title,
        "status": "todo",
        "created_at": str(datetime.now())
    }

    tasks.append(task)
    save_tasks(tasks)
    print("✔ 任务已添加")


def list_tasks():
    tasks = load_tasks()

    if not tasks:
        print("暂无任务")
        return

    for t in tasks:
        print(f"[{t['id']}] {t['title']} - {t['status']}")


def done_task(task_id):
    tasks = load_tasks()

    for t in tasks:
        if t["id"] == task_id:
            t["status"] = "done"
            print("✔ 已完成")
            break

    save_tasks(tasks)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("用法：add/list/done")
        sys.exit()

    cmd = sys.argv[1]

    if cmd == "add":
        add_task(sys.argv[2])
    elif cmd == "list":
        list_tasks()
    elif cmd == "done":
        done_task(int(sys.argv[2]))