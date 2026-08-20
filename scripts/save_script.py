#!/usr/bin/env python
# usage: python save_script.py 2026-W34 30s-cursor "path/to/file.md"
import os, sys, shutil

project_root = r"C:\kaifa_teacher\AI-四小只\video"
if len(sys.argv) < 3:
    print("usage: save_script.py <YYYY-Wxx> <slug> [source_file]")
    sys.exit(1)

week = sys.argv[1]
slug = sys.argv[2]
target_dir = os.path.join(project_root, week)
os.makedirs(target_dir, exist_ok=True)
target_file = os.path.join(target_dir, f"{slug}.md")

if len(sys.argv) >= 4 and os.path.exists(sys.argv[3]):
    shutil.copy2(sys.argv[3], target_file)
    print(f"OK copied to {target_file}")
else:
    print(f"Created dir {target_dir}; please save content to {target_file}")
