# Project Definition

## Project Name
TrafficVision AI - Hệ thống phát hiện phương tiện, biển báo giao thông và phân vùng làn đường bằng OpenCV và trí tuệ nhân tạo.

## Problem Statement
Camera giao thông và camera hành trình cần nhận biết phương tiện, người đi bộ, biển báo, đèn giao thông và vùng đường chạy để hỗ trợ cảnh báo an toàn. Bài toán yêu cầu một hệ thống AI có thể chạy thử trên ảnh, video, webcam, đồng thời đủ rõ ràng để trình bày trong đồ án tốt nghiệp.

## Business Understanding
Hệ thống mô phỏng một phần ADAS, giúp minh họa cách AI hỗ trợ nhận thức môi trường giao thông. Giá trị chính nằm ở khả năng cảnh báo sớm, trực quan hóa kết quả và đo hiệu năng pipeline.

## User Requirement
- Sinh viên có thể demo bằng ảnh/video/webcam.
- Giảng viên có thể xem tài liệu, test report và log.
- Người dùng không chuyên có thể dùng giao diện tiếng Việt.
- Hệ thống không bị lỗi khi thiếu custom model.

## Feature List
- Detection bằng YOLO.
- Semantic road/lane segmentation có fallback.
- Tracking đối tượng.
- Cảnh báo rule-based tiếng Việt.
- Streamlit UI.
- FastAPI image prediction.
- Logging JSON/CSV.
- Test, Docker, CI/CD.

## User vs Feature Mapping
| Nhóm người dùng | Nhu cầu | Tính năng |
|---|---|---|
| Sinh viên | Demo đồ án | Streamlit, predict image/video |
| Giảng viên | Đánh giá kỹ thuật | Docs, test report, logs |
| QA | Kiểm chứng chất lượng | pytest, smoke test, API test |
| DevOps | Triển khai | Docker, CI/CD |

## Scope
Hệ thống chạy local hoặc Docker, xử lý ảnh/video/webcam, phát hiện nhóm đối tượng giao thông, phân vùng đường/làn đường ở mức semantic/demo, lưu kết quả và tài liệu hóa đầy đủ.

## Out of Scope
- Điều khiển xe thật.
- Đảm bảo an toàn thời gian thực cấp công nghiệp.
- Huấn luyện đầy đủ DeepLabV3+ khi chưa có dataset/mask.
- Streaming nhiều camera phân tán.

## Success Criteria
- Chạy được khi không có custom weight.
- Test offline pass.
- UI tiếng Việt không crash.
- API `/health` và `/predict/image` hoạt động.
- Log inference được lưu.
- Tài liệu phục vụ bảo vệ đầy đủ.

## Deliverables
- Source code module hóa.
- Streamlit UI.
- FastAPI service.
- Scripts train/validate/export/predict.
- Docker, CI/CD.
- README và tài liệu đồ án.
- Test suite và report template.
