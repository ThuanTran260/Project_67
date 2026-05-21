"""
runner_v2.py — Test-case runner tuần 3
Cập nhật so với tuần 2:
  + Giới hạn bộ nhớ (memory limit) bằng resource module
  + Giới hạn file system (chạy trong thư mục tạm riêng)
  + Danh sách import cấm rõ ràng hơn, có giải thích
  + Module thống kê lỗi tự động theo task
  + Ghi log chi tiết hơn
"""

import subprocess, sys, os, json, time, ast, textwrap, tempfile, shutil
from typing import Dict, List, Tuple

# ── Cấu hình ─────────────────────────────────────────────────────────────────
TIMEOUT_SECONDS   = 5
MAX_OUTPUT_BYTES  = 4096
MEMORY_LIMIT_MB   = 128    # Mới tuần 3: giới hạn 128MB RAM

# Import cấm và lý do
BANNED_IMPORTS = {
    "os":             "Truy cập hệ thống file và tiến trình",
    "sys":            "Truy cập tham số hệ thống (cho phép sys.stdin nếu cần)",
    "subprocess":     "Chạy lệnh shell tùy ý",
    "socket":         "Kết nối mạng",
    "ctypes":         "Truy cập bộ nhớ thấp",
    "multiprocessing":"Tạo tiến trình mới",
    "threading":      "Tạo luồng mới gây race condition",
    "shutil":         "Sao chép/xóa file hệ thống",
    "pathlib":        "Truy cập đường dẫn hệ thống",
    "glob":           "Liệt kê file hệ thống",
}

# ── Kiểm tra syntax tĩnh ──────────────────────────────────────────────────────
def check_syntax(code: str) -> Tuple[bool, str]:
    try:
        ast.parse(code)
        return True, ""
    except SyntaxError as e:
        return False, f"SyntaxError dòng {e.lineno}: {e.msg}"

# ── Kiểm tra import cấm ───────────────────────────────────────────────────────
def check_banned_imports(code: str) -> Tuple[bool, List[Dict]]:
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return True, []

    violations = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.name.split('.')[0]
                if name in BANNED_IMPORTS:
                    violations.append({
                        "module": name,
                        "reason": BANNED_IMPORTS[name],
                        "line": node.lineno
                    })
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                name = node.module.split('.')[0]
                if name in BANNED_IMPORTS:
                    violations.append({
                        "module": name,
                        "reason": BANNED_IMPORTS[name],
                        "line": node.lineno
                    })
    return len(violations) == 0, violations

# ── Script giới hạn bộ nhớ ───────────────────────────────────────────────────
MEMORY_LIMITER = f"""
try:
    import resource
    mem_bytes = {MEMORY_LIMIT_MB} * 1024 * 1024
    resource.setrlimit(resource.RLIMIT_AS, (mem_bytes, mem_bytes))
except Exception:
    pass  # resource module không khả dụng trên một số OS
"""

# ── Chạy một test case ────────────────────────────────────────────────────────
def run_single_test(code: str, func_name: str,
                    test_input: str, expected: str,
                    use_tempdir: bool = True) -> Dict:
    script = textwrap.dedent(f"""
{MEMORY_LIMITER}
{code}

import sys
try:
    result = {func_name}({test_input})
    print(result)
except Exception as e:
    print(f"RUNTIME_ERROR: {{type(e).__name__}}: {{e}}", file=sys.stderr)
    sys.exit(1)
""")

    tmpdir = None
    start = time.perf_counter()
    try:
        if use_tempdir:
            tmpdir = tempfile.mkdtemp(prefix="runner_")

        proc = subprocess.run(
            [sys.executable, "-c", script],
            capture_output=True,
            text=True,
            timeout=TIMEOUT_SECONDS,
            cwd=tmpdir if tmpdir else "."
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
        if len(actual) > MAX_OUTPUT_BYTES:
            actual = actual[:MAX_OUTPUT_BYTES]

        passed = _compare(actual, expected)
        return {
            "status": "PASS" if passed else "WA",
            "actual": actual,
            "expected": expected,
            "latency": latency,
            "error_msg": "" if passed else f"Expected '{expected}', got '{actual}'"
        }

    except subprocess.TimeoutExpired:
        latency = round(time.perf_counter() - start, 4)
        return {"status": "TLE", "actual": None, "expected": expected,
                "latency": latency, "error_msg": f"Timeout >{TIMEOUT_SECONDS}s"}
    finally:
        if tmpdir and os.path.exists(tmpdir):
            shutil.rmtree(tmpdir, ignore_errors=True)

def _compare(actual: str, expected: str) -> bool:
    a, e = actual.strip(), expected.strip()
    if a == e: return True
    try:
        return float(a) == float(e)
    except (ValueError, TypeError):
        pass
    try:
        av, ev = eval(a), eval(e)
        if isinstance(av, list) and isinstance(ev, list):
            return sorted(av) == sorted(ev) if len(av) == len(ev) else av == ev
        return av == ev
    except Exception:
        pass
    return False

# ── Chấm toàn bộ bài ─────────────────────────────────────────────────────────
def grade_submission(code: str, func_name: str,
                     tests: List[Dict],
                     test_set_name: str = "public") -> Dict:
    result = {
        "func": func_name,
        "test_set": test_set_name,
        "syntax_ok": True,
        "banned_imports": [],
        "test_results": [],
        "pass_count": 0,
        "total_count": len(tests),
        "test_pass_rate": 0.0,
        "error_counts": {"SE": 0, "WA": 0, "RE": 0, "TLE": 0},
        "total_latency": 0.0,
        "avg_latency": 0.0,
    }

    ok, msg = check_syntax(code)
    if not ok:
        result["syntax_ok"] = False
        result["error_counts"]["SE"] = len(tests)
        result["test_results"] = [
            {"status": "SE", "actual": None, "expected": t["expected"],
             "latency": 0.0, "error_msg": msg, "input": t["input"]}
            for t in tests
        ]
        return result

    clean, violations = check_banned_imports(code)
    if not clean:
        result["banned_imports"] = violations

    for test in tests:
        r = run_single_test(code, func_name.strip(), test["input"], test["expected"])
        r["input"] = test["input"]
        result["test_results"].append(r)
        if r["status"] == "PASS":
            result["pass_count"] += 1
        else:
            result["error_counts"][r["status"]] += 1
        result["total_latency"] += r["latency"]

    n = result["total_count"]
    result["test_pass_rate"] = round(result["pass_count"] / n * 100, 2) if n > 0 else 0.0
    result["avg_latency"] = round(result["total_latency"] / n, 4) if n > 0 else 0.0
    return result

# ── Tính FPR ──────────────────────────────────────────────────────────────────
def compute_fpr(public_result: Dict, hidden_result: Dict) -> Dict:
    pub_all_pass = public_result["pass_count"] == public_result["total_count"]
    hid_all_pass = hidden_result["pass_count"] == hidden_result["total_count"]
    return {
        "public_pass_all": pub_all_pass,
        "hidden_pass_all": hid_all_pass,
        "is_false_positive": pub_all_pass and not hid_all_pass,
        "public_rate": public_result["test_pass_rate"],
        "hidden_rate": hidden_result["test_pass_rate"],
    }

# ── Test nhanh ────────────────────────────────────────────────────────────────
if __name__ == "__main__":
    code = "def sum_list(lst):\n    return sum(lst)"
    tests_pub = [
        {"input": "[1,2,3]", "expected": "6"},
        {"input": "[]",      "expected": "0"},
    ]
    tests_hid = [
        {"input": "[-1,-2,-3]", "expected": "-6"},
        {"input": "[0]",        "expected": "0"},
    ]
    r_pub = grade_submission(code, "sum_list", tests_pub, "public")
    r_hid = grade_submission(code, "sum_list", tests_hid, "hidden")
    fpr   = compute_fpr(r_pub, r_hid)

    print(f"Public  : {r_pub['pass_count']}/{r_pub['total_count']} ({r_pub['test_pass_rate']}%)")
    print(f"Hidden  : {r_hid['pass_count']}/{r_hid['total_count']} ({r_hid['test_pass_rate']}%)")
    print(f"FPR     : {fpr['is_false_positive']}")
    print(f"Latency : {r_pub['avg_latency']}s/test")
    print(f"Config  : timeout={TIMEOUT_SECONDS}s, memory={MEMORY_LIMIT_MB}MB")
