# CHANGELOG

## v0.2.1

### Added

- 支持 `python -m campus_task` 方式运行。
- 新增 `--help` 查看帮助信息。
- 新增 `--version` 查看版本号。
- 新增 `export` 命令，可将任务导出为 CSV 文件。
- 新增 `campus_task.log` 日志文件。
- 新增 `USER_GUIDE.md` 用户手册。

### Fixed

- 修复 `tasks.json` 为空文件时可能导致程序异常的问题。

### Changed

- 使用 `argparse` 管理命令行参数。
- 保留原有平铺代码结构，同时新增 `campus_task` 模块入口。

## [0.2.0] - 实验五迭代

### ✨ 新增功能
- 增加任务搜索功能（search_tasks）
- 增加按 priority 排序功能（list_tasks_sorted_by_priority）

### 🔧 改进
- 优化命令行结构（main.py 增加 search/sort 命令）
- 提升任务查询能力

---

## [0.1.0] - 初始版本

### 功能
- add_task（添加任务）
- list_tasks（查看任务）
- done_task（完成任务）
- JSON持久化存储