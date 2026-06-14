# ✅ 实验1 README.md

````md
# CampusTask - 实验1

## 项目简介
CampusTask 是一个命令行任务管理工具，用于记录和管理学生日常任务（作业/实验/复习）。

支持任务的添加、查看和完成，并使用 JSON 文件进行数据持久化。

---

## 功能说明

### 1. 添加任务
```bash
python main.py add "完成软件工程实验1"
````

添加一个新任务，默认状态为 todo。

---

### 2. 查看任务

```bash
python main.py list
```

显示所有任务（id / 标题 / 状态 / 创建时间）。

---

### 3. 完成任务

```bash
python main.py done 1
```

将指定 ID 的任务标记为 done。

---

## 数据存储

任务保存在 `tasks.json` 文件中，结构如下：

```json
{
  "id": 1,
  "title": "实验1",
  "status": "todo",
  "created_at": "2026-06-14 10:00:00"
}
```

---

## 运行方式

```bash
python main.py add "任务"
python main.py list
python main.py done 1
```

---

## 用户故事（5条）

* 记录作业任务避免遗忘
* 标记任务完成状态
* 查看所有任务
* 保存任务到文件
* 修正错误任务

---

## 验收标准

* 可成功添加任务
* list 正确显示任务
* done 可修改状态
* 数据写入 tasks.json
* 重启后数据不丢失

```

---