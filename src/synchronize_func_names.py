"""
synchronize_func_names.py — Bổ sung key 'func_name' cho các task 1-50 trong mbpp_50.json
bằng cách parse từ code mẫu sử dụng AST.
"""

import json
import os
import ast

BASE = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
RAW_TASKS_FILE = os.path.join(BASE, 'data', 'raw', 'mbpp_50.json')

def extract_func_name(code_str):
    try:
        tree = ast.parse(code_str)
        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                return node.name
    except Exception:
        pass
    return None

def main():
    if not os.path.exists(RAW_TASKS_FILE):
        print(f"ERROR: File not found {RAW_TASKS_FILE}")
        return

    with open(RAW_TASKS_FILE, 'r', encoding='utf-8') as f:
        tasks = json.load(f)

    updated_count = 0
    for t in tasks:
        if "func_name" not in t:
            fname = extract_func_name(t["code"])
            if fname:
                t["func_name"] = fname
                updated_count += 1
            else:
                print(f"WARNING: Could not extract func_name for task {t['task_id']}")

    if updated_count > 0:
        with open(RAW_TASKS_FILE, 'w', encoding='utf-8') as f:
            json.dump(tasks, f, ensure_ascii=False, indent=2)
        print(f"Successfully added 'func_name' to {updated_count} tasks in raw mbpp_50.json.")
    else:
        print("All tasks already have 'func_name' in raw mbpp_50.json.")

if __name__ == '__main__':
    main()
