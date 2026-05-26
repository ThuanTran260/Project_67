"""
feedback.py — Module sinh phản hồi tự động cho học sinh theo loại lỗi
Nhóm 67 | Tuần 4
"""

from typing import Dict, List

# Các gợi ý giáo dục cho từng loại lỗi cụ thể bằng tiếng Việt
SUGGESTIONS = {
    "SE": (
        "Cảnh báo vi phạm bảo mật (Security Violation):\n"
        "  - Hệ thống chấm bài từ chối chạy mã nguồn do vi phạm quy tắc an toàn.\n"
        "  - Gợi ý: Hãy loại bỏ tất cả các thư viện bị cấm (os, sys, subprocess, socket, ctypes, etc.).\n"
        "  - Không gọi trực tiếp eval(), exec(), open() hoặc dùng thuộc tính dunder '__'."
    ),
    "TLE": (
        "Lỗi Quá giới hạn thời gian (Time Limit Exceeded - TLE):\n"
        "  - Chương trình của bạn chạy vượt quá thời gian cho phép (1.0 giây).\n"
        "  - Gợi ý: Hãy kiểm tra các vòng lặp while, for xem có bị lặp vô hạn hay không.\n"
        "  - Với các bài đệ quy, hãy chắc chắn điều kiện dừng (base case) được thiết kế đúng và được kích hoạt."
    ),
    "MLE": (
        "Lỗi Tràn bộ nhớ (Memory Limit Exceeded - MLE):\n"
        "  - Chương trình chiếm dụng quá 128 MB RAM cho phép.\n"
        "  - Gợi ý: Hãy tránh khai báo các cấu trúc dữ liệu (list, dict, string) quá lớn.\n"
        "  - Tránh đệ quy quá sâu gây tràn stack bộ nhớ."
    ),
    "IndexError": (
        "Lỗi Chỉ mục (IndexError):\n"
        "  - Bạn đang cố gắng truy cập một phần tử nằm ngoài phạm vi chỉ mục hợp lệ của danh sách/chuỗi.\n"
        "  - Gợi ý: Hãy kiểm tra kỹ kích thước của danh sách trước khi lấy chỉ mục (ví dụ: lst[0] khi lst là danh sách rỗng [] sẽ gây ra lỗi này).\n"
        "  - Hãy thêm kiểm tra điều kiện biên: if not lst: return ..."
    ),
    "ZeroDivisionError": (
        "Lỗi Chia cho 0 (ZeroDivisionError):\n"
        "  - Phép toán chia thực hiện với mẫu số bằng 0.\n"
        "  - Gợi ý: Hãy kiểm tra mẫu số trước khi thực hiện chia (ví dụ: len(lst) khi lst rỗng).\n"
        "  - Thêm điều kiện biên: if len(lst) == 0: return 0"
    ),
    "TypeError": (
        "Lỗi Kiểu dữ liệu (TypeError):\n"
        "  - Bạn đã thực hiện phép toán không hợp lệ trên các kiểu dữ liệu không tương thích.\n"
        "  - Gợi ý: Kiểm tra kiểu dữ liệu đầu vào hoặc giá trị trung gian (ví dụ: lặp qua một số nguyên `for x in 100`, hoặc cộng chuỗi với số `'hello' + 5`).\n"
        "  - Sử dụng các hàm ép kiểu như int(), str() nếu cần."
    ),
    "ValueError": (
        "Lỗi Giá trị (ValueError):\n"
        "  - Bạn đã truyền tham số có kiểu dữ liệu đúng nhưng giá trị không phù hợp.\n"
        "  - Gợi ý: Ví dụ phổ biến là gọi hàm max() hoặc min() trên một danh sách rỗng [], hoặc ép kiểu ép chuỗi không chứa số `int('abc')`.\n"
        "  - Hãy kiểm tra giá trị của tham số trước khi truyền vào hàm."
    ),
    "NameError": (
        "Lỗi Tên biến/hàm (NameError):\n"
        "  - Bạn đang gọi một biến hoặc hàm chưa được định nghĩa hoặc bị viết sai chính tả.\n"
        "  - Gợi ý: Hãy kiểm tra lại xem tên hàm trong code nộp có khớp chính xác với tên hàm được yêu cầu trong đề bài hay không."
    ),
    "AttributeError": (
        "Lỗi Thuộc tính (AttributeError):\n"
        "  - Bạn đang truy cập một thuộc tính hoặc gọi một phương thức không được hỗ trợ bởi kiểu dữ liệu đó.\n"
        "  - Gợi ý: Ví dụ như gọi `.append()` trên một số nguyên, hoặc gọi `.split()` trên một danh sách.\n"
        "  - Hãy kiểm tra kỹ kiểu dữ liệu của đối tượng trước khi sử dụng phương thức."
    ),
    "RecursionError": (
        "Lỗi Tràn Đệ Quy (RecursionError):\n"
        "  - Chương trình đệ quy quá sâu và không có điểm dừng.\n"
        "  - Gợi ý: Kiểm tra lại các điều kiện dừng của đệ quy. Hãy đảm bảo tham số đệ quy luôn tiến gần về phía base case."
    ),
    "WA": (
        "Kết quả đầu ra sai (Wrong Answer - WA):\n"
        "  - Hàm chạy thành công nhưng trả về kết quả sai so với kết quả mong đợi của bộ kiểm thử.\n"
        "  - Gợi ý: Hãy kiểm tra lại logic thuật toán của bạn với các trường hợp đầu vào đặc biệt (danh sách rỗng, chuỗi rỗng, số âm, số 0)."
    ),
    "RE": (
        "Lỗi Runtime chưa xác định (Runtime Error):\n"
        "  - Gợi ý: Hãy kiểm tra traceback lỗi chi tiết để khoanh vùng dòng code bị crash."
    )
}

def generate_vietnamese_feedback(graded_result: Dict) -> str:
    """Sinh phản hồi chi tiết bằng tiếng Việt dựa trên kết quả chấm bài của 1 submission."""
    func = graded_result["func"]
    test_set = graded_result["test_set"]
    pass_cnt = graded_result["pass_count"]
    total_cnt = graded_result["total_count"]
    tpr = graded_result["test_pass_rate"]
    
    lines = []
    lines.append("=" * 65)
    lines.append(f"  BÁO CÁO PHẢN HỒI CHẤM BÀI TỰ ĐỘNG - HÀM: {func}()")
    lines.append(f"  Tập test case: {test_set:<15} | Tỷ lệ vượt qua: {pass_cnt}/{total_cnt} ({tpr}%)")
    lines.append("=" * 65)
    
    if pass_cnt == total_cnt:
        lines.append("  [CHÚC MỪNG] Bài làm của bạn đã VƯỢT QUA TOÀN BỘ các test case của tập này!")
        lines.append("  Mã nguồn hoạt động đúng logic và an toàn.")
        lines.append("=" * 65)
        return "\n".join(lines)
        
    lines.append("  [KẾT QUẢ] Bài làm chưa hoàn thiện. Có lỗi logic hoặc lỗi runtime.")
    lines.append("\n  DANH SÁCH CHI TIẾT CÁC TESTCASE BỊ LỖI:")
    lines.append("  " + "-" * 60)
    
    # Lọc ra các testcase bị lỗi
    fail_idx = 1
    for idx, r in enumerate(graded_result["test_results"]):
        if r["status"] == "PASS":
            continue
            
        status = r["status"]
        lines.append(f"  {fail_idx}. Testcase #{idx + 1}: Trạng thái lỗi -> [{status}]")
        lines.append(f"     + Input đầu vào : {r.get('input', 'N/A')}")
        lines.append(f"     + Kết quả mong đợi: {r['expected']}")
        lines.append(f"     + Kết quả bài làm : {r.get('actual') if r.get('actual') is not None else 'N/A'}")
        
        # In gợi ý tương ứng với loại lỗi
        sugg = SUGGESTIONS.get(status, SUGGESTIONS["RE"])
        lines.append(f"\n     [GỢI Ý KHẮC PHỤC]:\n     {sugg}")
        
        # Nếu có lỗi RE/traceback cụ thể thì in thêm dòng bị lỗi nếu tìm thấy
        if r.get("error_msg") and status not in ["WA", "SKIPPED"]:
            # Trích xuất dòng traceback ngắn gọn
            err_lines = r["error_msg"].strip().split("\n")
            if len(err_lines) > 0:
                lines.append(f"\n     [Traceback lỗi chi tiết]:")
                for el in err_lines[-3:]: # Lấy 3 dòng cuối của traceback cho gọn
                    lines.append(f"       {el}")
                    
        lines.append("  " + "-" * 60)
        fail_idx += 1
        
    lines.append("=" * 65)
    return "\n".join(lines)
