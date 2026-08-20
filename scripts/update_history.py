#!/usr/bin/env python3
# 更新账号历史播放记录
# 调用：python update_history.py <周次> <视频序号 1-3> <实际播放> <备注>
# 例：python update_history.py 2026-W35 1 5200 "学生党反响不错"

import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent.parent
HISTORY_FILE = BASE / "references" / "account-history.md"

def update(week, video_no, actual_play, note=""):
    if not HISTORY_FILE.exists():
        print("history file not found")
        return
    content = HISTORY_FILE.read_text(encoding="utf-8")
    needle = f"| {video_no} | 待生成 |"
    if needle not in content:
        print(f"video {video_no} not in pending state")
        return
    replacement = f"| {video_no} | 已发布 | - | - | - | {actual_play} | - | {note} |"
    content = content.replace(needle, replacement)
    HISTORY_FILE.write_text(content, encoding="utf-8")
    print(f"updated W{week} video {video_no}: {actual_play}")

if __name__ == "__main__":
    if len(sys.argv) < 4:
        print("usage: update_history.py <week> <video_no 1-3> <actual_play> [note]")
        sys.exit(1)
    week = sys.argv[1]
    video_no = sys.argv[2]
    actual_play = sys.argv[3]
    note = sys.argv[4] if len(sys.argv) > 4 else ""
    update(week, video_no, actual_play, note)
