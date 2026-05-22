import json
import os
import sys

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
HIDDEN_FILE = os.path.join(BASE, 'data', 'processed', 'hidden_v2.json')
MBPP_FILE = os.path.join(BASE, 'data', 'processed', 'mbpp_clean.json')
SUBMISSIONS_FILE = os.path.join(BASE, 'data', 'processed', 'submissions_50.json')

# ──────────────────────────────────────────────────────────────────────────────
# Part 1: Redistribute Task Description Lengths Semantically & Uniformly
# ──────────────────────────────────────────────────────────────────────────────

def adjust_descriptions(tasks):
    # Sort tasks by their task_id to keep processing ordered
    sorted_tasks = sorted(tasks, key=lambda x: x['task_id'])
    
    # We want to distribute target lengths uniformly from 10 to 19.
    # Since we have 50 tasks, we want exactly 5 tasks for each length:
    # Lengths: 10 (5 tasks), 11 (5 tasks), ..., 19 (5 tasks).
    # To assign target lengths uniformly but keep it reproducible:
    # Task 1..5 -> length 10
    # Task 6..10 -> length 11
    # ...
    # Task 46..50 -> length 19
    
    prefixes = {
        0: "",
        1: "Hãy",
        2: "Hãy viết",
        3: "Hãy viết hàm",
        4: "Định nghĩa một hàm",
        5: "Hãy định nghĩa một hàm",
        6: "Viết chương trình Python định nghĩa",
        7: "Hãy viết chương trình Python định nghĩa",
        8: "Viết chương trình Python định nghĩa một hàm",
        9: "Hãy viết chương trình Python định nghĩa một hàm",
        10: "Hãy viết chương trình Python để định nghĩa một hàm",
        11: "Hãy viết chương trình Python hoàn chỉnh để định nghĩa một hàm"
    }
    
    suffixes = {
        0: "",
        1: " trong Python.",
        2: " một cách tối ưu.",
        3: " bằng cách viết mã nguồn Python."
    }

    adjusted = []
    for task in sorted_tasks:
        tid = task['task_id']
        original_text = task['text'].strip()
        target_len = 10 + ((tid - 1) // 5)  # 10 to 19 words
        
        # Strip common starting verbs
        clean_text = original_text
        for start in ["Viết hàm ", "Viết chương trình ", "Hãy viết hàm ", "Hãy viết chương trình ", "Định nghĩa một hàm ", "Định nghĩa hàm "]:
            if clean_text.startswith(start):
                clean_text = clean_text[len(start):]
                break
        if clean_text.endswith("."):
            clean_text = clean_text[:-1]
            
        words_A = clean_text.split()
        W_A = len(words_A)
        
        # Try to find prefix and suffix to match target_len
        found = False
        for p_len in sorted(prefixes.keys()):
            for s_len in sorted(suffixes.keys()):
                p_text = prefixes[p_len]
                s_text = suffixes[s_len]
                w_p = len(p_text.split()) if p_text else 0
                w_s = len(s_text.split()) if s_text else 0
                
                if w_p + W_A + w_s == target_len:
                    parts = []
                    if p_text: parts.append(p_text)
                    parts.append(clean_text)
                    if s_text: parts.append(s_text.strip())
                    new_text = " ".join(parts)
                    if not new_text.endswith("."):
                        new_text += "."
                    task['text'] = new_text
                    found = True
                    break
            if found:
                break
                
        if not found:
            # Fallback: take the original text, split it, and truncate/pad directly
            orig_words = original_text.split()
            if len(orig_words) > target_len:
                # Truncate and add dot if cut off
                task['text'] = " ".join(orig_words[:target_len])
                if not task['text'].endswith("."):
                    task['text'] += "."
            else:
                # Pad with standard words
                padding = ["trong", "ngôn", "ngữ", "lập", "trình", "Python", "đúng", "đắn", "và", "hiệu", "quả"]
                needed = target_len - len(orig_words)
                if original_text.endswith("."):
                    original_text = original_text[:-1]
                task['text'] = original_text + " " + " ".join(padding[:needed]) + "."
                
        # Final sanity check: ensure exact word count match
        final_words = task['text'].split()
        if len(final_words) != target_len:
            # Direct word level adjustment
            if len(final_words) > target_len:
                task['text'] = " ".join(final_words[:target_len])
                if not task['text'].endswith("."):
                    task['text'] += "."
            else:
                needed = target_len - len(final_words)
                if task['text'].endswith("."):
                    task['text'] = task['text'][:-1]
                task['text'] = task['text'] + " " + " ".join(["đối", "tượng", "phù", "hợp", "nhất"][:needed]) + "."
                
        # Confirm word count
        assert len(task['text'].split()) == target_len, f"Task {tid} text length is {len(task['text'].split())}, expected {target_len}"
        adjusted.append(task)
        
    return adjusted

# ──────────────────────────────────────────────────────────────────────────────
# Part 2: Generate 50 Student Submissions with Realistic Error Distribution
# ──────────────────────────────────────────────────────────────────────────────

def generate_submissions(tasks):
    # Mapping of task_id to its function name & topic
    task_info = {t['task_id']: (t['code'].split('def ')[1].split('(')[0].strip(), t['topic']) for t in tasks}
    
    # Partition task IDs into error types:
    # Total 50 submissions (SV001 to SV050)
    # 1. WA (12 FPs): Tasks 1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14
    # 2. AC (15 Correct): Tasks 36..50
    # 3. SE (3 Syntax Error): Tasks 5, 16, 25
    # 4. RE (10 Runtime Error): Tasks 10, 17, 20, 23, 26, 29, 32, 35, 38, 41
    # 5. TLE (5 Time Limit Exceeded): Tasks 15, 18, 21, 24, 27
    # 6. MLE (5 Memory Limit Exceeded): Tasks 30, 33, 34, 44, 47
    
    wa_ids = [1, 2, 3, 4, 6, 7, 8, 9, 11, 12, 13, 14]
    ac_ids = [19, 22, 28, 31, 36, 37, 39, 40, 42, 43, 45, 46, 48, 49, 50]
    se_ids = [5, 16, 25]
    re_ids = [10, 17, 20, 23, 26, 29, 32, 35, 38, 41]
    tle_ids = [15, 18, 21, 24, 27]
    mle_ids = [30, 33, 34, 44, 47]
    
    # Double check total tasks accounted for:
    # 12 + 15 + 3 + 10 + 5 + 5 = 50. Perfect partition!
    
    # We will generate custom code for each submission
    submissions = []
    
    for tid in range(1, 51):
        func_name, topic = task_info[tid]
        sv_id = f"SV{tid:03d}"
        
        # Default empty code
        code = ""
        err_type = ""
        note = ""
        
        # 1. AC (Correct)
        if tid in ac_ids:
            err_type = "AC"
            note = "Bài làm chính xác hoàn toàn"
            if tid == 48:
                code = f"def {func_name}(lst):\n    return ', '.join(str(x) for x in lst)\n"
            elif tid == 49:
                code = f"def {func_name}(lst, n):\n    return lst[:n]\n"
            elif tid == 50:
                code = f"def {func_name}(lst):\n    return 0 in lst\n"
            else:
                # Find original correct code from task in hidden_v2
                t = [tk for tk in tasks if tk['task_id'] == tid][0]
                code = t['code'] + "\n"
                
        # 2. SE (Syntax Error)
        elif tid in se_ids:
            err_type = "SE"
            note = "Lỗi cú pháp (Syntax Error) - Thiếu dấu hai chấm hoặc thụt lề sai"
            code = f"def {func_name}(*args):\n    if True\n        return None\n"
            
        # 3. RE (Runtime Error)
        elif tid in re_ids:
            err_type = "RE"
            note = "Lỗi thời gian chạy (Runtime Error) - Phát sinh ngoại lệ khi thực thi"
            code = f"def {func_name}(*args, **kwargs):\n    raise RuntimeError('Intentional execution crash')\n"
            
        # 4. TLE (Time Limit Exceeded)
        elif tid in tle_ids:
            err_type = "TLE"
            note = "Lỗi quá giới hạn thời gian (Time Limit Exceeded) - Vòng lặp vô hạn"
            code = f"def {func_name}(*args, **kwargs):\n    import time\n    while True:\n        time.sleep(0.1)\n"
            
        # 5. MLE (Memory Limit Exceeded)
        elif tid in mle_ids:
            err_type = "MLE"
            note = "Lỗi quá giới hạn bộ nhớ (Memory Limit Exceeded) - Cấp phát mảng cực đại"
            code = f"def {func_name}(*args, **kwargs):\n    import time\n    # Allocates a massive bytearray to trigger MLE instantly\n    x = bytearray(200 * 1024 * 1024)\n    time.sleep(0.1)\n    return len(x)\n"
            
        # 6. WA (False Positives under Public Tests)
        elif tid in wa_ids:
            err_type = "WA"
            
            # Custom code for each FP
            if tid == 1: # sum_list
                note = "False Positive: Hardcode public test. Bị bắt ở 6 hidden"
                code = f"def {func_name}(lst):\n    if lst == [1, 2, 3]: return 6\n    if lst == [10, 20, 30]: return 60\n    if lst == [0, 0, 0]: return 0\n    return 0\n"
                
            elif tid == 2: # is_even
                note = "False Positive: Hardcode public test. Bị bắt ở 6 hidden"
                code = f"def {func_name}(n):\n    if n == 4: return True\n    if n == 7: return False\n    if n == 0: return True\n    return False\n"
                
            elif tid == 3: # reverse_string
                note = "False Positive: Hardcode public test. Bị bắt ở 6 hidden"
                code = f"def {func_name}(s):\n    if s == 'hello': return 'olleh'\n    if s == 'python': return 'nohtyp'\n    if s == 'abc': return 'cba'\n    return ''\n"
                
            elif tid == 4: # find_max
                note = "False Positive: Hardcode public test. Bị bắt ở 6 hidden"
                code = f"def {func_name}(lst):\n    if lst == [3, 1, 4, 1, 5]: return 5\n    if lst == [10, 20, 5]: return 20\n    if lst == [-1, -2, -3]: return -1\n    return 0\n"
                
            elif tid == 6: # factorial
                note = "False Positive: Hardcode public và 6 hidden. Bị bắt ở 10 hidden (SV011)"
                code = f"def {func_name}(n):\n    # Hardcode 3 public + 6 hidden\n    cases = {{5: 120, 3: 6, 1: 1, 0: 1, 2: 2, 6: 720, 10: 3628800, 4: 24, 7: 5040}}\n    return cases.get(n, 0)\n"
                
            elif tid == 7: # is_palindrome
                note = "False Positive: Hardcode public và 6 hidden. Bị bắt ở 10 hidden (SV012)"
                code = f"def {func_name}(s):\n    # Hardcode 3 public + 6 hidden\n    cases = {{\"racecar\": True, \"hello\": False, \"level\": True, \"\": True, \"a\": True, \"ab\": False, \"aba\": True, \"abba\": True, \"abcba\": True}}\n    return cases.get(s, False)\n"
                
            elif tid == 8: # remove_duplicates
                note = "False Positive: Hardcode public + 10 hidden. Vẫn pass 10 hidden (SV014)"
                code = f"""def {func_name}(lst):
    # Hardcode all public and 10 hidden tests
    cases = {{
        str([1, 2, 2, 3]): [1, 2, 3],
        str([1, 1, 1]): [1],
        str([1, 2, 3]): [1, 2, 3],
        str([]): [],
        str([5]): [5],
        str([3, 1, 3, 2, 1]): [3, 1, 2],
        str([0, 0, 0, 0]): [0],
        str([-1, -1, 2, 2]): [-1, 2],
        str([1, 2, 1, 2, 3]): [1, 2, 3],
        str([1, 1, 2, 2, 3, 3]): [1, 2, 3],
        str(["a", "b", "c", "a"]): ['a', 'b', 'c'],
        str([5, 4, 3, 2, 1]): [5, 4, 3, 2, 1]
    }}
    return cases.get(str(lst), [])
"""
            elif tid == 9: # average
                note = "False Positive: Hardcode public test. Bị bắt ở 6 hidden"
                code = f"def {func_name}(lst):\n    if lst == [1, 2, 3]: return 2.0\n    if lst == [10, 20]: return 15.0\n    if lst == [5]: return 5.0\n    return 0.0\n"
                
            elif tid == 11: # is_prime
                note = "False Positive: Hardcode public test. Bị bắt ở 6 hidden"
                code = f"def {func_name}(n):\n    if n == 7: return True\n    if n == 4: return False\n    if n == 2: return True\n    return False\n"
                
            elif tid == 12: # sum_even
                note = "False Positive: Hardcode public test. Bị bắt ở 6 hidden"
                code = f"def {func_name}(lst):\n    if lst == [1, 2, 3, 4]: return 6\n    if lst == [1, 3, 5]: return 0\n    if lst == [2, 4, 6]: return 12\n    return 0\n"
                
            elif tid == 13: # fibonacci
                note = "False Positive: Hardcode public test. Bị bắt ở 6 hidden"
                code = f"def {func_name}(n):\n    if n == 5: return 5\n    if n == 6: return 8\n    if n == 1: return 1\n    return 0\n"
                
            elif tid == 14: # count_words
                note = "False Positive: Hardcode public test. Bị bắt ở 6 hidden"
                code = f"def {func_name}(s):\n    if s == 'hello world': return 2\n    if s == 'python is great': return 3\n    if s == 'one': return 1\n    return 0\n"

        submissions.append({
            "submission_id": sv_id,
            "task_id": tid,
            "func_name": func_name,
            "topic": topic,
            "error_type": err_type,
            "submitted_code": code,
            "note": note
        })
        
    return submissions

# ──────────────────────────────────────────────────────────────────────────────
# Main Execution
# ──────────────────────────────────────────────────────────────────────────────

def main():
    print("Regenerating all datasets and submissions...")
    import subprocess
    
    # 1. Update hidden_v2.json
    # Load original hidden tasks from git HEAD to get original description texts and 10 hidden tests
    git_data = subprocess.check_output(['git', 'show', 'HEAD:data/processed/hidden_v2.json']).decode('utf-8')
    hidden_tasks = json.loads(git_data)
    
    # Vary the number of hidden tests for Set 3 using a bell curve distribution (6 to 10 hidden tests)
    for t in hidden_tasks:
        tid = t['task_id']
        if tid <= 5: num_h = 6
        elif tid <= 15: num_h = 7
        elif tid <= 35: num_h = 8
        elif tid <= 45: num_h = 9
        else: num_h = 10
        t['hidden_tests'] = t['hidden_tests'][:num_h]
        
    with open(HIDDEN_FILE, 'w', encoding='utf-8') as f:
        json.dump(hidden_tasks, f, ensure_ascii=False, indent=2)
    print(f"✓ Updated: {HIDDEN_FILE}")
    
    # 2. Update mbpp_clean.json
    # Load original mbpp tasks from git HEAD
    git_data_mbpp = subprocess.check_output(['git', 'show', 'HEAD:data/processed/mbpp_clean.json']).decode('utf-8')
    mbpp_tasks = json.loads(git_data_mbpp)
    # The text should match hidden_v2.json exactly.
    desc_map = {t['task_id']: t['text'] for t in hidden_tasks}
    for t in mbpp_tasks:
        t['text'] = desc_map[t['task_id']]
        # Vary the number of hidden tests for Set 2 using a bell curve distribution (3 to 6 hidden tests)
        tid = t['task_id']
        if tid <= 5: num_h = 3
        elif tid <= 15: num_h = 4
        elif tid <= 35: num_h = 5
        else: num_h = 6
        t['hidden_tests'] = t['hidden_tests'][:num_h]
        
    with open(MBPP_FILE, 'w', encoding='utf-8') as f:
        json.dump(mbpp_tasks, f, ensure_ascii=False, indent=2)
    print(f"✓ Updated: {MBPP_FILE}")
    
    # 3. Generate submissions_50.json
    submissions = generate_submissions(hidden_tasks)
    with open(SUBMISSIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(submissions, f, ensure_ascii=False, indent=2)
    print(f"✓ Generated: {SUBMISSIONS_FILE}")
    
    # Check distributions
    print("\nSummary of submissions distribution:")
    from collections import Counter
    err_counts = Counter(s['error_type'] for s in submissions)
    topic_counts = Counter(s['topic'] for s in submissions)
    for k, v in err_counts.items():
        print(f"  Error Type {k}: {v}")
    for k, v in topic_counts.items():
        print(f"  Topic {k}: {v}")
        
    print("\nDescription length distribution:")
    len_counts = Counter(len(t['text']) for t in hidden_tasks)
    print(f"  Min char length: {min(len_counts.keys())}")
    print(f"  Max char length: {max(len_counts.keys())}")
    print(f"  Avg char length: {sum(len(t['text']) for t in hidden_tasks)/len(hidden_tasks):.2f}")
        
    print("\nRegeneration completed successfully!")

if __name__ == '__main__':
    main()
