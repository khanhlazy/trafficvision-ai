# Full Pipeline Test Report

## End-to-end pipeline test
Pipeline cần kiểm tra đầy đủ các bước: OpenCV input, detector, segmenter, tracker, warning logic, overlay, output save và JSON log.

## Test cases
| ID | Input | Kỳ vọng | Trạng thái |
|---|---|---|---|
| FP-01 | Ảnh trắng sinh tự động | Không crash, có safe warning hoặc lane warning | [x] |
| FP-02 | Ảnh đường mẫu | Lưu ảnh output, log JSON | [ ] |
| FP-03 | Video ngắn | Lưu video output | [ ] |
| FP-04 | Thiếu model detector | Fallback mode, không crash | [x] |
| FP-05 | Thiếu model segmentation | Hiển thị chế độ phân vùng demo | [x] |

## Result checklist
- [ ] Ảnh/video output mở được.
- [ ] Bảng predictions đúng schema.
- [ ] Cảnh báo tiếng Việt đúng rule.
- [ ] Log có timestamp, FPS, processing time.
- [ ] UI không crash khi thiếu model.
