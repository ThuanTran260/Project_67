"""
runner_v3.py — Advanced Secure Testrunner (Week 4)
Cải tiến:
  + AST Whitelist check (chỉ cho phép các import an toàn: math, string, re, collections, itertools, functools, json, datetime, typing)
  + Tách lỗi RE thành các Exception cụ thể: IndexError, ZeroDivisionError, TypeError, ValueError, NameError, etc.
  + Cơ chế Early-Exit (Fail-Fast) để tối ưu hóa latency chấm bài
  + Sandbox Docker chính chủ kèm theo bộ Giả lập Docker (Simulated Docker Sandbox) nếu Docker daemon tắt.
"""

import subprocess
import sys
import os
import json
import time
import ast
import textwrap
import tempfile
import shutil
import math
from typing import Dict, List, Tuple

# ── Cấu hình ─────────────────────────────────────────────────────────────────
TIMEOUT_SECONDS   = 1.0    # 1.0 giây mỗi test case (Process sandbox)
TIMEOUT_DOCKER_S  = 5.0    # 5.0 giây cho Docker (1s code + ~4s container overhead)
MAX_OUTPUT_BYTES  = 4096
MEMORY_LIMIT_MB   = 128    # Giới hạn 128MB RAM mỗi test case

# Whitelist các import được phép
ALLOWED_IMPORTS = {
    "math", "string", "re", "collections", "itertools", "functools", "json", "datetime", "typing", "heapq", "operator"
}

# Ký từ cấm cho AST safety check
BANNED_BUILTINS = {
    "eval", "exec", "open", "__import__", "globals", "locals", "compile", "getattr", "setattr"
}

# ── Kiểm tra syntax tĩnh ──────────────────────────────────────────────────────
def check_syntax(code: str) -> Tuple[bool, str]:
    try:
        ast.parse(code)
        return True, ""
    except SyntaxError as e:
        return False, f"SyntaxError dòng {e.lineno}: {e.msg}"

# ── Kiểm tra bảo mật (AST Safety Check - Whitelist) ───────────────────────────
def check_safety(code: str) -> Tuple[bool, List[str]]:
    try:
        tree = ast.parse(code)
    except SyntaxError:
        return True, []

    violations = []
    
    for node in ast.walk(tree):
        # 1. Kiểm tra Import dựa trên Whitelist
        if isinstance(node, ast.Import):
            for alias in node.names:
                name = alias.name.split('.')[0]
                if name not in ALLOWED_IMPORTS:
                    violations.append(f"Import cấm '{name}' không có trong whitelist (Dòng {node.lineno})")
        elif isinstance(node, ast.ImportFrom):
            if node.module:
                name = node.module.split('.')[0]
                if name not in ALLOWED_IMPORTS:
                    violations.append(f"Import cấm '{name}' không có trong whitelist (Dòng {node.lineno})")
        
        # 2. Kiểm tra các hàm built-in bị cấm
        elif isinstance(node, ast.Name):
            if node.id in BANNED_BUILTINS:
                violations.append(f"Hàm/Từ khóa bị cấm '{node.id}' (Dòng {node.lineno})")
            elif "__" in node.id:
                violations.append(f"Không được sử dụng từ khóa có gạch dưới kép '__' trong tên biến/hàm '{node.id}' (Dòng {node.lineno})")
                
        # 3. Thuộc tính cấm (e.g. obj.__class__)
        elif isinstance(node, ast.Attribute):
            if "__" in node.attr:
                violations.append(f"Không được truy cập thuộc tính gạch dưới kép '{node.attr}' (Dòng {node.lineno})")
                
    return len(violations) == 0, violations

# ── Trích xuất loại exception cụ thể ──────────────────────────────────────────
def get_exception_type(stderr_msg: str) -> str:
    if not stderr_msg:
        return "RE"
    
    lines = [line.strip() for line in stderr_msg.strip().split('\n') if line.strip()]
    if not lines:
        return "RE"
        
    known_exceptions = [
        "IndexError", "ZeroDivisionError", "TypeError", "ValueError", 
        "NameError", "AttributeError", "KeyError", "SyntaxError", 
        "RecursionError", "OverflowError", "ModuleNotFoundError"
    ]
    
    # Check the last line first (standard Python format "ErrorType: message")
    last_line = lines[-1]
    if ":" in last_line:
        parts = last_line.split(":", 1)
        exc_name = parts[0].strip()
        if exc_name in known_exceptions:
            return exc_name
            
    # Fallback: scan all lines from the end
    for line in reversed(lines):
        for exc in known_exceptions:
            if line.startswith(exc):
                return exc
                
    return "RE"

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
    actual_clean = actual.strip()
    expected_clean = expected.strip()
    
    if actual_clean == expected_clean:
        return True
        
    # Thử so sánh sau khi bỏ các dấu nháy thừa của chuỗi ở expected
    # Ví dụ expected là "'Varsha'" hoặc '"Varsha"'
    if (expected_clean.startswith("'") and expected_clean.endswith("'")) or \
       (expected_clean.startswith('"') and expected_clean.endswith('"')):
        unquoted_expected = expected_clean[1:-1]
        if actual_clean == unquoted_expected:
            return True
            
    # Thử so sánh số thực đơn giản
    try:
        return math.isclose(float(actual_clean), float(expected_clean), rel_tol=1e-9, abs_tol=1e-9)
    except (ValueError, TypeError):
        pass
        
    # Thử literal_eval cấu trúc phức tạp
    try:
        import ast
        ev_val = ast.literal_eval(expected_clean)
        try:
            av_val = ast.literal_eval(actual_clean)
        except Exception:
            av_val = actual_clean
            
        return compare_structures(av_val, ev_val)
    except Exception:
        pass
        
    return False


# ── Chạy một test case (Process-Based / Host Sandbox) ─────────────────────────
def run_single_test_process(code: str, func_name: str,
                            test_input: str, expected: str,
                            use_tempdir: bool = True) -> Dict:
    import psutil
    
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
        
        script_path = os.path.join(tmpdir if tmpdir else ".", "solution.py")
        with open(script_path, "w", encoding="utf-8") as f:
            f.write(script)

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
            ret = proc.poll()
            if ret is not None:
                break

            elapsed = time.perf_counter() - start
            if elapsed > TIMEOUT_SECONDS:
                tle_triggered = True
                proc.kill()
                break

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
            exc_type = get_exception_type(stderr)
            return {
                "status": exc_type,
                "actual": None,
                "expected": expected,
                "latency": latency,
                "error_msg": stderr.strip()
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

# ── Chạy bằng Docker thật hoặc Giả lập Docker Sandbox ─────────────────────────
def is_docker_available() -> bool:
    try:
        # Chạy thử docker info để kiểm tra daemon
        res = subprocess.run(["docker", "info"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=2)
        return res.returncode == 0
    except Exception:
        return False

def run_single_test_docker(code: str, func_name: str,
                           test_input: str, expected: str) -> Dict:
    # Nếu không có Docker, chuyển ngay sang Giả lập Docker
    if not is_docker_available():
        # Giả lập Docker bằng cách chạy Process Sandbox nhưng log dạng Docker Container
        res = run_single_test_process(code, func_name, test_input, expected)
        # Thêm flag đánh dấu Giả lập
        res["docker_mode"] = "Simulated Docker Container (Alpine-Python)"
        return res
        
    # Nếu có Docker chính chủ:
    tmpdir = tempfile.mkdtemp(prefix="docker_runner_")
    start = time.perf_counter()
    try:
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
        with open(os.path.join(tmpdir, "solution.py"), "w", encoding="utf-8") as f:
            f.write(script)
            
        # Chạy trong container docker nhẹ alpine
        # Giới hạn RAM bằng cờ docker -m và CPU bằng cờ timeout của host
        cmd = [
            "docker", "run", "--rm",
            "-v", f"{os.path.abspath(tmpdir)}:/app",
            "-w", "/app",
            "-m", f"{MEMORY_LIMIT_MB}m",
            "python:3.10-alpine",
            "python", "solution.py"
        ]
        
        proc = subprocess.run(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=TIMEOUT_DOCKER_S  # Bao gồm cả thời gian khởi động container
        )
        
        latency = round(time.perf_counter() - start, 4)
        
        if proc.returncode == 137: # OOM (Out Of Memory) trong Docker trả về exit code 137
            return {
                "status": "MLE",
                "actual": None,
                "expected": expected,
                "latency": latency,
                "docker_mode": "Official Docker Container (Alpine-Python)",
                "error_msg": "Container killed by Docker OOM (Out Of Memory) limit"
            }
            
        if proc.returncode != 0:
            exc_type = get_exception_type(proc.stderr)
            return {
                "status": exc_type,
                "actual": None,
                "expected": expected,
                "latency": latency,
                "docker_mode": "Official Docker Container (Alpine-Python)",
                "error_msg": proc.stderr.strip()
            }
            
        actual = proc.stdout.strip()
        passed = _compare(actual, expected)
        return {
            "status": "PASS" if passed else "WA",
            "actual": actual,
            "expected": expected,
            "latency": latency,
            "docker_mode": "Official Docker Container (Alpine-Python)",
            "error_msg": "" if passed else f"Expected '{expected}', got '{actual}'"
        }
        
    except subprocess.TimeoutExpired:
        latency = round(time.perf_counter() - start, 4)
        return {
            "status": "TLE",
            "actual": None,
            "expected": expected,
            "latency": latency,
            "docker_mode": "Official Docker Container (Alpine-Python)",
            "error_msg": f"Time Limit Exceeded in Docker Container (>{TIMEOUT_SECONDS}s code limit)"
        }
    except Exception as e:
        latency = round(time.perf_counter() - start, 4)
        return {
            "status": "RE",
            "actual": None,
            "expected": expected,
            "latency": latency,
            "docker_mode": "Official Docker Container (Alpine-Python)",
            "error_msg": f"Docker execution error: {str(e)}"
        }
    finally:
        shutil.rmtree(tmpdir, ignore_errors=True)

# ── Hàm chấm điểm tổng hợp (hỗ trợ fail_fast & docker) ─────────────────────────
def grade_submission(code: str, func_name: str,
                     tests: List[Dict],
                     test_set_name: str = "public",
                     fail_fast: bool = False,
                     use_docker: bool = False) -> Dict:
    result = {
        "func": func_name,
        "test_set": test_set_name,
        "syntax_ok": True,
        "banned_imports": [],
        "test_results": [],
        "pass_count": 0,
        "total_count": len(tests),
        "test_pass_rate": 0.0,
        "error_counts": {
            "SE": 0, "WA": 0, "RE": 0, "TLE": 0, "MLE": 0,
            "IndexError": 0, "ZeroDivisionError": 0, "TypeError": 0, 
            "ValueError": 0, "NameError": 0, "AttributeError": 0, 
            "KeyError": 0, "SyntaxError": 0, "RecursionError": 0, "SKIPPED": 0
        },
        "total_latency": 0.0,
        "avg_latency": 0.0,
        "early_exited": False
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
        result["error_counts"]["SE"] = len(tests)
        result["test_results"] = [
            {"status": "SE", "actual": None, "expected": t["expected"],
             "latency": 0.0, "error_msg": f"Security Violation: {'; '.join(violations)}", "input": t["input"]}
            for t in tests
        ]
        result["banned_imports"] = [{"module": v, "reason": "AST Security Violation", "line": 0} for v in violations]
        return result

    # 3. Chạy từng test case
    exited_early = False
    for idx, test in enumerate(tests):
        if exited_early:
            # Gắn nhãn SKIPPED cho các test case còn lại nếu fail_fast kích hoạt
            r = {
                "status": "SKIPPED",
                "actual": None,
                "expected": test["expected"],
                "latency": 0.0,
                "error_msg": "Skipped due to fail-fast early-exit",
                "input": test["input"]
            }
            result["test_results"].append(r)
            result["error_counts"]["SKIPPED"] += 1
            continue
            
        # Chọn runner
        if use_docker:
            r = run_single_test_docker(code, func_name.strip(), test["input"], test["expected"])
        else:
            r = run_single_test_process(code, func_name.strip(), test["input"], test["expected"])
            
        r["input"] = test["input"]
        result["test_results"].append(r)
        result["total_latency"] += r["latency"]
        
        if r["status"] == "PASS":
            result["pass_count"] += 1
        else:
            status = r["status"]
            # Nếu là exception cụ thể, ghi nhận
            if status in result["error_counts"]:
                result["error_counts"][status] += 1
            else:
                result["error_counts"]["RE"] += 1
                
            if fail_fast:
                exited_early = True
                result["early_exited"] = True

    n = result["total_count"]
    # Số test thực tế đã chạy
    run_count = sum(1 for r in result["test_results"] if r["status"] != "SKIPPED")
    result["test_pass_rate"] = round(result["pass_count"] / n * 100, 2) if n > 0 else 0.0
    result["avg_latency"] = round(result["total_latency"] / run_count, 4) if run_count > 0 else 0.0
    return result

# ── Tính Public Test Leakage / FPR ────────────────────────────────────────────
def compute_leakage(public_result: Dict, hidden_result: Dict) -> Dict:
    pub_all_pass = public_result["pass_count"] == public_result["total_count"]
    # Nếu public pass hết nhưng hidden bị fail bất kỳ test nào (kể cả skipped/error)
    hid_all_pass = hidden_result["pass_count"] == hidden_result["total_count"]
    return {
        "public_pass_all": pub_all_pass,
        "hidden_pass_all": hid_all_pass,
        "is_public_test_leakage": pub_all_pass and not hid_all_pass,
        "public_rate": public_result["test_pass_rate"],
        "hidden_rate": hidden_result["test_pass_rate"],
    }
