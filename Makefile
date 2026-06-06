.PHONY: install run-ui run-api test predict-image predict-video benchmark docker-build docker-up

install:
	pip install -r requirements.txt

run-ui:
	streamlit run app/streamlit_app.py

run-api:
	uvicorn app.api:app --reload --host 0.0.0.0 --port 8000

test:
	pytest

predict-image:
	python scripts/predict_image.py datasets/samples/sample_road.jpg

predict-video:
	python scripts/create_sample_data.py
	python scripts/predict_video.py datasets/samples/sample_video.mp4 --max-frames 30

benchmark:
	python scripts/benchmark_fps.py --runs 20

docker-build:
	docker build -t traffic-ai-adas:latest .

docker-up:
	docker compose up --build
