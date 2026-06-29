import json
import os
import logging

FILE = "tasks.json"
LOG_FILE = "campus_task.log"

logging.basicConfig(
    filename=LOG_FILE,
    level=logging.INFO,
    encoding="utf-8",
    format="%(asctime)s | %(levelname)s | %(message)s"
)

def load_tasks():
    if not os.path.exists(FILE):
        logging.info("tasks.json 不存在，返回空列表")
        return []

    try:
        with open(FILE, "r", encoding="utf-8") as f:
            content = f.read().strip()

            if not content:
                logging.warning("tasks.json 是空文件，返回空列表")
                return []

            data = json.loads(content)

            if not isinstance(data, list):
                logging.error("tasks.json 内容不是列表，返回空列表")
                return []

            return data

    except json.JSONDecodeError:
        logging.error("tasks.json 格式损坏，返回空列表")
        return []

def save_tasks(tasks):
    with open(FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)

    logging.info("任务数据已保存")