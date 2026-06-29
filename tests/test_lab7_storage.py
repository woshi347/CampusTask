from task_storage import load_tasks, save_tasks
import task_storage

def test_load_empty_tasks_json(tmp_path, monkeypatch):
    test_file = tmp_path / "tasks.json"
    test_file.write_text("", encoding="utf-8")

    monkeypatch.setattr(task_storage, "FILE", str(test_file))

    tasks = load_tasks()

    assert tasks == []

def test_save_and_load_tasks(tmp_path, monkeypatch):
    test_file = tmp_path / "tasks.json"

    monkeypatch.setattr(task_storage, "FILE", str(test_file))

    save_tasks([
        {
            "id": 1,
            "title": "实验七测试任务",
            "status": "todo",
            "deadline": "",
            "priority": 1,
            "created_at": "2026-06-29 10:00:00"
        }
    ])

    tasks = load_tasks()

    assert len(tasks) == 1
    assert tasks[0]["title"] == "实验七测试任务"