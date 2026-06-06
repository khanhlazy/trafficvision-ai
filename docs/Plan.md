# Plan.md

## Kế hoạch 10 tuần
| Tuần | Công việc | Deliverables | Rủi ro | Giảm thiểu | Vai trò | Trạng thái |
|---|---|---|---|---|---|---|
| 1 | Phân tích yêu cầu, scope | Project Definition, User Requirement | Scope quá rộng | Chốt must-have | BA, Writer | [x] |
| 2 | Thiết kế kiến trúc | Tech Solution, cấu trúc repo | Kiến trúc rối | Module nhỏ, interface rõ | AI, Backend | [x] |
| 3 | Chuẩn bị dataset | Dataset README, YAML | Dataset lớn/khó tải | Dùng sample và fallback | Data Engineer | [x] |
| 4 | Tích hợp YOLO detector | `detector.py`, script train | Thiếu GPU | Cho phép pretrained/fallback | AI Engineer | [x] |
| 5 | Thiết kế segmentation | `segmenter.py`, remap mask | Chưa có weight | Demo polygon ROI | CV Engineer | [x] |
| 6 | Pipeline OpenCV | `inference.py`, overlay, logs | Lỗi video codec | OpenCV fallback, test ảnh | CV, Backend | [x] |
| 7 | Streamlit UI | UI tiếng Việt | Text overlay tiếng Việt lỗi font | UI tiếng Việt, frame text không dấu | Backend | [x] |
| 8 | FastAPI và CLI | API, scripts predict/benchmark | Upload lỗi định dạng | Validate input rõ | Backend | [x] |
| 9 | Test và Docker/CI | pytest, Dockerfile, CI | CI thiếu GPU/internet | Test fallback offline | QA, DevOps | [x] |
| 10 | Hoàn thiện tài liệu | Test reports, defense checklist | Thiếu bằng chứng | Log mẫu, checklist | Writer, QA | [x] |

## Nguyên tắc thực hiện
- Ưu tiên chạy được end-to-end.
- Tách detection và semantic segmentation.
- Không commit dataset/model lớn.
- Tất cả tài liệu, log, báo cáo và commit message dùng tiếng Việt.
