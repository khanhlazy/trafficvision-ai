# Prompt History

## Prompt chính ngày 2026-06-06
Người dùng yêu cầu xây dựng repository đồ án tốt nghiệp tên **Traffic Object Detection and Lane/Road Segmentation System using OpenCV and AI** với các yêu cầu chính:

- Giao diện người dùng phải bằng tiếng Việt.
- README, Project Definition, Plan.md, skill documents, AI logs, test reports và commit messages phải bằng tiếng Việt.
- Python 3.11, OpenCV, Ultralytics YOLO, semantic segmentation cho road/lane, Streamlit, FastAPI, pytest, Docker và GitHub Actions.
- Repo phải module hóa, không dồn vào một file.
- Hệ thống phải chạy được khi thiếu custom model bằng YOLO/local/offline fallback và segmentation demo fallback.
- Cần có scripts train, validate, export, predict, benchmark, convert annotations, remap masks và create sample data.
- Cần có tests cho logic, overlay, API, config, logs và pipeline smoke.
- Cần có tài liệu đầy đủ phục vụ bảo vệ đồ án.

## Prompt vận hành
Tạo mã nguồn, test, tài liệu và cấu hình triển khai theo thứ tự logic; không bỏ qua docs, tests, UI tiếng Việt, logs, skill files hoặc commit guide.

## Prompt tiếp tục ngày 2026-06-06
Người dùng yêu cầu hoàn thiện repo hiện hữu theo tên **TrafficVision AI**, không viết lại từ đầu, giữ thư mục `traffic-ai-adas`, tạo `docs/Repository_Audit.md`, bổ sung config/API/schema, hoàn thiện detector/segmenter/tracking/logic/overlay/logging/inference, cập nhật Streamlit UI tiếng Việt, scripts, tests, docs, DevOps và chạy validation.

## Cách sử dụng prompt
- Prompt chính dùng để dựng nền tảng đồ án.
- Prompt tiếp tục dùng để audit, chuẩn hóa và hoàn thiện phần thiếu trên repository hiện hữu.
- Các quyết định quan trọng được ghi lại trong `docs/AI_Agent_Logs.md`.
