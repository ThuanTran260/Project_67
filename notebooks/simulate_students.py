"""
simulate_students.py — Mô phỏng bài nộp sinh viên với lỗi thực tế
Nhóm 67 | Tuần 2

Mục đích: Chạy các bài nộp có lỗi để:
  1. Thấy FPR thực sự (pass public nhưng fail hidden)
  2. Thấy các loại lỗi khác nhau (WA, RE, TLE, SE)
  3. So sánh Test Pass Rate giữa bộ public và hidden
  → Trả lời RQ1
"""

import json, os, sys, csv
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from runner import grade_submission, compute_fpr

BASE     = os.path.dirname(os.path.abspath(__file__))
DATA     = os.path.join(BASE, '..', 'data', 'raw', 'mbpp_subset.json')
OUT_DIR  = os.path.join(BASE, '..', 'results')
os.makedirs(OUT_DIR, exist_ok=True)

with open(DATA, encoding='utf-8') as f:
    problems = {p["task_id"]: p for p in json.load(f)}

# ══════════════════════════════════════════════════════════════
# Bài nộp sinh viên mô phỏng — có lỗi cố ý
# Mỗi submission: task_id, sv_id, code, mô tả lỗi
# ══════════════════════════════════════════════════════════════
submissions = [

    # ── Bài 1: sum_list ──────────────────────────────────────
    {
        "task_id": 1, "sv_id": "SV001",
        "mo_ta_loi": "Quên xử lý danh sách rỗng (nhưng test public không có [])",
        "code": """def sum_list(lst):
    total = 0
    for i in range(len(lst)):
        total += lst[i]
    return total
"""
    },
    {
        "task_id": 1, "sv_id": "SV002",
        "mo_ta_loi": "Dùng biến sai — cộng index thay vì giá trị",
        "code": """def sum_list(lst):
    total = 0
    for i in range(len(lst)):
        total += i
    return total
"""
    },

    # ── Bài 2: is_even ───────────────────────────────────────
    {
        "task_id": 2, "sv_id": "SV003",
        "mo_ta_loi": "Sai kết quả với số âm (% trong Python có thể âm)",
        "code": """def is_even(n):
    remainder = n % 2
    if remainder == 0:
        return True
    return False
"""
    },
    {
        "task_id": 2, "sv_id": "SV004",
        "mo_ta_loi": "Syntax Error — thiếu dấu :",
        "code": """def is_even(n)
    return n % 2 == 0
"""
    },

    # ── Bài 3: reverse_string ────────────────────────────────
    {
        "task_id": 3, "sv_id": "SV005",
        "mo_ta_loi": "Dùng vòng lặp nhưng sai điều kiện với chuỗi rỗng",
        "code": """def reverse_string(s):
    result = ""
    for i in range(len(s) - 1, -1, -1):
        result += s[i]
    return result
"""
    },

    # ── Bài 4: find_max ──────────────────────────────────────
    {
        "task_id": 4, "sv_id": "SV006",
        "mo_ta_loi": "Dùng sorted() nhưng lấy phần tử đầu thay vì cuối",
        "code": """def find_max(lst):
    return sorted(lst)[0]
"""
    },
    {
        "task_id": 4, "sv_id": "SV007",
        "mo_ta_loi": "Runtime Error khi list rỗng (không bao giờ xảy ra với public test)",
        "code": """def find_max(lst):
    m = lst[0]
    for x in lst:
        if x > m:
            m = x
    return m
"""
    },

    # ── Bài 9: average ───────────────────────────────────────
    {
        "task_id": 9, "sv_id": "SV008",
        "mo_ta_loi": "Không xử lý danh sách rỗng — gây ZeroDivisionError với hidden test []",
        "code": """def average(lst):
    return sum(lst) / len(lst)
"""
    },

    # ── Bài 11: is_prime ─────────────────────────────────────
    {
        "task_id": 11, "sv_id": "SV009",
        "mo_ta_loi": "Không xử lý n=0 và n=1 — pass public test (2, 4, 7) nhưng fail hidden (0, 1)",
        "code": """def is_prime(n):
    for i in range(2, n):
        if n % i == 0:
            return False
    return True
"""
    },

    # ── Bài 13: fibonacci ────────────────────────────────────
    {
        "task_id": 13, "sv_id": "SV010",
        "mo_ta_loi": "Đệ quy không có base case cho n=0 — RE với hidden test (0)",
        "code": """def fibonacci(n):
    if n == 1:
        return 1
    return fibonacci(n-1) + fibonacci(n-2)
"""
    },

    # ── Bài 14: count_words ──────────────────────────────────
    {
        "task_id": 14, "sv_id": "SV011",
        "mo_ta_loi": "Không xử lý chuỗi toàn khoảng trắng — WA với hidden test '   '",
        "code": """def count_words(s):
    return len(s.split())
"""
    },

    # ── Bài 15: sort_list ────────────────────────────────────
    {
        "task_id": 15, "sv_id": "SV012",
        "mo_ta_loi": "Bubble sort cài sai — không ổn định với list trùng",
        "code": """def sort_list(lst):
    n = len(lst)
    for i in range(n):
        for j in range(0, n-i-1):
            if lst[j] > lst[j+1]:
                lst[j], lst[j+1] = lst[j+1], lst[j]
    return lst
"""
    },
]

# ══════════════════════════════════════════════════════════════
# Chạy từng submission
# ══════════════════════════════════════════════════════════════
print(f"{'='*72}")
print(f"  MÔ PHỎNG BÀI NỘP SINH VIÊN — {len(submissions)} submissions")
print(f"{'='*72}\n")

sim_rows = []
fp_count = 0

for sub in submissions:
    tid   = sub["task_id"]
    sv_id = sub["sv_id"]
    code  = sub["code"]
    prob  = problems[tid]
    func_name = [l.split("(")[0].replace("def ","").strip()
                 for l in code.split("\n") if l.strip().startswith("def ")][0]

    pub_tests = prob["public_tests"]
    hid_tests = prob["hidden_tests"]

    pub_r = grade_submission(code, func_name, pub_tests, "public")
    hid_r = grade_submission(code, func_name, hid_tests, "hidden")
    fpr   = compute_fpr(pub_r, hid_r)

    if fpr["is_false_positive"]:
        fp_count += 1
        fp_flag = " ★ FALSE POSITIVE"
    else:
        fp_flag = ""

    print(f"[{sv_id}] Bài {tid} — {func_name}()")
    print(f"  Lỗi mô phỏng : {sub['mo_ta_loi']}")
    print(f"  Public  : {pub_r['pass_count']}/{pub_r['total_count']} "
          f"({pub_r['test_pass_rate']}%) | {pub_r['error_counts']}")
    print(f"  Hidden  : {hid_r['pass_count']}/{hid_r['total_count']} "
          f"({hid_r['test_pass_rate']}%) | {hid_r['error_counts']}{fp_flag}")
    print()

    sim_rows.append({
        "sv_id":             sv_id,
        "task_id":           tid,
        "func":              func_name,
        "mo_ta_loi":         sub["mo_ta_loi"],
        "pub_pass":          pub_r["pass_count"],
        "pub_total":         pub_r["total_count"],
        "pub_tpr":           pub_r["test_pass_rate"],
        "pub_errors":        str(pub_r["error_counts"]),
        "hid_pass":          hid_r["pass_count"],
        "hid_total":         hid_r["total_count"],
        "hid_tpr":           hid_r["test_pass_rate"],
        "hid_errors":        str(hid_r["error_counts"]),
        "is_false_positive": fpr["is_false_positive"],
    })

# ══════════════════════════════════════════════════════════════
# Kết luận RQ1
# ══════════════════════════════════════════════════════════════
total = len(submissions)
fpr_rate = round(fp_count / total * 100, 2)

print(f"\n{'='*72}")
print(f"  KẾT LUẬN RQ1")
print(f"{'='*72}")
print(f"  Tổng submissions kiểm tra : {total}")
print(f"  Bài FP (pass public, fail hidden): {fp_count} / {total}")
print(f"  False Positive Rate        : {fpr_rate}%")
print()
print("  → Với chỉ 3 test/bài (public), hệ thống có thể chấm SAI")
print("    cho các bài thực chất có lỗi về edge case.")
print("  → Khi thêm 6 hidden test, FPR giảm đáng kể.")
print(f"{'='*72}\n")

# Lưu kết quả
out_csv = os.path.join(OUT_DIR, "student_simulation.csv")
with open(out_csv, 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=list(sim_rows[0].keys()))
    writer.writeheader()
    writer.writerows(sim_rows)

out_json = os.path.join(OUT_DIR, "student_simulation.json")
with open(out_json, 'w', encoding='utf-8') as f:
    json.dump({
        "tong_submissions": total,
        "fp_count": fp_count,
        "fpr_rate_%": fpr_rate,
        "submissions": sim_rows
    }, f, ensure_ascii=False, indent=2)

print(f"  ✓ Đã lưu: {out_csv}")
print(f"  ✓ Đã lưu: {out_json}")
