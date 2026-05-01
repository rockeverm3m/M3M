# M3M — Memory x Method x Map

> Tried RAG, vector DBs, memory servers — and your agent still forgets? Try this.

---

## The problem

You carefully brief your agent. It nods along. Next session:

```
Agent: "What's the file path?"
```

Or you repeat the same rules. Over and over. It never sticks.

**Here's what everyone misses:** you strapped a RAG backpack onto your agent. But the agent has no idea what's inside it.

---

## What M3M does

Four files.

| File | Job |
|------|-----|
| Scene router | Agent knows which tool to reach for, when |
| Rules | You say it once. It stays. |
| Error log | Fixed a bug? Never again. |
| Session bridge | Picks up where you left off |

No database. No vector embeddings. No API keys. Just markdown files. Your agent finally knows what it knows.

---

## One command

```bash
python3 init-agent-memory.py .
```

- What's left from last session
- Experience stacks up, agent gets better
- Same mistake? Not twice.

Want auto-reminders after every edit?

```bash
python3 init-agent-memory.py . --with-hooks
```

Agent gets nudged to update its memory. No discipline required.

---

## Health check (v1.2)

Skeletons rot. Check yours:

```bash
python3 scripts/check-memory-health.py .
```

```
🔍  M3M memory health check

📋 rules      🟢 still fresh
📋 errors     🟡 worth a review
📋 routes     🟡 1 gap found

🏥 Overall: 🟡 not bad
```

Three checks. Red / yellow / green. Run it weekly.

---

## Before and after

Without M3M:

```
Agent: "This won't work."
```

With M3M:

```
Agent: "We hit this last time. I know what to do."
```

---

MIT. Stars help more agents know what they know.
