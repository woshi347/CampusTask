import argparse
from campus_task import __version__
from task_service import add_task, list_tasks, done_task, search_tasks, list_tasks_sorted_by_priority, export_tasks

def build_parser():
    parser = argparse.ArgumentParser(
        prog="python -m campus_task",
        description="CampusTask 校园任务清单工具"
    )

    parser.add_argument(
        "--version",
        action="version",
        version=f"CampusTask {__version__}"
    )

    subparsers = parser.add_subparsers(dest="command")

    add_parser = subparsers.add_parser("add", help="添加任务")
    add_parser.add_argument("title", help="任务标题")
    add_parser.add_argument("--deadline", default="", help="任务截止日期")
    add_parser.add_argument("--priority", default=1, help="任务优先级")

    subparsers.add_parser("list", help="查看所有任务")

    done_parser = subparsers.add_parser("done", help="完成任务")
    done_parser.add_argument("id", type=int, help="任务编号")

    search_parser = subparsers.add_parser("search", help="搜索任务")
    search_parser.add_argument("keyword", help="搜索关键词")

    subparsers.add_parser("sort", help="按优先级排序")

    export_parser = subparsers.add_parser("export", help="导出任务到 CSV")
    export_parser.add_argument("filename", help="导出的 CSV 文件名")

    return parser

def main(argv=None):
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "add":
        add_task(args.title, args.deadline, args.priority)

    elif args.command == "list":
        list_tasks()

    elif args.command == "done":
        done_task(args.id)

    elif args.command == "search":
        search_tasks(args.keyword)

    elif args.command == "sort":
        list_tasks_sorted_by_priority()

    elif args.command == "export":
        export_tasks(args.filename)

    else:
        parser.print_help()