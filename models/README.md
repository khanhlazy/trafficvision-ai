# Hướng dẫn model

## Vị trí đặt weight
Đặt model detector đã huấn luyện tại:
```text
models/weights/best.pt
```

Đặt model semantic segmentation tại:
```text
models/weights/deeplabv3plus_road.pth
```

## Fallback pretrained model
Nếu có các file `yolo11s.pt`, `yolo11n.pt` hoặc `yolov8n.pt` trong `models/weights/`, hệ thống sẽ tự dùng làm fallback. Mặc định repo không tải model từ internet để CI và test chạy ổn định.

## Export ONNX
Model ONNX được lưu tại:
```text
models/exported/
```
Lệnh export:
```bash
python scripts/export_models.py --model models/weights/best.pt --format onnx
```

## Quy tắc Git
Không commit file model lớn như `.pt`, `.pth`, `.onnx`, `.engine`. Chỉ commit `.gitkeep` và tài liệu hướng dẫn.
