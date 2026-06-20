import os
import pytest
from task_service import add_task, list_tasks, done_task
from task_storage import load_tasks

TEST_FILE = "tasks.json"


@pytest.fixture(autouse=True)
def setup_and_teardown():
    # 安全删除文件
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)
    yield
    if os.path.exists(TEST_FILE):
        os.remove(TEST_FILE)


def test_add_task():
    add_task("实验三测试任务")

    tasks = load_tasks()
    assert len(tasks) == 1
    assert tasks[0]["title"] == "实验三测试任务"
    assert tasks[0]["status"] == "todo"


def test_done_task():
    add_task("待完成任务")

    tasks = load_tasks()
    task_id = tasks[0]["id"]

    done_task(task_id)

    tasks = load_tasks()
    assert tasks[0]["status"] == "done"


def test_list_tasks_output(capsys):
    add_task("任务1")
    list_tasks()

    captured = capsys.readouterr()
    assert "任务1" in captured.out


def test_done_invalid_id():
    add_task("正常任务")

    done_task(999)  # 不存在ID

    tasks = load_tasks()
    assert len(tasks) == 1  # ⚠️修正这里


def test_json_persistence():
    add_task("持久化测试")

    tasks1 = load_tasks()

    tasks2 = load_tasks()
    assert tasks1 == tasks2


#空标题测试
def test_empty_title():
    add_task("")
    tasks = load_tasks()
    assert len(tasks) == 0


def test_done_task_twice():
    add_task("重复完成测试")
    tasks = load_tasks()
    task_id = tasks[0]["id"]

    done_task(task_id)
    done_task(task_id)  # 第二次

    tasks = load_tasks()
    assert tasks[0]["status"] == "done"


def test_multiple_tasks():
    add_task("任务A")
    add_task("任务B")

    tasks = load_tasks()
    assert len(tasks) == 2


def test_blank_spaces_title():
    add_task("   ")
    tasks = load_tasks()
    assert len(tasks) == 0


def test_list_empty_output(capsys):
    list_tasks()
    captured = capsys.readouterr()
    assert "暂无任务" in captured.out or "当前暂无任务" in captured.out