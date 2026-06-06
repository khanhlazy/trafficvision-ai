# Tech Solution

## YOLO detection
Detector dùng Ultralytics YOLO vì tốc độ tốt, API đơn giản và phù hợp phát hiện nhiều lớp giao thông. Thứ tự ưu tiên weight: `best.pt`, `yolo11s.pt`, `yolo11n.pt`, `yolov8n.pt`. Khi không có model local, hệ thống dùng fallback offline trả danh sách rỗng thay vì crash.

## DeepLabV3+ semantic segmentation
Module `LaneRoadSegmenter` được thiết kế theo hướng semantic segmentation: đầu vào là frame, đầu ra là mask road/drivable area và tỷ lệ vùng đường. Khi có `deeplabv3plus_road.pth`, nhóm có thể thay placeholder bằng loader PyTorch DeepLabV3+.

## OpenCV pipeline
OpenCV chịu trách nhiệm đọc ảnh/video/webcam, resize mask, blend overlay, vẽ bounding box, vẽ FPS, lưu ảnh và ghi video. Đây là lớp xử lý thị giác nền tảng, độc lập với UI.

## Streamlit
Streamlit dùng cho demo nhanh bằng tiếng Việt: upload ảnh/video, chỉnh confidence, bật/tắt segmentation/tracking, xem bảng đối tượng, cảnh báo và FPS.

## FastAPI
FastAPI cung cấp endpoint tích hợp backend: `/health`, `/predict/image`, `/predict/video` metadata placeholder. API trả JSON có predictions, warnings, processing time và model info.

## Docker
Dockerfile dùng Python 3.11 slim, cài OpenCV dependencies, expose 8000 và 8501. Docker Compose có hai service: API và Streamlit, mount `models/` và `outputs/`.

## ONNX/TensorRT
Script export hỗ trợ ONNX. Nếu TensorRT không có, script in hướng dẫn rõ ràng và không crash.

## Vì sao không dùng YOLO-seg làm lane segmentation chính
YOLO-seg là instance segmentation, phù hợp tách từng object. Vùng đường/làn đường là bài toán semantic segmentation theo pixel class, cần mô hình như DeepLabV3+, SegFormer hoặc U-Net. Vì vậy dự án tách detector YOLO và segmenter semantic để đúng bản chất kỹ thuật.
