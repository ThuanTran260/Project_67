"""
run_grading_v2.py — Chạy chấm bài tự động trên bộ bài nộp mô phỏng
Sử dụng bộ test cases v2 (13 tests/bài: 3 public, 10 hidden) và lưu kết quả.
Nhóm 67 | Tuần 3 | Ngôn ngữ lập trình Python
"""

import json
import os
import sys
from pathlib import Path

# ── Auto-resolve BASE path ────────────────────────────────────────────────────
cwd = os.getcwd()
if os.path.basename(cwd) in ["data", "src", "notebooks", "results"]:
    BASE = Path(cwd).parent
else:
    BASE = Path(cwd)

sys.path.insert(0, str(BASE / "src"))
from runner_v2 import grade_submission, compute_fpr
from error_stats import compute_stats, save_stats_csv, print_summary

# ── Đường dẫn file ───────────────────────────────────────────────────────────
SUBMISSIONS_FILE = BASE / "data" / "processed" / "submissions_50.json"
DATASET_FILE     = BASE / "data" / "processed" / "hidden_v2.json"
OUTPUT_CSV       = BASE / "results" / "error_analysis_v2.csv"
OUTPUT_JSON      = BASE / "results" / "error_analysis_v2.json"


def main():
    print("=" * 65)
    print("  CHẠY CHẤM BÀI TỰ ĐỘNG V2")
    print("  Bộ test: 3 public + 10 hidden = 13 test/bài")
    print("=" * 65)

    # ── 1. Load dữ liệu ───────────────────────────────────────────────────────
    if not SUBMISSIONS_FILE.exists():
        print(f"\n[LỖI] Không tìm thấy file bài nộp: {SUBMISSIONS_FILE}")
        print("  → Chạy 03_simulate_v2.ipynb trước để tạo file này.")
        return

    if not DATASET_FILE.exists():
        print(f"\n[LỖI] Không tìm thấy file dataset: {DATASET_FILE}")
        print("  → Kiểm tra lại thư mục data/processed/")
        return

    with open(SUBMISSIONS_FILE, encoding="utf-8") as f:
        submissions = json.load(f)

    with open(DATASET_FILE, encoding="utf-8") as f:
        problems = {p["task_id"]: p for p in json.load(f)}

    print(f"\n  ✓ Đã load {len(submissions)} bài nộp mô phỏng")
    print(f"  ✓ Đã load {len(problems)} bài toán MBPP")
    print(f"\n  Bắt đầu chấm (có thể mất 3–5 phút do subprocess)...")
    print()

    # ── 2. Chấm từng bài nộp ─────────────────────────────────────────────────
    results = []

    for i, sub in enumerate(submissions):
        sub_id    = sub["submission_id"]
        tid       = sub["task_id"]
        func_name = sub["func_name"]
        code      = sub["submitted_code"]
        err_type  = sub.get("error_type", "")

        prob = problems.get(tid)
        if not prob:
            print(f"  [!] Không tìm thấy task_id={tid} trong dataset")
            continue

        pub_tests = prob["public_tests"]
        hid_tests = prob["hidden_tests"]

        pub_r = grade_submission(code, func_name, pub_tests, "public")
        hid_r = grade_submission(code, func_name, hid_tests, "hidden")
        fpr   = compute_fpr(pub_r, hid_r)

        # ── Xác định trạng thái tổng hợp ──────────────────────────────────
        # Ưu tiên lỗi nặng nhất: SE > TLE > RE > WA > PASS
        # (Chỉ dùng SE/WA/RE/TLE — không có MLE trong runner_v2)
        if not pub_r["syntax_ok"]:
            status = "SE"
        else:
            ec_hid = hid_r["error_counts"]
            ec_pub = pub_r["error_counts"]

            if ec_hid["TLE"] > 0 or ec_pub["TLE"] > 0:
                status = "TLE"
            elif ec_hid["RE"] > 0 or ec_pub["RE"] > 0:
                status = "RE"
            elif ec_hid["WA"] > 0 or ec_pub["WA"] > 0:
                status = "WA"
            else:
                status = "PASS"

        results.append({
            "submission_id":   sub_id,
            "task_id":         tid,
            "func_name":       func_name,
            "topic":           sub.get("topic", ""),
            "error_type":      err_type,
            "status":          status,
            # Public test metrics
            "pub_pass":        pub_r["pass_count"],
            "pub_total":       pub_r["total_count"],
            "pub_tpr":         pub_r["test_pass_rate"],
            "pub_SE":          pub_r["error_counts"]["SE"],
            "pub_WA":          pub_r["error_counts"]["WA"],
            "pub_RE":          pub_r["error_counts"]["RE"],
            "pub_TLE":         pub_r["error_counts"]["TLE"],
            # Hidden test metrics
            "hid_pass":        hid_r["pass_count"],
            "hid_total":       hid_r["total_count"],
            "hid_tpr":         hid_r["test_pass_rate"],
            "hid_SE":          hid_r["error_counts"]["SE"],
            "hid_WA":          hid_r["error_counts"]["WA"],
            "hid_RE":          hid_r["error_counts"]["RE"],
            "hid_TLE":         hid_r["error_counts"]["TLE"],
            # FPR
            "is_false_positive": fpr["is_false_positive"],
            "avg_latency_s":   hid_r["avg_latency"],
        })

        # In tiến độ mỗi 10 bài
        if (i + 1) % 10 == 0:
            print(f"  Chấm xong {i + 1}/{len(submissions)} bài...")

    print(f"\n  ✓ Chấm xong {len(results)} bài\n")

    # ── 3. Lưu kết quả ───────────────────────────────────────────────────────
    os.makedirs(OUTPUT_CSV.parent, exist_ok=True)

    # CSV chi tiết
    save_stats_csv(results, str(OUTPUT_CSV))
    print(f"  ✓ Lưu CSV: {OUTPUT_CSV}")

    # JSON đầy đủ
    with open(OUTPUT_JSON, "w", encoding="utf-8") as f:
        json.dump(results, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Lưu JSON: {OUTPUT_JSON}")

    # ── 4. In thống kê tổng hợp ──────────────────────────────────────────────
    # Chuyển format cho compute_stats
    wrapped = []
    for r in results:
        wrapped.append({
            "sv_id":    r["submission_id"],
            "task_id":  r["task_id"],
            "func":     r["func_name"],
            "topic":    r["topic"],
            "mo_ta_loi": r["error_type"],
            "public": {
                "pass_count":    r["pub_pass"],
                "total_count":   r["pub_total"],
                "test_pass_rate": r["pub_tpr"],
                "error_counts":  {
                    "SE": r["pub_SE"], "WA": r["pub_WA"],
                    "RE": r["pub_RE"], "TLE": r["pub_TLE"],
                },
                "avg_latency": r["avg_latency_s"],
            },
            "hidden": {
                "pass_count":    r["hid_pass"],
                "total_count":   r["hid_total"],
                "test_pass_rate": r["hid_tpr"],
                "error_counts":  {
                    "SE": r["hid_SE"], "WA": r["hid_WA"],
                    "RE": r["hid_RE"], "TLE": r["hid_TLE"],
                },
                "avg_latency": r["avg_latency_s"],
            },
            "fpr": {
                "is_false_positive": r["is_false_positive"],
                "public_rate":  r["pub_tpr"],
                "hidden_rate":  r["hid_tpr"],
                "public_pass_all": r["pub_pass"] == r["pub_total"],
                "hidden_pass_all": r["hid_pass"] == r["hid_total"],
            },
        })

    stats = compute_stats(wrapped)
    print_summary(stats, "KẾT QUẢ CHẤM BÀI V2")


if __name__ == "__main__":
    main()
