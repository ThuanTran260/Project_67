"""
run_baseline.py — Chạy code chuẩn (AC) của 50 bài toán để xác nhận bộ test hợp lệ.
Tối ưu: Dùng ThreadPoolExecutor để chạy song song 50 bài → nhanh hơn 3-5x.

Kết quả lưu ra:
  - results/baseline_summary.csv   : Chi tiết từng bài
  - results/baseline_summary.json  : JSON đầy đủ

Nhóm 67 | Tuần 3 | Ngôn ngữ lập trình Python
"""

import json
import os
import sys
import csv
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed

# ── Auto-resolve BASE path ───────────────────────────────────────────────────
BASE = Path("/content/drive/MyDrive/Project")

sys.path.insert(0, str(BASE / "src"))
from runner_v2 import grade_submission

# try:
#     sys.stdout.reconfigure(encoding="utf-8")
#     sys.stderr.reconfigure(encoding="utf-8")
# except AttributeError:
#     pass

# ── Cấu hình ────────────────────────────────────────────────────────────────
DATASET_FILE = BASE / "data" / "processed" / "hidden_v2.json"
OUT_CSV      = BASE / "results" / "baseline_summary.csv"
OUT_JSON     = BASE / "results" / "baseline_summary.json"
MAX_WORKERS  = 8   # Số luồng song song (tăng nếu máy mạnh)


def run_one_task(task: dict) -> dict:
    """Chạy code chuẩn của một bài toán trên cả public và hidden tests."""
    tid       = task["task_id"]
    func_name = task["code"].split("def ")[1].split("(")[0].strip()
    code      = task["code"]
    pub_tests = task["public_tests"]
    hid_tests = task["hidden_tests"]

    pub_r = grade_submission(code, func_name, pub_tests, "public")
    hid_r = grade_submission(code, func_name, hid_tests, "hidden")

    pub_ok = pub_r["pass_count"] == pub_r["total_count"]
    hid_ok = hid_r["pass_count"] == hid_r["total_count"]

    return {
        "task_id":    tid,
        "func_name":  func_name,
        "topic":      task.get("topic", ""),
        # Public
        "pub_pass":   pub_r["pass_count"],
        "pub_total":  pub_r["total_count"],
        "pub_tpr":    pub_r["test_pass_rate"],
        "pub_WA":     pub_r["error_counts"]["WA"],
        "pub_RE":     pub_r["error_counts"]["RE"],
        "pub_TLE":    pub_r["error_counts"]["TLE"],
        "pub_SE":     pub_r["error_counts"]["SE"],
        "pub_MLE":    pub_r["error_counts"].get("MLE", 0),
        "pub_latency":pub_r["avg_latency"],
        # Hidden
        "hid_pass":   hid_r["pass_count"],
        "hid_total":  hid_r["total_count"],
        "hid_tpr":    hid_r["test_pass_rate"],
        "hid_WA":     hid_r["error_counts"]["WA"],
        "hid_RE":     hid_r["error_counts"]["RE"],
        "hid_TLE":    hid_r["error_counts"]["TLE"],
        "hid_SE":     hid_r["error_counts"]["SE"],
        "hid_MLE":    hid_r["error_counts"].get("MLE", 0),
        "hid_latency":hid_r["avg_latency"],
        # Tổng hợp
        "pub_all_pass":      pub_ok,
        "hid_all_pass":      hid_ok,
        "baseline_ok":       pub_ok and hid_ok,
        "avg_latency_total": round((pub_r["avg_latency"] + hid_r["avg_latency"]) / 2, 4),
    }


def main():
    t_start = time.perf_counter()
    print("=" * 65)
    print("  CHẠY BASELINE — Code chuẩn trên 50 bài toán")
    print(f"  Dataset: {DATASET_FILE.name}  |  Luồng song song: {MAX_WORKERS}")
    print("=" * 65)

    if not DATASET_FILE.exists():
        print(f"[LỖI] Không tìm thấy: {DATASET_FILE}")
        return

    with open(DATASET_FILE, encoding="utf-8") as f:
        tasks = json.load(f)

    print(f"\n  ✓ Đã load {len(tasks)} bài toán")
    print(f"  → Mỗi bài: {len(tasks[0]['public_tests'])} public + {len(tasks[0]['hidden_tests'])} hidden tests")
    print(f"\n  Bắt đầu chạy song song ({MAX_WORKERS} luồng)...\n")

    results = [None] * len(tasks)
    task_map = {t["task_id"]: i for i, t in enumerate(tasks)}

    with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
        future_to_task = {executor.submit(run_one_task, t): t for t in tasks}
        done_count = 0
        for future in as_completed(future_to_task):
            try:
                res = future.result()
                results[task_map[res["task_id"]]] = res
                status = "✓" if res["baseline_ok"] else "✗ FAIL"
                print(f"  [{status}] Task {res['task_id']:>2} {res['func_name']:<30} "
                      f"pub={res['pub_pass']}/{res['pub_total']} "
                      f"hid={res['hid_pass']}/{res['hid_total']} "
                      f"lat={res['avg_latency_total']}s")
            except Exception as e:
                t = future_to_task[future]
                print(f"  [✗ ERR] Task {t['task_id']} — {e}")
            done_count += 1

    t_elapsed = round(time.perf_counter() - t_start, 2)

    # ── Tính tổng kết ────────────────────────────────────────────────────────
    n = len(results)
    n_ok   = sum(1 for r in results if r and r["baseline_ok"])
    n_fail = n - n_ok
    avg_lat = round(sum(r["avg_latency_total"] for r in results if r) / n, 4)
    avg_pub_lat = round(sum(r["pub_latency"] for r in results if r) / n, 4)
    avg_hid_lat = round(sum(r["hid_latency"] for r in results if r) / n, 4)

    print(f"\n{'=' * 65}")
    print(f"  KẾT QUẢ BASELINE ({n} bài | {t_elapsed}s tổng)")
    print(f"{'=' * 65}")
    print(f"  ✓ PASS toàn bộ : {n_ok}/{n} bài")
    if n_fail > 0:
        print(f"  ✗ FAIL         : {n_fail} bài — CẦN KIỂM TRA TEST CASE!")
    print(f"  Latency public  : {avg_pub_lat}s/test")
    print(f"  Latency hidden  : {avg_hid_lat}s/test")
    print(f"  Latency trung bình : {avg_lat}s/test")
    print(f"{'=' * 65}")

    # ── Lưu CSV ─────────────────────────────────────────────────────────────
    os.makedirs(OUT_CSV.parent, exist_ok=True)
    fieldnames = list(results[0].keys())
    with open(OUT_CSV, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(r for r in results if r)
    print(f"\n  ✓ Lưu CSV: {OUT_CSV}")

    # ── Lưu JSON ─────────────────────────────────────────────────────────────
    output = {
        "meta": {
            "dataset": str(DATASET_FILE),
            "n_tasks": n,
            "n_pass":  n_ok,
            "n_fail":  n_fail,
            "elapsed_s": t_elapsed,
            "avg_latency_pub_s":  avg_pub_lat,
            "avg_latency_hid_s":  avg_hid_lat,
            "avg_latency_total_s": avg_lat,
        },
        "results": [r for r in results if r]
    }
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    print(f"  ✓ Lưu JSON: {OUT_JSON}")
    print(f"\n  Hoàn tất trong {t_elapsed}s\n")


if __name__ == "__main__":
    main()
