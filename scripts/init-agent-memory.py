#!/usr/bin/env python3
"""
init-agent-memory.py — 一键初始化 M3M 骨架

用法：
  python3 init-agent-memory.py                      # 在当前目录初始化
  python3 init-agent-memory.py /path/to/project     # 在指定项目初始化
  python3 init-agent-memory.py --with-hooks         # 同时安装 Claude Code hooks
"""

import os
import sys
import json
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

HOOKS_QUOTE = """
┌─────────────────────────────────────────────────┐
│  M3M Hooks installed.                           │
│                                                 │
│  PostToolUse → 文件修改后自动提醒三位一体检查   │
│  Stop → 会话结束时检查 session_summary.md       │
│                                                 │
│  Restart or run /hooks to activate.             │
└─────────────────────────────────────────────────┘
"""

SHARE_HINT = """
If M3M saves you from re-explaining everything to your agent,
give it a star: github.com/rk/m3m
"""


def compute_claude_memory_path(target):
    """计算 Claude Code 的 memory 目录路径"""
    home = Path.home()
    cwd = target.resolve()
    sanitized = str(cwd).replace("/", "-")
    return home / ".claude" / "projects" / sanitized / "memory"


def install_hooks(target):
    """在项目的 .claude/settings.json 中安装 M3M hooks"""
    hooks_template = TEMPLATES_DIR / "hooks.json"
    if not hooks_template.exists():
        print("  ⚠️  templates/hooks.json 不存在，跳过 hooks 安装")
        return

    hooks_config = json.loads(hooks_template.read_text(encoding="utf-8"))

    # 替换 __MEMORY_PATH__ 占位符
    memory_path = str(compute_claude_memory_path(target))
    raw = json.dumps(hooks_config)
    raw = raw.replace("__MEMORY_PATH__", memory_path)
    hooks_config = json.loads(raw)

    # 确保 .claude 目录存在
    claude_dir = target / ".claude"
    claude_dir.mkdir(parents=True, exist_ok=True)

    settings_file = claude_dir / "settings.json"

    # 读取现有配置（如果有）
    if settings_file.exists():
        try:
            settings = json.loads(settings_file.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            print("  ⚠️  settings.json 格式错误，将覆盖")
            settings = {}
    else:
        settings = {}

    # 合并 hooks（保留已有的其他 hooks）
    if "hooks" not in settings:
        settings["hooks"] = {}

    existing_hooks = settings.get("hooks", {})

    for event, entries in hooks_config.items():
        if event not in existing_hooks:
            existing_hooks[event] = []
        # 简单去重：如果相同 event+matcher 已存在，跳过
        existing_matchers = {
            e.get("matcher", ""): e for e in existing_hooks[event]
        }
        for entry in entries:
            matcher = entry.get("matcher", "")
            if matcher in existing_matchers:
                print(f"  ⏭  hooks.{event}[matcher={matcher}] 已存在，跳过")
            else:
                existing_hooks[event].append(entry)
                print(f"  ✅ hooks.{event}[matcher={matcher}]")

    settings["hooks"] = existing_hooks

    settings_file.write_text(
        json.dumps(settings, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8"
    )

    # 确保 .gitignore 里有 .claude/settings.local.json
    gitignore = target / ".gitignore"
    if gitignore.exists():
        content = gitignore.read_text(encoding="utf-8")
        if ".claude/settings.local.json" not in content:
            with gitignore.open("a", encoding="utf-8") as f:
                f.write("\n.claude/settings.local.json\n")
    else:
        gitignore.write_text(".claude/settings.local.json\n", encoding="utf-8")

    print(HOOKS_QUOTE)


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = [a for a in sys.argv[1:] if a.startswith("--")]

    with_hooks = "--with-hooks" in flags

    target = Path(args[0]) if args else Path.cwd()
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
            print(f"  ⏭  {filename}（已存在，跳过）— {description}")
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

    if with_hooks:
        install_hooks(target)

    print(SHARE_HINT)


if __name__ == "__main__":
    main()
