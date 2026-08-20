#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
抓取 AI四小只 抖音账号数据，更新 account-history.md

用法：
  python fetch_account_metrics.py            # 跑爬虫 + 更新 history
  python fetch_account_metrics.py --parse    # 只解析已有 jsonl（不跑爬虫）

前置：
  - Chrome 已启动远程调试（tools/start_chrome.bat）
  - 第一次跑需要抖音扫码登录
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

TOOLS_DIR = Path(r"C:\kaifa_teacher\AI-四小只\tools")
MC_DIR = TOOLS_DIR / "MediaCrawler"
DATA_DIR = TOOLS_DIR / "data" / "creator"
HISTORY_FILE = Path(__file__).resolve().parent.parent / "references" / "account-history.md"
SEC_UID = "MS4wLjABAAAAQg5TgrTfWN0FphobcDhritBsLl8V3SS5H3ckUfdrXrI"


def run_crawler() -> bool:
    """调 MediaCrawler 抓 AI四小只 creator 主页数据"""
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    cmd = [
        sys.executable, "main.py",
        "--platform", "dy",
        "--lt", "qrcode",
        "--type", "creator",
        "--creator_id", SEC_UID,
        "--save_data_option", "jsonl",
        "--save_data_path", str(DATA_DIR),
        "--get_comment", "true",
        "--crawler_max_notes_count", "30",
    ]
    print("=" * 60)
    print("启动 MediaCrawler 抓取 AI四小只 creator 主页数据")
    print("sec_uid:", SEC_UID)
    print("输出目录:", DATA_DIR)
    print("=" * 60)
    print("第一次跑会弹二维码，请在 Chrome 里扫码登录抖音")
    print()
    try:
        result = subprocess.run(cmd, cwd=str(MC_DIR), check=False)
        return result.returncode == 0
    except FileNotFoundError:
        print("找不到 main.py，目录:", MC_DIR)
        return False


def parse_jsonl():
    """读 contents.jsonl，返回视频列表"""
    contents_file = DATA_DIR / "contents.jsonl"
    if not contents_file.exists():
        print("找不到", contents_file)
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


def update_history(contents):
    """把抓到的视频数据追加到 account-history.md"""
    if not HISTORY_FILE.exists():
        print("找不到", HISTORY_FILE)
        return

    today = datetime.now().strftime("%Y-%m-%d %H:%M")
    history = HISTORY_FILE.read_text(encoding="utf-8")

    log_line = f"- **{today}**：MediaCrawler 自动抓取 {len(contents)} 个视频"

    if "## 回测日志" in history:
        history = history.replace("## 回测日志\n", "## 回测日志\n" + log_line + "\n")
    else:
        history = history.rstrip() + "\n\n## 自动抓取日志\n" + log_line + "\n"

    HISTORY_FILE.write_text(history, encoding="utf-8")
    print("已写入 history.md")


def print_summary(contents):
    """打印抓取摘要"""
    print()
    print("=" * 60)
    print("抓取到", len(contents), "个视频")
    print("=" * 60)
    for i, v in enumerate(contents[:15], 1):
        title = (v.get("title") or v.get("desc") or "(无标题)")[:40]
        play = v.get("video_play_count") or "0"
        like = v.get("liked_count") or "0"
        fav = v.get("video_favorite_count") or "0"
        comment = v.get("video_comment") or "0"
        ts = v.get("create_time") or 0
        date = datetime.fromtimestamp(ts / 1000).strftime("%Y-%m-%d") if ts else "?"
        print(f"  {i:2d}. [{date}] play={play:>10}  like={like:>6}  fav={fav:>6}  cmt={comment:>5}  | {title}")
    print()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--parse", action="store_true", help="只解析已有 jsonl")
    args = parser.parse_args()

    if not args.parse:
        ok = run_crawler()
        if not ok:
            print()
            print("爬虫失败或被取消。可以稍后重跑，或用 --parse 只解析已有数据。")
            sys.exit(1)

    contents = parse_jsonl()
    if not contents:
        print("无数据可解析")
        sys.exit(1)

    print_summary(contents)
    update_history(contents)

    print("下一步：手动跑 tune_weights.py 看要不要调权重")
