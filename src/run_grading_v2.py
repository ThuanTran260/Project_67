"""
run_grading_v2.py — Chạy chấm bài tự động trên bộ bài nộp mô phỏng
Sử dụng bộ test cases v2 (13 tests/bài: 3 public, 10 hidden) và lưu kết quả.
Nhóm 67 | Tuần 3 | Ngôn ngữ lập trình Python
"""

import json
import os
import sys
from pathlib import Path

# Auto-resolve BASE path
cwd = os.getcwd()
if os.path.basename(cwd) in ["data", "src", "notebookes", "results"]:
    BASE = Path(cwd).parent
else:
    BASE = Path(cwd)

sys.path.insert(0, str(BASE / "src"))
from runner_v2 import grade_submission, compute_leakage
from error_stats import compute_stats, save_stats_csv, print_summary

SUBMISSIONS_FILE = BASE / "data" / "processed" / "submissions_50.json"
DATASET_FILE     = BASE / "data" / "processed" / "hidden_v2.json"
OUTPUT_CSV       = BASE / "results" / "error_analysis_v2.csv"
OUTPUT_JSON      = BASE / "results" / "error_analysis_v2.json"
TARGET_SUBMISSIONS = 100

# Đồng bộ hệ thống file để hiển thị được tiếng Việt có dấu trên Windows console
# try:
#     sys.stdout.reconfigure(encoding='utf-8')
#     sys.stderr.reconfigure(encoding='utf-8')
# except AttributeError:
#     pass

def main():
    print("=" * 65)
    print("  CHẠY CHẤM BÀI TỰ ĐỘNG V2")
    print("  Bộ test: 3 public + 6-10 hidden (Phân bố Chuông)")
    print("=" * 65)

    if not SUBMISSIONS_FILE.exists():
        print(f"\n[LỖI] Không tìm thấy file bài nộp: {SUBMISSIONS_FILE}")
        return

    if not DATASET_FILE.exists():
        print(f"\n[LỖI] Không tìm thấy file dataset: {DATASET_FILE}")
        return

    with open(SUBMISSIONS_FILE, encoding="utf-8") as f:
        submissions = json.load(f)

    if len(submissions) > TARGET_SUBMISSIONS:
        submissions = submissions[:TARGET_SUBMISSIONS]

    with open(DATASET_FILE, encoding="utf-8") as f:
        problems = {p["task_id"]: p for p in json.load(f)}

    print(f"\n  ✓ Đã load {len(submissions)} bài nộp mô phỏng")
    print(f"  ✓ Đã load {len(problems)} bài toán MBPP")
    print(f"  ✓ Số bài sẽ chấm: {len(submissions)}/{TARGET_SUBMISSIONS}")
    print(f"\n  Bắt đầu chấm (sử dụng psutil giới hạn tài nguyên và thu thập lỗi)...")
    print()

    results = []
    wrapped = []

    for i, sub in enumerate(submissions):
        try:
            sub_id    = sub["submission_id"]
            tid       = sub["task_id"]
            func_name = sub["func_name"]
            code      = sub["submitted_code"]
            err_type  = sub.get("error_type", "")
            topic     = sub.get("topic", "")

            prob = problems.get(tid)
            if not prob:
                print(f"  [!] Không tìm thấy task_id={tid} trong dataset")
                continue

            pub_tests = prob["public_tests"]
            hid_tests = prob["hidden_tests"]

            pub_r = grade_submission(code, func_name, pub_tests, "public")
            hid_r = grade_submission(code, func_name, hid_tests, "hidden")
            leakage = compute_leakage(pub_r, hid_r)

            # Xác định trạng thái tổng hợp cho học sinh
            if not pub_r["syntax_ok"]:
                status = "SE"
            else:
                ec_hid = hid_r["error_counts"]
                ec_pub = pub_r["error_counts"]

                if ec_hid.get("MLE", 0) > 0 or ec_pub.get("MLE", 0) > 0:
                    status = "MLE"
                elif ec_hid["TLE"] > 0 or ec_pub["TLE"] > 0:
                    status = "TLE"
                elif ec_hid["RE"] > 0 or ec_pub["RE"] > 0:
                    status = "RE"
                elif ec_hid["WA"] > 0 or ec_pub["WA"] > 0:
                    status = "WA"
                else:
                    status = "PASS"

            # Thu thập chi tiết lỗi đầy đủ làm feedback
            error_details = []
            for idx, r in enumerate(pub_r["test_results"]):
                if r["status"] != "PASS" and r.get("error_msg"):
                    error_details.append({
                        "set": "public",
                        "test_case_index": idx + 1,
                        "input": r["input"],
                        "expected": r["expected"],
                        "actual": r["actual"],
                        "status": r["status"],
                        "error_msg": r["error_msg"]
                    })
            for idx, r in enumerate(hid_r["test_results"]):
                if r["status"] != "PASS" and r.get("error_msg"):
                    error_details.append({
                        "set": "hidden",
                        "test_case_index": idx + 1,
                        "input": r["input"],
                        "expected": r["expected"],
                        "actual": r["actual"],
                        "status": r["status"],
                        "error_msg": r["error_msg"]
                    })

            res_item = {
                "submission_id":   sub_id,
                "task_id":         tid,
                "func_name":       func_name,
                "topic":           topic,
                "error_type":      err_type,
                "status":          status,

                "pub_pass":        pub_r["pass_count"],
                "pub_total":       pub_r["total_count"],
                "pub_tpr":         pub_r["test_pass_rate"],
                "pub_SE":          pub_r["error_counts"]["SE"],
                "pub_WA":          pub_r["error_counts"]["WA"],
                "pub_RE":          pub_r["error_counts"]["RE"],
                "pub_TLE":         pub_r["error_counts"]["TLE"],
                "pub_MLE":         pub_r["error_counts"].get("MLE", 0),

                "hid_pass":        hid_r["pass_count"],
                "hid_total":       hid_r["total_count"],
                "hid_tpr":         hid_r["test_pass_rate"],
                "hid_SE":          hid_r["error_counts"]["SE"],
                "hid_WA":          hid_r["error_counts"]["WA"],
                "hid_RE":          hid_r["error_counts"]["RE"],
                "hid_TLE":         hid_r["error_counts"]["TLE"],
                "hid_MLE":         hid_r["error_counts"].get("MLE", 0),

                "is_false_positive": leakage["is_public_test_leakage"],
                "is_public_test_leakage": leakage["is_public_test_leakage"],
                "avg_latency_s":   hid_r["avg_latency"],
                "error_details":   error_details
            }
            results.append(res_item)

            # Chuyển format tương thích cho compute_stats và save_stats_csv
            wrapped.append({
                "sv_id":    sub_id,
                "task_id":  tid,
                "func":     func_name,
                "topic":    topic,
                "mo_ta_loi": sub.get("note", ""),
                "public": {
                    "pass_count":    pub_r["pass_count"],
                    "total_count":   pub_r["total_count"],
                    "test_pass_rate": pub_r["test_pass_rate"],
                    "error_counts":  {
                        "SE": pub_r["error_counts"]["SE"],
                        "WA": pub_r["error_counts"]["WA"],
                        "RE": pub_r["error_counts"]["RE"],
                        "TLE": pub_r["error_counts"]["TLE"],
                        "MLE": pub_r["error_counts"].get("MLE", 0),
                    },
                    "avg_latency": pub_r["avg_latency"],
                },
                "hidden": {
                    "pass_count":    hid_r["pass_count"],
                    "total_count":   hid_r["total_count"],
                    "test_pass_rate": hid_r["test_pass_rate"],
                    "error_counts":  {
                        "SE": hid_r["error_counts"]["SE"],
                        "WA": hid_r["error_counts"]["WA"],
                        "RE": hid_r["error_counts"]["RE"],
                        "TLE": hid_r["error_counts"]["TLE"],
                        "MLE": hid_r["error_counts"].get("MLE", 0),
                    },
                    "avg_latency": hid_r["avg_latency"],
                },
                "leakage": {
                    "is_public_test_leakage": leakage["is_public_test_leakage"],
                    "is_false_positive": leakage["is_public_test_leakage"],
                    "public_rate":  leakage["public_rate"],
                    "hidden_rate":  leakage["hidden_rate"],
                    "public_pass_all": leakage["public_pass_all"],
                    "hidden_pass_all": leakage["hidden_pass_all"],
                },
            })

        except Exception as e:
            print(f"  [LỖI] Submission {i+1} bị crash: {e}")
            continue

        if (i + 1) % 10 == 0:
            print(f"  Chấm xong {i + 1}/{len(submissions)} bài...")

    # Lưu kết quả
    os.makedirs(OUTPUT_CSV.parent, exist_ok=True)

    # Ghi CSV theo chuẩn format đã chỉnh sửa
    save_stats_csv(wrapped, str(OUTPUT_CSV))
    print(f"  ✓ Lưu CSV: {OUTPUT_CSV}")

    # Ghi JSON đầy đủ bao gồm thông tin traceback chi tiết
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Lưu JSON (Đầy đủ traceback): {OUTPUT_JSON}")

    # Thống kê tổng hợp
    stats = compute_stats(wrapped)
    print_summary(stats, "KẾT QUẢ CHẤM BÀI V2 (Set 3: Bell Curve)")

if __name__ == "__main__":
    main()
