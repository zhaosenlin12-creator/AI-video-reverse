#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抓取抖音 / 小红书 AI 关键词搜索热榜，输出 hotlist.json 给 Stage 2 用

用法：
  python fetch_hotlist.py dy    # 抓抖音
  python fetch_hotlist.py xhs   # 抓小红书
  python fetch_hotlist.py both  # 两个都抓
"""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

TOOLS_DIR = Path(r"C:\kaifa_teacher\AI-四小只\tools")
MC_DIR = TOOLS_DIR / "MediaCrawler"
DATA_DIR = TOOLS_DIR / "data" / "hotlist"
OUTPUT_JSON = Path(__file__).resolve().parent.parent / "tools" / "hotlist.json"

KEYWORDS_DY = "AI工具,AI编程,WorkBuddy,AI Agent"
KEYWORDS_XHS = "AI工具,AI编程,WorkBuddy,提示词"


def run_one(platform: str, keywords: str) -> bool:
    platform_dir = DATA_DIR / platform
    platform_dir.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable, "main.py",
        "--platform", platform,
        "--lt", "qrcode",
        "--type", "search",
        "--keywords", keywords,
        "--save_data_option", "jsonl",
        "--save_data_path", str(platform_dir),
        "--get_comment", "false",
        "--crawler_max_notes_count", "50",
    ]
    print("=" * 60)
    print(f"抓取 {platform} 关键词: {keywords}")
    print("=" * 60)
    result = subprocess.run(cmd, cwd=str(MC_DIR), check=False)
    return result.returncode == 0


def parse_jsonl(platform: str):
    contents_file = DATA_DIR / platform / "contents.jsonl"
    if not contents_file.exists():
        return []
    items = []
    with open(contents_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            try:
                items.append(json.loads(line))
            except json.JSONDecodeError:
                continue
    return items


def summarize(items, platform: str):
    """汇总成 hotlist.json"""
    summary = {
        "platform": platform,
        "fetched_at": datetime.now().isoformat(),
        "total": len(items),
        "items": [],
    }
    for v in items[:30]:
        summary["items"].append({
            "aweme_id": v.get("aweme_id"),
            "title": (v.get("title") or v.get("desc") or "")[:80],
            "play_count": v.get("video_play_count") or "0",
            "liked_count": v.get("liked_count") or "0",
            "source_keyword": v.get("source_keyword") or "",
            "create_time": v.get("create_time") or 0,
        })
    return summary


def main():
    arg = sys.argv[1] if len(sys.argv) > 1 else "both"
    results = {"fetched_at": datetime.now().isoformat(), "platforms": {}}

    if arg in ("dy", "both"):
        if run_one("dy", KEYWORDS_DY):
            items = parse_jsonl("dy")
            results["platforms"]["dy"] = summarize(items, "dy")
            print(f"抖音抓取 {len(items)} 条")

    if arg in ("xhs", "both"):
        if run_one("xhs", KEYWORDS_XHS):
            items = parse_jsonl("xhs")
            results["platforms"]["xhs"] = summarize(items, "xhs")
            print(f"小红书抓取 {len(items)} 条")

    OUTPUT_JSON.write_text(json.dumps(results, ensure_ascii=False, indent=2), encoding="utf-8")
    print(f"\n汇总写入: {OUTPUT_JSON}")
    print("\nTop 10 高播放词条：")
    if results["platforms"]:
        all_items = []
        for plat, summary in results["platforms"].items():
            for item in summary["items"]:
                item["_platform"] = plat
                all_items.append(item)
        all_items.sort(key=lambda x: int(x.get("play_count") or 0), reverse=True)
        for i, v in enumerate(all_items[:10], 1):
            print(f"  {i:2d}. [{v['_platform']}] play={v['play_count']:>10}  | {v['title'][:50]}")


if __name__ == "__main__":
    main()
