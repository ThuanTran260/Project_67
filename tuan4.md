**KẾ HOẠCH TUẦN 4**

**Thời gian:** 25/5-01/6/2026  
**Hạn nộp:** Thứ 7, ngày 30/5/2026  
**Chủ đề:** Tối ưu phương pháp chính, phân tích lỗi chuyên sâu và chuẩn bị sản phẩm gần hoàn chỉnh

Tuần 3, các nhóm đã được yêu cầu sửa lỗi tuần 2, hoàn thiện baseline, triển khai phương pháp chính, so sánh với baseline và phân tích lỗi. Báo cáo tuần 3 cũng bắt buộc có lịch sử làm việc, minh chứng cá nhân và bảng so sánh kết quả.

Sang tuần 4, các nhóm cần chuyển từ mức **"chạy được phương pháp chính"** sang mức **"tối ưu, giải thích được kết quả và chuẩn bị sản phẩm gần hoàn chỉnh"**. Tuần 4 không chỉ yêu cầu kết quả tốt hơn, mà còn yêu cầu pipeline ổn định, số liệu nhất quán, metric phù hợp, phân tích lỗi sâu hơn và có demo hoặc ví dụ chạy thử.

**1\. Mục tiêu tuần 4**

| **Mục tiêu**                 | **Yêu cầu**                                                                                    |
| ---------------------------- | ---------------------------------------------------------------------------------------------- |
| **Ổn định pipeline**         | Code/notebook phải chạy lại được từ đầu đến cuối, không bị lỗi đường dẫn hoặc thiếu file       |
| **Tối ưu phương pháp chính** | Tinh chỉnh tham số, xử lý mất cân bằng, chỉnh threshold, thêm đặc trưng hoặc cải thiện mô hình |
| **So sánh nhiều cấu hình**   | So sánh baseline, phương pháp chính tuần 3 và mô hình/cấu hình tối ưu tuần 4                   |
| **Chốt metric chính**        | Mỗi nhóm phải nêu rõ metric chính dùng để chọn mô hình tốt nhất                                |
| **Phân tích lỗi chuyên sâu** | Chỉ ra mẫu sai, lớp yếu, nhóm dữ liệu khó, nguyên nhân và hướng khắc phục                      |
| **Đánh giá tính thực tế**    | Báo thời gian chạy, khả năng triển khai, chi phí tính toán, hạn chế                            |
| **Chuẩn bị demo**            | Có notebook/script/giao diện đơn giản hoặc ví dụ chạy thử                                      |
| **Hoàn thiện báo cáo**       | Báo cáo tuần 4 phải gần giống bản tổng kết cuối, có bảng/hình đầy đủ                           |
| **Khóa số liệu chính thức**  | Các bảng metric, confusion matrix, hình vẽ và phần nhận xét phải dùng cùng một bộ số liệu      |

**2\. Mức hoàn thành tối thiểu và mức nâng cao**

Để tránh quá tải, tuần 4 chia thành hai mức yêu cầu.

| **Mức**          | **Yêu cầu**                                                                                                                                                   |
| ---------------- | ------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Bắt buộc**     | Pipeline chạy được; có bảng so sánh baseline - tuần 3 - tuần 4; có ít nhất một cải tiến; có phân tích lỗi; có demo hoặc ví dụ chạy thử; có minh chứng cá nhân |
| **Khuyến khích** | Cross-validation, external test, ablation study, nhiều mô hình nâng cao, giao diện demo, inference time, phân tích lỗi định lượng sâu                         |

Nếu mô hình tuần 4 **không tốt hơn tuần 3**, nhóm vẫn có thể được đánh giá tốt nếu giải thích được vì sao không cải thiện, chứng minh thí nghiệm chạy đúng và rút ra kết luận hợp lý.

**3\. Nội dung bắt buộc trong báo cáo tuần 4**

Báo cáo tuần 4 nên có cấu trúc như sau:

- Tóm tắt đề tài và mục tiêu tuần 4
- Lịch sử làm việc trong tuần 4
- Tóm tắt kết quả tuần 3 và vấn đề còn tồn tại
- Dữ liệu và pipeline xử lý cuối cùng
- Baseline và phương pháp chính đã triển khai
- Các cải tiến/tối ưu trong tuần 4
- Kết quả thực nghiệm và bảng so sánh
- Phân tích lỗi chuyên sâu
- Demo hoặc sản phẩm thử nghiệm
- Phân công, minh chứng cá nhân và khai báo sử dụng AI
- Kế hoạch tuần 5
- Tài liệu tham khảo

**4\. Yêu cầu về lịch sử làm việc tuần 4**

Mỗi nhóm phải có mục **Lịch sử làm việc trong tuần 4**.

| **Thời điểm** | **Thành viên thực hiện** | **Nội dung công việc**               | **Sản phẩm/minh chứng**               | **Trạng thái** |
| ------------- | ------------------------ | ------------------------------------ | ------------------------------------- | -------------- |
| 25-26/5       | Thành viên A             | Rà soát lỗi tuần 3, ổn định pipeline | pipeline_final.ipynb                  | Hoàn thành     |
| 26-28/5       | Thành viên B             | Tối ưu mô hình, thử tham số mới      | model_tuning.ipynb, metrics_week4.csv | Hoàn thành     |
| 28-29/5       | Thành viên C             | Phân tích lỗi và mẫu sai             | error_analysis.csv, hình minh họa     | Hoàn thành     |
| 29-30/5       | Cả nhóm                  | Chuẩn bị demo và báo cáo tuần 4      | demo.py, report_week4.docx            | Hoàn thành     |

Không ghi chung chung như **"làm mô hình"**, **"làm báo cáo"**, **"hoàn thành 100%"**. Phải có file, notebook, bảng kết quả, hình ảnh hoặc demo minh chứng cụ thể.

**5\. Yêu cầu kỹ thuật chung**

**5.1. Pipeline phải chạy lại được**

| **Nội dung**    | **Yêu cầu**                                                                     |
| --------------- | ------------------------------------------------------------------------------- |
| Dữ liệu đầu vào | Ghi rõ file dữ liệu, nguồn dữ liệu, số mẫu cuối cùng                            |
| Tiền xử lý      | Có mô tả các bước xử lý và file/notebook tương ứng                              |
| Mô hình         | Ghi rõ mô hình, tham số chính, random seed nếu có                               |
| Kết quả         | Metric trong báo cáo phải khớp với notebook/code                                |
| Output          | Bảng metric, confusion matrix, biểu đồ, file lỗi nên lưu trong thư mục results/ |
| Demo            | Có hướng dẫn chạy ngắn gọn                                                      |

Khuyến khích có thêm:

| **File**                         | **Vai trò**                          |
| -------------------------------- | ------------------------------------ |
| requirements.txt                 | Liệt kê thư viện cần cài             |
| README.md                        | Hướng dẫn chạy pipeline/demo         |
| config.yaml hoặc run_config.json | Ghi lại cấu hình thí nghiệm          |
| final_metrics.csv                | Bảng kết quả chính thức              |
| error_analysis.csv               | Danh sách mẫu sai dùng trong báo cáo |

**5.2. Phải chốt metric chính**

Mỗi nhóm phải ghi rõ **metric chính** dùng để chọn mô hình tốt nhất.

| **Loại đề tài**           | **Metric chính nên dùng**                              |
| ------------------------- | ------------------------------------------------------ |
| Phân loại cân bằng        | Accuracy, F1-score                                     |
| Phân loại mất cân bằng    | Macro-F1, F1 lớp thiểu số, Recall lớp quan trọng       |
| IDS / Phishing / DDoS     | Recall attack/phishing, FPR, F1, MCC, Confusion Matrix |
| Hồi quy                   | MAE, RMSE, R²                                          |
| Dự báo chuỗi thời gian    | MAE, RMSE, sMAPE, lỗi tại peak/valley                  |
| Object detection          | mAP50, mAP50-95, Precision, Recall theo lớp            |
| Retrieval / Visual Search | Recall@K, Precision@K, mAP, MRR                        |
| Calibration               | ECE, Brier Score, Reliability Diagram                  |
| Code grading              | FPR, số bài sai bị lọt, số bài đúng bị chấm sai        |
| Đạo văn code              | Precision, Recall, F1 lớp đạo văn, FP/FN cụ thể        |

Không chọn mô hình chỉ vì Accuracy cao nếu bài toán mất cân bằng hoặc có lớp quan trọng cần ưu tiên.

**5.3. Phải có một bộ số liệu chính thức**

Báo cáo tuần 4 chỉ nên dùng **một bộ kết quả chính thức**. Các số liệu trong bảng metric, confusion matrix, biểu đồ và phần nhận xét phải khớp nhau.

Nếu có nhiều lần chạy, nhóm phải ghi rõ:

| **Nội dung**     | **Cần ghi**                                                           |
| ---------------- | --------------------------------------------------------------------- |
| Run chính thức   | Run nào được chọn làm kết quả cuối                                    |
| Dữ liệu test     | Tập test nào được dùng                                                |
| Cấu hình mô hình | Tham số, seed, threshold                                              |
| Metric           | Cách tính metric và lớp nào là lớp dương                              |
| Ghi chú          | Nếu có external test/cross-validation, phải tách riêng với test chuẩn |

Các lỗi như **số mẫu không khớp**, **mapping nhãn bị đảo**, **bảng metric mâu thuẫn với confusion matrix** sẽ bị trừ nặng.

**6\. Bảng so sánh kết quả bắt buộc**

Mỗi nhóm cần có bảng so sánh ít nhất 3 mức:

| **Phương pháp**                | **Metric chính** | **Metric phụ** | **Ưu điểm**                      | **Hạn chế**     |
| ------------------------------ | ---------------- | -------------- | -------------------------------- | --------------- |
| Baseline tuần 2                |                  |                | Đơn giản, làm mốc so sánh        | Có thể còn yếu  |
| Phương pháp chính tuần 3       |                  |                | Đúng hướng đề tài                | Cần tối ưu      |
| Cấu hình/mô hình tối ưu tuần 4 |                  |                | Kết quả tốt hơn hoặc ổn định hơn | Vẫn còn hạn chế |

Ví dụ với bài toán phân loại:

| **Mô hình**              | **Accuracy** | **Precision** | **Recall** | **F1/Macro-F1** | **Nhận xét** |
| ------------------------ | ------------ | ------------- | ---------- | --------------- | ------------ |
| Baseline                 |              |               |            |                 |              |
| Phương pháp chính tuần 3 |              |               |            |                 |              |
| Mô hình tối ưu tuần 4    |              |               |            |                 |              |

Với hồi quy dùng MAE, RMSE, R². Với IDS dùng Recall, FPR, F1-score và Confusion Matrix. Với object detection dùng mAP50, mAP50-95, Precision, Recall.

**7\. Yêu cầu tối ưu hoặc cải tiến tuần 4**

Tuần 4 không chỉ chạy lại tuần 3. Mỗi nhóm phải có ít nhất **một cải tiến rõ ràng**.

| **Loại cải tiến**  | **Ví dụ**                                                          |
| ------------------ | ------------------------------------------------------------------ |
| Tối ưu tham số     | GridSearch, RandomSearch, chỉnh learning rate, số epoch, max_depth |
| Chỉnh threshold    | Tối ưu threshold theo F1, F2, Recall, Precision hoặc PR Curve      |
| Xử lý mất cân bằng | class_weight, oversampling, undersampling, focal loss              |
| Xử lý dữ liệu      | Làm sạch nhãn, xử lý outlier, thêm đặc trưng, kiểm tra leakage     |
| Thử mô hình khác   | Linear SVM, Random Forest, XGBoost, LightGBM, CNN, PhoBERT, CRNN   |
| Cải thiện đánh giá | Cross-validation, external test, domain split, per-class report    |
| Tăng tính ứng dụng | Demo notebook/script, giao diện nhỏ, đo inference time             |

Nếu cải tiến không làm tăng metric, nhóm phải giải thích nguyên nhân và rút ra kết luận.

**8\. Phân tích lỗi chuyên sâu**

Tuần 4 cần phân tích lỗi sâu hơn tuần 3. Mỗi nhóm phải có ví dụ cụ thể.

| **Loại đề tài**  | **Nội dung phân tích lỗi tuần 4**                             |
| ---------------- | ------------------------------------------------------------- |
| NLP              | 10-20 câu dự đoán sai, đặc biệt lớp yếu hoặc lớp thiểu số     |
| Ảnh              | 5-10 ảnh sai, lớp dễ nhầm, điều kiện ảnh khó                  |
| Object detection | Ảnh detect sai, vật thể nhỏ, lớp mAP thấp                     |
| IDS              | Attack bị bỏ sót, Benign bị báo động nhầm, FPR cao            |
| Hồi quy          | Mẫu sai số lớn nhất, phân tích theo nhóm/phân khúc            |
| Dự báo           | Khoảng thời gian dự báo sai nhiều, đỉnh/đáy không bắt được    |
| Visual search    | Query trả top-k sai, thiếu ảnh liên quan trong gallery        |
| Code grading     | Bài sai nhưng qua test, bài đúng bị chấm sai                  |
| Đạo văn code     | Cặp đạo văn bị bỏ lọt, cặp tự làm bị bắt oan                  |
| Calibration      | Nhóm xác suất nào bị lệch nhiều nhất trên Reliability Diagram |

Mục phân tích lỗi cần trả lời 4 câu hỏi:

- Mô hình sai ở đâu?
- Nguyên nhân có thể là gì?
- Nhóm đã thử cách sửa nào?
- Tuần 5 cần hoàn thiện điểm nào?

Khuyến khích có bảng mẫu lỗi:

| **Mẫu** | **Nhãn thật** | **Dự đoán** | **Xác suất/điểm số** | **Loại lỗi** | **Nguyên nhân** |
| ------- | ------------- | ----------- | -------------------- | ------------ | --------------- |
| Mẫu 1   |               |             |                      | FP/FN        |                 |
| Mẫu 2   |               |             |                      | FP/FN        |                 |

**9\. Demo hoặc sản phẩm thử nghiệm**

Tuần 4 mỗi nhóm cần chuẩn bị bản demo đơn giản. Demo chưa cần đẹp, nhưng phải chạy được và nhóm phải giải thích được.

| **Loại demo**    | **Ví dụ**                                    |
| ---------------- | -------------------------------------------- |
| Notebook demo    | Một cell nhập dữ liệu mẫu và in kết quả      |
| Script Python    | python predict.py --input sample.csv         |
| Giao diện nhỏ    | Streamlit hoặc Gradio nếu nhóm làm được      |
| NLP              | Nhập câu → dự đoán nhãn                      |
| Ảnh              | Upload ảnh → dự đoán lớp                     |
| Object detection | Upload ảnh → vẽ bounding box                 |
| Visual search    | Nhập ảnh query → trả top-k ảnh giống         |
| Code grading     | Nộp code → trả pass/fail và loại lỗi         |
| Đạo văn code     | Nhập 2 file .py → trả similarity và cảnh báo |
| IDS              | Nhập một flow → dự đoán Normal/Attack        |

Demo không được chỉ là hình minh họa. Phải có notebook/script/giao diện hoặc ví dụ chạy thử.

**10\. Nhắc nhở riêng theo từng đề tài**

| **Đề tài / nhóm đề tài**                 | **Nhắc nhở đặc thù tuần 4**                                                                                                                                                        |
| ---------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| **Phát hiện URL lừa đảo**                | Kiểm tra domain-level split và external/temporal test. So sánh DistilBERT với TF-IDF char n-gram + Linear SVM/Logistic Regression bằng F1, Recall, AUC, MCC và thời gian suy luận. |
| **Phân tích cảm xúc phản hồi sinh viên** | Tập trung cải thiện lớp Trung tính. Báo Macro-F1, Recall lớp Trung tính và Confusion Matrix. Nếu có phân loại chủ đề, phải có bảng topic riêng.                                    |
| **Fake News**                            | Phân tích top features để kiểm tra leakage. Thêm Title Only baseline. So sánh Text Only, Title Only và Title + Text.                                                               |
| **Spam Email / SMS Spam**                | Chốt lại bài toán là SMS hay Email. Tối ưu Recall lớp Spam, phân tích spam bị bỏ lọt, thử Complement NB, Logistic Regression và Linear SVM.                                        |
| **Dự đoán học tập sinh viên**            | So sánh bài toán 3 lớp với bài toán nhị phân "Cần cảnh báo" vs "Đạt". Ưu tiên Recall nhóm cần cảnh báo hơn Accuracy.                                                               |
| **Job Trend IT**                         | Bổ sung per-class F1, phân tích nhóm Other IT Role, thử Linear SVM/class_weight, thêm title và skill keywords.                                                                     |
| **Dự đoán nguy cơ rời bỏ từ review**     | Không gọi là churn thật nếu chưa có dữ liệu mua lại. Sửa tên thành tín hiệu bất mãn/nguy cơ rời bỏ tiềm ẩn. Tuần 4 phải thống nhất lại metric và Confusion Matrix.                 |
| **Bot Detection Twitter**                | Nếu tuần 3 đã sửa dữ liệu 2 lớp, tuần 4 mới tối ưu Random Forest/XGBoost. Nếu dữ liệu vẫn một lớp thì chưa được tối ưu mô hình, phải sửa dữ liệu trước.                            |
| **DDoS / Anomaly Detection**             | So sánh Isolation Forest/LOF/One-Class SVM với mô hình có giám sát. Báo Recall, FPR, F1, Confusion Matrix. Không dùng Accuracy làm metric chính.                                   |
| **Calibration IDS**                      | Tuần 4 phải có bảng Raw vs Platt vs Isotonic gồm Brier Score, ECE, Precision, Recall, F1. Có Reliability Diagram trước/sau hiệu chỉnh.                                             |
| **Dự đoán giá nhà**                      | Kiểm soát leakage từ price_per_m2, thử Ridge/Lasso/Random Forest/XGBoost. Phân tích sai số theo quận, phân khúc giá và loại bất động sản. Làm rõ đơn vị tiền.                      |
| **Dự báo tiêu thụ điện**                 | Đọc đúng dữ liệu đầy đủ, xác định horizon. So sánh Naive Lag-1, Seasonal Naive, Linear Regression, Random Forest/XGBoost trước khi dùng LSTM.                                      |
| **Nhận diện biển báo giao thông**        | Bổ sung per-class F1, confusion matrix, ảnh sai. Thử MobileNetV2 hoặc data augmentation có kiểm soát.                                                                              |
| **Rác thải YOLO**                        | Báo mAP50, mAP50-95, Precision, Recall theo lớp. Phân tích Glass/Paper/Metal. Thêm ảnh detect đúng/sai.                                                                            |
| **Visual Search sản phẩm**               | Nếu đã có FAISS, tuần 4 cần tập trung tăng chất lượng embedding: CLIP, image phash, title TF-IDF, image+text fusion. Báo Recall@K/mAP.                                             |
| **Tái cấu trúc vật thể 3D**              | Bổ sung hình input-ground truth-prediction. Mở rộng dữ liệu ngoài 256 mẫu chair. Làm rõ Chamfer Distance, F-score threshold và số điểm point cloud.                                |
| **Nhận dạng từ viết tay tiếng Anh**      | Tuần 4 phải có pipeline IAM thật: đọc words.txt, DataLoader ảnh từ, CRNN nhỏ, CTC Loss, CER/WER. Không chỉ tiếp tục EMNIST.                                                        |
| **Đạo văn code**                         | Tuần 4 cần chuyển từ Jaccard ký tự sang token similarity/AST similarity. Thử threshold tuning và phân tích FP/FN cụ thể.                                                           |
| **Automated Python Grading**             | Mở rộng MBPP, chuẩn hóa FPR, kiểm chứng hidden test, thêm sandbox cơ bản và bắt đầu sinh phản hồi tự động theo loại lỗi.                                                           |

**11\. Phân công và minh chứng cá nhân**

Mỗi nhóm cần nộp bảng phân công tuần 4.

| **Thành viên** | **Công việc đã làm**                    | **File/code/minh chứng**           | **Mức độ hoàn thành** |
| -------------- | --------------------------------------- | ---------------------------------- | --------------------- |
| Thành viên 1   | Tối ưu dữ liệu, xử lý lỗi, EDA bổ sung  | 01_data_pipeline.ipynb             | Hoàn thành            |
| Thành viên 2   | Tối ưu mô hình, tuning, so sánh kết quả | 02_model_tuning.ipynb, metrics.csv | Hoàn thành            |
| Thành viên 3   | Phân tích lỗi, demo, báo cáo            | 03_error_demo.ipynb, demo.py       | Hoàn thành            |

Không chấp nhận phân công chỉ ghi **"làm mục 1, 2, 3"** hoặc **"100%"** mà không có file minh chứng.

**12\. Cấu trúc thư mục nộp khuyến nghị**

Để dễ kiểm tra và chấm bài, mỗi nhóm nên nộp theo cấu trúc sau:

NhomXX_Tuan4/  
├── report/  
│ └── BaoCao_Tuan4_NhomXX.docx  
├── notebooks/  
│ ├── 01_data_pipeline.ipynb  
│ ├── 02_model_tuning.ipynb  
│ └── 03_error_analysis.ipynb  
├── src/  
│ └── predict.py  
├── demo/  
│ └── demo.py hoặc demo.ipynb  
├── results/  
│ ├── final_metrics.csv  
│ ├── confusion_matrix.png  
│ ├── error_analysis.csv  
│ └── figures/  
├── data_sample/  
│ └── sample_input.csv  
├── README.md  
└── requirements.txt

Không bắt buộc phải đúng hoàn toàn cấu trúc này, nhưng các file quan trọng phải dễ tìm.

**13\. Sản phẩm cần nộp vào thứ 7**

| **Thành phần**           | **Yêu cầu**                                         |
| ------------------------ | --------------------------------------------------- |
| Báo cáo tuần 4           | Có lịch sử làm việc, kết quả, tối ưu, phân tích lỗi |
| Notebook/code            | Chạy được từ đầu đến cuối                           |
| Bảng so sánh kết quả     | Baseline - phương pháp chính - mô hình tối ưu       |
| Biểu đồ/Confusion Matrix | Tùy đề tài                                          |
| Phân tích lỗi            | Có mẫu sai cụ thể                                   |
| Demo hoặc ví dụ chạy thử | Notebook/script/giao diện nhỏ                       |
| Minh chứng cá nhân       | File/code/notebook theo từng người                  |
| Khai báo AI              | Ghi rõ AI hỗ trợ phần nào                           |
| Tài liệu tham khảo       | Có nguồn dữ liệu, mô hình, phương pháp chính        |

**14\. Rubric đánh giá tuần 4**

| **Tiêu chí**                                          | **Tỷ trọng** | **Mô tả**                                                                          |
| ----------------------------------------------------- | ------------ | ---------------------------------------------------------------------------------- |
| **Ổn định dữ liệu và pipeline xử lý**                 | **15%**      | Dữ liệu đúng, không sai nhãn, pipeline chạy lại được, không lỗi đường dẫn          |
| **Tối ưu hoặc cải tiến phương pháp chính**            | **25%**      | Có ít nhất một cải tiến rõ, cấu hình mô hình rõ, có giải thích nếu không cải thiện |
| **So sánh kết quả với baseline và tuần 3**            | **15%**      | So sánh công bằng, cùng test set hoặc giải thích rõ nếu khác                       |
| **Metric phù hợp và bảng kết quả rõ ràng**            | **10%**      | Không chỉ dùng Accuracy; có metric phù hợp với đề tài                              |
| **Phân tích lỗi chuyên sâu**                          | **15%**      | Có mẫu lỗi cụ thể, nguyên nhân, cách sửa và hướng tuần 5                           |
| **Demo hoặc sản phẩm thử nghiệm**                     | **10%**      | Demo/notebook/script chạy được, có ví dụ input/output                              |
| **Lịch sử làm việc, minh chứng cá nhân, khai báo AI** | **10%**      | Có bảng công việc theo người, file minh chứng rõ, khai báo AI nếu có               |
| **Tổng**                                              | **100%**     |                                                                                    |

**15\. Quy định trừ điểm**

| **Lỗi**                                                   | **Mức xử lý** |
| --------------------------------------------------------- | ------------- |
| Code không chạy được                                      | Trừ nặng      |
| Không có bảng so sánh với baseline                        | Trừ nặng      |
| Không có cải tiến so với tuần 3                           | Trừ điểm      |
| Chỉ báo Accuracy                                          | Trừ điểm      |
| Không có phân tích lỗi                                    | Trừ điểm      |
| Không có demo hoặc ví dụ chạy thử                         | Trừ điểm      |
| Không có lịch sử làm việc                                 | Trừ điểm      |
| Không có minh chứng cá nhân                               | Trừ điểm      |
| Dữ liệu sai nhãn hoặc số mẫu không thống nhất             | Trừ rất nặng  |
| Metric trong báo cáo không khớp confusion matrix/notebook | Trừ nặng      |
| Dùng AI nhưng không khai báo                              | Trừ điểm      |
| Báo cáo có nhiều bảng số liệu mâu thuẫn                   | Trừ nặng      |

**16\. Lưu ý cuối**

Các nhóm nộp bài vào **thứ 7 hằng tuần**. Chủ nhật, giảng viên chấm bài, nhận xét và yêu cầu chỉnh sửa nếu cần. Thứ 2 tuần tiếp theo, giảng viên làm việc với từng nhóm để kiểm tra phần chỉnh sửa, đánh giá tiến độ và giao kế hoạch mới.

Báo cáo tuần 4 cần thể hiện rõ nhóm đã đi từ **baseline** đến **phương pháp chính**, sau đó đến **tối ưu/cải tiến**. Không chấp nhận báo cáo chỉ liệt kê kết quả mà không có so sánh, không phân tích lỗi và không có minh chứng công việc.

Tuần 4 là bước chuẩn bị trực tiếp cho tuần 5. Vì vậy, nhóm cần ưu tiên làm sạch số liệu, ổn định pipeline, hoàn thiện bảng so sánh, phân tích lỗi và chuẩn bị demo chạy được.