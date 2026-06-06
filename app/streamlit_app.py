"""Vietnamese Streamlit interface."""

from __future__ import annotations

import tempfile
import time
from pathlib import Path

import cv2
import numpy as np
import pandas as pd
import streamlit as st

from app.config import get_settings
from app.inference import TrafficAIPipeline


st.set_page_config(page_title="Hệ thống AI giao thông", layout="wide")


@st.cache_resource
def load_pipeline() -> TrafficAIPipeline:
    return TrafficAIPipeline(settings=get_settings())


def bgr_to_rgb(image):
    return cv2.cvtColor(image, cv2.COLOR_BGR2RGB)


def predictions_to_vietnamese_table(predictions: list[dict]) -> pd.DataFrame:
    rows = []
    for pred in predictions:
        rows.append(
            {
                "Loại đối tượng": pred.get("class_name"),
                "Độ tin cậy": round(float(pred.get("confidence", 0.0)), 3),
                "Tọa độ hộp": [round(float(v), 1) for v in pred.get("xyxy", [])],
                "Diện tích": round(float(pred.get("area", 0.0)), 1),
                "Mã tracking": pred.get("track_id"),
            }
        )
    return pd.DataFrame(rows)


st.title("Hệ thống phát hiện phương tiện, biển báo và làn đường")

settings = get_settings()
pipeline = load_pipeline()

with st.sidebar:
    mode = st.radio("Chọn chế độ xử lý", ["Ảnh", "Video", "Webcam"])
    conf = st.slider("Ngưỡng confidence", 0.05, 0.95, float(settings.default_conf), 0.05)
    enable_segmentation = st.toggle("Bật phân vùng làn đường", value=settings.enable_segmentation)
    enable_tracking = st.toggle("Bật tracking", value=settings.enable_tracking)
    save_result = st.toggle("Lưu kết quả", value=True)
    run_processing = st.button("Chạy xử lý", type="primary")

pipeline.settings.enable_segmentation = enable_segmentation
pipeline.settings.enable_tracking = enable_tracking

st.caption(f"Chế độ mô hình: {pipeline.detector.model_mode}")
st.caption(f"Chế độ phân vùng: {pipeline.segmenter.segmentation_mode}")
st.caption(settings.streamlit_upload_limit_note)

if pipeline.detector.get_model_info()["is_fallback"]:
    st.warning("Đang dùng chế độ detector fallback vì chưa tìm thấy weight YOLO local.")
if pipeline.segmenter.get_segmenter_info()["is_fallback"]:
    st.info("Đang dùng chế độ phân vùng demo bằng polygon ROI.")

if mode == "Ảnh":
    uploaded_image = st.file_uploader("Tải ảnh lên", type=["jpg", "jpeg", "png", "bmp"])
    if uploaded_image is not None:
        file_bytes = uploaded_image.read()
        image_array = cv2.imdecode(np.frombuffer(file_bytes, dtype="uint8"), cv2.IMREAD_COLOR)
        if image_array is None:
            st.error("Không thể đọc ảnh đã tải lên.")
        elif run_processing:
            started = time.perf_counter()
            result = pipeline.process_image(image_array, conf=conf, save_output=save_result)
            elapsed = time.perf_counter() - started

            col_input, col_output = st.columns(2)
            with col_input:
                st.subheader("Ảnh đầu vào")
                st.image(bgr_to_rgb(image_array), use_container_width=True)
            with col_output:
                st.subheader("Kết quả đã chú thích")
                st.image(bgr_to_rgb(result["annotated_image"]), use_container_width=True)

            st.subheader("Danh sách đối tượng phát hiện")
            table = predictions_to_vietnamese_table(result["predictions"])
            if table.empty:
                st.info("Chưa phát hiện đối tượng giao thông trong ảnh.")
            else:
                st.dataframe(table, use_container_width=True)

            st.subheader("Cảnh báo")
            for warning in result["warnings"]:
                if warning.startswith("Cảnh báo"):
                    st.warning(warning)
                elif warning.startswith("Thông tin"):
                    st.info(warning)
                else:
                    st.success(warning)

            metric_cols = st.columns(4)
            metric_cols[0].metric("FPS", f"{result['fps']:.2f}")
            metric_cols[1].metric("Thời gian xử lý", f"{elapsed:.3f} giây")
            metric_cols[2].metric("Chế độ mô hình", pipeline.detector.model_mode)
            metric_cols[3].metric("Phân vùng", result["segmentation_mode"])
            st.subheader("Thông tin mô hình")
            st.dataframe(
                pd.DataFrame(
                    [
                        {"Thông tin": "Mô hình phát hiện", "Giá trị": result["model_info"]["detector_model"]},
                        {"Thông tin": "Chế độ phát hiện", "Giá trị": result["model_info"]["detector_mode"]},
                        {"Thông tin": "Chế độ phân vùng", "Giá trị": result["segmentation_info"]["segmentation_mode"]},
                        {"Thông tin": "Tỷ lệ vùng đường", "Giá trị": result["segmentation_info"]["road_area_ratio"]},
                        {"Thông tin": "Fallback phân vùng", "Giá trị": result["segmentation_info"]["is_fallback"]},
                    ]
                ),
                use_container_width=True,
            )
            if result.get("output_path"):
                st.success(f"Đã lưu kết quả: {result['output_path']}")
            if result.get("log_path"):
                st.info(f"Log suy luận: {result['log_path']}")
        else:
            st.subheader("Ảnh đầu vào")
            st.image(bgr_to_rgb(image_array), use_container_width=True)

elif mode == "Video":
    uploaded_video = st.file_uploader("Tải video lên", type=["mp4", "avi", "mov", "mkv"])
    if uploaded_video is not None and run_processing:
        suffix = Path(uploaded_video.name).suffix or ".mp4"
        with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as temp_file:
            temp_file.write(uploaded_video.read())
            temp_path = temp_file.name
        with st.spinner("Đang xử lý video..."):
            result = pipeline.process_video(temp_path, conf=conf, max_frames=None)
        st.success("Đã xử lý video.")
        st.video(result["output_path"])
        st.metric("FPS trung bình", f"{result['fps']:.2f}")
        st.metric("Số khung hình", result["frame_count"])
        st.write("Cảnh báo cuối cùng:")
        for warning in result["warnings"]:
            if warning.startswith("Cảnh báo"):
                st.warning(warning)
            elif warning.startswith("Thông tin"):
                st.info(warning)
            else:
                st.success(warning)
        st.write(f"Chế độ phân vùng: {result['segmentation_info']['segmentation_mode']}")
        if result.get("log_path"):
            st.info(f"Log suy luận: {result['log_path']}")

else:
    st.info("Chế độ webcam cần chạy trên máy có camera. Nhấn nút bên dưới để xử lý thử một phiên ngắn.")
    if run_processing:
        try:
            result = pipeline.process_webcam(0, max_frames=120)
            st.success("Đã xử lý webcam.")
            st.video(result["output_path"])
        except Exception as exc:
            st.error(f"Không thể mở webcam: {exc}")
