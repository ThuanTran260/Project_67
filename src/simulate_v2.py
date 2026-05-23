"""
simulate_v2.py — Đọc 50 bài nộp từ thư mục raw và lưu sang thư mục processed
Nhóm 67 | Tuần 3 | Ngôn ngữ lập trình Python
"""

import json
import os
import sys
from pathlib import Path
from collections import Counter

# Thiết lập encoding UTF-8 cho Windows console
if sys.stdout.encoding != 'utf-8':
    import io
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Auto-resolve BASE path
BASE = Path("/content/drive/MyDrive/Project")
RAW_FILE = BASE / "data" / "raw" / "submissions_50.json"
OUT_FILE = BASE / "data" / "processed" / "submissions_50.json"

def generate():
    if not RAW_FILE.exists():
        print(f"ERROR: Khong tim thay file nguon {RAW_FILE}")
        return
        
    print(f"Dang doc du lieu tu {RAW_FILE}...")
    with open(RAW_FILE, "r", encoding="utf-8") as f:
        submissions = json.load(f)
        
    # Đảm bảo thư mục đầu ra tồn tại
    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(submissions, f, ensure_ascii=False, indent=2)
        
    print(f"OK: Da sao chep {len(submissions)} bai nop tu raw sang processed -> {OUT_FILE}")
    
    # In phân bố lỗi để kiểm chứng
    counts = Counter(s["error_type"] for s in submissions)
    for k, v in sorted(counts.items()):
        print(f"  {k}: {v} bai nop")
        
    # In phân bố task_id để kiểm chứng đủ 50 task
    task_ids = sorted(set(s["task_id"] for s in submissions))
    print(f"  Task IDs ({len(task_ids)} tasks): {task_ids[0]} -> {task_ids[-1]}")

if __name__ == "__main__":
    generate()
