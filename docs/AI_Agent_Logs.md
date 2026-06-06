# AI Agent Logs

## Mẫu log
| Trường | Nội dung |
|---|---|
| Date | Ngày trao đổi |
| Topic | Chủ đề |
| Prompt | Prompt đã dùng |
| AI response summary | Tóm tắt phản hồi AI |
| Decision | Quyết định |
| Reason | Lý do |
| Follow-up | Việc tiếp theo |

## Log 1: Requirement analysis
| Trường | Nội dung |
|---|---|
| Date | 2026-06-06 |
| Topic | Phân tích yêu cầu |
| Prompt | Xây dựng repository đồ án phát hiện phương tiện và phân vùng làn đường. |
| AI response summary | AI đề xuất kiến trúc module gồm detector, segmenter, tracking, overlay, logic, UI, API, docs và tests. |
| Decision | Chọn kiến trúc module hóa. |
| Reason | Dễ test, dễ thay model, phù hợp đồ án 2-3 tháng. |
| Follow-up | Tạo codebase và tài liệu. |

## Log 2: Model selection
| Trường | Nội dung |
|---|---|
| Date | 2026-06-06 |
| Topic | Chọn model |
| Prompt | Chọn model detection và segmentation phù hợp. |
| AI response summary | YOLO dùng cho detection; DeepLabV3+ dùng cho semantic road segmentation; có fallback demo khi thiếu weight. |
| Decision | Dùng YOLO11s nếu có, fallback YOLO11n/YOLOv8n/local/offline. |
| Reason | YOLO nhanh, phổ biến; semantic segmentation đúng bản chất phân vùng đường. |
| Follow-up | Huấn luyện custom khi có dataset. |

## Log 3: Dataset selection
| Trường | Nội dung |
|---|---|
| Date | 2026-06-06 |
| Topic | Chọn dataset |
| Prompt | Xác định dataset cho detection và segmentation. |
| AI response summary | BDD100K cho detection, Cityscapes cho semantic road mask, Roboflow cho dữ liệu biển báo Việt Nam. |
| Decision | Không commit dataset lớn, chỉ commit YAML và README. |
| Reason | Dataset lớn vượt giới hạn Git và giấy phép phân phối. |
| Follow-up | Tải dataset ngoài Git khi train thật. |

## Log 4: Test plan
| Trường | Nội dung |
|---|---|
| Date | 2026-06-06 |
| Topic | Kế hoạch kiểm thử |
| Prompt | Thiết kế test cho model và pipeline. |
| AI response summary | Tách model level, independent model, full pipeline, API, UI, performance và regression test. |
| Decision | Pytest offline bắt buộc pass bằng fallback/demo mode. |
| Reason | CI không có GPU, internet hoặc dataset lớn. |
| Follow-up | Bổ sung test report sau khi có kết quả model thật. |

## Log 5: README generation
| Trường | Nội dung |
|---|---|
| Date | 2026-06-06 |
| Topic | Tạo README |
| Prompt | Viết README tiếng Việt cho đồ án. |
| AI response summary | README gồm mô tả, mục tiêu, tính năng, công nghệ, cài đặt, chạy UI/API/test/train/export/logs và hạn chế. |
| Decision | README dùng tiếng Việt, lệnh dùng English CLI. |
| Reason | Phù hợp yêu cầu đồ án Việt Nam và vẫn dễ chạy kỹ thuật. |
| Follow-up | Cập nhật README khi có kết quả huấn luyện thật. |

## Log 6: Code continuation request
| Trường | Nội dung |
|---|---|
| Date | 2026-06-06 |
| Topic | Tiếp tục hoàn thiện repo hiện hữu |
| Prompt | Không viết lại từ đầu; audit repository, sửa phần thiếu, chuẩn hóa TrafficVision AI và giữ code đang chạy. |
| AI response summary | AI kiểm tra repo, xác định phần thiếu như Repository Audit, config mới, segmentation info, UI labels, logging helpers và docs cập nhật. |
| Decision | Hoàn thiện trên thư mục `traffic-ai-adas`, không đổi tên folder. |
| Reason | Đây là repo hiện hữu duy nhất trong workspace và đã có pipeline/test nền tảng. |
| Follow-up | Chạy pytest, kiểm tra CLI/UI/API và chuẩn bị commit tiếng Việt. |
