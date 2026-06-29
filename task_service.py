import csv
import logging

from task_model import create_task
from task_storage import load_tasks, save_tasks


def get_next_id(tasks):
    if not tasks:
        return 1

    return max(t["id"] for t in tasks) + 1

def add_task(title, deadline="", priority=1):
    if not title or not title.strip():
        print("[ERROR] 标题不能为空")
        logging.warning("添加任务失败：标题为空")
        return

    try:
        priority = int(priority)
    except ValueError:
        priority = 1

    tasks = load_tasks()

    task = create_task(
        get_next_id(tasks),
        title.strip(),
        deadline,
        priority
    )

    tasks.append(task)
    save_tasks(tasks)

    print(f"[ADD] (# {task['id']}) {task['title']}")
    logging.info(f"添加任务成功：{task['title']}")

def list_tasks():
    tasks = load_tasks()

    if not tasks:
        print("[INFO] 暂无任务")
        logging.info("查看任务：暂无任务")
        return

    for t in tasks:
        print(
            f"[{t['id']}] {t['title']} | {t['status']} | "
            f"deadline: {t.get('deadline', '-')} | "
            f"priority: {t.get('priority', '-')} | "
            f"{t.get('created_at', '-')}"
        )

def done_task(task_id):
    tasks = load_tasks()

    for t in tasks:
        if t["id"] == task_id:
            if t["status"] == "done":
                print("[WARN] 已完成，无需重复操作")
                logging.warning(f"重复完成任务：id={task_id}")
                return

            t["status"] = "done"
            save_tasks(tasks)

            print(f"[DONE] (# {t['id']}) {t['title']}")
            logging.info(f"完成任务成功：id={task_id}")
            return

    print("[ERROR] 未找到任务")
    logging.error(f"完成任务失败：未找到 id={task_id}")

def list_tasks_sorted_by_priority():
    tasks = load_tasks()
    tasks.sort(key=lambda x: x.get("priority", 1), reverse=True)

    for t in tasks:
        print(f"[{t['id']}] {t['title']} | priority:{t.get('priority', 1)}")

def search_tasks(keyword):
    tasks = load_tasks()

    result = []

    for t in tasks:
        if keyword.lower() in t["title"].lower():
            result.append(t)

    if not result:
        print("[INFO] 没有匹配任务")
        logging.info(f"搜索无结果：{keyword}")
        return

    for t in result:
        print(f"[{t['id']}] {t['title']} | {t['status']}")

def export_tasks(filename):
    tasks = load_tasks()

    fieldnames = ["id", "title", "status", "deadline", "priority", "created_at"]

    with open(filename, "w", encoding="utf-8-sig", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()

        for t in tasks:
            row = {key: t.get(key, "") for key in fieldnames}
            writer.writerow(row)

    print(f"[EXPORT] 已导出到 {filename}")
    logging.info(f"导出任务成功：{filename}")