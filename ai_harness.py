import argparse
import io
import json
import re
from contextlib import redirect_stdout
from datetime import datetime

from task_storage import load_tasks
from task_service import add_task
from task_service import list_tasks
from task_service import done_task
from task_service import search_tasks
from task_service import list_tasks_sorted_by_priority

try:
    from task_service import export_tasks
except ImportError:
    export_tasks = None


TRACE_FILE = "trace.jsonl"


def prompt_builder(user_input, task_state):
    prompt = {
        "role": "CampusTask AI Harness",
        "instruction": "请把用户自然语言转换成任务管理动作，只输出 JSON。",
        "allowed_actions": [
            "add_task",
            "list_tasks",
            "done_task",
            "search_tasks",
            "sort_tasks",
            "export_tasks",
            "delete_all_tasks",
            "unknown"
        ],
        "user_input": user_input,
        "task_state": task_state
    }

    return json.dumps(prompt, ensure_ascii=False)


def extract_user_input(prompt):
    try:
        data = json.loads(prompt)
        return data.get("user_input", "")
    except json.JSONDecodeError:
        return prompt


def extract_first_number(text):
    match = re.search(r"\d+", text)

    if match:
        return int(match.group())

    return None


def extract_add_title(text):
    title = text.strip()
    title = re.sub(r"^(请|帮我|给我|麻烦你)?", "", title)
    title = re.sub(r"^(添加|新增|创建|记录|记一下)", "", title)
    title = re.sub(r"^(一个|一条)?", "", title)
    title = re.sub(r"^(任务|待办)", "", title)
    title = title.replace("：", ":")
    
    if ":" in title:
        title = title.split(":", 1)[1]

    title = re.sub(r"的任务$", "", title)
    title = re.sub(r"任务$", "", title)
    title = title.strip()

    if not title:
        title = "未命名任务"

    return title


def extract_search_keyword(text):
    keyword = text.strip()
    keyword = re.sub(r"^(搜索|查找|查询|找一下|帮我找)", "", keyword)
    keyword = re.sub(r"任务$", "", keyword)
    keyword = keyword.strip()

    if not keyword:
        keyword = ""

    return keyword


def mock_model(prompt):
    user_input = extract_user_input(prompt)
    text = user_input.strip()

    if any(word in text for word in ["删除所有", "删除全部", "清空所有", "清空全部", "全部删除", "清除所有"]):
        action = {
            "action": "delete_all_tasks",
            "args": {},
            "reason": "用户请求删除或清空全部任务，属于高风险操作"
        }

    elif any(word in text for word in ["添加", "新增", "创建", "记录", "记一下"]):
        action = {
            "action": "add_task",
            "args": {
                "title": extract_add_title(text)
            },
            "reason": "用户想新增一个任务"
        }

    elif any(word in text for word in ["列出", "查看", "显示", "看看"]) and "任务" in text:
        action = {
            "action": "list_tasks",
            "args": {},
            "reason": "用户想查看任务列表"
        }

    elif any(word in text for word in ["完成", "标记为完成", "做完"]):
        task_id = extract_first_number(text)

        action = {
            "action": "done_task",
            "args": {
                "id": task_id
            },
            "reason": "用户想完成某个任务"
        }

    elif any(word in text for word in ["搜索", "查找", "查询", "找一下"]):
        action = {
            "action": "search_tasks",
            "args": {
                "keyword": extract_search_keyword(text)
            },
            "reason": "用户想按关键词搜索任务"
        }

    elif any(word in text for word in ["排序", "优先级", "按优先级"]):
        action = {
            "action": "sort_tasks",
            "args": {},
            "reason": "用户想按优先级查看任务"
        }

    elif any(word in text for word in ["导出", "保存为CSV", "导出CSV", "csv", "CSV"]):
        action = {
            "action": "export_tasks",
            "args": {
                "filename": "tasks_ai_export.csv"
            },
            "reason": "用户想导出任务数据"
        }

    else:
        action = {
            "action": "unknown",
            "args": {},
            "reason": "无法识别用户意图"
        }

    return json.dumps(action, ensure_ascii=False)


def parse_model_output(model_output):
    try:
        action = json.loads(model_output)

        if not isinstance(action, dict):
            return {
                "action": "unknown",
                "args": {},
                "reason": "模型输出不是字典"
            }

        if "action" not in action:
            action["action"] = "unknown"

        if "args" not in action:
            action["args"] = {}

        return action

    except json.JSONDecodeError:
        return {
            "action": "unknown",
            "args": {},
            "reason": "模型输出不是合法 JSON"
        }


def guardrail(action):
    dangerous_actions = ["delete_all_tasks", "clear_all_tasks", "remove_all_tasks"]

    if action.get("action") in dangerous_actions:
        return {
            "allowed": False,
            "message": "危险操作已拦截：不能直接删除或清空所有任务"
        }

    if action.get("action") == "done_task" and action.get("args", {}).get("id") is None:
        return {
            "allowed": False,
            "message": "完成任务需要提供任务 ID"
        }

    return {
        "allowed": True,
        "message": "安全检查通过"
    }


def capture_output(func, *args):
    buffer = io.StringIO()

    with redirect_stdout(buffer):
        func(*args)

    return buffer.getvalue().strip()


def execute_tool(action):
    name = action.get("action")
    args = action.get("args", {})

    if name == "add_task":
        output = capture_output(add_task, args.get("title", ""))

    elif name == "list_tasks":
        output = capture_output(list_tasks)

    elif name == "done_task":
        output = capture_output(done_task, args.get("id"))

    elif name == "search_tasks":
        output = capture_output(search_tasks, args.get("keyword", ""))

    elif name == "sort_tasks":
        output = capture_output(list_tasks_sorted_by_priority)

    elif name == "export_tasks":
        if export_tasks is None:
            output = "[ERROR] 当前 task_service.py 中没有 export_tasks 函数"
        else:
            output = capture_output(export_tasks, args.get("filename", "tasks_ai_export.csv"))

    elif name == "unknown":
        output = "[ERROR] 无法识别用户意图"

    else:
        output = f"[ERROR] 不支持的动作：{name}"

    return {
        "action": name,
        "output": output
    }


def write_trace(event):
    event["time"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    with open(TRACE_FILE, "a", encoding="utf-8") as f:
        f.write(json.dumps(event, ensure_ascii=False) + "\n")


def handle_user_input(user_input):
    task_state = load_tasks()
    prompt = prompt_builder(user_input, task_state)
    model_output = mock_model(prompt)
    action = parse_model_output(model_output)
    safety = guardrail(action)

    if safety["allowed"]:
        result = execute_tool(action)
    else:
        result = {
            "action": action.get("action"),
            "output": safety["message"]
        }

    event = {
        "user_input": user_input,
        "prompt": prompt,
        "model_output": model_output,
        "parsed_action": action,
        "guardrail": safety,
        "result": result
    }

    write_trace(event)

    return result


def load_eval_cases(filename):
    with open(filename, "r", encoding="utf-8") as f:
        return json.load(f)


def run_eval(eval_cases):
    total = len(eval_cases)
    passed = 0
    details = []

    for case in eval_cases:
        user_input = case["input"]
        expected_action = case["expected_action"]
        prompt = prompt_builder(user_input, [])
        model_output = mock_model(prompt)
        action = parse_model_output(model_output)
        safety = guardrail(action)

        if not safety["allowed"]:
            actual_action = "blocked"
        else:
            actual_action = action.get("action")

        ok = actual_action == expected_action

        if ok:
            passed += 1

        details.append({
            "input": user_input,
            "expected_action": expected_action,
            "actual_action": actual_action,
            "passed": ok
        })

    accuracy = passed / total if total else 0

    report = {
        "total": total,
        "passed": passed,
        "accuracy": accuracy,
        "details": details
    }

    return report


def main():
    parser = argparse.ArgumentParser(description="CampusTask AI Harness")
    subparsers = parser.add_subparsers(dest="command")

    ask_parser = subparsers.add_parser("ask")
    ask_parser.add_argument("text")

    eval_parser = subparsers.add_parser("eval")
    eval_parser.add_argument("--file", default="eval_cases.json")

    args = parser.parse_args()

    if args.command == "ask":
        result = handle_user_input(args.text)
        print(result["output"])

    elif args.command == "eval":
        cases = load_eval_cases(args.file)
        report = run_eval(cases)

        print(f"total: {report['total']}")
        print(f"passed: {report['passed']}")
        print(f"accuracy: {report['accuracy']:.2f}")

        for item in report["details"]:
            status = "PASS" if item["passed"] else "FAIL"
            print(f"{status} | {item['input']} | expected={item['expected_action']} | actual={item['actual_action']}")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()