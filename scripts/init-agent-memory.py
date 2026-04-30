#!/usr/bin/env python3
"""
init-agent-memory.py — 一键初始化 M3M 骨架

用法：
  python3 init-agent-memory.py                    # 在当前目录初始化
  python3 init-agent-memory.py /path/to/project   # 在指定项目初始化
"""

import os
import sys
from pathlib import Path

SCRIPT_DIR = Path(__file__).resolve().parent
TEMPLATES_DIR = SCRIPT_DIR.parent / "templates"

FILES = {
    "MEMORY.md": "场景路由 + 文件索引（骨架）",
    "rules.md": "执行规则（模型常驻记忆）",
    "error-log.md": "踩坑归档（出问题时搜索）",
    "session_summary.md": "跨 session 记忆桥梁",
}

SPINE_QUOTE = """
┌─────────────────────────────────────────────────┐
│  Spine installed.                               │
│                                                 │
│  Your agent now remembers:                      │
│    • What you were doing last session           │
│    • Every rule you've taught it                │
│    • Every bug it's ever fixed                  │
│                                                 │
│  Same mistakes? Not anymore.                    │
└─────────────────────────────────────────────────┘
"""

SHARE_HINT = """
If M3M saves you from re-explaining everything to your agent,
give it a star: github.com/yourname/m3m
"""


def main():
    target = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
    memory_dir = target / "memory"
    memory_dir.mkdir(parents=True, exist_ok=True)

    print(f"  M3M — Memory × Method × Map")
    print(f"  {memory_dir}")
    print()

    created = 0
    skipped = 0

    for filename, description in FILES.items():
        dest = memory_dir / filename
        src = TEMPLATES_DIR / filename

        if dest.exists():
            print(f"  ⏭ {filename}（已存在，跳过）— {description}")
            skipped += 1
            continue

        if src.exists():
            content = src.read_text(encoding="utf-8")
        else:
            content = f"# {filename.replace('.md', '')}\n\n（待填写）\n"

        dest.write_text(content, encoding="utf-8")
        print(f"  ✅ {filename} — {description}")
        created += 1

    print()
    print(f"  完成：新建 {created} 个，跳过 {skipped} 个")

    claude_md = target / "CLAUDE.md"
    if not claude_md.exists():
        claude_md.write_text(
            "# CLAUDE.md\n\n"
            "启动时读 memory/MEMORY.md\n",
            encoding="utf-8"
        )
        print(f"  ✅ CLAUDE.md — 已生成（引用 MEMORY.md）")

    print(SPINE_QUOTE)
    print(SHARE_HINT)


if __name__ == "__main__":
    main()
