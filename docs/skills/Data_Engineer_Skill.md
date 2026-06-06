# Data Engineer Skill

## Vai trò
Data Engineer chịu trách nhiệm tổ chức dataset, chuyển đổi annotation và chuẩn bị mask cho semantic segmentation.

## Nhiệm vụ
- Thiết kế layout dataset.
- Chuyển COCO-like annotation sang YOLO.
- Remap Cityscapes mask sang road mask.
- Quản lý dữ liệu lớn ngoài Git.
- Kiểm tra nhãn train/val.

## Kỹ năng cần có
- Dataset versioning.
- YOLO annotation format.
- COCO annotation.
- Semantic mask processing.
- Python scripting.

## Công việc trong dự án
- Viết `datasets/README.md`.
- Viết `datasets/bdd_custom_detect.yaml`.
- Viết `datasets/cityscapes_semantic.yaml`.
- Viết `scripts/convert_annotations.py`.
- Viết `scripts/remap_cityscapes_masks.py`.

## Deliverables
- Dataset guide.
- YAML config.
- Converted YOLO labels.
- Binary road masks.
- Sample data.

## Checklist hoàn thành
- [ ] Không commit dataset lớn.
- [ ] Có hướng dẫn layout YOLO.
- [ ] Có script convert annotation.
- [ ] Có script remap mask.
- [ ] Có sample nhỏ cho smoke test/demo.
