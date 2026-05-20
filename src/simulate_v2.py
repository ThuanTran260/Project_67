"""
simulate_v2.py — Tạo 100 bài nộp mô phỏng đa dạng (WA, RE, SE, TLE, Hard-code)
Nhóm 67 | Tuần 3 | Ngôn ngữ lập trình Python
"""

import json
import os
import sys
from pathlib import Path
from collections import Counter

# Thiết lập encoding UTF-8 cho Windows console
# if sys.stdout.encoding != 'utf-8':
#     import io
#     sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
if sys.stdout.encoding != 'utf-8':
    import io
    # Kiểm tra xem sys.stdout có thuộc tính 'buffer' không (tránh lỗi trên Jupyter)
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# Auto-resolve BASE path
cwd = os.getcwd()
if os.path.basename(cwd) in ["data", "src", "notebooks", "results"]:
    BASE = Path(cwd).parent
else:
    BASE = Path(cwd)

MBPP_FILE = BASE / "data" / "processed" / "mbpp_50.json"
OUT_FILE = BASE / "data" / "processed" / "submissions_50.json"


def extract_func_name(code: str) -> str:
    """Trích xuất tên hàm từ mã nguồn."""
    first = code.strip().split("\n")[0]
    return first.split("def ")[1].split("(")[0].strip()


def make_SE(task: dict) -> str:
    """Tạo mã nguồn lỗi cú pháp (Syntax Error)."""
    func = extract_func_name(task["code"])
    t = task["task_id"]
    se_codes = [
        f"def {func}(lst)\n    return sum(lst)",            # Thiếu dấu hai chấm
        f"def {func}(lst):\nreturn lst",                      # Lỗi thụt lề
        f"def {func}(lst):\n    return sum(lst",              # Thiếu đóng ngoặc
        f"def {func}(lst):\n    if True\n        return 1",   # Thiếu dấu hai chấm ở if
    ]
    return se_codes[(t - 1) % len(se_codes)]


def make_WA(task: dict) -> str:
    """Tạo mã nguồn chạy được nhưng trả về kết quả sai (Wrong Answer)."""
    func = extract_func_name(task["code"])
    t = task["task_id"]
    topic = task["topic"]

    if topic == "list":
        wa = [
            f"def {func}(lst):\n    return sum(lst) * 2",
            f"def {func}(lst):\n    return lst",
            f"def {func}(lst):\n    return list(set(lst))",   # Mất thứ tự
            f"def {func}(lst):\n    return len(lst)",
        ]
    elif topic == "string":
        wa = [
            f"def {func}(s, *args):\n    return s",
            f"def {func}(s, *args):\n    return s.lstrip()",
            f"def {func}(s, *args):\n    return s[::-1]",      # Đảo ngược chuỗi (có thể sai cho bài khác)
            f"def {func}(s, *args):\n    return s.upper()",
        ]
    else:  # math
        wa = [
            f"def {func}(n, *args):\n    return n * n",
            f"def {func}(n, *args):\n    return n + 1",
            f"def {func}(n, *args):\n    return n % 2 == 1",
            f"def {func}(n, *args):\n    return n",
        ]
    return wa[(t - 1) % len(wa)]


def make_RE(task: dict) -> str:
    """Tạo mã nguồn crash khi chạy (Runtime Error)."""
    func = extract_func_name(task["code"])
    t = task["task_id"]
    topic = task["topic"]

    if topic == "list":
        re_codes = [
            f"def {func}(lst):\n    return lst[0] + sum(lst[1:])",  # Crash nếu danh sách rỗng
            f"def {func}(lst):\n    return sum(lst) / len(lst)",   # ZeroDivisionError nếu rỗng
            f"def {func}(lst):\n    return lst[-999]",             # IndexError
        ]
    elif topic == "string":
        re_codes = [
            f"def {func}(s, *args):\n    return s[0].upper() + s[1:]", # Crash nếu chuỗi rỗng
            f"def {func}(s, *args):\n    return int(s) * 2",          # ValueError nếu chuỗi không chứa số
            f"def {func}(s, *args):\n    return s.nonexistent_method()", # AttributeError
        ]
    else:  # math
        re_codes = [
            f"def {func}(n, *args):\n    return 100 // (n - n)",       # ZeroDivisionError
            f"def {func}(n, *args):\n    import math\n    return math.sqrt(n - 9999)", # ValueError số âm
            f"def {func}(n, *args):\n    return {func}(n - 1) + 1",    # RecursionError
        ]
    return re_codes[(t - 1) % len(re_codes)]


def make_TLE(task: dict) -> str:
    """Tạo mã nguồn lặp vô hạn (Time Limit Exceeded)."""
    func = extract_func_name(task["code"])
    return f"def {func}(*args):\n    i = 0\n    while True:\n        i += 1\n"


def make_HC(task: dict) -> str:
    """
    Tạo mã nguồn cheat cứng (Hard-code).
    Vượt qua 100% public test nhưng sẽ fail trên tất cả hidden test.
    """
    func = extract_func_name(task["code"])
    public_tests = task.get("public_tests", [])
    
    code_lines = [f"def {func}(*args):"]
    # Trích xuất tham số đầu vào và kết quả mong muốn
    for i, test in enumerate(public_tests):
        inp = test["input"]
        expected = test["expected"]
        
        # Tạo câu lệnh rẽ nhánh if/elif cho từng public test
        if i == 0:
            code_lines.append(f"    # Hard-code test case 1")
            code_lines.append(f"    if str(args[0]) == \"{inp}\" or args[0] == {inp}:")
            code_lines.append(f"        return {expected}")
        else:
            code_lines.append(f"    # Hard-code test case {i+1}")
            code_lines.append(f"    elif str(args[0]) == \"{inp}\" or args[0] == {inp}:")
            code_lines.append(f"        return {expected}")
            
    # Kết quả mặc định nếu không khớp public test
    code_lines.append("    # Gia tri mac dinh khi vao hidden test")
    code_lines.append("    return None")
    
    return "\n".join(code_lines)


DESCRIPTIONS = {
    "SE": "Code bi loi cu phap (Syntax Error) truoc khi chay.",
    "WA": "Code chay duoc nhung tra ve ket qua sai (Wrong Answer) vi logic loi.",
    "RE": "Code crash khi chay (Runtime Error) do chia cho 0, loi index, vv.",
    "TLE": "Code lap vo tan gay ra loi qua thoi gian chay (Time Limit Exceeded).",
    "HC": "Code gian lan hard-code chi de qua public test, luon fail hidden test."
}

MAKERS = {
    "SE": make_SE,
    "WA": make_WA,
    "RE": make_RE,
    "TLE": make_TLE,
    "HC": make_HC
}


def generate():
    if not MBPP_FILE.exists():
        print(f"ERROR: Khong tim thay file nguon {MBPP_FILE}")
        return

    with open(MBPP_FILE, encoding="utf-8") as f:
        tasks = json.load(f)

    # Lập lịch xoay vòng 2 loại lỗi trên 50 bài để tạo 100 bài nộp
    # Mỗi task_id sẽ tạo đúng 2 bài nộp mô phỏng (50 task × 2 = 100)
    # Xoay vòng 5 loại lỗi theo từng nhóm 10 task:
    # Task 1-10:  SE, WA
    # Task 11-20: RE, TLE
    # Task 21-30: HC, SE
    # Task 31-40: WA, RE
    # Task 41-50: TLE, HC
    # => Tổng: SE×20, WA×20, RE×20, TLE×20, HC×20 = 100 bài

    submissions = []
    sv_counter = 1

    for task in tasks:
        tid = task["task_id"]
        func_name = extract_func_name(task["code"])

        # Xác định 2 loại lỗi cho task này (xoay vòng 5 cặp qua 50 task)
        if tid <= 10:
            errs = ["SE", "WA"]
        elif tid <= 20:
            errs = ["RE", "TLE"]
        elif tid <= 30:
            errs = ["HC", "SE"]
        elif tid <= 40:
            errs = ["WA", "RE"]
        else:
            errs = ["TLE", "HC"]

        for err in errs:
            code = MAKERS[err](task)
            submissions.append({
                "submission_id": f"SV{sv_counter:03d}",
                "task_id": tid,
                "func_name": func_name,
                "topic": task["topic"],
                "error_type": err,
                "submitted_code": code,
                "note": DESCRIPTIONS[err]
            })
            sv_counter += 1

    os.makedirs(os.path.dirname(OUT_FILE), exist_ok=True)
    with open(OUT_FILE, "w", encoding="utf-8") as f:
        json.dump(submissions, f, ensure_ascii=False, indent=2)

    print(f"OK: Da tao {len(submissions)} bai nop mo phong -> {OUT_FILE}")

    # In phân bố lỗi để kiểm chứng
    counts = Counter(s["error_type"] for s in submissions)
    for k, v in sorted(counts.items()):
        print(f"  {k}: {v} bai nop")

    # In phân bố task_id để kiểm chứng đủ 50 task
    task_ids = sorted(set(s["task_id"] for s in submissions))
    print(f"  Task IDs ({len(task_ids)} tasks): {task_ids[0]} -> {task_ids[-1]}")


if __name__ == "__main__":
    generate()
