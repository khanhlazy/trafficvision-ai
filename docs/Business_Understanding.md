# Business Understanding

## Context
Hệ thống giao thông hiện đại sử dụng camera để nhận biết môi trường xung quanh. Trong bối cảnh đồ án tốt nghiệp, một hệ thống mô phỏng ADAS giúp sinh viên chứng minh kiến thức AI, computer vision, backend và triển khai.

## Business problem
Người lái hoặc hệ thống hỗ trợ cần biết có người đi bộ, phương tiện, biển báo, đèn giao thông hoặc vùng đường không rõ ràng phía trước. Nếu thông tin này được phát hiện và cảnh báo sớm, trải nghiệm an toàn có thể được cải thiện.

## Why AI/OpenCV
YOLO phù hợp cho phát hiện đối tượng thời gian gần thực. Semantic segmentation phù hợp cho vùng đường/làn đường. OpenCV cung cấp công cụ ổn định cho xử lý ảnh/video, overlay và đo FPS.

## ADAS simulation value
Dự án không điều khiển xe thật nhưng minh họa pipeline nhận thức môi trường: camera input, AI inference, tracking, cảnh báo và log.

## Limitations
- Không có chứng nhận an toàn.
- Kết quả phụ thuộc dataset và điều kiện ánh sáng.
- Fallback segmentation chỉ phục vụ demo.
- Model pretrained quốc tế có thể thiếu đặc thù biển báo Việt Nam.
