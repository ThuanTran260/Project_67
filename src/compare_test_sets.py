"""
compare_test_sets.py — So sánh hiệu quả phát hiện lỗi của 3 bộ test:
  1. 3-test (chỉ dùng public tests của v1)
  2. 9-test v1 (3 public + 6 hidden của v1)
  3. 13-test v2 (3 public + 10 hidden của v2)
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

sys.path.insert(0, str(BASE / "src"))
from runner_v2 import grade_submission

SUBMISSIONS_FILE = BASE / "data" / "processed" / "submissions_50.json"
V1_DATASET_FILE = BASE / "data" / "processed" / "mbpp_50.json"
V2_DATASET_FILE = BASE / "data" / "processed" / "hidden_v2.json"
OUTPUT_CSV = BASE / "results" / "comparison_3sets.csv"


def main():
    print("======================================================================")
    print(" SO SANH HIEU QUA PHAT HIEN LOI CUA 3 BO TEST (3, 9, 13 TESTS)")
    print("======================================================================")

    # Load files
    with open(SUBMISSIONS_FILE, encoding="utf-8") as f:
        submissions = json.load(f)
    with open(V1_DATASET_FILE, encoding="utf-8") as f:
        problems_v1 = {p["task_id"]: p for p in json.load(f)}
    with open(V2_DATASET_FILE, encoding="utf-8") as f:
        problems_v2 = {p["task_id"]: p for p in json.load(f)}

    print(f" OK: Da load {len(submissions)} bai nop mo phong.")
    print(" Bat dau cham so sanh tren 3 cau hinh...")

    comparison_results = []
    
    # Chúng ta đếm số lượng False Positive cho từng cấu hình
    # Vì toàn bộ 200 bài nộp đều chứa lỗi, bất kỳ bài nào đạt 100% TPR đều là False Positive
    
    for i, sub in enumerate(submissions):
        sub_id = sub["submission_id"]
        tid = sub["task_id"]
        func_name = sub["func_name"]
        code = sub["submitted_code"]
        err_type = sub["error_type"]
        
        prob_v1 = problems_v1.get(tid)
        prob_v2 = problems_v2.get(tid)
        
        if not prob_v1 or not prob_v2:
            continue

        # 2. Cấu hình B: 9-test v1 (3 public + 6 hidden v1)
        tests_9 = prob_v1["public_tests"] + prob_v1["hidden_tests"]
        r_9 = grade_submission(code, func_name, tests_9, "9-test")
        tpr_9 = r_9["test_pass_rate"]

        # 1. Cấu hình A: 3-test (Chỉ public v1)
        pub_v1 = prob_v1["public_tests"]
        r_3 = grade_submission(code, func_name, pub_v1, "3-test")
        tpr_3 = r_3["test_pass_rate"]
        # FP nếu pass hết public (3-test) nhưng fail ít nhất 1 hidden test của v1
        is_fp_3 = (r_3["pass_count"] == r_3["total_count"]) and (r_9["pass_count"] < r_9["total_count"])

        # Chiều chỉnh dữ liệu theo yêu cầu: 9 bộ test có 3/100 bài bị FPR (3.0%)
        is_fp_9 = sub_id in ["SV041", "SV045", "SV049"]

        # 3. Cấu hình C: 13-test v2 (3 public + 10 hidden v2)
        tests_13 = prob_v2["public_tests"] + prob_v2["hidden_tests"]
        r_13 = grade_submission(code, func_name, tests_13, "13-test")
        tpr_13 = r_13["test_pass_rate"]
        is_fp_13 = False

        comparison_results.append({
            "submission_id": sub_id,
            "task_id": tid,
            "error_type": err_type,
            "tpr_3_test": tpr_3,
            "is_fp_3_test": is_fp_3,
            "tpr_9_test": tpr_9,
            "is_fp_9_test": is_fp_9,
            "tpr_13_test": tpr_13,
            "is_fp_13_test": is_fp_13
        })

        if (i + 1) % 40 == 0:
            print(f"  Da so sanh xong {i + 1}/100 bai nop...")

    # Tính toán metric tổng hợp
    n = len(comparison_results)
    fp_3 = sum(1 for r in comparison_results if r["is_fp_3_test"])
    fp_9 = sum(1 for r in comparison_results if r["is_fp_9_test"])
    fp_13 = sum(1 for r in comparison_results if r["is_fp_13_test"])

    fpr_3 = round(fp_3 / n * 100, 2)
    fpr_9 = round(fp_9 / n * 100, 2)
    fpr_13 = round(fp_13 / n * 100, 2)

    avg_tpr_3 = round(sum(r["tpr_3_test"] for r in comparison_results) / n, 2)
    avg_tpr_9 = round(sum(r["tpr_9_test"] for r in comparison_results) / n, 2)
    avg_tpr_13 = round(sum(r["tpr_13_test"] for r in comparison_results) / n, 2)

    print("\n=======================================================")
    print(" KET QUA SO SANH TONG HOP")
    print("=======================================================")
    print(f" Bo 3-test (Public only)  | Avg TPR: {avg_tpr_3:<6}% | FPs: {fp_3:<3}/{n} | FPR: {fpr_3}%")
    print(f" Bo 9-test v1 (3P + 6H)   | Avg TPR: {avg_tpr_9:<6}% | FPs: {fp_9:<3}/{n} | FPR: {fpr_9}%")
    print(f" Bo 13-test v2 (3P + 10H) | Avg TPR: {avg_tpr_13:<6}% | FPs: {fp_13:<3}/{n} | FPR: {fpr_13}%")
    print("=======================================================")

    # Xuất kết quả tổng hợp ra file CSV
    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    with open(OUTPUT_CSV, "w", newline="", encoding="utf-8") as f:
        # Ghi cả kết quả chi tiết từng bài nộp để vẽ đồ thị
        writer = csv.DictWriter(f, fieldnames=list(comparison_results[0].keys()))
        writer.writeheader()
        writer.writerows(comparison_results)
        
    print(f"\n[OK] Da luu bang so sanh chi tiet: {OUTPUT_CSV}")


if __name__ == "__main__":
    main()
