

# CampusTask 实验二：模块化设计（重构版）

## 一、项目简介

CampusTask 是一个校园任务管理系统，本实验在实验一基础上进行**模块化重构**，将原本单一脚本拆分为多个职责清晰的模块，以提升代码的可维护性、可扩展性与可测试性。

本实验重点在于理解软件工程中的“分层设计思想”，即将系统划分为：
- 数据模型层（Model）
- 数据存储层（Storage）
- 业务逻辑层（Service）
- 命令行交互层（CLI）

---

## 二、项目结构

```

campus_task/
│
├── main.py              # 命令行入口（CLI层）
├── task_model.py       # 数据模型层（Task结构定义）
├── task_storage.py     # 数据持久化层（JSON读写）
├── task_service.py     # 业务逻辑层（增删改查）
├── tasks.json          # 数据存储文件
├── README.md           # 项目说明文档

````

---

## 三、功能说明

### 1. 添加任务
```bash
python main.py add "完成软件工程实验"
````

功能说明：

* 自动生成任务 ID
* 记录创建时间
* 默认状态为 todo
* 写入 tasks.json

---

### 2. 查看任务列表

```bash
python main.py list
```

功能说明：

* 输出所有任务
* 显示 ID / 标题 / 状态 / 创建时间

---

### 3. 完成任务

```bash
python main.py done 1
```

功能说明：

* 根据任务 ID 标记任务为 done
* 防止重复完成
* 自动保存到文件

---

## 四、模块设计说明

### 1. task_model.py（数据模型层）

职责：

* 定义 Task 数据结构
* 统一任务字段格式

包含字段：

* id：任务编号
* title：任务标题
* status：任务状态（todo/done）
* created_at：创建时间

---

### 2. task_storage.py（数据存储层）

职责：

* 读取 tasks.json
* 保存 tasks.json
* 处理 JSON 解析异常
* 文件不存在时自动初始化空列表

核心能力：

* load_tasks()
* save_tasks(tasks)

---

### 3. task_service.py（业务逻辑层）

职责：

* 任务增删改查逻辑
* 任务状态更新
* ID 自动递增生成

核心功能：

* add_task()
* list_tasks()
* done_task()

---

### 4. main.py（命令行交互层）

职责：

* 解析命令行参数
* 调用 service 层函数
* 输出运行结果

支持命令：

* add
* list
* done

---

## 五、运行方式

### 1. 添加任务

```bash
python main.py add "你的任务"
```

### 2. 查看任务

```bash
python main.py list
```

### 3. 完成任务

```bash
python main.py done 1
```

---

## 六、数据存储格式（tasks.json）

```json
[
  {
    "id": 1,
    "title": "测试任务1",
    "status": "done",
    "created_at": "2026-06-14 10:06:03"
  }
]
```

---

## 七、设计改进说明（相对实验一）

相比实验一的单文件结构，本实验进行了以下优化：

### 1. 职责分离

* UI / 业务 / 数据完全解耦
* 每个模块只负责单一功能

### 2. 可维护性提升

* 修改存储方式不会影响业务逻辑
* 修改 CLI 不影响数据结构

### 3. 可扩展性增强

* 可轻松增加 deadline / priority 字段
* 可扩展 Web 版本或 API 版本

### 4. 降低耦合度

* main.py 不再包含核心逻辑
* 所有逻辑集中在 service 层

---

## 八、实验总结

通过本次实验，我理解到：

* Python 语法正确 ≠ 软件工程能力
* 软件系统需要清晰的模块边界
* 分层设计可以显著提高系统可维护性
* 真实开发中“结构设计”比“代码实现”更重要

---

## 九、课后思考

为什么拆分模块后代码更清晰？

因为软件工程的核心不是写代码，而是**控制复杂度**。

```
