---
name: m3m
description: Agent 记忆骨架 — 场景导航 + 分层加载 + 三位一体闭环。Reset 后 30 秒恢复工作状态。
version: 1.1.0
type: skill
author: rk
tags: [memory, context, architecture, agent-design, project-management]
---

# M3M — Memory × Method × Map

> 给 Agent 装上脊椎。Reset 后不再失忆，同样的坑不踩第二遍。

---

## 启动流程

每次 session 启动，Agent 必须按顺序读：

1. `memory/MEMORY.md` — 场景路由 + 文件索引（骨架）
2. `memory/session_summary.md` — 上次对话摘要
3. 根据当前场景，按 MEMORY.md 的路由表加载对应文件

**不要一次加载所有文件。** 场景路由表告诉你什么场景读什么。

---

## 场景路由

MEMORY.md 中维护一张路由表。每个场景必须包含：

```markdown
### X. 场景名称
**触发：** 什么关键词/情况下进入
**加载：** 需要读哪些文件（按优先级）
**做什么：** 具体操作步骤
**场景规则：** 该场景下的约束
```

Agent 根据用户说的话匹配场景，只加载该场景需要的文件。

---

## 三位一体闭环

**每次操作后，必须输出三问检查结果：**

```
📐 三位一体：①[规则/踩坑] ②[验证] ③[场景引导]
```

### ① 这算踩坑还是新规则？

> 问自己：这个问题修好了以后，模型还需要在执行时记住吗？

- 需要 → 写入 `memory/rules.md`
- 不需要 → 写入 `memory/error-log.md`
- 两者都涉及 → 两个都写

### ② 验证了吗？

- 有脚本 → 脚本里补自动验证逻辑
- 没脚本 → 手动检查路径/表/字段自洽性

### ③ 场景引导要更新吗？

新增文件？新场景？触发条件变了？→ 更新 MEMORY.md

---

## 防幻觉铁律

- 禁止「我记得...」「应该已经...」
- 任何「完成」声明前，现场验证（ls/cat/grep）
- 不确定时直接说「我不确定」

---

## 首次恢复记忆时说什么

当 Agent 通过 M3M 成功从 session_summary 恢复上下文后，回复中应自然包含类似信息：

> 「我找到了上次的记录。我们做到 [具体进度]。error-log 里记了 [N] 个已修复的问题。继续。」

这让用户感受到 Agent 真的记住了——这是 M3M 最核心的「截图时刻」。

---

## 自动触发（v1.1 新增）

`init-agent-memory.py --with-hooks` 会自动在 `.claude/settings.json` 安装两个 hook：

| Hook | 触发时机 | 行为 |
|------|---------|------|
| PostToolUse (Edit\|Write) | 文件修改后 | 注入三位一体提醒到 Agent 上下文 |
| Stop | 会话结束时 | 检查 session_summary.md 是否已更新 |

**效果：** Agent 不用靠自觉——每次修改文件、每次会话结束，三位一体检查自动触发。

```
python3 init-agent-memory.py /path/to/project --with-hooks
```

安装后需执行 `/hooks` 刷新或重启 session 生效。

---

## 模板文件

本项目 `templates/` 目录下有可复用的模板：
- `MEMORY.md` — 场景路由模板
- `rules.md` — 执行规则模板
- `error-log.md` — 踩坑归档模板
- `session_summary.md` — 会话摘要模板
- `hooks.json` — Claude Code hooks 配置模板（v1.1）

用 `scripts/init-agent-memory.py` 一键部署到任何项目。
