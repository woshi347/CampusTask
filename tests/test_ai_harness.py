import json

from ai_harness import prompt_builder
from ai_harness import mock_model
from ai_harness import parse_model_output
from ai_harness import guardrail
from ai_harness import run_eval


def test_mock_model_add_task():
    prompt = prompt_builder("帮我添加一个复习软件工程的任务", [])
    model_output = mock_model(prompt)
    action = parse_model_output(model_output)

    assert action["action"] == "add_task"


def test_mock_model_list_tasks():
    prompt = prompt_builder("列出所有任务", [])
    model_output = mock_model(prompt)
    action = parse_model_output(model_output)

    assert action["action"] == "list_tasks"


def test_mock_model_done_task():
    prompt = prompt_builder("完成第1个任务", [])
    model_output = mock_model(prompt)
    action = parse_model_output(model_output)

    assert action["action"] == "done_task"
    assert action["args"]["id"] == 1


def test_guardrail_blocks_delete_all_tasks():
    action = {
        "action": "delete_all_tasks",
        "args": {}
    }

    result = guardrail(action)

    assert result["allowed"] is False


def test_parse_model_output_invalid_json():
    action = parse_model_output("not json")

    assert action["action"] == "unknown"


def test_run_eval_accuracy():
    cases = [
        {
            "input": "列出所有任务",
            "expected_action": "list_tasks"
        },
        {
            "input": "删除所有任务",
            "expected_action": "blocked"
        }
    ]

    report = run_eval(cases)

    assert report["total"] == 2
    assert report["passed"] == 2
    assert report["accuracy"] == 1.0