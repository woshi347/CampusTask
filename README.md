
# CampusTask - 实验五版本

## 项目简介
CampusTask 是一个命令行任务管理系统，支持任务的添加、查看、完成、搜索与排序，并使用 JSON 文件进行持久化存储。

本项目用于软件工程实验五：迭代开发与变更管理。

---

## 功能说明

### 1. 添加任务
```bash
python main.py add "实验五"
````

### 2. 查看所有任务

```bash
python main.py list
```

### 3. 完成任务

```bash
python main.py done 1
```

### 4. 搜索任务

```bash
python main.py search 实验
```

### 5. 按优先级排序

```bash
python main.py sort
```

---

## 数据存储

任务数据存储在：

```
tasks.json
```

每个任务包含：

* id
* title
* status
* priority
* created_at

---

## 运行方式

```bash
python main.py <command> [args]
```

支持命令：

* add
* list
* done
* search
* sort

---

## 设计说明

本项目采用简单分层结构：

* task_model.py：数据模型
* task_storage.py：数据持久化（JSON读写）
* task_service.py：业务逻辑
* main.py：命令行入口

---

## 变更说明（实验五）

本版本新增：

* 任务搜索功能
* 按优先级排序功能
* CLI扩展命令

---


# 🧪 2. 更新测试说明（TEST.md）


# 测试说明 - CampusTask 实验五

## 测试环境
- Python 3.8+
- 无需第三方库

---

## 功能测试用例

### TC1：添加任务
```bash
python main.py add "测试任务1"
````

预期：

* 成功输出 [ADD]
* tasks.json 中新增记录

---

### TC2：查看任务

```bash
python main.py list
```

预期：

* 输出所有任务列表

---

### TC3：完成任务

```bash
python main.py done 1
```

预期：

* status 变为 done

---

### TC4：搜索任务

```bash
python main.py search 测试
```

预期：

* 返回包含关键词的任务

---

### TC5：排序任务

```bash
python main.py sort
```

预期：

* 按 priority 从高到低输出

---

## 边界测试

### 空标题

```bash
python main.py add ""
```

预期：

* 提示错误：[ERROR] 标题不能为空

---

### 错误ID

```bash
python main.py done abc
```

预期：

* 提示 ID 必须是数字

````

---

