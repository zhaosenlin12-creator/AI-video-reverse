#!/usr/bin/env python3
# 4 周回测后自动调权重
# 调用：python tune_weights.py
# 读 account-history.md，按近 4 周实际播放自动调权重，写回 weight-tuning.md

from pathlib import Path
import re
from datetime import datetime, timedelta

BASE = Path(__file__).resolve().parent.parent
HISTORY = BASE / "references" / "account-history.md"
WEIGHTS = BASE / "references" / "weight-tuning.md"

def parse_history():
    """解析历史表，返回 [(周次, [(视频号, 类型, 实际播放, 备注)])]"""
    if not HISTORY.exists():
        return []
    text = HISTORY.read_text(encoding="utf-8")
    weeks = []
    for week_match in re.finditer(r"## (\d{4}-W\d+).*?\n(.*?)(?=\n## |\Z)", text, re.DOTALL):
        week = week_match.group(1)
        body = week_match.group(2)
        videos = []
        for row in re.finditer(r"\| (\d) \| (.+?) \| (.+?) \| .+?\| .+?\| ([^|]+?) \|", body):
            vno = row.group(1)
            topic = row.group(2).strip()
            vtype = row.group(3).strip()
            play = row.group(4).strip()
            videos.append((vno, topic, vtype, play))
        weeks.append((week, videos))
    return weeks

def parse_play(s):
    """解析播放数字（支持 10000+ / 8000 / <500）"""
    s = s.strip()
    if s in ("-", "待回填", ""):
        return None
    s = s.replace("+", "").replace("<", "").replace(">", "")
    try:
        return int(s)
    except:
        return None

def compute_adjustments(weeks):
    """根据近 4 周数据计算权重调整建议"""
    recent = weeks[-4:] if len(weeks) >= 4 else weeks
    type_avg = {}
    for week, videos in recent:
        for vno, topic, vtype, play in videos:
            p = parse_play(play)
            if p is None:
                continue
            type_avg.setdefault(vtype, []).append(p)
    adjustments = {}
    for vtype, plays in type_avg.items():
        avg = sum(plays) / len(plays)
        if avg > 10000:
            adjustments["赛道匹配"] = adjustments.get("赛道匹配", 0) + 1
        elif avg < 1000 and len(plays) >= 2:
            adjustments["赛道匹配"] = adjustments.get("赛道匹配", 0) - 1
    return adjustments, type_avg

def apply_adjustments(adjustments):
    if not WEIGHTS.exists():
        return
    text = WEIGHTS.read_text(encoding="utf-8")
    today = datetime.now().strftime("%Y-%m-%d")
    log_line = f"- **{today}**：自动调权 {adjustments}"
    text = text.replace("- **2026-08-20**：初始权重定标（基于 W34 已有数据）",
                        log_line + "\n- **2026-08-20**：初始权重定标（基于 W34 已有数据）")
    for dim, delta in adjustments.items():
        pattern = rf"(\| {re.escape(dim)} \| \d+ \| )(\d+)"
        m = re.search(pattern, text)
        if m:
            old = int(m.group(2))
            new = max(1, min(5, old + delta))
            text = text.replace(f"| {dim} | 3 | {old}", f"| {dim} | 3 | {new}", 1)
    WEIGHTS.write_text(text, encoding="utf-8")
    print(f"weights updated: {adjustments}")

if __name__ == "__main__":
    weeks = parse_history()
    adjustments, type_avg = compute_adjustments(weeks)
    print("近 4 周各类型平均播放:", type_avg)
    print("建议调整:", adjustments)
    if input("apply? (y/n) ").strip().lower() == "y":
        apply_adjustments(adjustments)
