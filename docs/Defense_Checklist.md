# Defense Checklist

## Câu hỏi kỹ thuật
- [ ] Vì sao tách detection và semantic segmentation?
- [ ] Vì sao YOLO phù hợp cho phát hiện phương tiện?
- [ ] Vì sao OpenCV vẫn cần thiết khi đã có YOLO?
- [ ] Vì sao dùng Streamlit cho demo và FastAPI cho tích hợp backend?
- [ ] Vì sao không dùng YOLO-seg làm phân vùng làn đường chính?
- [ ] Model level test là gì?
- [ ] Independent model test là gì?
- [ ] Full pipeline test là gì?
- [ ] Fallback mode dùng để làm gì?
- [ ] Hạn chế lớn nhất của hệ thống hiện tại là gì?
- [ ] Có thể cải thiện bằng dữ liệu Việt Nam như thế nào?
- [ ] ONNX/TensorRT giúp gì cho triển khai?

## Checklist demo
- [ ] Chạy được `pytest`.
- [ ] Chạy được Streamlit.
- [ ] Upload ảnh và xem kết quả.
- [ ] Chỉ ra chế độ mô hình detector.
- [ ] Chỉ ra chế độ phân vùng demo/semantic.
- [ ] Mở JSON log sau một lần suy luận.
- [ ] Giải thích warning rule bằng tiếng Việt.
