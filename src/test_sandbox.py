"""
test_sandbox.py - Stress-testing the secure auto-grading sandbox (ASCII safe)
Nhom 67 | Tuan 4
"""

import sys
import os
import unicodedata
from typing import Dict

from pathlib import Path
BASE = str(Path(__file__).resolve().parent.parent)
sys.path.insert(0, os.path.join(BASE, 'src'))

from runner_v3 import grade_submission

def clean_accents(text: str) -> str:
    """Loai bo dau tieng Viet de in ra console Windows khong bi loi encoding."""
    if not text:
        return ""
    # Chuyen tieng Viet co dau sang khong dau
    s1 = u'ÀÁÂÃÈÉÊÌÍÒÓÔÕÙÚÝàáâãèéêìíòóôõùúýĂăĐđĨĩŨũƠơƯưẠạẢảẤấẦầẨẩẪẫẬậẮắẰằẲẳẴẵẬcheckẬẮắẰằẲẳẴẵẶặẸẹẺẻẼẽẾếỀềỂểỄễỆệỊịỌọỎỏỐốỒồỔổỖỗỘộỚớỜờỞởỠỡỢợỤụỦủỨứỪừỬửỮữỰựỲỳỶỷỸỹỵỷỹ'
    s2 = u'AAAAEEEIIOOOOUUYaaaaeeeiioooouuyAaDdIiUuOoUuAaAaAaAaAaAaAaAaAaAaAaAaAaecheckaAaAaAaAaAeAeAeAeAeAeAeAeIiOoOoOoOoOoOoOoOoOoOoOoOoUuUuUuUuUuUuUuYyYyYyyyY'
    map_dict = {ord(c1): c2 for c1, c2 in zip(s1, s2)}
    res = text.translate(map_dict)
    # Loai bo tat ca cac ky tu non-ASCII con lai
    return "".join(c for c in res if ord(c) < 128)

def test_attack(code: str, label: str, expected_status: str) -> bool:
    print(f"\n[STRESS TEST] {clean_accents(label)}:")
    print("-" * 50)
    print("Ma nguon thu nghiem:")
    print(code.strip())
    print("-" * 50)
    
    # 1 test case gia lap
    test_cases = [{"input": "5", "expected": "10"}]
    res = grade_submission(code, "test_func", test_cases, "stress_test")
    
    status = res["test_results"][0]["status"]
    error_msg = res["test_results"][0]["error_msg"]
    
    print(f"Trang thai nhan dien duoc: [{status}]")
    if error_msg:
        clean_msg = clean_accents(error_msg.split(';')[0][:100])
        print(f"Chi tiet thong bao loi: {clean_msg}")
        
    if status == expected_status or (expected_status == "RE" and status in ["IndexError", "ZeroDivisionError", "TypeError", "ValueError", "NameError", "AttributeError", "KeyError"]):
        print("=> KET QUA: DAT YEU CAU (Sandbox phat hien va chan thanh cong!)")
        return True
    else:
        print(f"=> KET QUA: THAT BAI! Mong doi [{expected_status}], Nhan [{status}]")
        return False

def main():
    print("=" * 65)
    print("  BO KIEM THU AN TOAN VA GIOI HAN TAI NGUYEN SANDBOX V3")
    print("=" * 65)
    
    tests = [
        # 1. Tan cong import thu vien cam (os)
        (
            "def test_func(x):\n    import os\n    return os.getcwd()",
            "Tan cong Import thu vien he thong cam (os)",
            "SE"
        ),
        # 2. Tan cong goi open()
        (
            "def test_func(x):\n    with open('dummy.txt', 'w') as f:\n        f.write('hack')\n    return x",
            "Tan cong goi ham ghi tep cam open()",
            "SE"
        ),
        # 3. Tan cong truy cap dunder attribute
        (
            "def test_func(x):\n    return x.__class__.__base__",
            "Tan cong truy cap thuoc tinh gach duoi kep (__class__)",
            "SE"
        ),
        # 4. Tan cong goi eval
        (
            "def test_func(x):\n    eval(\"print('injected')\")\n    return x",
            "Tan cong thuc thi chuoi lenh dong eval()",
            "SE"
        ),
        # 5. Gay loi TLE - vong lap vo han
        (
            "def test_func(x):\n    while True:\n        pass\n    return x",
            "Qua gioi han thoi gian (Time Limit Exceeded - TLE)",
            "TLE"
        ),
        # 6. Gay loi MLE - cap phat 200MB
        (
            "def test_func(x):\n    arr = ' ' * (200 * 1024 * 1024) # 200MB\n    return len(arr)",
            "Qua gioi han bo nho (Memory Limit Exceeded - MLE)",
            "MLE"
        ),
        # 7. Gay loi ZeroDivisionError
        (
            "def test_func(x):\n    return x / 0",
            "Phan loai loi runtime cu the (ZeroDivisionError)",
            "ZeroDivisionError"
        ),
        # 8. Tan cong import subprocess (thuc thi lenh he dieu hanh)
        (
            "def test_func(x):\n    import subprocess\n    subprocess.run(['whoami'], capture_output=True)\n    return x",
            "Tan cong Import subprocess (thuc thi lenh shell)",
            "SE"
        ),
        # 9. Tan cong import socket (ket noi mang)
        (
            "def test_func(x):\n    import socket\n    s = socket.socket()\n    s.connect(('google.com', 80))\n    return x",
            "Tan cong Import socket (ket noi mang ngoai)",
            "SE"
        ),
        # 10. Tan cong bypass whitelist qua importlib
        (
            "def test_func(x):\n    import importlib\n    os = importlib.import_module('os')\n    return os.getcwd()",
            "Tan cong bypass whitelist bang importlib.import_module",
            "SE"
        ),
        # 11. Tan cong import ctypes (truong hop yeu cau thao tac bo nho thap cap)
        (
            "def test_func(x):\n    import ctypes\n    return ctypes.CDLL(None)",
            "Tan cong Import ctypes (thao tac bo nho thap cap)",
            "SE"
        ),
        # 12. Recursion bomb (stack overflow / RecursionError)
        (
            "def test_func(x):\n    return test_func(x + 1)",
            "Recursion bomb (gay tran stack - RecursionError)",
            "RecursionError"
        ),
        # 13. Generator memory bomb (tao iterator vo han roi ep list)
        (
            "def test_func(x):\n    import itertools\n    return list(itertools.repeat(0, 10**9))",
            "Generator memory bomb (list(itertools.repeat) qua lon - MLE/TLE)",
            "MLE"
        ),
    ]
    
    success_count = 0
    for code, label, expected_status in tests:
        if test_attack(code, label, expected_status):
            success_count += 1
            
    print("\n" + "=" * 65)
    print(f"  TONG KET: Vuot qua {success_count}/{len(tests)} bai kiem tra bao mat.")
    print("=" * 65)
    
    if success_count == len(tests):
        print("OK: SANBOX HOAT DONG AN TOAN VA GIOI HAN CO LAP TOT!")
        sys.exit(0)
    else:
        print("ERROR: CO LOI RO RI BAO MAT TRONG SANDBOX!")
        sys.exit(1)

if __name__ == "__main__":
    main()
