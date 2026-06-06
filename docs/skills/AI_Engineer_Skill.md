# AI Engineer Skill

## Vai trò
AI Engineer chịu trách nhiệm lựa chọn model, tích hợp detector, cấu hình train/validate/export và đảm bảo hệ thống chạy được khi thiếu weight.

## Nhiệm vụ
- Tích hợp Ultralytics YOLO.
- Chuẩn bị script train và validate.
- Thiết kế fallback model.
- Xuất model sang ONNX.
- Theo dõi metrics model.

## Kỹ năng cần có
- Deep learning cơ bản.
- Object detection.
- Ultralytics YOLO.
- Đánh giá mAP, precision, recall.
- Tối ưu inference.

## Công việc trong dự án
- Phát triển `app/detector.py`.
- Viết `scripts/train_detect.py`.
- Viết `scripts/validate_detect.py`.
- Viết `scripts/export_models.py`.
- Cập nhật model level report.

## Deliverables
- Detector module.
- Training command.
- Validation metrics.
- ONNX export.
- Tài liệu lựa chọn model.

## Checklist hoàn thành
- [ ] Detector load được custom weight nếu có.
- [ ] Detector fallback không crash khi thiếu weight.
- [ ] Prediction schema có class, confidence, xyxy, area, center.
- [ ] Validate script lưu metrics JSON/CSV.
- [ ] Export script xử lý trường hợp thiếu TensorRT.
