"""
runner_v2.py — Test-case runner tuần 3
Cập nhật so với tuần 2:
  + Giới hạn bộ nhớ (memory limit) bằng psutil (hoạt động tốt trên Windows/Linux)
  + Giới hạn file system (chạy trong thư mục tạm riêng)
  + Danh sách import và ký tự cấm rõ ràng (AST safety check)
  + Module thống kê lỗi tự động theo task
  + Ghi log chi tiết và đầy đủ traceback
"""

import subprocess, sys, os, json, time, ast, textwrap, tempfile, shutil, math
import psutil
from typing import Dict, List, Tuple

# ── Cấu hình ─────────────────────────────────────────────────────────────────
TIMEOUT_SECONDS   = 1.0    # 1.0 giây mỗi test case
MAX_OUTPUT_BYTES  = 4096
MEMORY_LIMIT_MB   = 128    # Giới hạn 128MB RAM mỗi test case

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

# ── Kiểm tra bảo mật (AST Safety Check) ───────────────────────────────────────
def check_safety(code: str) -> Tuple[bool, List[str]]:
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return True, [] # Syntax check sẽ bắt lỗi này

    violations = []
    banned_names = {"eval", "exec", "open", "__import__", "getattr", "setattr", "compile", "globals", "locals"}
    
    for node in ast.walk(tree):
        # 1. Kiểm tra Import
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.name.split('.')[0]
                if name in BANNED_IMPORTS:
                    violations.append(f"Import cấm '{name}' (Dòng {node.lineno}): {BANNED_IMPORTS[name]}")
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                name = node.module.split('.')[0]
                if name in BANNED_IMPORTS:
                    violations.append(f"Import cấm '{name}' (Dòng {node.lineno}): {BANNED_IMPORTS[name]}")
        
        # 2. Kiểm tra các hàm và biến cấm hoặc chứa double-underscore
        elif isinstance(node, ast.Name):
            if node.id in banned_names:
                violations.append(f"Hàm/Từ khóa bị cấm '{node.id}' (Dòng {node.lineno})")
            elif "__" in node.id:
                violations.append(f"Không được sử dụng từ khóa có gạch dưới kép '__' trong tên biến/hàm '{node.id}' (Dòng {node.lineno})")
                
        # 3. Thuộc tính cấm (e.g. obj.__class__)
        elif isinstance(node, ast.Attribute):
            if "__" in node.attr:
                violations.append(f"Không được truy cập thuộc tính gạch dưới kép '{node.attr}' (Dòng {node.lineno})")
                
    return len(violations) == 0, violations

# ── Hỗ trợ so sánh cấu trúc chứa Floats ───────────────────────────────────────
def compare_structures(val1, val2) -> bool:
    if isinstance(val1, (int, float)) and isinstance(val2, (int, float)):
        return math.isclose(float(val1), float(val2), rel_tol=1e-9, abs_tol=1e-9)
    if type(val1) != type(val2):
        return False
    if isinstance(val1, (list, tuple)):
        if len(val1) != len(val2):
            return False
        return all(compare_structures(x, y) for x, y in zip(val1, val2))
    if isinstance(val1, dict):
        if len(val1) != len(val2):
            return False
        for k in val1:
            if k not in val2:
                return False
            if not compare_structures(val1[k], val2[k]):
                return False
        return True
    return val1 == val2

def _compare(actual: str, expected: str) -> bool:
    a, e = actual.strip(), expected.strip()
    if a == e:
        return True
    # Thử so sánh số thực đơn giản
    try:
        return math.isclose(float(a), float(e), rel_tol=1e-9, abs_tol=1e-9)
    except (ValueError, TypeError):
        pass
    # Thử eval cấu trúc phức tạp (list, dict, tuple)
    try:
        av, ev = eval(a), eval(e)
        return compare_structures(av, ev)
    except Exception:
        pass
    return False

# ── Chạy một test case ────────────────────────────────────────────────────────
def run_single_test(code: str, func_name: str,
                    test_input: str, expected: str,
                    use_tempdir: bool = True) -> Dict:
    # Đoạn script chạy test case cụ thể
    script = textwrap.dedent(f"""
import sys
{code}

try:
    result = {func_name}({test_input})
    print(result)
except MemoryError:
    print("MEMORY_LIMIT_EXCEEDED", file=sys.stderr)
    sys.exit(2)
except Exception as e:
    import traceback
    traceback.print_exc(file=sys.stderr)
    sys.exit(1)
""")

    tmpdir = None
    start = time.perf_counter()
    tle_triggered = False
    mle_triggered = False
    stdout = ""
    stderr = ""
    latency = 0.0

    try:
        if use_tempdir:
            tmpdir = tempfile.mkdtemp(prefix="runner_")
        
        # Ghi script ra file thay vì dùng -c để có traceback đẹp và chính xác hơn
        script_path = os.path.join(tmpdir if tmpdir else ".", "solution.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script)

        # Chạy python với cờ -X utf8 để đồng bộ encoding
        proc = subprocess.Popen(
            [sys.executable, "-X", "utf8", "solution.py"],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            cwd=tmpdir if tmpdir else "."
        )

        try:
            p = psutil.Process(proc.pid)
        except psutil.NoSuchProcess:
            p = None

        while True:
            # Kiểm tra trạng thái tiến trình
            ret = proc.poll()
            if ret is not None:
                break

            # Kiểm tra Timeout (1.0s)
            elapsed = time.perf_counter() - start
            if elapsed > TIMEOUT_SECONDS:
                tle_triggered = True
                proc.kill()
                break

            # Kiểm tra Memory (128MB)
            if p is not None:
                try:
                    total_rss = p.memory_info().rss
                    for child in p.children(recursive=True):
                        try:
                            total_rss += child.memory_info().rss
                        except (psutil.NoSuchProcess, psutil.AccessDenied):
                            pass
                    rss_mb = total_rss / (1024 * 1024)
                    if rss_mb > MEMORY_LIMIT_MB:
                        mle_triggered = True
                        for child in p.children(recursive=True):
                            try:
                                child.kill()
                            except Exception:
                                pass
                        proc.kill()
                        break
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    pass
            time.sleep(0.005)

        stdout, stderr = proc.communicate()
        latency = round(time.perf_counter() - start, 4)

        if tle_triggered:
            return {
                "status": "TLE",
                "actual": None,
                "expected": expected,
                "latency": latency,
                "error_msg": f"Time Limit Exceeded (>{TIMEOUT_SECONDS}s)"
            }

        if mle_triggered or proc.returncode == 2 or "MEMORY_LIMIT_EXCEEDED" in stderr:
            return {
                "status": "MLE",
                "actual": None,
                "expected": expected,
                "latency": latency,
                "error_msg": f"Memory Limit Exceeded (>{MEMORY_LIMIT_MB}MB)"
            }

        if proc.returncode != 0:
            return {
                "status": "RE",
                "actual": None,
                "expected": expected,
                "latency": latency,
                "error_msg": stderr.strip()  # Giữ nguyên full traceback/stderr
            }

        actual = stdout.strip()
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

    except Exception as e:
        latency = round(time.perf_counter() - start, 4)
        return {
            "status": "RE",
            "actual": None,
            "expected": expected,
            "latency": latency,
            "error_msg": f"Runner Internal Error: {str(e)}"
        }
    finally:
        if tmpdir and os.path.exists(tmpdir):
            shutil.rmtree(tmpdir, ignore_errors=True)

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
        "error_counts": {"SE": 0, "WA": 0, "RE": 0, "TLE": 0, "MLE": 0},
        "total_latency": 0.0,
        "avg_latency": 0.0,
    }

    # 1. Kiểm tra lỗi cú pháp
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

    # 2. Kiểm tra bảo mật
    safe, violations = check_safety(code)
    if not safe:
        result["syntax_ok"] = False
        result["error_counts"]["SE"] = len(tests) # Vi phạm bảo mật coi như lỗi SE
        result["test_results"] = [
            {"status": "SE", "actual": None, "expected": t["expected"],
             "latency": 0.0, "error_msg": f"Security Violation: {'; '.join(violations)}", "input": t["input"]}
            for t in tests
        ]
        result["banned_imports"] = [{"module": v, "reason": "AST Security Violation", "line": 0} for v in violations]
        return result

    # 3. Chạy từng test case
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

# ── Tính Public Test Leakage ──────────────────────────────────────────────────
def compute_leakage(public_result: Dict, hidden_result: Dict) -> Dict:
    pub_all_pass = public_result["pass_count"] == public_result["total_count"]
    hid_all_pass = hidden_result["pass_count"] == hidden_result["total_count"]
    return {
        "public_pass_all": pub_all_pass,
        "hidden_pass_all": hid_all_pass,
        "is_public_test_leakage": pub_all_pass and not hid_all_pass,
        "public_rate": public_result["test_pass_rate"],
        "hidden_rate": hidden_result["test_pass_rate"],
    }

def compute_fpr(public_result: Dict, hidden_result: Dict) -> Dict:
    leakage = compute_leakage(public_result, hidden_result)
    return {
        "public_pass_all": leakage["public_pass_all"],
        "hidden_pass_all": leakage["hidden_pass_all"],
        "is_false_positive": leakage["is_public_test_leakage"],
        "public_rate": leakage["public_rate"],
        "hidden_rate": leakage["hidden_rate"],
    }
