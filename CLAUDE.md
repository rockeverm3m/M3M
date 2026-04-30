# CLAUDE.md — Agent Memory Architecture

> 本项目是「Agent Memory Architecture」技能的独立开发和维护仓库。
> 与数字分身项目（~/Documents/AI-memory/）物理隔离。

## 项目身份

在开发和维护一个开源 Claude Code Skill：Agent Memory Architecture（Agent 记忆骨架）。

核心价值：场景导航 + 分层加载 + 三位一体闭环。解决 Agent 长期项目的上下文膨胀和记忆丢失问题。

## 文件地图

| 文件 | 用途 |
|------|------|
| `skill/SKILL.md` | 技能说明书（给 Agent 读的方法论） |
| `templates/` | 模板文件（MEMORY.md / rules.md / error-log.md / session_summary） |
| `scripts/init-agent-memory.py` | 初始化脚本（一键搭骨架） |
| `README.md` | 人类可读的项目说明 |
| `CHANGELOG.md` | 版本变更记录 |

## 开发规则

- 本仓库是纯公开内容，不含任何 rk 私人数据
- 数字分身项目的落地经验可以提炼到本仓库，但不能包含 HA token、health.db 路径等隐私
- 三位一体原则同样适用于本仓库本身的维护
