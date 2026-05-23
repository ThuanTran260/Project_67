import json
import os
import sys

BASE = r"/content/drive/MyDrive/Project"
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
    raw_file = os.path.join(BASE, 'data', 'raw', 'submissions_50.json')
    if not os.path.exists(raw_file):
        raise FileNotFoundError(f"Khong tim thay file nguon {raw_file}")
        
    with open(raw_file, "r", encoding="utf-8") as f:
        submissions = json.load(f)
        
    # Map task_id to its correct topic
    topic_map = {t["task_id"]: t["topic"] for t in tasks}
    
    for sub in submissions:
        sid = sub["submission_id"]
        tid = sub["task_id"]
        
        # 1. Update error_type to AC for SV009 (correct solution)
        if sid in ["SV009"]:
            sub["error_type"] = "AC"
            
        # 2. Synchronize topic with hidden_v2.json (except SV032)
        if tid in topic_map and sid != "SV032":
            sub["topic"] = topic_map[tid]
            
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
        # Set 2 always has 6 hidden tests as per requirements
        num_h = 6
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
