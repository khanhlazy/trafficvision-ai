# Independent Model Test Report

## Mục tiêu
Kiểm tra model độc lập ngoài UI để xác nhận weight, config và output hoạt động.

## Lệnh chạy
```bash
python scripts/predict_image.py datasets/samples/sample_road.jpg --conf 0.35
python scripts/predict_video.py path/to/video.mp4 --conf 0.35 --max-frames 100
```

## Expected outputs
- JSON in ra console có `predictions`, `warnings`, `model_info`.
- Ảnh kết quả lưu trong `outputs/images/`.
- Video kết quả lưu trong `outputs/videos/`.
- Log lưu trong `outputs/logs/`.

## Checklist
- [ ] Model load thành công hoặc fallback rõ ràng.
- [ ] Không crash khi ảnh không có đối tượng.
- [ ] Confidence threshold ảnh hưởng số lượng prediction.
- [ ] Output có timestamp.
