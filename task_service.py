from task_model import create_task
from task_storage import load_tasks, save_tasks


def get_next_id(tasks):
    if not tasks:
        return 1
    return max(t["id"] for t in tasks) + 1


def add_task(title):
    if not title.strip():
        print("[ERROR] 标题不能为空")
        return

    tasks = load_tasks()
    task = create_task(get_next_id(tasks), title)

    tasks.append(task)
    save_tasks(tasks)

    print(f"[ADD] (# {task['id']}) {task['title']}")


def list_tasks():
    tasks = load_tasks()

    if not tasks:
        print("[INFO] 暂无任务")
        return

    for t in tasks:
        print(f"[{t['id']}] {t['title']} | {t['status']} | {t['created_at']}")


def done_task(task_id):
    tasks = load_tasks()

    for t in tasks:
        if t["id"] == task_id:

            if t["status"] == "done":
                print("[WARN] 已完成，无需重复操作")
                return

            t["status"] = "done"
            save_tasks(tasks)

            print(f"[DONE] (# {t['id']}) {t['title']}")
            return

    print("[ERROR] 未找到任务")