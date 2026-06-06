# Scope và Out of Scope

## In scope
- Xử lý ảnh, video, webcam.
- Phát hiện phương tiện, người đi bộ, biển báo, đèn giao thông.
- Phân vùng đường/làn đường dạng semantic hoặc demo fallback.
- Tracking cơ bản bằng IoU.
- Cảnh báo tiếng Việt.
- Streamlit UI, FastAPI, logs, metrics, tests.
- Docker và CI/CD không cần GPU.

## Out of scope
- Điều khiển xe thật.
- Xử lý real-time cấp sản phẩm thương mại.
- Huấn luyện model lớn trong CI.
- Lưu trữ dataset/model lớn trong Git.
- Nhận diện tất cả loại biển báo chi tiết theo luật Việt Nam.

## Assumptions
- Người dùng chạy local hoặc Docker.
- Có thể bổ sung weight vào `models/weights/`.
- Dữ liệu lớn được quản lý ngoài Git.

## Constraints
- Test phải chạy offline.
- UI phải bằng tiếng Việt.
- Documentation và commit message phải bằng tiếng Việt.
- Pipeline không được crash khi thiếu model.
