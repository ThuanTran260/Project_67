import json
import os
import re
import ast
import random
import string
import urllib.request
import math
import cmath
import heapq
import collections
from collections import Counter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_TASKS_FILE = os.path.join(BASE, 'data', 'raw', 'mbpp_50.json')
RAW_SUBMISSIONS_FILE = os.path.join(BASE, 'data', 'raw', 'submissions_50.json')

def is_dangerous_or_recursive(code_str, func_name):
    try:
        tree = ast.parse(code_str)
        func_def = None
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef) and node.name == func_name:
                func_def = node
                break
        if not func_def:
            return True # if function definition not found, treat as unsafe
            
        # Check for recursive calls or while loops or sys.maxsize
        for node in ast.walk(func_def):
            if isinstance(node, ast.While):
                return True
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == func_name:
                return True
            if isinstance(node, ast.Attribute) and node.attr == "maxsize":
                return True
    except Exception:
        return True
    return False

def classify_task(prompt, code):
    prompt = prompt.lower()
    
    list_keywords = ["list", "array", "tuple", "matrix", "nested", "similar_elements", "sequence", "sublist", "dictionaries", "dictionary", "freq_count", "subject_marks", "recursive_list_sum", "comb_sort"]
    string_keywords = ["string", "character", "vowel", "regex", "lowercase", "uppercase", "anagram", "palindrome", "words", "sentence", "text", "binary string"]
    math_keywords = ["number", "integer", "prime", "math", "sum", "product", "divisible", "power", "square", "gcd", "lcm", "volume", "perimeter", "area", "octagonal", "tetrahedral", "fibonacci", "factorial", "woodall", "amicable", "centered", "eulerian", "divisor", "angle", "binary equivalent"]
    
    list_score = sum(1 for kw in list_keywords if kw in prompt)
    string_score = sum(1 for kw in string_keywords if kw in prompt)
    math_score = sum(1 for kw in math_keywords if kw in prompt)
    
    if "import math" in code or "import cmath" in code:
        math_score += 3
    if "import re" in code:
        string_score += 3
    if "import heapq" in code or "collections.Counter" in code or "collections" in code:
        list_score += 2
        
    if list_score == 0 and string_score == 0 and math_score == 0:
        return "list"
        
    max_score = max(list_score, string_score, math_score)
    if max_score == list_score:
        return "list"
    elif max_score == math_score:
        return "math"
    else:
        return "string"

def extract_func_name(code_str):
    try:
        tree = ast.parse(code_str)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                return node.name
    except Exception:
        pass
    return None

def parse_assert(assert_str, func_name):
    try:
        tree = ast.parse(assert_str)
        if not isinstance(tree.body[0], ast.Assert):
            return None
        test_node = tree.body[0].test
        if not isinstance(test_node, ast.Compare):
            return None
        
        left_node = test_node.left
        call_node = None
        for node in ast.walk(left_node):
            if isinstance(node, ast.Call) and isinstance(node.func, ast.Name) and node.func.id == func_name:
                call_node = node
                break
        if not call_node:
            for node in ast.walk(left_node):
                if isinstance(node, ast.Call):
                    for arg in node.args:
                        if isinstance(arg, ast.Call) and isinstance(arg.func, ast.Name) and arg.func.id == func_name:
                            call_node = arg
                            break
                if call_node:
                    break
                    
        if not call_node:
            return None
            
        args_unparsed = [ast.unparse(arg) for arg in call_node.args]
        return args_unparsed
    except Exception:
        return None

def generate_mutated_inputs(base_inputs, num_needed):
    mutated = []
    try:
        evaluated_base = []
        for inp_list in base_inputs:
            evaluated_base.append([eval(arg) for arg in inp_list])
    except Exception:
        for i in range(num_needed):
            base = random.choice(base_inputs)
            new_inp = []
            for arg in base:
                if arg.isdigit():
                    new_inp.append(str(int(arg) + random.randint(1, 10)))
                elif arg.startswith("'") or arg.startswith('"'):
                    new_inp.append(arg[:-1] + "x" + arg[-1])
                else:
                    new_inp.append(arg)
            mutated.append(new_inp)
        return mutated

    for idx in range(num_needed):
        new_args = []
        base_case = random.choice(evaluated_base)
        for arg in base_case:
            if isinstance(arg, int):
                new_args.append(random.randint(1, 20)) # small values to avoid TLE/overflow
            elif isinstance(arg, float):
                new_args.append(round(random.uniform(1.0, 20.0), 2))
            elif isinstance(arg, str):
                chars = string.ascii_letters
                new_str = "".join(random.choice(chars) for _ in range(random.randint(3, 8)))
                new_args.append(new_str)
            elif isinstance(arg, list):
                if len(arg) > 0:
                    el_type = type(arg[0])
                else:
                    el_type = int
                size = random.randint(1, 8)
                if el_type == int:
                    new_list = [random.randint(1, 50) for _ in range(size)]
                elif el_type == str:
                    new_list = ["".join(random.choice(string.ascii_lowercase) for _ in range(3)) for _ in range(size)]
                else:
                    new_list = arg[:]
                new_args.append(new_list)
            elif isinstance(arg, tuple):
                size = random.randint(1, 5)
                new_tup = tuple(random.randint(1, 50) for _ in range(size))
                new_args.append(new_tup)
            else:
                new_args.append(arg)
        mutated.append([repr(x) for x in new_args])
        
    return mutated

def main():
    print("Loading original 50 tasks...", flush=True)
    with open(RAW_TASKS_FILE, 'r', encoding='utf-8') as f:
        orig_tasks = json.load(f)[:50]
    print(f"Loaded {len(orig_tasks)} tasks.", flush=True)
    
    print("Fetching sanitized MBPP dataset from GitHub...", flush=True)
    url = "https://raw.githubusercontent.com/google-research/google-research/master/mbpp/sanitized-mbpp.json"
    try:
        with urllib.request.urlopen(url, timeout=10) as response:
            json_content = response.read().decode('utf-8')
        sanitized_tasks = json.loads(json_content, strict=False)
        print(f"Loaded {len(sanitized_tasks)} tasks from GitHub.", flush=True)
    except Exception as e:
        print(f"Error fetching: {e}. Cannot proceed without MBPP dataset.", flush=True)
        return
    
    used_funcs = set()
    for t in orig_tasks:
        fname = extract_func_name(t['code'])
        if fname:
            used_funcs.add(fname)
            
    candidates = []
    for t in sanitized_tasks:
        code = t['code']
        prompt = t['prompt']
        func_name = extract_func_name(code)
        
        if not func_name:
            continue
        if func_name in used_funcs:
            continue
        if is_dangerous_or_recursive(code, func_name):
            continue
            
        topic = classify_task(prompt, code)
        candidates.append({
            "prompt": prompt,
            "code": code,
            "func_name": func_name,
            "topic": topic,
            "test_list": t['test_list']
        })
        
    print(f"Found {len(candidates)} safe candidate tasks.", flush=True)
    
    target_counts = {"list": 20, "math": 16, "string": 14}
    selected_tasks = {"list": [], "math": [], "string": []}
    
    def translate_prompt(prompt, func_name):
        p = prompt.lower()
        p = p.replace("write a function to ", "")
        p = p.replace("write a python function to ", "")
        p = p.replace("write a function that ", "")
        p = p.replace("write a python function that ", "")
        
        if func_name == "similar_elements":
            return "Tìm các phần tử chung giữa hai danh sách."
        if func_name == "check":
            if "one less than twice its reverse" in p:
                return "Kiểm tra một số có bằng hai lần số đảo ngược của nó trừ 1 hay không."
        if func_name == "find_Max_Num":
            return "Tìm số lớn nhất có thể được tạo ra từ danh sách các chữ số cho trước."
        if func_name == "opposite_Signs":
            return "Kiểm tra xem hai số nguyên cho trước có khác dấu nhau hay không."
        if func_name == "is_octagonal":
            return "Tính số bát giác thứ n trong dãy số bát giác."
        if func_name == "count_Substrings":
            return "Đếm số lượng chuỗi con có tổng các chữ số bằng độ dài của chính chuỗi con đó."
        if func_name == "smallest_num":
            return "Tìm số nhỏ nhất trong một danh sách số cho trước."
        if func_name == "max_difference":
            return "Tìm khoảng cách lớn nhất giữa các cặp số trong một danh sách tuple cho trước."
        if func_name == "subject_marks":
            return "Sắp xếp danh sách các tuple điểm số môn học theo thứ tự điểm tăng dần."
        if func_name == "pos_count":
            return "Đếm số lượng số dương trong một danh sách số nguyên cho trước."
        if func_name == "is_Monotonic":
            return "Kiểm tra xem một danh sách số nguyên cho trước có đơn điệu hay không."
        if func_name == "is_sublist":
            return "Kiểm tra xem một danh sách có chứa danh sách con khác hay không."
        if func_name == "get_equal":
            return "Kiểm tra xem tất cả các tuple trong danh sách có cùng độ dài hay không."
        if func_name == "comb_sort":
            return "Sắp xếp một danh sách các số nguyên bằng thuật toán Comb Sort."
        if func_name == "dif_Square":
            return "Kiểm tra một số có thể biểu diễn dưới dạng hiệu của hai số chính phương không."
        if func_name == "is_samepatterns":
            return "Kiểm tra xem danh sách màu sắc có tuân theo mẫu hình pattern cho trước không."
        if func_name == "find_tuples":
            return "Tìm các tuple trong danh sách có tất cả phần tử chia hết cho số k."
        if func_name == "is_Diff":
            return "Kiểm tra xem một số nguyên cho trước có chia hết cho 11 hay không."
        if func_name == "word_len":
            return "Kiểm tra xem trong chuỗi có từ nào có độ dài lẻ hay không."
        if func_name == "tetrahedral_number":
            return "Tính số tứ diện thứ n trong dãy số tứ diện."
        if func_name == "volume_sphere":
            return "Tính thể tích của hình cầu có bán kính r cho trước."
        if func_name == "get_Char":
            return "Tìm ký tự bằng cách cộng mã ASCII của chuỗi rồi chia lấy dư cho 26."
        if func_name == "centered_hexagonal_number":
            return "Tính số lục giác tâm thứ n trong dãy số lục giác tâm."
        if func_name == "freq_count":
            return "Đếm tần suất xuất hiện của các phần tử trong danh sách và trả về từ điển."
        if func_name == "closest_num":
            return "Tìm số nguyên nhỏ hơn và gần số n nhất."
        if func_name == "len_log":
            return "Tìm độ dài của từ dài nhất trong một danh sách từ cho trước."
        if func_name == "find_substring":
            return "Kiểm tra xem chuỗi con có xuất hiện trong bất kỳ từ nào của danh sách không."
        if func_name == "index_minimum":
            return "Tìm phần tử đầu tiên của tuple có giá trị phần tử thứ hai nhỏ nhất."
        if func_name == "Find_Min_Length":
            return "Tìm độ dài của danh sách con nhỏ nhất trong danh sách các danh sách."
        if func_name == "divisor":
            return "Tìm số lượng các ước số của một số nguyên dương n cho trước."
        if func_name == "frequency_lists":
            return "Đếm tần suất xuất hiện các phần tử trong danh sách lồng nhau phẳng."
        if func_name == "multiply_num":
            return "Tính tích các số trong danh sách rồi chia cho độ dài của danh sách."
        if func_name == "decimal_to_binary":
            return "Chuyển đổi số thập phân cho trước thành chuỗi nhị phân tương ứng."
        if func_name == "kth_element":
            return "Tìm phần tử nhỏ thứ k trong danh sách bằng cách sắp xếp nổi bọt."
        if func_name == "snake_to_camel":
            return "Chuyển đổi chuỗi định dạng snake_case sang định dạng CamelCase."
        if func_name == "sort_sublists":
            return "Sắp xếp các chuỗi con trong danh sách các danh sách theo thứ tự bảng chữ cái."
        if func_name == "count":
            return "Đếm số lượng giá trị True (booleans) trong một danh sách cho trước."
        if func_name == "add_lists":
            return "Thêm các phần tử của một danh sách vào sau một tuple cho trước."
        if func_name == "merge_sorted_list":
            return "Gộp ba danh sách số thành một danh sách duy nhất đã được sắp xếp."
        if func_name == "odd_Equivalent":
            return "Đếm số lượng chuỗi con có giá trị lẻ khi xoay chuỗi nhị phân."
        if func_name == "common_in_nested_lists":
            return "Tìm các phần tử chung xuất hiện trong tất cả các danh sách con lồng nhau."
        if func_name == "check_integer":
            return "Kiểm tra xem một chuỗi cho trước có biểu diễn một số nguyên hợp lệ không."
        if func_name == "empty_dit":
            return "Kiểm tra xem tất cả các từ điển trong danh sách có rỗng hay không."
        if func_name == "tuple_to_int":
            return "Chuyển đổi một tuple các số nguyên dương thành một số nguyên duy nhất."
        if func_name == "list_to_float":
            return "Chuyển đổi các phần tử có thể chuyển đổi trong danh sách lồng nhau sang số thực."
        if func_name == "string_to_list":
            return "Tách một chuỗi thành danh sách các từ dựa trên khoảng trắng."
        if func_name == "search":
            return "Tìm phần tử xuất hiện đúng một lần trong mảng đã được sắp xếp."
        if func_name == "max_product_tuple":
            return "Tìm tích trị tuyệt đối lớn nhất giữa các cặp số trong danh sách tuple."
        if func_name == "find_length":
            return "Tìm hiệu số lớn nhất giữa số chữ số 0 và số chữ số 1 trong chuỗi con."
        
        return "Hãy viết chương trình Python thực hiện chức năng của hàm " + func_name + "."

    for c in candidates:
        topic = c['topic']
        if len(selected_tasks[topic]) >= target_counts[topic]:
            continue
            
        prompt_vi = translate_prompt(c['prompt'], c['func_name'])
        code = c['code']
        func_name = c['func_name']
        test_list = c['test_list']
        
        parsed_inputs = []
        for t in test_list:
            inp = parse_assert(t, func_name)
            if inp:
                parsed_inputs.append(inp)
                
        if len(parsed_inputs) < 3:
            continue
            
        local_scope = {
            "math": math,
            "cmath": cmath,
            "heapq": heapq,
            "re": re,
            "collections": collections,
            "Counter": Counter
        }
        try:
            exec(code, local_scope)
            func = local_scope[func_name]
        except Exception as e:
            print(f"Skipping task {func_name} due to compilation error: {e}", flush=True)
            continue
            
        public_tests = []
        for inp in parsed_inputs[:3]:
            try:
                args_eval = [eval(x, local_scope) for x in inp]
                result = func(*args_eval)
                public_tests.append({
                    "input": ", ".join(inp),
                    "expected": repr(result)
                })
            except Exception as e:
                print(f"Error evaluating test for {func_name} with input {inp}: {e}", flush=True)
                
        if len(public_tests) < 3:
            continue
            
        mutated_args_lists = generate_mutated_inputs(parsed_inputs, 20)
        hidden_tests = []
        for inp in parsed_inputs:
            try:
                args_eval = [eval(x, local_scope) for x in inp]
                result = func(*args_eval)
                hidden_tests.append({
                    "input": ", ".join(inp),
                    "expected": repr(result)
                })
            except Exception:
                pass
                
        for inp in mutated_args_lists:
            if len(hidden_tests) >= 10:
                break
            try:
                args_eval = [eval(x, local_scope) for x in inp]
                result = func(*args_eval)
                hidden_tests.append({
                    "input": ", ".join(inp),
                    "expected": repr(result)
                })
            except Exception:
                pass
                
        while len(hidden_tests) < 10:
            hidden_tests.append(public_tests[0])
            
        selected_tasks[topic].append({
            "prompt_vi": prompt_vi,
            "code": code,
            "func_name": func_name,
            "topic": topic,
            "public_tests": public_tests,
            "hidden_tests": hidden_tests
        })
        
        if len(selected_tasks["list"]) >= target_counts["list"] and \
           len(selected_tasks["math"]) >= target_counts["math"] and \
           len(selected_tasks["string"]) >= target_counts["string"]:
            break
            
    new_tasks = []
    task_idx = 51
    for topic in ["list", "math", "string"]:
        for t in selected_tasks[topic]:
            t["task_id"] = task_idx
            t["text"] = t["prompt_vi"]
            del t["prompt_vi"]
            new_tasks.append(t)
            task_idx += 1
            
    print(f"Successfully generated {len(new_tasks)} new tasks.", flush=True)
    
    combined_tasks = orig_tasks + new_tasks
    print(f"Total tasks in combined dataset: {len(combined_tasks)}", flush=True)
    
    with open(RAW_TASKS_FILE, 'w', encoding='utf-8') as f:
        json.dump(combined_tasks, f, ensure_ascii=False, indent=2)
    print(f"Overwritten: {RAW_TASKS_FILE}", flush=True)
    
    combined_topic_counts = Counter(t['topic'] for t in combined_tasks)
    print(f"Combined topic distribution: {dict(combined_topic_counts)}", flush=True)
    
    print("Generating 50 new submissions SV051 to SV100...", flush=True)
    with open(RAW_SUBMISSIONS_FILE, 'r', encoding='utf-8') as f:
        orig_subs = json.load(f)[:50]
    print(f"Loaded {len(orig_subs)} original submissions.", flush=True)
    
    error_types = (
        ["CE"] * 2 +
        ["MLE"] * 1 +
        ["TLE"] * 1 +
        ["RE"] * 4 +
        ["AC"] * 5 +
        ["WA"] * 37
    )
    random.shuffle(error_types)
    
    new_subs = []
    for idx, t in enumerate(new_tasks):
        sid = f"SV{51 + idx:03d}"
        tid = t['task_id']
        func_name = t['func_name']
        topic = t['topic']
        err = error_types[idx]
        
        orig_code = t['code']
        submitted_code = orig_code
        note = ""
        
        if err == "AC":
            submitted_code = orig_code
            note = f"{func_name} - Solution đúng hoàn toàn"
        elif err == "CE":
            lines = orig_code.split('\n')
            for l_idx, line in enumerate(lines):
                if line.strip().startswith("def "):
                    lines[l_idx] = line.rstrip()[:-1]
                    break
            submitted_code = '\n'.join(lines)
            note = f"Syntax Error - thiếu dấu hoặc lỗi cú pháp trong {func_name}"
        elif err == "TLE":
            lines = orig_code.split('\n')
            indent = "    "
            for line in lines:
                if line.strip().startswith("def "):
                    m = re.match(r"^(\s*)def ", line)
                    if m:
                        indent = m.group(1) + "    "
                    break
            injected_lines = []
            def_found = False
            for line in lines:
                injected_lines.append(line)
                if line.strip().startswith("def ") and not def_found:
                    injected_lines.append(indent + "while True: pass")
                    def_found = True
            submitted_code = '\n'.join(injected_lines)
            note = f"Quá thời gian (TLE) - vòng lặp vô hạn trong {func_name}"
        elif err == "MLE":
            lines = orig_code.split('\n')
            indent = "    "
            for line in lines:
                if line.strip().startswith("def "):
                    m = re.match(r"^(\s*)def ", line)
                    if m:
                        indent = m.group(1) + "    "
                    break
            injected_lines = []
            def_found = False
            for line in lines:
                injected_lines.append(line)
                if line.strip().startswith("def ") and not def_found:
                    injected_lines.append(indent + "x = ' ' * (200 * 1024 * 1024) # 200MB allocation")
                    def_found = True
            submitted_code = '\n'.join(injected_lines)
            note = f"Vượt quá bộ nhớ (MLE) - cấp phát mảng 200MB trong {func_name}"
        elif err == "RE":
            lines = orig_code.split('\n')
            indent = "    "
            for line in lines:
                if line.strip().startswith("def "):
                    m = re.match(r"^(\s*)def ", line)
                    if m:
                        indent = m.group(1) + "    "
                    break
            
            # Xoay tua các loại lỗi RE thực tế khác nhau để đa dạng hóa
            re_payloads = [
                ("x = 1 / 0", "ZeroDivisionError - chia cho 0"),
                ("x = int('abc')", "ValueError - ép kiểu sai"),
                ("x = undefined_variable", "NameError - gọi biến chưa định nghĩa"),
                ("x = None.append(1)", "AttributeError - gọi thuộc tính không tồn tại"),
                ("x = {}['missing']", "KeyError - truy cập key không tồn tại"),
                ("x = [][99]", "IndexError - vượt quá chỉ mục mảng")
            ]
            payload, error_note = re_payloads[idx % len(re_payloads)]
            
            injected_lines = []
            def_found = False
            for line in lines:
                injected_lines.append(line)
                if line.strip().startswith("def ") and not def_found:
                    injected_lines.append(indent + payload)
                    def_found = True
            submitted_code = '\n'.join(injected_lines)
            note = f"Lỗi thực thi (RE) - {error_note} trong {func_name}"
        elif err == "WA":
            if "+" in orig_code:
                submitted_code = orig_code.replace("+", "-")
                note = f"Sai logic - thay đổi dấu cộng thành dấu trừ trong {func_name}"
            elif "-" in orig_code:
                submitted_code = orig_code.replace("-", "+")
                note = f"Sai logic - thay đổi dấu trừ thành dấu cộng trong {func_name}"
            elif ">" in orig_code:
                submitted_code = orig_code.replace(">", "<")
                note = f"Sai logic - thay đổi toán tử so sánh > thành < trong {func_name}"
            elif "==" in orig_code:
                submitted_code = orig_code.replace("==", "!=")
                note = f"Sai logic - thay đổi toán tử so sánh == thành != trong {func_name}"
            else:
                lines = orig_code.split('\n')
                for l_idx, line in enumerate(lines):
                    if "return " in line:
                        indent_m = re.match(r"^(\s*)return", line)
                        indent_str = indent_m.group(1) if indent_m else "    "
                        lines[l_idx] = indent_str + "return None # Buggy return"
                submitted_code = '\n'.join(lines)
                note = f"Sai logic - trả về None thay vì kết quả đúng trong {func_name}"
                
        new_subs.append({
            "submission_id": sid,
            "task_id": tid,
            "func_name": func_name,
            "topic": topic,
            "error_type": (error_note.split()[0] if err == "RE" else err),
            "submitted_code": submitted_code,
            "note": note
        })
        
    combined_subs = orig_subs + new_subs
    print(f"Total submissions in combined dataset: {len(combined_subs)}", flush=True)
    
    with open(RAW_SUBMISSIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(combined_subs, f, ensure_ascii=False, indent=2)
    print(f"Overwritten: {RAW_SUBMISSIONS_FILE}", flush=True)
    
    print("Dataset expansion completed successfully!", flush=True)

if __name__ == '__main__':
    main()
