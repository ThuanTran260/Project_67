"""
runner.py — Test-case runner cho hệ thống chấm bài Python tự động
Nhóm 67 | Tuần 2 | Ngôn ngữ lập trình Python

Cơ chế:
  - Nhận bài nộp Python (.py hoặc code string)
  - Chạy từng test case qua subprocess với timeout
  - Phân loại lỗi: SE / WA / RE / TLE
  - Tính Test Pass Rate và ghi nhận kết quả
"""

import subprocess, sys, os, json, time, ast, textwrap
from typing import Dict, List, Tuple

# ─── Cấu hình ────────────────────────────────────────────────
TIMEOUT_SECONDS = 5      # giới hạn thời gian mỗi test
MAX_OUTPUT_BYTES = 4096  # giới hạn output


# ─── Kiểm tra syntax tĩnh trước khi chạy ────────────────────
def check_syntax(code: str) -> Tuple[bool, str]:
    """Trả về (True, '') nếu OK, (False, lỗi) nếu có Syntax Error."""
    try:
        ast.parse(code)
        return True, ""
    except SyntaxError as e:
        return False, f"SyntaxError dòng {e.lineno}: {e.msg}"


# ─── Kiểm tra import cấm ─────────────────────────────────────
BANNED_IMPORTS = {"os", "sys", "subprocess", "shutil", "socket",
                  "ctypes", "multiprocessing", "threading"}

def check_banned_imports(code: str) -> Tuple[bool, List[str]]:
    """Trả về (True, []) nếu OK, (False, [thư viện cấm]) nếu vi phạm."""
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return True, []  # syntax error sẽ bị bắt ở bước khác

    banned_found = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.name.split('.')[0]
                if name in BANNED_IMPORTS:
                    banned_found.append(name)
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                name = node.module.split('.')[0]
                if name in BANNED_IMPORTS:
                    banned_found.append(name)
    return len(banned_found) == 0, list(set(banned_found))


# ─── Chạy một test case ──────────────────────────────────────
def run_single_test(code: str, func_name: str,
                    test_input: str, expected: str) -> Dict:
    """
    Chạy một test case, trả về dict kết quả.

    Args:
        code:       mã nguồn Python của sinh viên
        func_name:  tên hàm cần gọi (ví dụ: "sum_list")
        test_input: chuỗi đầu vào (ví dụ: "[1, 2, 3]")
        expected:   đầu ra mong đợi (ví dụ: "6")

    Returns:
        {
          "status": "PASS" | "WA" | "RE" | "TLE" | "SE",
          "actual":  giá trị thực tế,
          "expected": giá trị mong đợi,
          "latency": thời gian chạy (giây),
          "error_msg": mô tả lỗi nếu có
        }
    """
    # Tạo script tạm chạy độc lập
    script = textwrap.dedent(f"""
{code}

import sys
try:
    result = {func_name}({test_input})
    print(result)
except Exception as e:
    print(f"RUNTIME_ERROR: {{type(e).__name__}}: {{e}}", file=sys.stderr)
    sys.exit(1)
""")
    start = time.perf_counter()
    try:
        proc = subprocess.run(
            [sys.executable, "-c", script],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS
        )
        latency = round(time.perf_counter() - start, 4)

        if proc.returncode != 0:
            stderr = proc.stderr.strip()
            return {
                "status": "RE",
                "actual": None,
                "expected": expected,
                "latency": latency,
                "error_msg": stderr[:200]
            }

        actual = proc.stdout.strip()

        # Giới hạn output
        if len(actual) > MAX_OUTPUT_BYTES:
            actual = actual[:MAX_OUTPUT_BYTES]

        # So sánh kết quả
        passed = _compare(actual, expected)
        return {
            "status": "PASS" if passed else "WA",
            "actual": actual,
            "expected": expected,
            "latency": latency,
            "error_msg": "" if passed else f"Mong đợi '{expected}', nhận '{actual}'"
        }

    except subprocess.TimeoutExpired:
        latency = round(time.perf_counter() - start, 4)
        return {
            "status": "TLE",
            "actual": None,
            "expected": expected,
            "latency": latency,
            "error_msg": f"Vượt quá {TIMEOUT_SECONDS}s"
        }


def _compare(actual: str, expected: str) -> bool:
    """So sánh output thực tế và mong đợi, chuẩn hóa trước khi so."""
    a = actual.strip()
    e = expected.strip()
    if a == e:
        return True
    # Thử so sánh giá trị số
    try:
        return float(a) == float(e)
    except (ValueError, TypeError):
        pass
    # Thử eval (cho list, bool...)
    try:
        return eval(a) == eval(e)
    except Exception:
        pass
    return False


# ─── Chấm toàn bộ bài ────────────────────────────────────────
def grade_submission(code: str, func_name: str,
                     tests: List[Dict],
                     test_set_name: str = "public") -> Dict:
    """
    Chấm một bài nộp trên toàn bộ test set.

    Returns: dict kết quả đầy đủ
    """
    result = {
        "func": func_name,
        "test_set": test_set_name,
        "syntax_ok": True,
        "banned_import": [],
        "test_results": [],
        "pass_count": 0,
        "total_count": len(tests),
        "test_pass_rate": 0.0,
        "error_counts": {"SE": 0, "WA": 0, "RE": 0, "TLE": 0},
        "total_latency": 0.0,
        "avg_latency": 0.0,
    }

    # Bước 1: Kiểm tra syntax
    ok, msg = check_syntax(code)
    if not ok:
        result["syntax_ok"] = False
        result["error_counts"]["SE"] = len(tests)
        result["test_results"] = [{
            "status": "SE", "actual": None,
            "expected": t["expected"],
            "latency": 0.0,
            "error_msg": msg,
            "input": t["input"]
        } for t in tests]
        return result

    # Bước 2: Kiểm tra import cấm
    clean, banned = check_banned_imports(code)
    if not clean:
        result["banned_import"] = banned

    # Bước 3: Chạy từng test
    func_name_clean = func_name.strip()
    for test in tests:
        r = run_single_test(code, func_name_clean,
                            test["input"], test["expected"])
        r["input"] = test["input"]
        result["test_results"].append(r)
        if r["status"] == "PASS":
            result["pass_count"] += 1
        else:
            result["error_counts"][r["status"]] += 1
        result["total_latency"] += r["latency"]

    # Bước 4: Tính metric
    n = result["total_count"]
    result["test_pass_rate"] = round(
        result["pass_count"] / n * 100, 2) if n > 0 else 0.0
    result["avg_latency"] = round(
        result["total_latency"] / n, 4) if n > 0 else 0.0

    return result


# ─── Tính FPR ────────────────────────────────────────────────
def compute_fpr(public_result: Dict, hidden_result: Dict) -> Dict:
    """
    Tính False Positive Rate:
    FPR = bài pass toàn bộ public test nhưng fail ít nhất 1 hidden test.

    Trong context này: so sánh kết quả trên 2 bộ test của cùng 1 bài nộp.
    """
    public_all_pass = public_result["pass_count"] == public_result["total_count"]
    hidden_all_pass = hidden_result["pass_count"] == hidden_result["total_count"]

    is_false_positive = public_all_pass and not hidden_all_pass
    return {
        "public_pass_all": public_all_pass,
        "hidden_pass_all": hidden_all_pass,
        "is_false_positive": is_false_positive,
        "public_rate": public_result["test_pass_rate"],
        "hidden_rate": hidden_result["test_pass_rate"],
    }


if __name__ == "__main__":
    # Chạy thử đơn giản
    code = "def sum_list(lst):\n    return sum(lst)"
    tests = [
        {"input": "[1,2,3]", "expected": "6"},
        {"input": "[]",      "expected": "0"},
        {"input": "[-1,-2]", "expected": "-3"},
    ]
    r = grade_submission(code, "sum_list", tests, "demo")
    print(json.dumps(r, ensure_ascii=False, indent=2))
