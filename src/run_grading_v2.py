"""
run_grading_v2.py — Chạy chấm bài chấm điểm tự động trên 200 bài nộp mô phỏng
Sử dụng bộ test cases v2 (13 tests/bài: 3 public, 10 hidden) và lưu kết quả.
Nhóm 67 | Tuần 3 | Ngôn ngữ lập trình Python
"""

import json
import os
import sys
import csv
from pathlib import Path

# Auto-resolve BASE path
cwd = os.getcwd()
if os.path.basename(cwd) in ["data", "src", "notebooks", "results"]:
    BASE = Path(cwd).parent
else:
    BASE = Path(cwd)

# Thêm thư mục src vào PATH để import runner_v2 và error_stats
sys.path.insert(0, str(BASE / "src"))
from runner_v2 import grade_submission, compute_fpr
from error_stats import analyze_errors, print_ascii_report, export_stats_to_csv

SUBMISSIONS_FILE = BASE / "data" / "processed" / "submissions_50.json"
V2_DATASET_FILE = BASE / "data" / "processed" / "hidden_v2.json"
OUTPUT_CSV = BASE / "results" / "error_analysis_v2.csv"
OUTPUT_JSON = BASE / "results" / "error_analysis_v2.json"


def main():
    print("======================================================================")
    print(" CHAY CHAM DIEM TU DONG V2 - 100 BAI NOP TREN 13 TESTS/BAI (V2)")
    print("======================================================================")

    # 1. Load files
    if not SUBMISSIONS_FILE.exists():
        print(f"ERROR: Thieu file bai nop {SUBMISSIONS_FILE}")
        return
    if not V2_DATASET_FILE.exists():
        print(f"ERROR: Thieu file dataset v2 {V2_DATASET_FILE}")
        return

    with open(SUBMISSIONS_FILE, encoding="utf-8") as f:
        submissions = json.load(f)
    with open(V2_DATASET_FILE, encoding="utf-8") as f:
        problems = {p["task_id"]: p for p in json.load(f)}

    print(f" OK: Da load {len(submissions)} bai nop mo phong.")
    print(f" OK: Da load {len(problems)} bai toan MBPP.")
    print(" Bat dau cham bai (co the mat thoi gian chay do co TLE)...")

    results = []
    
    for i, sub in enumerate(submissions):
        sub_id = sub["submission_id"]
        tid = sub["task_id"]
        func_name = sub["func_name"]
        code = sub["submitted_code"]
        err_type = sub["error_type"]
        
        prob = problems.get(tid)
        if not prob:
            print(f"  [!] Khong tim thay bai toan task_id={tid}")
            continue

        # Chấm điểm trên 3 public tests và 10 hidden tests
        pub_tests = prob["public_tests"]
        hid_tests = prob["hidden_tests"]
        
        pub_r = grade_submission(code, func_name, pub_tests, "public")
        hid_r = grade_submission(code, func_name, hid_tests, "hidden")
        fpr = compute_fpr(pub_r, hid_r)
        
        # Xác định status đại diện
        # Nếu có lỗi cú pháp
        if not pub_r["syntax_ok"]:
            status = "SE"
        elif pub_r["banned_import"]:
            status = "RE"
        else:
            # Chọn lỗi nặng nhất trong hidden hoặc public
            errors = hid_r["error_counts"]
            pub_errors = pub_r["error_counts"]
            
            if errors["TLE"] > 0 or pub_errors["TLE"] > 0:
                status = "TLE"
            elif errors["MLE"] > 0 or pub_errors["MLE"] > 0:
                status = "MLE"
            elif errors["RE"] > 0 or pub_errors["RE"] > 0:
                status = "RE"
            elif errors["WA"] > 0 or pub_errors["WA"] > 0:
                status = "WA"
            else:
                status = "PASS"

        results.append({
            "submission_id": sub_id,
            "task_id": tid,
            "func_name": func_name,
            "topic": sub["topic"],
            "error_type": err_type,
            "status": status,
            "pub_pass": pub_r["pass_count"],
            "pub_total": pub_r["total_count"],
            "pub_tpr": pub_r["test_pass_rate"],
            "hid_pass": hid_r["pass_count"],
            "hid_total": hid_r["total_count"],
            "hid_tpr": hid_r["test_pass_rate"],
            "is_false_positive": fpr["is_false_positive"],
            "avg_latency": hid_r["avg_latency"]
        })

        if (i + 1) % 40 == 0:
            print(f"  Cham xong {i + 1}/100 bai nop...")

    # 2. Lưu kết quả ra CSV
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0].keys()))
        writer.writeheader()
        writer.writerows(results)

    # 3. Lưu kết quả ra JSON để mô phỏng
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)

    print(f"\n[OK] Da luu ket qua chi tiet: {OUTPUT_CSV}")

    # 4. Tạo thống kê
    stats = analyze_errors(results)
    print_ascii_report(stats)


if __name__ == "__main__":
    main()
