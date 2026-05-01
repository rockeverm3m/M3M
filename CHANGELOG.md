# Changelog

## [1.1.0] — 2026-05-01

### Added
- `--with-hooks` flag: 一键安装 Claude Code hooks，实现三位一体自动触发
- `templates/hooks.json`: hooks 配置模板
- PostToolUse hook: 每次 Edit/Write 后自动注入三位一体提醒到 Agent 上下文
- Stop hook: 会话结束时检查 session_summary.md 更新状态

### Changed
- `init-agent-memory.py`: 新增 `install_hooks()` 和 `compute_claude_memory_path()`
- `skill/SKILL.md`: 版本号 1.0.0 → 1.1.0，新增「自动触发」章节
- `README.md`: 新增 v1.1 hooks 特性说明

## [1.0.0] — 2026-04-30

### Added
- 初始发布：M3M 记忆骨架
- `init-agent-memory.py`: 一键部署脚本
- 四个模板文件: MEMORY.md, rules.md, error-log.md, session_summary.md
- `skill/SKILL.md`: M3M 技能说明书
- 三位一体闭环方法论
- 场景路由 + 分层加载设计
