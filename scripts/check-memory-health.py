#!/usr/bin/env python3
"""
check-memory-health.py — M3M 记忆健康检查

用法：
  python3 check-memory-health.py                     # 当前目录
  python3 check-memory-health.py /path/to/project    # 指定项目
"""

import sys
import re
from pathlib import Path
from datetime import datetime, timezone


RULES_STALE_DAYS = 30
RULES_WARN_DAYS = 14
ERROR_HOT_TAG_THRESHOLD = 3  # 同一标签超过此数量 → 警告


def stat_file(path):
    """返回文件修改时间，不存在返回 None"""
    p = Path(path)
    if not p.exists():
        return None
    return datetime.fromtimestamp(p.stat().st_mtime)


def days_ago(mtime):
    """距今多少天"""
    if mtime is None:
        return None
    now = datetime.now()
    return (now - mtime).days


def check_rules(memory_dir):
    """检查 rules.md 是否过期"""
    path = memory_dir / "rules.md"
    mtime = stat_file(path)
    age = days_ago(mtime)

    if mtime is None:
        return {
            "status": "red",
            "label": "文件不存在",
            "detail": "rules.md 缺失，骨架不完整",
            "age": None,
        }

    if age > RULES_STALE_DAYS:
        return {
            "status": "red",
            "label": f"过期 {age} 天",
            "detail": f"超过 {RULES_STALE_DAYS} 天未更新，规则可能已过时",
            "age": age,
        }
    elif age > RULES_WARN_DAYS:
        return {
            "status": "yellow",
            "label": f"{age} 天未更新",
            "detail": f"接近 {RULES_STALE_DAYS} 天阈值，建议检查一遍",
            "age": age,
        }
    else:
        return {
            "status": "green",
            "label": f"{age} 天前更新",
            "detail": "状态新鲜",
            "age": age,
        }


def parse_error_entries(memory_dir):
    """解析 error-log.md 中的踩坑条目"""
    path = memory_dir / "error-log.md"
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")

    # 匹配 ### [#标签] 标题，过滤模板占位符
    entries = []
    pattern = re.compile(r"^###\s+\[(#\w+)\]\s+(.+)", re.MULTILINE)
    for m in pattern.finditer(text):
        tag = m.group(1)
        title = m.group(2).strip()
        # 跳过模板占位符（#标签、问题简述 等模板内容）
        if tag == "#标签" or title == "问题简述":
            continue
        entries.append({"tag": tag, "title": title})
    return entries


def check_errors(memory_dir):
    """检查 error-log.md 重复模式"""
    entries = parse_error_entries(memory_dir)

    if not entries:
        return {
            "status": "yellow",
            "label": "无踩坑记录",
            "detail": "还是模板状态，没有真实内容",
            "count": 0,
            "hot_tags": [],
            "duplicates": [],
        }

    # 统计标签分布
    from collections import Counter
    tag_counts = Counter(e["tag"] for e in entries)
    hot_tags = [(tag, cnt) for tag, cnt in tag_counts.items() if cnt >= ERROR_HOT_TAG_THRESHOLD]

    # 简单去重：标题相似度 > 0.6 视为重复
    duplicates = []
    titles = [e["title"] for e in entries]
    for i in range(len(titles)):
        for j in range(i + 1, len(titles)):
            words_i = set(titles[i].lower().split())
            words_j = set(titles[j].lower().split())
            if not words_i or not words_j:
                continue
            overlap = len(words_i & words_j) / min(len(words_i), len(words_j))
            if overlap > 0.6:
                duplicates.append((titles[i], titles[j], entries[i]["tag"], entries[j]["tag"]))

    # 判定
    if hot_tags or duplicates:
        issues = []
        if hot_tags:
            issues.append(f"标签 {'、'.join(t + '(' + str(c) + ')' for t, c in hot_tags)} 踩坑密集")
        if duplicates:
            issues.append(f"{len(duplicates)} 组疑似重复踩坑")
        return {
            "status": "red",
            "label": f"{len(entries)} 条记录",
            "detail": "；".join(issues),
            "count": len(entries),
            "hot_tags": hot_tags,
            "duplicates": duplicates,
        }

    return {
        "status": "green",
        "label": f"{len(entries)} 条记录",
        "detail": "无重复模式",
        "count": len(entries),
        "hot_tags": [],
        "duplicates": [],
    }


def parse_scenes(memory_dir):
    """解析 MEMORY.md 中的场景路由"""
    path = memory_dir / "MEMORY.md"
    if not path.exists():
        return []
    text = path.read_text(encoding="utf-8")

    scenes = []
    # 匹配 ### X：场景名称
    pattern = re.compile(r"^###\s+([A-Z]+)：(.+)", re.MULTILINE)
    for m in pattern.finditer(text):
        scene_id = m.group(1)
        scene_name = m.group(2).strip()
        scenes.append({"id": scene_id, "name": scene_name})
    return scenes


def check_scene(memory_dir, scene_id):
    """检查单个场景是否填写完整"""
    path = memory_dir / "MEMORY.md"
    text = path.read_text(encoding="utf-8")

    # 找到场景块
    pattern = re.compile(rf"^###\s+{re.escape(scene_id)}：.+$", re.MULTILINE)
    m = pattern.search(text)
    if not m:
        return None

    start = m.start()
    # 找下一个 ### 或者文件结束
    rest = text[start:]
    next_scene = re.search(r"\n###\s+[A-Z]+：", rest[len(m.group()):])
    if next_scene:
        block = rest[:len(m.group()) + next_scene.start()]
    else:
        block = rest

    # 检查三个字段
    trigger = re.search(r"\*\*触发\*\*：\s*(.+)", block)
    load = re.search(r"\*\*加载\*\*：\s*(.+)", block)
    action = re.search(r"\*\*做什么\*\*：\s*(.+)", block)

    missing = []
    if not trigger or not trigger.group(1).strip():
        missing.append("触发条件")
    if not load or not load.group(1).strip():
        missing.append("加载文件")
    if not action or not action.group(1).strip():
        missing.append("操作步骤")

    return {
        "filled": len(missing) == 0,
        "missing": missing,
        "partially_filled": len(missing) < 3 and len(missing) > 0,
    }


def check_routes(memory_dir):
    """检查 MEMORY.md 场景路由健康度"""
    path = memory_dir / "MEMORY.md"
    if not path.exists():
        return {"status": "red", "label": "MEMORY.md 不存在", "detail": "骨架缺失", "dead": [], "partial": [], "ok": []}

    scenes = parse_scenes(memory_dir)
    if not scenes:
        return {"status": "yellow", "label": "无场景路由", "detail": "尚未定义任何场景", "dead": [], "partial": [], "ok": []}

    dead = []
    partial = []
    ok = []

    for s in scenes:
        result = check_scene(memory_dir, s["id"])
        if result is None:
            continue
        if not result["filled"]:
            if result["partially_filled"]:
                partial.append({**s, "missing": result["missing"]})
            else:
                dead.append({**s, "missing": result["missing"]})
        else:
            ok.append(s)

    # 检查文件索引
    has_file_index = False
    text = path.read_text(encoding="utf-8")
    file_index_section = re.search(r"##\s+完整文件索引\s*\n+(?!<!--)", text)
    if file_index_section:
        after = text[file_index_section.start():]
        # 找下一级标题，中间有表格或列表内容
        next_section = re.search(r"\n##\s+", after[len(file_index_section.group()):])
        content = after[:len(file_index_section.group()) + next_section.start()] if next_section else after
        # 有实际内容（不是只有注释）
        if re.search(r"\|.+\|", content) or re.search(r"^- \*\*", content, re.MULTILINE):
            has_file_index = True

    issues = []
    if dead:
        issues.append(f"{len(dead)} 个死路由: {', '.join(s['name'] for s in dead)}")
    if partial:
        issues.append(f"{len(partial)} 个路由不完整: {', '.join(s['name'] for s in partial)}")
    if not has_file_index:
        issues.append("文件索引为空")

    if dead:
        status = "red"
    elif partial or not has_file_index:
        status = "yellow"
    else:
        status = "green"

    label = f"{len(scenes)} 个场景路由"
    detail = "；".join(issues) if issues else "所有路由已填写完整"

    return {
        "status": status,
        "label": label,
        "detail": detail,
        "dead": dead,
        "partial": partial,
        "ok": ok,
        "has_file_index": has_file_index,
    }


def emoji(status):
    return {"green": "🟢", "yellow": "🟡", "red": "🔴"}.get(status, "⚪")


def run(target):
    memory_dir = Path(target) / "memory"

    if not memory_dir.exists():
        print("🔴 memory/ 目录不存在，先运行 init-agent-memory.py 搭建骨架")
        return 1

    results = {
        "rules": check_rules(memory_dir),
        "errors": check_errors(memory_dir),
        "routes": check_routes(memory_dir),
    }

    # 输出报告
    print()
    print("🔍  M3M 记忆健康检查")
    print("━" * 44)
    print()

    # rules.md
    r = results["rules"]
    print(f"📋 rules.md")
    age_str = f"（{r['age']} 天前）" if r.get("age") is not None else ""
    print(f"   {emoji(r['status'])} {r['label']} {age_str}")
    if r["status"] != "green":
        print(f"   → {r['detail']}")
    print()

    # error-log.md
    e = results["errors"]
    print(f"📋 error-log.md")
    print(f"   {emoji(e['status'])} {e['label']}")
    if e["status"] != "green":
        print(f"   → {e['detail']}")
    if e.get("count", 0) > 0:
        tag_summary = ", ".join(f"{t}({c})" for t, c in e.get("hot_tags", []))
        if tag_summary:
            print(f"   → 高频标签: {tag_summary}")
    print()

    # MEMORY.md
    ro = results["routes"]
    print(f"📋 MEMORY.md")
    print(f"   {emoji(ro['status'])} {ro['label']}")
    if ro["status"] != "green":
        print(f"   → {ro['detail']}")
    if ro["ok"]:
        print(f"   ✅ 已就绪: {', '.join(s['name'] for s in ro['ok'])}")
    if ro.get("partial"):
        for s in ro["partial"]:
            print(f"   ⚠️  {s['name']} 缺少: {', '.join(s['missing'])}")
    if ro.get("dead"):
        for s in ro["dead"]:
            print(f"   🔴 {s['name']} 完全空白（死路由）")
    print()

    # 综合评级
    print("━" * 44)
    statuses = [r["status"], e["status"], ro["status"]]
    reds = statuses.count("red")
    yellows = statuses.count("yellow")
    greens = statuses.count("green")

    if reds > 0:
        overall = "🔴 需要关注"
    elif yellows > 1:
        overall = "🟡 有点问题"
    elif yellows == 1:
        overall = "🟡 基本健康"
    else:
        overall = "🟢 骨架健康"

    print(f"🏥 综合评级: {overall}")
    print(f"   {greens} 项绿色 | {yellows} 项黄色 | {reds} 项红色")
    print()

    return 0 if reds == 0 else 1


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else "."
    sys.exit(run(target))


if __name__ == "__main__":
    main()
