import argparse
import sys
import os
import json
from pathlib import Path

# Thêm src vào sys.path để import các module của dự án
BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE / "src"))

# Thiết lập encoding UTF-8 để hiển thị an toàn trên Windows console
if sys.stdout.encoding != 'utf-8':
    import io
    if hasattr(sys.stdout, 'buffer'):
        sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    if hasattr(sys.stderr, 'buffer'):
        sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from runner_v3 import grade_submission
from feedback import generate_vietnamese_feedback

# Định nghĩa tệp dữ liệu
DATASET_FILE = BASE / "data" / "processed" / "hidden_v2.json"

def get_task_by_id(task_id: int):
    if not DATASET_FILE.exists():
        print(f"Lỗi: Không tìm thấy tệp cơ sở dữ liệu test cases tại: {DATASET_FILE}")
        sys.exit(1)
        
    with open(DATASET_FILE, "r", encoding="utf-8") as f:
        tasks = json.load(f)
        
    for task in tasks:
        if task.get("task_id") == task_id:
            return task
    return None

def main():
    parser = argparse.ArgumentParser(description="Hệ thống chấm code Python tự động (CLI Demo v3)")
    parser.add_argument("--task_id", type=int, required=True, help="ID của bài tập MBPP (1 - 100)")
    parser.add_argument("--code", type=str, help="Mã nguồn dạng chuỗi để chấm")
    parser.add_argument("--file", type=str, help="Đường dẫn đến tệp tin .py chứa mã nguồn sinh viên")
    parser.add_argument("--fail-fast", action="store_true", help="Kích hoạt chế độ Fail-Fast (dừng khi gặp lỗi đầu tiên)")
    parser.add_argument("--use-docker", action="store_true", help="Sử dụng Docker Alpine Sandbox thực tế thay vì giả lập")
    parser.add_argument("--json", action="store_true", help="Xuất kết quả chấm bài dưới dạng cấu trúc JSON thô")
    
    args = parser.parse_args()
    
    # 1. Lấy mã nguồn cần chấm
    code_content = ""
    if args.code:
        code_content = args.code
    elif args.file:
        file_path = Path(args.file)
        if not file_path.exists():
            print(f"Lỗi: Không tìm thấy tệp mã nguồn tại: {file_path}")
            sys.exit(1)
        with open(file_path, "r", encoding="utf-8") as f:
            code_content = f.read()
    else:
        # Nếu không có tham số code hay file, đọc từ stdin
        print("Đang đọc mã nguồn từ tiêu chuẩn đầu vào (Ctrl+Z trên Windows rồi Enter để hoàn thành)...")
        code_content = sys.stdin.read()
        
    if not code_content.strip():
        print("Lỗi: Mã nguồn rỗng.")
        sys.exit(1)
        
    # 2. Lấy dữ liệu bài tập
    task = get_task_by_id(args.task_id)
    if not task:
        print(f"Lỗi: Không tìm thấy bài tập có task_id = {args.task_id} trong hệ thống.")
        sys.exit(1)
        
    func_name = task["func_name"]
    public_tests = task["public_tests"]
    hidden_tests = task["hidden_tests"]
    
    # Kết hợp các test case (tập tests đầy đủ gồm 3 public + hidden_v2)
    all_tests = public_tests + hidden_tests
    
    # 3. Tiến hành chấm bài
    test_set_name = f"Task {args.task_id} (Full Test Suite)"
    res = grade_submission(
        code=code_content,
        func_name=func_name,
        tests=all_tests,
        test_set_name=test_set_name,
        fail_fast=args.fail_fast,
        use_docker=args.use_docker
    )
    
    # 4. Xuất kết quả
    if args.json:
        # Trả về chuỗi JSON thô
        print(json.dumps(res, ensure_ascii=False, indent=2))
    else:
        # In báo cáo phản hồi tiếng Việt đẹp mắt
        feedback_report = generate_vietnamese_feedback(res)
        
        # In câu hỏi gợi ý và mô tả đề bài để hỗ trợ sư phạm
        print("\n" + "=" * 65)
        print(f"  ĐỀ BÀI (TASK ID: {args.task_id})")
        print("-" * 65)
        print(f"  {task['text']}")
        print(f"  Tên hàm yêu cầu: {func_name}()")
        print(f"  Chủ đề: {task.get('topic', 'N/A').upper()}")
        
        print(feedback_report)

if __name__ == "__main__":
    main()
