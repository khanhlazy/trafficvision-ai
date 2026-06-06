# TrafficVision AI - Hệ thống phát hiện phương tiện, biển báo giao thông và phân vùng làn đường bằng OpenCV và trí tuệ nhân tạo

## Mô tả dự án
Dự án xây dựng hệ thống mô phỏng ADAS phục vụ đồ án tốt nghiệp: nhận ảnh, video hoặc webcam; phát hiện phương tiện, người đi bộ, biển báo, đèn giao thông; phân vùng vùng đường/làn đường; tracking đối tượng; sinh cảnh báo tiếng Việt; hiển thị kết quả bằng Streamlit và cung cấp API FastAPI.

## Mục tiêu
- Xây dựng pipeline computer vision dạng module, dễ thay model.
- Dùng OpenCV cho đọc/ghi ảnh-video, overlay, FPS và xử lý khung hình.
- Dùng Ultralytics YOLO cho phát hiện đối tượng giao thông.
- Thiết kế module semantic segmentation cho đường/làn đường, có chế độ demo fallback khi chưa có weight.
- Có test, log, Docker, CI/CD và tài liệu đầy đủ bằng tiếng Việt.

## Tính năng
- Nhận đầu vào: ảnh, video, webcam.
- Phát hiện: car, motorcycle, bus, truck, person, traffic sign, traffic light.
- Phân vùng vùng đường bằng semantic segmentation placeholder hoặc polygon ROI demo.
- Tracking nhẹ bằng IoU fallback.
- Cảnh báo rule-based bằng tiếng Việt.
- Streamlit UI tiếng Việt.
- FastAPI endpoint `/health`, `/predict/image`, `/predict/video`.
- Lưu ảnh/video/log/metrics/report.
- Test offline không cần GPU, internet hoặc dataset lớn.

## Business Understanding
TrafficVision AI mô phỏng một phần hệ thống hỗ trợ lái xe nâng cao. Giá trị của dự án là chứng minh luồng nhận thức thị giác máy tính: camera đầu vào, AI inference, phân vùng vùng đường, tracking, cảnh báo rule-based và ghi log phục vụ đánh giá.

## User Requirement
- Người dùng có thể tải ảnh/video hoặc chạy webcam để xem kết quả.
- Giao diện hiển thị hoàn toàn bằng tiếng Việt.
- API trả JSON cho tích hợp backend.
- Hệ thống không crash khi thiếu YOLO weight hoặc segmentation weight.
- Test chạy được trên máy không có GPU.

## Feature List
- Detection branch: YOLO phát hiện phương tiện, người đi bộ, biển báo và đèn giao thông.
- Segmentation branch: semantic road/drivable-area interface; fallback demo polygon ROI khi thiếu weight.
- OpenCV overlay: box, tracking ID, mask, FPS và cảnh báo.
- Rule engine: sinh cảnh báo tiếng Việt từ output AI.
- Logging: JSON/CSV/Markdown trong `outputs/logs/`.

## Công nghệ sử dụng
Python 3.11, OpenCV, Ultralytics YOLO, Streamlit, FastAPI, Pydantic, NumPy, Pandas, pytest, Docker, GitHub Actions.

## Kiến trúc hệ thống
TrafficVision AI dùng pipeline hai nhánh:
- Detection branch: YOLO phát hiện traffic objects.
- Segmentation branch: semantic segmentation cho road/drivable area; nếu thiếu weight thì dùng demo polygon ROI.

Luồng tổng quát: input OpenCV → detector YOLO → segmenter semantic/demo → tracker → rule warning engine → overlay OpenCV → Streamlit/API/output/log.

## Data Flow
1. OpenCV đọc ảnh, video hoặc webcam.
2. Detector trả danh sách `class_name`, `confidence`, `xyxy`, `area`, `center_x`, `center_y`.
3. Segmenter trả `mask`, `segmentation_mode`, `road_area_ratio`, `is_fallback`.
4. Tracker gán `track_id` nếu bật tracking.
5. Rule engine sinh cảnh báo tiếng Việt.
6. Overlay vẽ kết quả và pipeline lưu output/log.

## Cấu trúc thư mục
```text
traffic-ai-adas/
├── app/                  # Mã nguồn ứng dụng
├── scripts/              # Script train, validate, predict, benchmark
├── tests/                # Pytest offline
├── datasets/             # Cấu trúc dataset và hướng dẫn
├── models/               # Nơi đặt weight và model export
├── outputs/              # Ảnh, video, logs, metrics, reports
├── docs/                 # Tài liệu đồ án tiếng Việt
├── .github/workflows/    # CI/CD
├── Dockerfile
├── docker-compose.yml
├── Makefile
└── README.md
```

## Cài đặt
```bash
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python scripts/create_sample_data.py
```

Trên Windows PowerShell:
```powershell
python -m venv .venv
.venv\Scripts\Activate.ps1
pip install -r requirements.txt
python scripts/create_sample_data.py
```

## Chạy Streamlit
```bash
streamlit run app/streamlit_app.py
```
Giao diện hiển thị bằng tiếng Việt tại `http://localhost:8501`.

## Chạy FastAPI
```bash
uvicorn app.api:app --reload --host 0.0.0.0 --port 8000
```
Kiểm tra: `http://localhost:8000/health`.

## Chạy test
```bash
pytest
```
Test dùng fallback/demo mode nên không cần tải model lớn.

## Test 2 đợt
- Đợt 1: model-level và independent model test bằng `validate_detect.py`, `predict_image.py`, `predict_video.py`.
- Đợt 2: full pipeline/API/UI/regression test bằng `pytest`, Streamlit và FastAPI.

## Train model
```bash
python scripts/train_detect.py --data datasets/bdd_custom_detect.yaml --model yolo11s.pt --epochs 50
```
Sau huấn luyện, đặt `best.pt` vào `models/weights/best.pt`.

## Validate model
```bash
python scripts/validate_detect.py --model models/weights/best.pt --data datasets/bdd_custom_detect.yaml
```
Metrics được lưu ở `outputs/metrics/`.

## Export ONNX
```bash
python scripts/export_models.py --model models/weights/best.pt --format onnx
```
Model export được lưu ở `models/exported/`.

## Logs
Pipeline lưu JSON log tại `outputs/logs/`, gồm timestamp, input, model, confidence, predictions, warnings, FPS, thời gian xử lý và chế độ phân vùng.

## Tài liệu quan trọng
- Audit repo: `docs/Repository_Audit.md`
- Định nghĩa dự án: `docs/Project_Definition.md`
- Kế hoạch: `docs/Plan.md`
- Kế hoạch test: `docs/Test_Plan.md`
- AI logs: `docs/AI_Agent_Logs.md`
- Commit guide: `docs/Commit_Guide.md`

## Hạn chế
- Không thay thế hệ thống ADAS thật trên xe.
- Chưa có weight semantic segmentation trong repo vì file lớn.
- YOLO pretrained có thể chưa tối ưu cho biển báo giao thông Việt Nam.
- Demo fallback phân vùng đường chỉ là ROI hình học.

## Hướng phát triển
- Huấn luyện YOLO bằng BDD100K/Roboflow custom.
- Huấn luyện DeepLabV3+ cho road/drivable area.
- Thêm ByteTrack/StrongSORT đầy đủ.
- Tối ưu ONNX/TensorRT.
- Thêm dashboard thống kê cảnh báo theo thời gian.

## Câu hỏi bảo vệ đồ án
- Vì sao tách detection và semantic segmentation?
- Vì sao chọn YOLO thay vì Faster R-CNN?
- Vì sao không dùng YOLO-seg làm module chính cho làn đường?
- Fallback mode có ý nghĩa gì trong triển khai?
- Model level test khác full pipeline test như thế nào?

## Vietnamese commit guide
Ví dụ:
```bash
git commit -m "docs: bổ sung audit repository và định nghĩa dự án"
git commit -m "feat: hoàn thiện pipeline phát hiện giao thông bằng YOLO"
git commit -m "test: bổ sung kiểm thử model level và pipeline smoke"
```
