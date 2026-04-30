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
Agent: "You're right, I apologize. Let me—"
You: *rage quits*
```

You've tried vector databases. RAG. Memory servers. $200/month on API calls with bloated context windows. Still happens.

**Here's why:** everyone's selling you muscles. Nobody checked if your skeleton was intact.

---

## M3M is the skeleton

One command. Your agent gets a file architecture that doesn't collapse under its own weight:

```bash
python3 init-agent-memory.py .
```

That's it. Now:

- **Reset?** Agent reads MEMORY.md. Knows what it was doing in 30 seconds. No "could you summarize."
- **Same bug twice?** Impossible. Every fix archived in error-log. Auto-searched on next error.
- **Context bloated?** Not anymore. Only loads files for the current task. Everything else stays on disk.
- **Made a change?** Three-question check fires automatically. Rules updated. Docs synced. Nothing falls through cracks.

---

## What's in the box

| Pillar | What | Why you need it |
|--------|------|-----------------|
| **M**emory | Rules + error log + session summary | Your agent's long-term memory that survives resets |
| **M**ethod | Three-in-one closure + layered loading | Every change self-checks. Context never bloats. |
| **M**ap | Scene router + file index | One index file. Agent always knows where to find things. |

---

## Real results

Running on a live trading agent for over a month:

- Zero memory loss across resets
- Context footprint cut from "everything" to under 1,000 lines
- Bugs stopped repeating
- New sessions start productive in seconds, not minutes

---

## Start now

```bash
git clone https://github.com/yourname/m3m.git
cd m3m
python3 scripts/init-agent-memory.py /path/to/your/project
```

Then tell your agent: "Read memory/MEMORY.md."

MIT. Stars help more agents grow spines.
