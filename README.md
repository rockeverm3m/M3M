# M3M — Memory x Method x Map

> Your agent has the memory of a goldfish. Fix that in 30 seconds.

---

## The problem

You spend 20 minutes bringing your agent up to speed. It nods along. Next session:

```
You: "Continue where we left off."
Agent: "I don't have context from previous sessions."
```

Or it makes the same bug you fixed three days ago. Again.

You've tried RAG. Vector databases. Memory servers. Still happens.

**Here's the thing everyone misses:** you're giving your agent muscles. It has no spine. Without a skeleton, all the retrieval in the world won't help — because the agent doesn't know *what* to remember or *when* to use it.

---

## What M3M does

Four files. That's it.

| File | Job |
|------|-----|
| `MEMORY.md` | Scene router — tells the agent what to load and when |
| `rules.md` | Rules that survive session resets |
| `error-log.md` | Every bug you've fixed, searchable by tag |
| `session_summary.md` | Bridge between sessions — where you left off |

No database. No vector embeddings. No API keys. Just markdown files that give your agent a memory structure that actually works.

---

## One command

```bash
python3 init-agent-memory.py .
```

Result:

```
Spine installed.

Your agent now remembers:
  - What you were doing last session
  - Every rule you've taught it
  - Every bug it's ever fixed

Same mistakes? Not anymore.
```

Want auto-reminders after every file change?

```bash
python3 init-agent-memory.py . --with-hooks
```

That installs Claude Code hooks so the agent gets nudged to update its memory after every edit. No discipline required.

---

## Health check (v1.2)

Skeletons rot if you don't maintain them. Check yours:

```bash
python3 scripts/check-memory-health.py .
```

```
🔍  M3M 记忆健康检查

📋 rules.md          🟢 3 天前更新
📋 error-log.md      🟢 12 条记录，无重复模式
📋 MEMORY.md         🟡 5 个场景路由，1 个未填写完整

🏥 综合评级: 🟡 有点问题
```

Three checks. Red / yellow / green. Run it once a week.

---

## Real example

Before M3M:

```
Agent: "Let me check the logs for that error."
Agent: *spends 30 minutes re-discovering the log format*
```

After M3M:

```
Agent: "Read error-log.md — ah, we fixed this log format issue on April 28.
       I'll skip the rediscovery and go straight to the new approach."
```

That's not a better model. That's a spine.

---

## Why not RAG / vector DB / etc.

RAG finds similar text. It doesn't know what matters. M3M forces you and your agent to decide what's worth remembering — and when to recall it. That's the difference between a library and a brain.

---

MIT. [Stars help more agents grow spines.](https://github.com/rk/m3m)
