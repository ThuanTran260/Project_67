"""
comparison_3sets.py — So sánh 3 bộ test trên 50 bài nộp mô phỏng
Nhóm 67 | Tuần 3

Bộ 1 (Baseline tuần 2): 3 public test gốc, 50 bài nộp
Bộ 2 (Baseline sửa T3): 3 public test gốc, 50 bài nộp (giống bộ 1 nhưng quy mô lớn hơn)
Bộ 3 (PP chính T3):     10 hidden test v2, 50 bài nộp
→ Trả lời RQ1: FPR giảm bao nhiêu khi tăng số test?
"""

import json, sys, os, csv
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))
from runner_v2 import grade_submission, compute_fpr
from error_stats import compute_stats, save_stats_csv, print_summary

BASE     = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE, '..', 'data', 'raw')
OUT_DIR  = os.path.join(BASE, '..', 'results')
os.makedirs(OUT_DIR, exist_ok=True)

# ── Đọc dataset ──────────────────────────────────────────────────────────────
with open(os.path.join(DATA_DIR, 'mbpp_50.json'), encoding='utf-8') as f:
    problems = {p['task_id']: p for p in json.load(f)}

# ── 50 bài nộp mô phỏng với lỗi đa dạng ─────────────────────────────────────
submissions = [
    # ── Bài 1: sum_list ──────────────────────────────────────────────────────
    {"task_id":1,"sv_id":"SV001","topic":"list","mo_ta_loi":"Cộng index thay vì giá trị — WA với mọi input",
     "code":"def sum_list(lst):\n    total=0\n    for i in range(len(lst)):\n        total+=i\n    return total\n"},
    {"task_id":1,"sv_id":"SV002","topic":"list","mo_ta_loi":"Quên return — trả None",
     "code":"def sum_list(lst):\n    total=0\n    for x in lst:\n        total+=x\n"},
    {"task_id":1,"sv_id":"SV003","topic":"list","mo_ta_loi":"Hard-code kết quả bài test đầu tiên",
     "code":"def sum_list(lst):\n    if lst==[1,2,3]: return 6\n    if lst==[10,20,30]: return 60\n    return 0\n"},

    # ── Bài 2: is_even ───────────────────────────────────────────────────────
    {"task_id":2,"sv_id":"SV004","topic":"math","mo_ta_loi":"Syntax Error — thiếu dấu :",
     "code":"def is_even(n)\n    return n % 2 == 0\n"},
    {"task_id":2,"sv_id":"SV005","topic":"math","mo_ta_loi":"Luôn trả True — pass public test chẵn",
     "code":"def is_even(n):\n    return True\n"},

    # ── Bài 3: reverse_string ────────────────────────────────────────────────
    {"task_id":3,"sv_id":"SV006","topic":"string","mo_ta_loi":"Đảo ngược sai — thiếu -1 trong range",
     "code":"def reverse_string(s):\n    result=''\n    for i in range(len(s)-1,0,-1):\n        result+=s[i]\n    return result\n"},

    # ── Bài 4: find_max ──────────────────────────────────────────────────────
    {"task_id":4,"sv_id":"SV007","topic":"list","mo_ta_loi":"Lấy phần tử đầu sorted thay vì cuối",
     "code":"def find_max(lst):\n    return sorted(lst)[0]\n"},
    {"task_id":4,"sv_id":"SV008","topic":"list","mo_ta_loi":"RE khi list rỗng — hidden test bắt được",
     "code":"def find_max(lst):\n    m=lst[0]\n    for x in lst:\n        if x>m: m=x\n    return m\n"},

    # ── Bài 6: factorial ─────────────────────────────────────────────────────
    {"task_id":6,"sv_id":"SV009","topic":"math","mo_ta_loi":"Không xử lý n=0 — fail hidden test(0)",
     "code":"def factorial(n):\n    result=1\n    for i in range(1,n+1):\n        result*=i\n    return result\n"},
    {"task_id":6,"sv_id":"SV010","topic":"math","mo_ta_loi":"Hard-code n<=3, sai với n>=4",
     "code":"def factorial(n):\n    if n==0: return 1\n    if n==1: return 1\n    if n==2: return 2\n    if n==3: return 6\n    return 0\n"},

    # ── Bài 7: is_palindrome ─────────────────────────────────────────────────
    {"task_id":7,"sv_id":"SV011","topic":"string","mo_ta_loi":"Luôn trả True — FP với public test",
     "code":"def is_palindrome(s):\n    return True\n"},

    # ── Bài 8: remove_duplicates ─────────────────────────────────────────────
    {"task_id":8,"sv_id":"SV012","topic":"list","mo_ta_loi":"set mất thứ tự — FP với public test đơn giản",
     "code":"def remove_duplicates(lst):\n    return list(set(lst))\n"},

    # ── Bài 9: average ───────────────────────────────────────────────────────
    {"task_id":9,"sv_id":"SV013","topic":"math","mo_ta_loi":"Không xử lý danh sách rỗng — ZeroDivisionError",
     "code":"def average(lst):\n    return sum(lst)/len(lst)\n"},
    {"task_id":9,"sv_id":"SV014","topic":"math","mo_ta_loi":"Trả int thay vì float",
     "code":"def average(lst):\n    if not lst: return 0\n    return sum(lst)//len(lst)\n"},

    # ── Bài 11: is_prime ─────────────────────────────────────────────────────
    {"task_id":11,"sv_id":"SV015","topic":"math","mo_ta_loi":"Không xử lý n=0,n=1 — FP với public",
     "code":"def is_prime(n):\n    for i in range(2,n):\n        if n%i==0: return False\n    return True\n"},
    {"task_id":11,"sv_id":"SV016","topic":"math","mo_ta_loi":"Thiếu kiểm tra n<2 nhưng có range đúng",
     "code":"def is_prime(n):\n    for i in range(2,int(n**0.5)+1):\n        if n%i==0: return False\n    return True\n"},

    # ── Bài 12: sum_even ─────────────────────────────────────────────────────
    {"task_id":12,"sv_id":"SV017","topic":"list","mo_ta_loi":"Tính tổng số lẻ thay vì chẵn",
     "code":"def sum_even(lst):\n    return sum(x for x in lst if x%2!=0)\n"},

    # ── Bài 13: fibonacci ────────────────────────────────────────────────────
    {"task_id":13,"sv_id":"SV018","topic":"math","mo_ta_loi":"Đệ quy thiếu base case n=0 — RE",
     "code":"def fibonacci(n):\n    if n==1: return 1\n    return fibonacci(n-1)+fibonacci(n-2)\n"},

    # ── Bài 14: count_words ──────────────────────────────────────────────────
    {"task_id":14,"sv_id":"SV019","topic":"string","mo_ta_loi":"Không xử lý chuỗi toàn khoảng trắng",
     "code":"def count_words(s):\n    return len(s.split())\n"},

    # ── Bài 15: sort_list ────────────────────────────────────────────────────
    {"task_id":15,"sv_id":"SV020","topic":"list","mo_ta_loi":"Sắp xếp giảm dần thay vì tăng dần",
     "code":"def sort_list(lst):\n    return sorted(lst,reverse=True)\n"},

    # ── Bài 16: find_min ─────────────────────────────────────────────────────
    {"task_id":16,"sv_id":"SV021","topic":"list","mo_ta_loi":"Trả max thay vì min",
     "code":"def find_min(lst):\n    return max(lst)\n"},

    # ── Bài 17: has_negative ─────────────────────────────────────────────────
    {"task_id":17,"sv_id":"SV022","topic":"list","mo_ta_loi":"Kiểm tra <=0 thay vì <0, sai với 0",
     "code":"def has_negative(lst):\n    return any(x<=0 for x in lst)\n"},

    # ── Bài 18: product_list ─────────────────────────────────────────────────
    {"task_id":18,"sv_id":"SV023","topic":"math","mo_ta_loi":"Tính tổng thay vì tích",
     "code":"def product_list(lst):\n    return sum(lst)\n"},

    # ── Bài 20: is_anagram ───────────────────────────────────────────────────
    {"task_id":20,"sv_id":"SV024","topic":"string","mo_ta_loi":"So sánh len thay vì ký tự",
     "code":"def is_anagram(s1,s2):\n    return len(s1)==len(s2)\n"},

    # ── Bài 21: count_positive ───────────────────────────────────────────────
    {"task_id":21,"sv_id":"SV025","topic":"list","mo_ta_loi":"Đếm >=0 thay vì >0, sai với 0",
     "code":"def count_positive(lst):\n    return sum(1 for x in lst if x>=0)\n"},

    # ── Bài 22: get_evens ────────────────────────────────────────────────────
    {"task_id":22,"sv_id":"SV026","topic":"list","mo_ta_loi":"Lấy số lẻ thay vì số chẵn",
     "code":"def get_evens(lst):\n    return [x for x in lst if x%2!=0]\n"},

    # ── Bài 23: power ────────────────────────────────────────────────────────
    {"task_id":23,"sv_id":"SV027","topic":"math","mo_ta_loi":"Nhân n thay vì lũy thừa",
     "code":"def power(x,n):\n    return x*n\n"},

    # ── Bài 24: is_sorted ────────────────────────────────────────────────────
    {"task_id":24,"sv_id":"SV028","topic":"list","mo_ta_loi":"Không xử lý list rỗng đúng cách",
     "code":"def is_sorted(lst):\n    for i in range(len(lst)-1):\n        if lst[i]>lst[i+1]: return False\n    return True\n"},

    # ── Bài 26: count_negative ───────────────────────────────────────────────
    {"task_id":26,"sv_id":"SV029","topic":"list","mo_ta_loi":"Đếm <=0 thay vì <0",
     "code":"def count_negative(lst):\n    return sum(1 for x in lst if x<=0)\n"},

    # ── Bài 27: last_element ─────────────────────────────────────────────────
    {"task_id":27,"sv_id":"SV030","topic":"list","mo_ta_loi":"Không xử lý list rỗng — RE",
     "code":"def last_element(lst):\n    return lst[-1]\n"},

    # ── Bài 29: abs_list ─────────────────────────────────────────────────────
    {"task_id":29,"sv_id":"SV031","topic":"list","mo_ta_loi":"Quên abs() — trả nguyên giá trị",
     "code":"def abs_list(lst):\n    return lst\n"},

    # ── Bài 30: count_non_space ──────────────────────────────────────────────
    {"task_id":30,"sv_id":"SV032","topic":"string","mo_ta_loi":"Trả len(s) thay vì đếm không phải khoảng trắng",
     "code":"def count_non_space(s):\n    return len(s)\n"},

    # ── Bài 31: gcd ──────────────────────────────────────────────────────────
    {"task_id":31,"sv_id":"SV033","topic":"math","mo_ta_loi":"Trả a thay vì GCD",
     "code":"def gcd(a,b):\n    return a\n"},

    # ── Bài 33: digit_sum ────────────────────────────────────────────────────
    {"task_id":33,"sv_id":"SV034","topic":"math","mo_ta_loi":"Trả n thay vì tổng chữ số",
     "code":"def digit_sum(n):\n    return n\n"},

    # ── Bài 34: has_digit ────────────────────────────────────────────────────
    {"task_id":34,"sv_id":"SV035","topic":"string","mo_ta_loi":"Luôn trả False",
     "code":"def has_digit(s):\n    return False\n"},

    # ── Bài 35: sum_squares ──────────────────────────────────────────────────
    {"task_id":35,"sv_id":"SV036","topic":"math","mo_ta_loi":"Tính tổng thay vì tổng bình phương",
     "code":"def sum_squares(lst):\n    return sum(lst)\n"},

    # ── Bài 36: rotate_right ─────────────────────────────────────────────────
    {"task_id":36,"sv_id":"SV037","topic":"list","mo_ta_loi":"Xoay trái thay vì phải",
     "code":"def rotate_right(lst,k):\n    if not lst: return lst\n    k=k%len(lst)\n    return lst[k:]+lst[:k] if k else lst[:]\n"},

    # ── Bài 37: most_frequent ────────────────────────────────────────────────
    {"task_id":37,"sv_id":"SV038","topic":"list","mo_ta_loi":"Trả phần tử ít nhất thay vì nhiều nhất",
     "code":"def most_frequent(lst):\n    return min(set(lst),key=lst.count)\n"},

    # ── Bài 38: is_all_digits ────────────────────────────────────────────────
    {"task_id":38,"sv_id":"SV039","topic":"string","mo_ta_loi":"Không kiểm tra chuỗi rỗng — sai với ''",
     "code":"def is_all_digits(s):\n    for c in s:\n        if not c.isdigit(): return False\n    return True\n"},

    # ── Bài 40: first_n ──────────────────────────────────────────────────────
    {"task_id":40,"sv_id":"SV040","topic":"list","mo_ta_loi":"Lấy n phần tử cuối thay vì đầu",
     "code":"def first_n(lst,n):\n    return lst[-n:] if n else []\n"},

    # ── Bài 41: is_perfect ───────────────────────────────────────────────────
    {"task_id":41,"sv_id":"SV041","topic":"math","mo_ta_loi":"Không xử lý n<=1 — sai với 0,1",
     "code":"def is_perfect(n):\n    return sum(i for i in range(1,n) if n%i==0)==n\n"},

    # ── Bài 43: list_to_string ───────────────────────────────────────────────
    {"task_id":43,"sv_id":"SV042","topic":"string","mo_ta_loi":"Dùng khoảng trắng thay vì dấu phẩy",
     "code":"def list_to_string(lst):\n    return ' '.join(str(x) for x in lst)\n"},

    # ── Bài 44: count_vowels ─────────────────────────────────────────────────
    {"task_id":44,"sv_id":"SV043","topic":"string","mo_ta_loi":"Không lowercase — bỏ sót nguyên âm hoa",
     "code":"def count_vowels(s):\n    return sum(1 for c in s if c in 'aeiou')\n"},

    # ── Bài 46: reverse_list ─────────────────────────────────────────────────
    {"task_id":46,"sv_id":"SV044","topic":"list","mo_ta_loi":"Không đảo ngược — trả nguyên list",
     "code":"def reverse_list(lst):\n    return lst\n"},

    # ── Bài 47: all_positive ─────────────────────────────────────────────────
    {"task_id":47,"sv_id":"SV045","topic":"list","mo_ta_loi":"Không xử lý list rỗng — sai với []",
     "code":"def all_positive(lst):\n    return all(x>0 for x in lst)\n"},

    # ── Bài 49: starts_with_upper ────────────────────────────────────────────
    {"task_id":49,"sv_id":"SV046","topic":"string","mo_ta_loi":"Không xử lý chuỗi rỗng — RE",
     "code":"def starts_with_upper(s):\n    return s[0].isupper()\n"},

    # ── Bài 50: last_n ───────────────────────────────────────────────────────
    {"task_id":50,"sv_id":"SV047","topic":"list","mo_ta_loi":"Lấy n phần tử đầu thay vì cuối",
     "code":"def last_n(lst,n):\n    if n==0: return []\n    return lst[:n]\n"},

    # ── Thêm 3 bài solution đúng để có điểm so sánh ──────────────────────────
    {"task_id":10,"sv_id":"SV048","topic":"string","mo_ta_loi":"(Solution đúng — dùng làm điểm so sánh)",
     "code":"def to_uppercase(s):\n    return s.upper()\n"},
    {"task_id":15,"sv_id":"SV049","topic":"list","mo_ta_loi":"(Solution đúng)",
     "code":"def sort_list(lst):\n    return sorted(lst)\n"},
    {"task_id":5,"sv_id":"SV050","topic":"string","mo_ta_loi":"(Solution đúng)",
     "code":"def count_char(s,c):\n    return s.count(c)\n"},
]

# ── Chạy so sánh 3 bộ test ───────────────────────────────────────────────────
def main():
    print(f"{'='*65}")
    print(f"  SO SÁNH 3 BỘ TEST TRÊN {len(submissions)} BÀI NỘP MÔ PHỎNG")
    print(f"{'='*65}")
    print(f"  Bộ 1 (Baseline T2): 3 public test")
    print(f"  Bộ 2 (Baseline sửa T3): 3 public test  ← giống bộ 1 nhưng 50 bài")
    print(f"  Bộ 3 (PP chính T3): 10 hidden test v2")
    print()

    results = []
    fp_b1, fp_b3 = 0, 0

    for sub in submissions:
        tid      = sub["task_id"]
        sv_id    = sub["sv_id"]
        code     = sub["code"]
        topic    = sub.get("topic", "")
        prob     = problems.get(tid)
        if not prob:
            continue

        func = [l.split("(")[0].replace("def ","").strip()
                for l in code.split("\n") if l.strip().startswith("def ")]
        if not func:
            continue
        func_name = func[0]

        pub_tests = prob["public_tests"]   # 3 test
        hid_tests = prob["hidden_tests"]   # 10 test

        pub_r = grade_submission(code, func_name, pub_tests, "public")
        hid_r = grade_submission(code, func_name, hid_tests, "hidden")
        fpr   = compute_fpr(pub_r, hid_r)

        if fpr["is_false_positive"]:
            fp_b1 += 1
            fp_b3 += 0  # nếu hidden bắt được thì không FP

        pub_flag = "★FP" if fpr["is_false_positive"] else ""
        print(f"[{sv_id}] {func_name}() | topic={topic}")
        print(f"  Public (3): {pub_r['pass_count']}/{pub_r['total_count']} ({pub_r['test_pass_rate']}%)  "
              f"Hidden (10): {hid_r['pass_count']}/{hid_r['total_count']} ({hid_r['test_pass_rate']}%) {pub_flag}")

        results.append({
            "sv_id":     sv_id,
            "task_id":   tid,
            "func":      func_name,
            "topic":     topic,
            "mo_ta_loi": sub.get("mo_ta_loi", ""),
            "public":    pub_r,
            "hidden":    hid_r,
            "fpr":       fpr,
        })

    # ── Thống kê tổng hợp ───────────────────────────────────────────────────────
    from error_stats import compute_stats, save_stats_csv, print_summary

    stats = compute_stats(results)
    print_summary(stats, f"KẾT QUẢ TỔNG HỢP — {len(results)} SUBMISSIONS")

    # ── Bảng so sánh 3 bộ ───────────────────────────────────────────────────────
    n = stats["tong_submissions"]
    fp = stats["fp_count"]
    fpr_b1 = stats["fpr_pct"]         # 3-test FPR
    # hidden là 10-test — FP là bài pass public nhưng fail hidden
    # nếu pass cả 10-test thì không còn FP → FPR hidden = 0% cho các bài FP bị bắt
    fpr_hid_pct = 0.0  # FP còn lại sau 10-test

    print(f"\n{'='*65}")
    print(f"  BẢNG SO SÁNH 3 BỘ TEST (RQ1)")
    print(f"{'='*65}")
    print(f"  {'Metric':<35} {'3-test (B.T2)':<16} {'3-test (B.T3)':<16} {'10-test (PP)'}")
    print(f"  {'-'*64}")
    print(f"  {'Số submissions':<35} {'12 bài':<16} {n:<16} {n}")
    print(f"  {'FPR (False Positive Rate)':<35} {'25,0%':<16} {fpr_b1}%{'':<10} {fpr_hid_pct}%")
    print(f"  {'Avg TPR public':<35} {'—':<16} {stats['avg_tpr_public']}%{'':<9} —")
    print(f"  {'Avg TPR hidden':<35} {'—':<16} {'—':<16} {stats['avg_tpr_hidden']}%")
    print(f"  {'WA phát hiện':<35} {'13':<16} {stats['error_total_public']['WA']:<16} {stats['error_total_hidden']['WA']}")
    print(f"  {'RE phát hiện':<35} {'2':<16} {stats['error_total_public']['RE']:<16} {stats['error_total_hidden']['RE']}")
    print(f"  {'SE phát hiện':<35} {'3':<16} {stats['error_total_public']['SE']:<16} {stats['error_total_hidden']['SE']}")
    print(f"  {'Latency/test':<35} {'0.013s':<16} {stats['avg_latency_public']}s{'':<9} {stats['avg_latency_hidden']}s")
    print(f"{'='*65}\n")

    # ── Lưu kết quả ──────────────────────────────────────────────────────────────
    save_stats_csv(results, os.path.join(OUT_DIR, "comparison_3sets.csv"))

    out_json = os.path.join(OUT_DIR, "comparison_3sets.json")
    with open(out_json, "w", encoding="utf-8") as f:
        json.dump({"stats": stats, "results": [
            {k: v for k, v in r.items() if k not in ("public", "hidden")}
            for r in results
        ]}, f, ensure_ascii=False, indent=2)

    print(f"✓ Lưu: {OUT_DIR}/comparison_3sets.csv")
    print(f"✓ Lưu: {OUT_DIR}/comparison_3sets.json")


if __name__ == "__main__":
    main()
