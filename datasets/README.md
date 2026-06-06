# Hướng dẫn dataset

## Bố cục dataset
Thư mục `datasets/` chỉ chứa cấu trúc, file cấu hình và dữ liệu mẫu nhỏ. Dataset thật có dung lượng lớn nên không commit vào Git.

```text
datasets/
├── raw/                 # Dữ liệu gốc tải từ BDD100K, Cityscapes, Roboflow
├── processed/           # Dữ liệu đã chuyển đổi sang YOLO hoặc mask semantic
├── samples/             # Ảnh/video mẫu nhỏ cho demo
├── bdd_custom_detect.yaml
└── cityscapes_semantic.yaml
```

## Vai trò BDD100K
BDD100K phù hợp cho bài toán giao thông đô thị, gồm ảnh/video đường phố, phương tiện, người đi bộ, đèn giao thông và điều kiện thời tiết khác nhau. Dự án dùng BDD100K làm nguồn chính cho detection nếu nhóm có quyền tải dataset.

## Vai trò Cityscapes
Cityscapes có nhãn semantic segmentation chất lượng cao cho road, sidewalk, vehicle, person. Dự án dùng Cityscapes để remap mask đường/làn đường phục vụ DeepLabV3+.

## Vai trò Roboflow custom dataset
Roboflow có thể dùng để bổ sung biển báo giao thông Việt Nam hoặc ảnh camera thực tế do nhóm tự thu thập, sau đó export sang YOLO format.

## YOLO format kỳ vọng
```text
datasets/processed/bdd_custom_detect/
├── images/
│   ├── train/
│   └── val/
├── labels/
│   ├── train/
│   └── val/
└── data.yaml
```

Mỗi file `.txt` trong `labels/` có định dạng:
```text
class_id x_center y_center width height
```
Tọa độ được chuẩn hóa trong khoảng 0 đến 1.

## Quy tắc Git
Không commit dataset lớn. Chỉ commit `.gitkeep`, README, file YAML và ảnh mẫu nhỏ nếu cần.
