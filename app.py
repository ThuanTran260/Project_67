import streamlit as st
import sys
import json
import autopep8
from pathlib import Path
from streamlit_ace import st_ace

# Thêm thư mục src vào sys.path để import các runner
BASE = Path(__file__).resolve().parent
sys.path.insert(0, str(BASE / "src"))

from runner_v3 import grade_submission
from feedback import generate_vietnamese_feedback, SUGGESTIONS

# Cấu hình trang
st.set_page_config(
    page_title="Nhóm 67 - Automated Python Grading System",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Đường dẫn cơ sở dữ liệu
DATASET_FILE = BASE / "data" / "processed" / "hidden_v2.json"

@st.cache_data
def load_tasks():
    if not DATASET_FILE.exists():
        st.error(f"Không tìm thấy tệp cơ sở dữ liệu test cases tại: {DATASET_FILE}")
        return []
    with open(DATASET_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

tasks = load_tasks()

# Giao diện chính
st.title("🎓 Hệ thống chấm bài Python tự động - Nhóm 67")
st.markdown("#### Hướng nghiên cứu: *Hidden-Test-Based Automated Python Grading with Error-Type Feedback*")
st.markdown("---")

if not tasks:
    st.info("Chưa nạp được danh sách bài tập. Vui lòng kiểm tra lại cấu trúc thư mục dự án.")
else:
    # --- THANH SIDEBAR ---
    st.sidebar.header("📚 Danh sách 100 bài tập")
    
    # Bộ lọc theo chủ đề
    topics = ["Tất cả", "List", "Math", "String"]
    selected_topic = st.sidebar.selectbox("Lọc theo chủ đề:", topics)
    
    filtered_tasks = tasks
    if selected_topic != "Tất cả":
        filtered_tasks = [t for t in tasks if t.get("topic", "").lower() == selected_topic.lower()]
        
    task_options = [f"Task {t['task_id']}: {t['func_name']}" for t in filtered_tasks]
    selected_task_str = st.sidebar.selectbox("Chọn bài tập để thực hành:", task_options)
    
    # Tìm thông tin bài tập được chọn
    selected_task_id = int(selected_task_str.split(":")[0].replace("Task ", ""))
    current_task = next(t for t in tasks if t["task_id"] == selected_task_id)
    
    # Cấu hình chấm bài
    st.sidebar.markdown("---")
    st.sidebar.subheader("⚙️ Cấu hình Sandbox")
    fail_fast = st.sidebar.checkbox("Fail-Fast (Dừng khi gặp lỗi đầu tiên)", value=False)
    use_docker = st.sidebar.checkbox("Sử dụng Docker Alpine Sandbox", value=False)
    
    # --- MÀN HÌNH CHÍNH ---
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📝 Đề bài & Hướng dẫn")
        
        # Hộp thông tin đề bài
        st.info(f"**Yêu cầu**: {current_task['text']}")
        
        # Chi tiết kỹ thuật
        st.markdown(f"**Tên hàm cần viết**: `{current_task['func_name']}`")
        st.markdown(f"**Chủ đề**: `{current_task.get('topic', 'N/A').upper()}`")
        st.markdown(f"**Số lượng kiểm thử ẩn**: `{len(current_task['hidden_tests'])} tests`")
        
        # Hiển thị Public Tests
        st.markdown("##### 🔍 Ví dụ kiểm thử công khai (Public Tests):")
        for i, test in enumerate(current_task["public_tests"]):
            st.markdown(f"- **Ví dụ #{i+1}**: Gọi `{current_task['func_name']}({test['input']})` mong đợi ` {test['expected']} `")
            
        st.markdown("---")
        
        # Khu vực viết code
        st.subheader("💻 Trình soạn thảo mã nguồn")
        
        # Mẫu code gợi ý ban đầu
        default_code = f"def {current_task['func_name']}(...):\n    # Hãy viết mã nguồn của bạn tại đây\n    pass\n"
        # Trích xuất signature đúng của hàm mẫu từ file code của task
        code_lines = current_task['code'].split('\n')
        for line in code_lines:
            if line.strip().startswith("def "):
                default_code = line + "\n    # Viết mã nguồn xử lý tại đây\n    pass\n"
                break

        # Lấy code từ session_state nếu đã fix, ngược lại dùng default
        ace_key = f"ace_editor_{selected_task_id}"
        fixed_key = f"fixed_code_{selected_task_id}"
        initial_code = st.session_state.get(fixed_key, default_code)

        # --- ACE EDITOR (LeetCode-style) ---
        st.markdown(
            """
            <style>
            .ace-editor-label {
                font-size: 0.85rem;
                color: #aaa;
                margin-bottom: 4px;
            }
            </style>
            <div class="ace-editor-label">📝 Trình soạn thảo Python (Tab = 4 spaces | Enter = tự căn lề):</div>
            """,
            unsafe_allow_html=True
        )
        student_code = st_ace(
            value=initial_code,
            language="python",
            theme="monokai",
            key=ace_key,
            height=320,
            font_size=14,
            tab_size=4,
            show_gutter=True,
            show_print_margin=False,
            wrap=False,
            auto_update=True,
            readonly=False,
            annotations=None,
            placeholder="Nhập mã nguồn Python tại đây...",
        )

        # Nút auto-fix + chấm bài
        col_fix, col_grade = st.columns([1, 2])
        with col_fix:
            if st.button("🔧 Auto-fix thụt lề",
                         help="Dùng autopep8 tự động sửa lỗi indentation khi paste code từ nơi khác"):
                try:
                    fixed = autopep8.fix_code(
                        student_code or "",
                        options={"aggressive": 1}
                    )
                    st.session_state[fixed_key] = fixed
                    st.success("✅ Đã căn lề xong! Editor sẽ cập nhật.")
                    st.rerun()
                except Exception as e:
                    st.error(f"❌ Không thể sửa: {e}")
        with col_grade:
            btn_grade = st.button("🚀 Bấm chấm bài (Grade Submission)", type="primary", use_container_width=True)

    with col2:
        st.subheader("📊 Kết quả chấm & Phản hồi sư phạm")
        
        if btn_grade:
            with st.spinner("Đang chạy kiểm thử an toàn bên trong Sandbox..."):
                # Gộp toàn bộ tests (3 public + các hidden tests v2)
                all_tests = current_task["public_tests"] + current_task["hidden_tests"]
                
                # Thực hiện chấm
                res = grade_submission(
                    code=student_code,
                    func_name=current_task["func_name"],
                    tests=all_tests,
                    test_set_name=f"Task {selected_task_id} Web Test",
                    fail_fast=fail_fast,
                    use_docker=use_docker
                )
                
            # Hiển thị kết quả tổng quan
            pass_cnt = res["pass_count"]
            total_cnt = res["total_count"]
            tpr = res["test_pass_rate"]
            
            if pass_cnt == total_cnt:
                st.success(f"### 🎉 ĐẠT YÊU CẦU: {pass_cnt}/{total_cnt} ({tpr}%)")
                st.balloons()
            else:
                st.error(f"### ❌ CHƯA ĐẠT: {pass_cnt}/{total_cnt} ({tpr}%)")
                
            # Diễn giải phản hồi sư phạm
            if pass_cnt == total_cnt:
                st.info("Mã nguồn của bạn đã vượt qua tất cả các test case và bảo mật an toàn. Xin chúc mừng!")
            else:
                st.markdown("#### 🔍 Chi tiết các test case bị lỗi:")
                
                # Duyệt qua các testcase lỗi
                fail_idx = 1
                for idx, r in enumerate(res["test_results"]):
                    if r["status"] == "PASS":
                        continue
                        
                    status = r["status"]
                    with st.expander(f"Lỗi #{fail_idx}: Testcase #{idx + 1} -> [{status}]", expanded=(fail_idx == 1)):
                        st.markdown(f"**📥 Tham số đầu vào**: `{r.get('input', 'N/A')}`")
                        st.markdown(f"**🎯 Kết quả mong đợi**: `{r['expected']}`")
                        st.markdown(f"**📤 Kết quả thực tế**: `{r.get('actual') if r.get('actual') is not None else 'N/A'}`")
                        
                        # Gợi ý phản hồi
                        sugg = SUGGESTIONS.get(status, SUGGESTIONS["RE"])
                        st.markdown(f"💡 **Gợi ý sửa lỗi**: *{sugg}*")
                        
                        # In traceback nếu có
                        if r.get("error_msg") and status not in ["WA", "SKIPPED"]:
                            st.warning(f"**Traceback chi tiết**:\n```\n{r['error_msg']}\n```")
                            
                    fail_idx += 1
        else:
            st.info("Viết mã nguồn của bạn ở ô bên trái rồi bấm nút '🚀 Bấm chấm bài' để nhận phản hồi tự động bằng tiếng Việt.")
            
# Footer bản quyền nhóm 67
st.markdown("---")
st.markdown("<center>Đồ án Tiến độ Tuần 4 - Nhóm 67 | Đại học Sài Gòn | 2026</center>", unsafe_allow_html=True)
