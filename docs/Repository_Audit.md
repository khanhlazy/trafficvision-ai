# Repository Audit

## Thông tin audit
- Ngày audit: 2026-06-06
- Thư mục kiểm tra: `traffic-ai-adas`
- Tên dự án mục tiêu: TrafficVision AI
- Nguyên tắc: không viết lại từ đầu, giữ code đang chạy được, chỉ bổ sung và sửa phần thiếu.

## Current folder tree
```text
traffic-ai-adas/
├── app/
│   ├── __init__.py
│   ├── api.py
│   ├── config.py
│   ├── detector.py
│   ├── inference.py
│   ├── logic.py
│   ├── logging_utils.py
│   ├── overlay.py
│   ├── schemas.py
│   ├── segmenter.py
│   ├── streamlit_app.py
│   └── tracking.py
├── scripts/
│   ├── benchmark_fps.py
│   ├── cli_utils.py
│   ├── convert_annotations.py
│   ├── create_sample_data.py
│   ├── export_models.py
│   ├── predict_image.py
│   ├── predict_video.py
│   ├── remap_cityscapes_masks.py
│   ├── train_detect.py
│   ├── train_semantic.py
│   └── validate_detect.py
├── tests/
│   ├── test_api.py
│   ├── test_config.py
│   ├── test_logic.py
│   ├── test_logs.py
│   ├── test_overlay.py
│   └── test_pipeline_smoke.py
├── datasets/
├── docs/
├── models/
├── outputs/
├── .github/workflows/ci.yml
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── Makefile
├── pyproject.toml
├── README.md
├── requirements.txt
├── LICENSE
└── CHANGELOG.md
```

## Existing files
Repo đã có các nhóm file chính: module AI trong `app/`, script CLI trong `scripts/`, test pytest trong `tests/`, tài liệu đồ án trong `docs/`, cấu hình dataset/model/output, Docker, Docker Compose, Makefile và CI.

## Missing files
- Trước audit chưa có `docs/Repository_Audit.md`.
- Cấu trúc file bắt buộc còn lại đã tồn tại.

## Broken imports
- Chạy `python -m pytest -q` trước khi hoàn thiện: pass 10 test.
- Không phát hiện import lỗi trong test hiện có.

## Missing dependencies
- `requirements.txt` đã có dependency chính: `ultralytics`, `opencv-python`, `streamlit`, `fastapi`, `uvicorn[standard]`, `pydantic`, `pydantic-settings`, `numpy`, `pandas`, `pillow`, `matplotlib`, `python-multipart`, `pytest`, `pytest-cov`, `tqdm`.
- Chưa cần thêm dependency mới.

## Missing docs
- README và docs chính đã có, nhưng cần cập nhật tên TrafficVision AI.
- `Commit_Guide.md` cần mở rộng lên ít nhất 30 ví dụ commit tiếng Việt.
- `Prompt_History.md` cần lưu continuation prompt hiện tại.
- `AI_Agent_Logs.md` cần thêm log “Code continuation request”.

## Missing tests
- Test hiện có phủ logic, overlay, API health, config, logs và smoke pipeline.
- Cần bổ sung kiểm tra literal tiếng Việt để phát hiện lỗi mojibake.
- Cần kiểm tra `segmentation_info` trong API health hoặc predict response.

## Missing logs
- Đã có `save_run_log`, `append_csv_log`, `save_warning_log`.
- Cần bổ sung `save_metrics_log` và `save_ai_agent_log_template` theo yêu cầu.

## Missing AI modules
- Detector, segmenter, tracker, inference đã tồn tại.
- Detector cần thêm `get_model_info()`.
- Segmenter cần thêm `get_segmenter_info()` và trường `is_fallback`.
- Pipeline cần trả `segmentation_info` rõ hơn.

## Missing UI features
- UI Streamlit đã có upload ảnh/video/webcam, bảng đối tượng, cảnh báo, FPS.
- Cần đổi nhãn sidebar theo chuẩn: “Bật phân vùng làn đường”, “Bật tracking”, “Chạy xử lý”.
- Cần hiển thị log path và ghi chú hạn chế khi dùng fallback.

## Missing API features
- API đã có `/health`, `/predict/image`, `/predict/video`.
- Cần dùng `API_TITLE` từ config.
- Cần trả thêm `segmentation_info` trong JSON.
- Cần chuẩn hóa thông báo tiếng Việt.

## Priority fix list

### P0: must fix to run
- Không có lỗi P0 tại thời điểm audit vì test hiện có pass và pipeline fallback chạy được.

### P1: must fix for core project
- Thêm config `MODEL_FALLBACK_NAME`, `STREAMLIT_UPLOAD_LIMIT_NOTE`, `API_TITLE`.
- Thêm `get_model_info()` và `get_segmenter_info()`.
- Trả `is_fallback` và `segmentation_info`.
- Sửa warning traffic sign/light thành “Thông tin: phát hiện biển báo hoặc đèn giao thông”.

### P2: should fix for graduation quality
- Cập nhật README/docs theo tên TrafficVision AI.
- Mở rộng commit guide lên ít nhất 30 ví dụ.
- Bổ sung AI logs và prompt history.
- Thêm test literal tiếng Việt và API segmentation info.

### P3: optional enhancement
- Thêm ByteTrack thật nếu môi trường có dependency và weight phù hợp.
- Thêm mô hình DeepLabV3+ thật khi có dataset/mask đã chuẩn hóa.
- Thêm dashboard thống kê cảnh báo theo thời gian.
