# Feature Analysis

| Feature | Priority | Input | Output | Logic | Test case |
|---|---|---|---|---|---|
| Tải ảnh | Must-have | JPG/PNG/BMP | Ảnh chú thích | OpenCV decode | Smoke test pipeline |
| Tải video | Must-have | MP4/AVI/MOV | Video output | Đọc từng frame | CLI predict video |
| Webcam | Should-have | Camera ID | Video output | OpenCV capture | Demo thủ công |
| YOLO detection | Must-have | Frame BGR | Predictions | Ultralytics hoặc fallback | Pipeline smoke |
| Semantic segmentation | Must-have | Frame BGR | Mask road | DeepLabV3+ placeholder/demo ROI | Shape/mode check |
| Tracking | Should-have | Predictions | Track ID | IoU fallback | Unit test mở rộng |
| Cảnh báo tiếng Việt | Must-have | Predictions, mask ratio | Warning list | Rule engine | `test_logic.py` |
| Overlay OpenCV | Must-have | Frame, box, mask | Frame chú thích | Draw box/mask/FPS | `test_overlay.py` |
| FastAPI | Must-have | Upload image | JSON response | Pipeline image | `test_api.py` |
| Logging | Must-have | Pipeline result | JSON/CSV | Sanitized save | `test_logs.py` |
| Docker/CI | Should-have | Source code | Image/test status | Build no GPU | GitHub Actions |
