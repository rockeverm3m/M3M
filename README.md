# M3M — Memory × Method × Map

> Your agent forgets. M3M gives it a spine.

---

## You know this feeling

```
You: "Continue where we left off."
Agent: "I don't have context from previous sessions. Could you summarize?"
```

Or worse:

```
Agent: *makes the same bug you fixed three days ago*
You: "WE ALREADY FIXED THIS."
You: *rage quits*
```

You've tried vector databases. RAG. Memory servers. Still happens.

**Here's why:** everyone's selling you muscles. Nobody checked if your skeleton was intact.

---

## One command

```bash
python3 init-agent-memory.py .
```

That's it. Now your agent can do things you didn't think were possible:

> "I found our last session. We were refactoring the health data pipeline. Also — I checked my error log and I see we fixed that DELETE bug on the 28th. I won't repeat it."

> "Before I answer that: your rules say don't touch the smart home credentials. They're in the config file. I'll read from there."

> "This task is a scene E — data debugging. I only loaded the error log and the pipeline script. Context footprint: 420 tokens."

---

## v1.1 — Auto Hooks

```bash
python3 init-agent-memory.py . --with-hooks
```

Installs Claude Code hooks so the trinity check fires automatically after every file edit and on session stop. Agent doesn't have to remember — the harness does.

---

## What's inside?

Run the command. You'll see.

---

MIT. Stars help more agents grow spines.
