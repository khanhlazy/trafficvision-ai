# Computer Vision Skill

## Vai trò
Computer Vision Engineer chịu trách nhiệm xử lý ảnh/video, overlay, segmentation, tracking và đo FPS.

## Nhiệm vụ
- Xây dựng pipeline OpenCV.
- Thiết kế semantic segmentation interface.
- Tạo fallback polygon ROI.
- Vẽ box, mask, cảnh báo và FPS.
- Kiểm tra shape và chất lượng output.

## Kỹ năng cần có
- OpenCV.
- Semantic segmentation.
- Video processing.
- Tracking cơ bản.
- Hiểu tọa độ ảnh và ROI.

## Công việc trong dự án
- Phát triển `app/segmenter.py`.
- Phát triển `app/overlay.py`.
- Phát triển `app/tracking.py`.
- Hỗ trợ `app/inference.py`.
- Viết benchmark FPS.

## Deliverables
- Road mask output.
- Annotated frame.
- Video output.
- FPS metrics.
- Segmentation mode rõ ràng.

## Checklist hoàn thành
- [ ] Overlay giữ nguyên shape ảnh.
- [ ] Mask fallback tạo được vùng đường.
- [ ] Tracking gán track_id khi có object.
- [ ] Video writer lưu được output.
- [ ] UI hiển thị chế độ phân vùng demo khi thiếu weight.
