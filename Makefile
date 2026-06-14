.PHONY: docker-build docker-up docker-down docker-logs docker-verify

docker-build:
	docker compose build

docker-up:
	docker compose up --build -d

docker-down:
	docker compose down

docker-logs:
	docker compose logs -f industrial-health-api

docker-verify:
	curl -fsS http://127.0.0.1:8010/health
	curl -fsS http://127.0.0.1:8010/model-info
	python3 scripts/sample_predict.py
