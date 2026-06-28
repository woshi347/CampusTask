import sys
from task_service import add_task, list_tasks, done_task


def main():
    if len(sys.argv) < 2:
        print("Usage: add/list/done")
        return

    cmd = sys.argv[1]

    if cmd == "add":
        add_task(sys.argv[2] if len(sys.argv) > 2 else "")

    elif cmd == "list":
        list_tasks()

    elif cmd == "done":
        try:
            task_id = int(sys.argv[2])
            done_task(task_id)
        except:
            print("[ERROR] ID必须是数字")

    elif cmd == "search":
        from task_service import search_tasks
        search_tasks(sys.argv[2])

    elif cmd == "sort":
        from task_service import list_tasks_sorted_by_priority
        list_tasks_sorted_by_priority()

    else:
        print("[ERROR] unknown command")


if __name__ == "__main__":
    main()