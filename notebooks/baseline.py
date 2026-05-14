"""
baseline.py — Chạy baseline toàn bộ MBPP subset
Nhóm 67 | Tuần 2

Quy trình:
  1. Đọc mbpp_subset.json
  2. Với mỗi bài: chạy solution mẫu qua bộ public test VÀ hidden test
  3. Tính tất cả metric: TPR, FPR, Error Classification, Latency
  4. Lưu kết quả ra results/
  5. In bảng tổng hợp
"""

import json, os, sys, csv
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from runner import grade_submission, compute_fpr

BASE = os.path.dirname(os.path.abspath(__file__))
DATA_FILE  = os.path.join(BASE, '..', 'data', 'raw', 'mbpp_subset.json')
OUT_DIR    = os.path.join(BASE, '..', 'results')
os.makedirs(OUT_DIR, exist_ok=True)


def run_baseline():
    with open(DATA_FILE, encoding='utf-8') as f:
        problems = json.load(f)

    print(f"{'='*70}")
    print(f"  BASELINE — MBPP Subset ({len(problems)} bài)")
    print(f"{'='*70}\n")

    all_results = []
    summary_rows = []

    # ── Đếm tổng False Positive ──
    fp_count   = 0
    total_bai  = 0

    for prob in problems:
        task_id   = prob["task_id"]
        text      = prob["text"]
        code      = prob["code"]
        topic     = prob["topic"]
        pub_tests = prob["public_tests"]
        hid_tests = prob["hidden_tests"]

        # Lấy tên hàm từ code
        func_name = [line.split("(")[0].replace("def ", "").strip()
                     for line in code.split("\n")
                     if line.startswith("def ")][0]

        # ── Chấm bộ public ──
        pub_result = grade_submission(code, func_name, pub_tests, "public")

        # ── Chấm bộ hidden ──
        hid_result = grade_submission(code, func_name, hid_tests, "hidden")

        # ── Tính FPR cho bài này ──
        fpr_info = compute_fpr(pub_result, hid_result)

        total_bai += 1
        if fpr_info["is_false_positive"]:
            fp_count += 1

        # ── In kết quả từng bài ──
        fp_flag = " ← FALSE POSITIVE" if fpr_info["is_false_positive"] else ""
        print(f"[{task_id:02d}] {func_name}() | {topic}")
        print(f"     Public : {pub_result['pass_count']}/{pub_result['total_count']} "
              f"({pub_result['test_pass_rate']}%)  "
              f"| Lỗi: {pub_result['error_counts']}")
        print(f"     Hidden : {hid_result['pass_count']}/{hid_result['total_count']} "
              f"({hid_result['test_pass_rate']}%)  "
              f"| Lỗi: {hid_result['error_counts']}{fp_flag}")
        print(f"     Latency: {hid_result['avg_latency']}s/test\n")

        # ── Tổng hợp row ──
        row = {
            "task_id":          task_id,
            "func_name":        func_name,
            "topic":            topic,
            # Public
            "pub_pass":         pub_result["pass_count"],
            "pub_total":        pub_result["total_count"],
            "pub_tpr":          pub_result["test_pass_rate"],
            "pub_SE":           pub_result["error_counts"]["SE"],
            "pub_WA":           pub_result["error_counts"]["WA"],
            "pub_RE":           pub_result["error_counts"]["RE"],
            "pub_TLE":          pub_result["error_counts"]["TLE"],
            # Hidden
            "hid_pass":         hid_result["pass_count"],
            "hid_total":        hid_result["total_count"],
            "hid_tpr":          hid_result["test_pass_rate"],
            "hid_SE":           hid_result["error_counts"]["SE"],
            "hid_WA":           hid_result["error_counts"]["WA"],
            "hid_RE":           hid_result["error_counts"]["RE"],
            "hid_TLE":          hid_result["error_counts"]["TLE"],
            # FPR
            "is_false_positive": fpr_info["is_false_positive"],
            # Latency
            "avg_latency_hid":  hid_result["avg_latency"],
            "avg_latency_pub":  pub_result["avg_latency"],
        }
        summary_rows.append(row)
        all_results.append({
            "task_id": task_id,
            "func_name": func_name,
            "topic": topic,
            "public": pub_result,
            "hidden": hid_result,
            "fpr_info": fpr_info
        })

    # ══ TỔNG HỢP METRIC ═══════════════════════════════════════
    print(f"\n{'='*70}")
    print("  BẢNG METRIC TỔNG HỢP")
    print(f"{'='*70}\n")

    # Test Pass Rate
    avg_pub_tpr = round(sum(r["pub_tpr"] for r in summary_rows) / len(summary_rows), 2)
    avg_hid_tpr = round(sum(r["hid_tpr"] for r in summary_rows) / len(summary_rows), 2)

    # Error counts tổng
    total_pub_SE  = sum(r["pub_SE"]  for r in summary_rows)
    total_pub_WA  = sum(r["pub_WA"]  for r in summary_rows)
    total_pub_RE  = sum(r["pub_RE"]  for r in summary_rows)
    total_pub_TLE = sum(r["pub_TLE"] for r in summary_rows)
    total_hid_SE  = sum(r["hid_SE"]  for r in summary_rows)
    total_hid_WA  = sum(r["hid_WA"]  for r in summary_rows)
    total_hid_RE  = sum(r["hid_RE"]  for r in summary_rows)
    total_hid_TLE = sum(r["hid_TLE"] for r in summary_rows)

    # Latency
    avg_latency_pub = round(sum(r["avg_latency_pub"] for r in summary_rows) / len(summary_rows), 4)
    avg_latency_hid = round(sum(r["avg_latency_hid"] for r in summary_rows) / len(summary_rows), 4)

    # FPR
    fpr_rate = round(fp_count / total_bai * 100, 2) if total_bai > 0 else 0

    metric_summary = {
        "so_bai":               total_bai,
        "public_test_per_bai":  3,
        "hidden_test_per_bai":  6,

        "avg_TPR_public_%":     avg_pub_tpr,
        "avg_TPR_hidden_%":     avg_hid_tpr,

        "false_positive_count": fp_count,
        "FPR_%":                fpr_rate,

        "error_public":  {"SE": total_pub_SE, "WA": total_pub_WA,
                          "RE": total_pub_RE, "TLE": total_pub_TLE},
        "error_hidden":  {"SE": total_hid_SE, "WA": total_hid_WA,
                          "RE": total_hid_RE, "TLE": total_hid_TLE},

        "avg_latency_public_s":  avg_latency_pub,
        "avg_latency_hidden_s":  avg_latency_hid,
    }

    print(f"  Số bài:                 {total_bai}")
    print(f"  Test/bài (public):      3  |  Test/bài (hidden): 6")
    print()
    print(f"  ▶ Test Pass Rate:")
    print(f"    - Bộ public (3 test):  {avg_pub_tpr}%")
    print(f"    - Bộ hidden (6 test):  {avg_hid_tpr}%")
    print()
    print(f"  ▶ False Positive Rate (RQ1):")
    print(f"    - Số bài FP:           {fp_count}/{total_bai}")
    print(f"    - FPR:                 {fpr_rate}%")
    print(f"    (= bài pass 3/3 public nhưng fail ít nhất 1 hidden)")
    print()
    print(f"  ▶ Phân loại lỗi — Bộ public:")
    print(f"    SE={total_pub_SE}  WA={total_pub_WA}  RE={total_pub_RE}  TLE={total_pub_TLE}")
    print(f"  ▶ Phân loại lỗi — Bộ hidden:")
    print(f"    SE={total_hid_SE}  WA={total_hid_WA}  RE={total_hid_RE}  TLE={total_hid_TLE}")
    print()
    print(f"  ▶ Latency trung bình/test:")
    print(f"    - Public: {avg_latency_pub}s  |  Hidden: {avg_latency_hid}s")
    print(f"\n{'='*70}\n")

    # ══ LƯU KẾT QUẢ ═══════════════════════════════════════════
    # JSON chi tiết
    out_json = os.path.join(OUT_DIR, "baseline_results.json")
    with open(out_json, 'w', encoding='utf-8') as f:
        json.dump({
            "metric_summary": metric_summary,
            "per_problem":    all_results
        }, f, ensure_ascii=False, indent=2)

    # CSV tổng hợp
    out_csv = os.path.join(OUT_DIR, "baseline_summary.csv")
    with open(out_csv, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=list(summary_rows[0].keys()))
        writer.writeheader()
        writer.writerows(summary_rows)

    # JSON metric tổng hợp riêng
    out_metric = os.path.join(OUT_DIR, "metric_summary.json")
    with open(out_metric, 'w', encoding='utf-8') as f:
        json.dump(metric_summary, f, ensure_ascii=False, indent=2)

    print(f"  ✓ Đã lưu: {out_json}")
    print(f"  ✓ Đã lưu: {out_csv}")
    print(f"  ✓ Đã lưu: {out_metric}\n")

    return metric_summary, summary_rows


if __name__ == "__main__":
    run_baseline()
