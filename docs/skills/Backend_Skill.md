# Backend Skill

## Vai trò
Backend Developer chịu trách nhiệm FastAPI, schema, cấu hình, logging và tích hợp pipeline cho service.

## Nhiệm vụ
- Thiết kế API endpoint.
- Validate file upload.
- Trả response JSON rõ ràng.
- Quản lý cấu hình qua environment variables.
- Lưu log inference.

## Kỹ năng cần có
- FastAPI.
- Pydantic.
- REST API.
- Error handling.
- JSON logging.

## Công việc trong dự án
- Phát triển `app/api.py`.
- Phát triển `app/schemas.py`.
- Phát triển `app/config.py`.
- Phát triển `app/logging_utils.py`.
- Viết test API.

## Deliverables
- `/health`.
- `/predict/image`.
- `/predict/video` metadata placeholder.
- APIResponse schema.
- JSON logs.

## Checklist hoàn thành
- [ ] `/health` trả `status=ok`.
- [ ] Upload ảnh lỗi trả thông báo tiếng Việt.
- [ ] Response có predictions, warnings, processing_time.
- [ ] Config có default an toàn.
- [ ] Log không lưu ndarray trực tiếp.
