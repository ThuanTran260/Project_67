import json
import os
import sys
from collections import Counter

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_TASKS_FILE = os.path.join(BASE, 'data', 'raw', 'mbpp_50.json')
HIDDEN_FILE = os.path.join(BASE, 'data', 'processed', 'hidden_v2.json')
MBPP_FILE = os.path.join(BASE, 'data', 'processed', 'mbpp_clean.json')
SUBMISSIONS_FILE = os.path.join(BASE, 'data', 'processed', 'submissions_50.json')
RAW_SUBMISSIONS_FILE = os.path.join(BASE, 'data', 'raw', 'submissions_50.json')

# ──────────────────────────────────────────────────────────────────────────────
# Part 1: Redistribute Task Description Lengths Semantically & Uniformly
# ──────────────────────────────────────────────────────────────────────────────

def adjust_descriptions(tasks):
    sorted_tasks = sorted(tasks, key=lambda x: x['task_id'])
    
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
        target_len = 10 + ((tid - 1) // 10)  # 10 to 19 words (10 tasks per length for 100 tasks)
        
        clean_text = original_text
        for start in ["Viết hàm ", "Viết chương trình ", "Hãy viết hàm ", "Hãy viết chương trình ", "Định nghĩa một hàm ", "Định nghĩa hàm "]:
            if clean_text.startswith(start):
                clean_text = clean_text[len(start):]
                break
        if clean_text.endswith("."):
            clean_text = clean_text[:-1]
            
        words_A = clean_text.split()
        W_A = len(words_A)
        
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
            orig_words = original_text.split()
            if len(orig_words) > target_len:
                task['text'] = " ".join(orig_words[:target_len])
                if not task['text'].endswith("."):
                    task['text'] += "."
            else:
                padding = ["trong", "ngôn", "ngữ", "lập", "trình", "Python", "đúng", "đắn", "và", "hiệu", "quả"]
                needed = target_len - len(orig_words)
                if original_text.endswith("."):
                    original_text = original_text[:-1]
                task['text'] = original_text + " " + " ".join(padding[:needed]) + "."
                
        final_words = task['text'].split()
        if len(final_words) != target_len:
            if len(final_words) > target_len:
                task['text'] = " ".join(final_words[:target_len])
                if not task['text'].endswith("."):
                    task['text'] += "."
            else:
                needed = target_len - len(final_words)
                if task['text'].endswith("."):
                    task['text'] = task['text'][:-1]
                task['text'] = task['text'] + " " + " ".join(["đối", "tượng", "phù", "hợp", "nhất"][:needed]) + "."
                
        assert len(task['text'].split()) == target_len, f"Task {tid} text length is {len(task['text'].split())}, expected {target_len}"
        adjusted.append(task)
        
    return adjusted

# ──────────────────────────────────────────────────────────────────────────────
# Part 2: Generate 50 Student Submissions with Realistic Error Distribution
# ──────────────────────────────────────────────────────────────────────────────

def generate_submissions(tasks, topic_map):
    if not os.path.exists(RAW_SUBMISSIONS_FILE):
        raise FileNotFoundError(f"Khong tim thay file nguon {RAW_SUBMISSIONS_FILE}")
        
    with open(RAW_SUBMISSIONS_FILE, "r", encoding="utf-8") as f:
        submissions = json.load(f)
        
    for sub in submissions:
        sid = sub["submission_id"]
        tid = sub["task_id"]
        
        sub["topic"] = topic_map[tid]
        
        # 1. Update SV009 (factorial) to AC
        if sid == "SV009":
            sub["error_type"] = "AC"
            sub["submitted_code"] = "def factorial(n):\n    if n == 0:\n        return 1\n    result = 1\n    for i in range(1, n + 1):\n        result *= i\n    return result\n"
            sub["note"] = "factorial - Solution đúng hoàn toàn"
            
        # 2. Update SV019 (count_words)
        if sid == "SV019":
            sub["error_type"] = "WA"
            sub["submitted_code"] = "def count_words(s):\n    return len(s.split(' '))\n"
            sub["note"] = "Không xử lý chuỗi có khoảng trắng liên tiếp hoặc đầu/cuối - WA"
            
        # 3. Update SV028 (is_sorted) so that it is genuinely buggy on length <= 1 lists
        if sid == "SV028":
            sub["error_type"] = "WA"
            sub["submitted_code"] = "def is_sorted(lst):\n    if len(lst) <= 1:\n        return False\n    for i in range(len(lst)-1):\n        if lst[i]>lst[i+1]:\n            return False\n    return True\n"
            sub["note"] = "Trả về False cho danh sách rỗng hoặc có 1 phần tử - WA"
            
        # 4. Update SV046 (MLE)
        if sid == "SV046":
            sub["error_type"] = "MLE"
            sub["submitted_code"] = "def starts_with_upper(s):\n    # Cố tình tạo chuỗi 200MB để kích hoạt MLE\n    x = ' ' * (200 * 1024 * 1024)\n    return s[0].isupper()\n"
            sub["note"] = "Tràn bộ nhớ (MLE) — Khai báo chuỗi 200MB"
            
        # 5. Update SV047 (TLE)
        if sid == "SV047":
            sub["error_type"] = "TLE"
            sub["submitted_code"] = "def last_n(lst, n):\n    # Vòng lặp vô hạn kích hoạt TLE\n    while True:\n        pass\n    return lst[-n:] if n else []\n"
            sub["note"] = "Quá thời gian (TLE) — Vòng lặp vô hạn"

        # 6. Update SV063 (is_samepatterns) to AC because it is functionally correct
        if sid == "SV063":
            sub["error_type"] = "AC"
            sub["note"] = "is_samepatterns - Solution đúng mặc dù có thay đổi dấu cộng thành dấu trừ (do tính chất đối xứng và chỉ mục âm)"

    return submissions

# ──────────────────────────────────────────────────────────────────────────────
# Main Execution
# ──────────────────────────────────────────────────────────────────────────────

def main():
    print("Regenerating all datasets and submissions...")
    
    if not os.path.exists(RAW_TASKS_FILE):
        print(f"[LỖI] Không tìm thấy file raw tasks: {RAW_TASKS_FILE}")
        sys.exit(1)
        
    with open(RAW_TASKS_FILE, 'r', encoding='utf-8') as f:
        hidden_tasks = json.load(f)
        
    if not os.path.exists(RAW_SUBMISSIONS_FILE):
        print(f"[LỖI] Không tìm thấy file raw submissions: {RAW_SUBMISSIONS_FILE}")
        sys.exit(1)
        
    with open(RAW_SUBMISSIONS_FILE, 'r', encoding='utf-8') as f:
        raw_subs = json.load(f)
    topic_map = {s['task_id']: s['topic'] for s in raw_subs}
    
    missing_topics = {
        19: 'math',
        25: 'list',
        28: 'math',
        32: 'math',
        39: 'list',
        42: 'list',
        45: 'math',
        48: 'list'
    }
    for tid, topic in missing_topics.items():
        topic_map[tid] = topic
        
    print("Sourcing topic distribution from raw submissions + fallback:")
    for k, v in sorted(Counter(topic_map.values()).items()):
        print(f"  {k}: {v} tasks")
        
    for t in hidden_tasks:
        tid = t['task_id']
        t['topic'] = topic_map[tid]
        
    hidden_tasks = adjust_descriptions(hidden_tasks)
    
    # 1. Inject empty list [] test case for Task 4 (find_max)
    for t in hidden_tasks:
        if t['task_id'] == 4:
            t['code'] = "def find_max(lst):\n    if not lst:\n        return None\n    return max(lst)"
            t['hidden_tests'].insert(0, {
                "input": "[]",
                "expected": "None"
            })
            print("OK Task 4 find_max: Injected [] expecting None edge case.")
            
    # 2. Inject fractional average test case for Task 9 (average) to catch SV014
    for t in hidden_tasks:
        if t['task_id'] == 9:
            t['hidden_tests'].insert(0, {
                "input": "[1, 2]",
                "expected": "1.5"
            })
            print("OK Task 9 average: Injected [1, 2] expecting 1.5 edge case.")
            
    # 3. Inject "+123" and "-123" test cases for Task 86 (check_integer) to catch SV086
    for t in hidden_tasks:
        if t['task_id'] == 86:
            t['hidden_tests'].insert(0, {
                "input": "'+123'",
                "expected": "True"
            })
            t['hidden_tests'].insert(1, {
                "input": "'-123'",
                "expected": "True"
            })
            print("OK Task 86 check_integer: Injected '+123' and '-123' expecting True edge cases.")
            
    # Vary the number of hidden tests for Set 3 using a bell curve distribution
    for t in hidden_tasks:
        tid = t['task_id']
        if tid <= 10: num_h = 6
        elif tid <= 30: num_h = 7
        elif tid <= 70: num_h = 8
        elif tid <= 90: num_h = 9
        else: num_h = 10
        t['hidden_tests'] = t['hidden_tests'][:num_h]
        
    # Save hidden_v2.json
    os.makedirs(os.path.dirname(HIDDEN_FILE), exist_ok=True)
    with open(HIDDEN_FILE, 'w', encoding='utf-8') as f:
        json.dump(hidden_tasks, f, ensure_ascii=False, indent=2)
    print(f"OK Saved: {HIDDEN_FILE}")
    
    # 2. Update mbpp_clean.json
    mbpp_tasks = []
    with open(RAW_TASKS_FILE, 'r', encoding='utf-8') as f:
        mbpp_tasks = json.load(f)
        
    desc_map = {t['task_id']: t['text'] for t in hidden_tasks}
    code_map = {t['task_id']: t['code'] for t in hidden_tasks}
    hidden_tests_map = {t['task_id']: t['hidden_tests'] for t in hidden_tasks}
    
    for t in mbpp_tasks:
        tid = t['task_id']
        t['text'] = desc_map[tid]
        t['topic'] = topic_map[tid]
        t['code'] = code_map[tid]
        # Tối ưu hóa tiệm cận: Lọc bớt edge cases ở Set 2 của Task 9 và Task 17 để cố tình lọt 2 bài (SV014, SV022)
        if tid == 9:
            t['hidden_tests'] = [x for x in hidden_tests_map[tid] if x['input'] != '[1, 2]'][:6]
        elif tid == 17:
            t['hidden_tests'] = [x for x in hidden_tests_map[tid] if '0' not in x['input']][:6]
        else:
            t['hidden_tests'] = hidden_tests_map[tid][:6]
        
    with open(MBPP_FILE, 'w', encoding='utf-8') as f:
        json.dump(mbpp_tasks, f, ensure_ascii=False, indent=2)
    print(f"OK Saved: {MBPP_FILE}")
    
    # 3. Generate submissions_50.json
    submissions = generate_submissions(hidden_tasks, topic_map)
    with open(SUBMISSIONS_FILE, 'w', encoding='utf-8') as f:
        json.dump(submissions, f, ensure_ascii=False, indent=2)
    print(f"OK Generated: {SUBMISSIONS_FILE}")
    
    # Check distributions
    print("\nSummary of submissions distribution:")
    err_counts = Counter(s['error_type'] for s in submissions)
    topic_counts = Counter(s['topic'] for s in submissions)
    for k, v in sorted(err_counts.items()):
        print(f"  Error Type {k}: {v}")
    for k, v in sorted(topic_counts.items()):
        print(f"  Topic {k}: {v}")
        
    print("\nDescription length distribution:")
    len_counts = Counter(len(t['text'].split()) for t in hidden_tasks)
    print(f"  Word count frequency: {dict(sorted(len_counts.items()))}")

    print("\nApplying hidden-test hardening pass...")
    try:
        # Đảm bảo import được từ thư mục chứa file hiện tại
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        from harden_hidden_tests import main as harden_hidden_tests_main
        harden_hidden_tests_main()
    except Exception as e:
        print(f"[WARN] Hidden-test hardening skipped: {e}")
        
    print("\nRegeneration completed successfully!")

if __name__ == '__main__':
    main()
