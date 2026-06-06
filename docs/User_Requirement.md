# User Requirement

## Nhóm người dùng
- Sinh viên thực hiện đồ án.
- Giảng viên hướng dẫn/chấm phản biện.
- Người dùng demo không chuyên.
- Kỹ sư AI/CV mở rộng hệ thống.

## User stories
| ID | User story | Acceptance criteria |
|---|---|---|
| UR-01 | Là sinh viên, tôi muốn tải ảnh để xem kết quả phát hiện giao thông. | UI hiển thị ảnh đầu vào, ảnh kết quả, bảng đối tượng và cảnh báo. |
| UR-02 | Là sinh viên, tôi muốn xử lý video. | Video output được lưu và phát lại trong UI. |
| UR-03 | Là giảng viên, tôi muốn biết hệ thống có chạy khi thiếu model không. | Detector/segmenter fallback không crash, UI báo chế độ demo. |
| UR-04 | Là QA, tôi muốn chạy test offline. | `pytest` pass không cần GPU, internet, dataset lớn. |
| UR-05 | Là backend developer, tôi muốn gọi API dự đoán ảnh. | `/predict/image` trả predictions, warnings, processing time, model info. |
| UR-06 | Là người bảo vệ đồ án, tôi muốn có log và report. | `outputs/logs/` có JSON log, docs có test report template. |
