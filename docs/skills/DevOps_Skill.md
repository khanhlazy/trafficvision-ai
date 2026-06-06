# DevOps Skill

## Vai trò
DevOps Engineer chịu trách nhiệm môi trường chạy, Docker, Docker Compose, CI/CD và quy tắc không phụ thuộc GPU trong test.

## Nhiệm vụ
- Viết Dockerfile.
- Viết docker-compose.
- Tạo GitHub Actions.
- Đảm bảo test chạy offline.
- Quản lý `.gitignore`.

## Kỹ năng cần có
- Docker.
- GitHub Actions.
- Python packaging.
- CI troubleshooting.
- Quản lý biến môi trường.

## Công việc trong dự án
- Tạo `Dockerfile`.
- Tạo `docker-compose.yml`.
- Tạo `.github/workflows/ci.yml`.
- Tạo `.env.example`.
- Tạo `Makefile`.

## Deliverables
- Image API.
- Service Streamlit.
- CI chạy pytest.
- Docker build.
- Make commands.

## Checklist hoàn thành
- [ ] Docker expose 8000 và 8501.
- [ ] Compose mount `models/` và `outputs/`.
- [ ] CI dùng Python 3.11.
- [ ] CI không tải model lớn.
- [ ] `.gitignore` loại dataset/model/output lớn.
