# Test Plan

## Model level test
Kiểm tra detector độc lập bằng script `validate_detect.py`, đo mAP, precision, recall, confusion matrix nếu Ultralytics cung cấp.

## Independent model test
Chạy model trên ảnh/video mẫu, không qua UI, bằng `predict_image.py` hoặc `predict_video.py` để xác nhận input/output.

## Full pipeline test
Chạy toàn bộ pipeline: đọc ảnh → detect → segment → track → warning → overlay → save log.

## API test
Kiểm tra `/health` trả `ok`, `/predict/image` xử lý ảnh hợp lệ và trả JSON có warnings/model_info.

## UI test
Kiểm tra Streamlit hiển thị tiếng Việt, upload ảnh/video, bật/tắt segmentation/tracking, hiển thị cảnh báo và FPS.

## Performance test
Chạy `benchmark_fps.py` để đo latency trung bình, FPS trung bình, min/max latency.

## Regression test
Chạy `pytest` sau mỗi thay đổi để đảm bảo logic cảnh báo, overlay, API, config, logging và pipeline smoke không lỗi.

## Test cases table
| ID | Nhóm test | Input | Kỳ vọng | Công cụ | Ưu tiên |
|---|---|---|---|---|---|
| TC-01 | Logic | Prediction `person` confidence cao | Có cảnh báo người đi bộ | pytest | P0 |
| TC-02 | Logic | Vehicle trong center-lower ROI | Có cảnh báo phương tiện trong vùng đường chạy | pytest | P0 |
| TC-03 | Logic | Traffic sign/light | Có thông tin biển báo hoặc đèn giao thông | pytest | P0 |
| TC-04 | Overlay | Ảnh rỗng và box mẫu | Ảnh output giữ nguyên shape | pytest | P1 |
| TC-05 | API | GET `/health` | Trả `status=ok`, `model_info`, `segmentation_info` | pytest | P0 |
| TC-06 | Config | Không có `.env` | Load default an toàn | pytest | P0 |
| TC-07 | Logs | Payload inference mẫu | Lưu JSON log UTF-8 | pytest | P1 |
| TC-08 | Pipeline smoke | Ảnh trắng generated | Không crash, dùng fallback segmentation | pytest | P0 |
| TC-09 | Independent model | Ảnh mẫu | CLI trả JSON kết quả | `predict_image.py` | P1 |
| TC-10 | Performance | Ảnh mẫu hoặc ảnh trắng | Có FPS/latency metrics | `benchmark_fps.py` | P2 |
