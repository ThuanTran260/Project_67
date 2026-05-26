"""
diff_testing.py — Property-based Differential Testing
Tự động sinh ngẫu nhiên 50+ test cases dựa trên topic để đối chiếu tính đúng đắn giữa Solution gốc và Bài nộp.
Nhóm 67 | Tuần 4
"""

import random
import string
import sys
import os
from typing import Dict, List, Tuple, Any

# Thêm src vào path để import runner
BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(BASE, 'src'))
from runner_v3 import run_single_test_process

def generate_random_inputs(func_name: str, topic: str, count: int = 50) -> List[str]:
    """Sinh ngẫu nhiên các input phù hợp với tên hàm và chủ đề."""
    inputs = []
    
    # 1. Các hàm đặc biệt cần input đặc thù
    if func_name == "factorial" or func_name == "fibonacci" or func_name == "is_prime" or func_name == "is_perfect":
        # Cần số nguyên không âm
        inputs.append("0")
        inputs.append("1")
        inputs.append("2")
        for _ in range(count - 3):
            n = random.randint(0, 100)
            inputs.append(str(n))
        return inputs
        
    if func_name == "is_even":
        for _ in range(count):
            inputs.append(str(random.randint(-1000, 1000)))
        return inputs
        
    if func_name in ["power", "gcd", "lcm"]:
        # Cần 2 tham số số nguyên
        for _ in range(count):
            a = random.randint(1, 100)
            b = random.randint(1, 15) if func_name == "power" else random.randint(1, 100)
            inputs.append(f"{a}, {b}")
        return inputs

    if func_name == "count_char":
        # Cần chuỗi và ký tự
        for _ in range(count):
            s_len = random.randint(0, 20)
            s = "".join(random.choices(string.ascii_lowercase + " ", k=s_len))
            c = random.choice(string.ascii_lowercase + " ")
            inputs.append(f'"{s}", "{c}"')
        return inputs

    if func_name == "is_anagram":
        # Cần 2 chuỗi
        for _ in range(count):
            if random.random() < 0.4:
                # Tạo anagram thực sự
                s1_list = random.choices(string.ascii_lowercase, k=random.randint(1, 10))
                s2_list = s1_list.copy()
                random.shuffle(s2_list)
                s1 = "".join(s1_list)
                s2 = "".join(s2_list)
            else:
                s1 = "".join(random.choices(string.ascii_lowercase, k=random.randint(1, 10)))
                s2 = "".join(random.choices(string.ascii_lowercase, k=random.randint(1, 10)))
            inputs.append(f'"{s1}", "{s2}"')
        return inputs

    if func_name == "rotate_right" or func_name == "first_n" or func_name == "last_n" or func_name == "get_first_n":
        # Cần danh sách và số nguyên k
        for _ in range(count):
            lst = [random.randint(-50, 100) for _ in range(random.randint(0, 15))]
            k = random.randint(0, len(lst) + 2) if lst else 0
            inputs.append(f"{lst}, {k}")
        return inputs

    if func_name in ["merge_lists", "interleave", "intersection", "find_common_elements"]:
        # Cần 2 danh sách
        for _ in range(count):
            lst1 = [random.randint(-10, 20) for _ in range(random.randint(0, 10))]
            lst2 = [random.randint(-10, 20) for _ in range(random.randint(0, 10))]
            inputs.append(f"{lst1}, {lst2}")
        return inputs

    # 2. Sinh theo chủ đề chung
    if topic == "list":
        # Trả về các danh sách số nguyên ngẫu nhiên
        inputs.append("[]") # Trường hợp biên
        inputs.append("[0]")
        for _ in range(count - 2):
            lst_len = random.randint(1, 30)
            lst = [random.randint(-100, 100) for _ in range(lst_len)]
            inputs.append(str(lst))
            
    elif topic == "string":
        # Trả về các chuỗi ngẫu nhiên
        inputs.append('""') # Biên
        inputs.append('"   "') # Chuỗi khoảng trắng
        for _ in range(count - 2):
            s_len = random.randint(1, 40)
            # Thêm khoảng trắng đan xen để kiểm tra logic word count/trim
            chars = string.ascii_letters + string.digits + "   "
            s = "".join(random.choices(chars, k=s_len))
            inputs.append(f'"{s}"')
            
    elif topic == "math":
        # Mặc định là số nguyên ngẫu nhiên hoặc list số nguyên tùy thuộc tên hàm
        for _ in range(count):
            inputs.append(str(random.randint(-100, 1000)))
            
    else:
        # Dự phòng
        for _ in range(count):
            inputs.append("[]")
            
    return inputs

def run_differential_testing(student_code: str, standard_code: str, 
                             func_name: str, topic: str, 
                             test_count: int = 50) -> Tuple[bool, str, Dict]:
    """
    Chạy so sánh song song giữa bài làm của sinh viên và solution mẫu trên test case sinh tự động.
    Trả về: (Passed?, message_chi_tiet, thong_tin_failed_case)
    """
    inputs = generate_random_inputs(func_name, topic, test_count)
    
    for idx, inp in enumerate(inputs):
        # 1. Chạy mã nguồn chuẩn trước để lấy expected output chính xác
        std_res = run_single_test_process(standard_code, func_name, inp, expected="")
        
        # Nếu standard code bị crash trên input sinh ngẫu nhiên, bỏ qua input đó (do input không hợp lệ với hàm)
        if std_res["status"] not in ["PASS", "WA"] and std_res["error_msg"]:
            continue
            
        expected_output = std_res["actual"]
        
        # 2. Chạy bài làm sinh viên với expected output vừa tìm được
        stud_res = run_single_test_process(student_code, func_name, inp, expected=expected_output)
        
        if stud_res["status"] != "PASS":
            # Phát hiện sai lệch (WA) hoặc crash (RE/TLE/MLE)
            error_type = stud_res["status"]
            msg = (
                f"Phát hiện lỗi ở test case tự động #{idx + 1} (Input: {inp}):\n"
                f"  - Trạng thái bài làm: {error_type}\n"
                f"  - Kết quả chuẩn mong đợi: {expected_output}\n"
                f"  - Kết quả bài làm của bạn: {stud_res['actual'] if stud_res['actual'] is not None else 'N/A'}\n"
                f"  - Chi tiết: {stud_res['error_msg']}"
            )
            return False, msg, {
                "test_case_index": idx + 1,
                "input": inp,
                "expected": expected_output,
                "actual": stud_res["actual"],
                "status": error_type,
                "error_msg": stud_res["error_msg"]
            }
            
    return True, "Passed all generated differential tests.", {}
