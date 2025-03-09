install:
	uv sync

install-prod:
	uv sync --no-dev

lint:
	uv run ruff check python_dev_questionnaire

test:
	uv run pytest

test-cov:
	uv run pytest --cov=python_dev_questionnaire --cov-report=xml --cov-report=html

shell:
	uv run python manage.py shell_plus

static:
	uv run python manage.py collectstatic --noinput

createsuperuser:
	uv run python manage.py createsuperuser --noinput

migrations:
	uv run python manage.py makemigrations

migrate:
	uv run python manage.py migrate

dev:
	uv run python manage.py runserver 0.0.0.0:$${PORT:-5050}

build:
	./build.sh

start:
	uv run gunicorn -w 5 -b 0.0.0.0:$${PORT:-8000} python_dev_questionnaire.wsgi

docker-build-dev:
	TARGET=development docker compose build

docker-build-prod:
	TARGET=production docker compose build

docker-start-dev:
	TARGET=development docker compose up

docker-start-prod:
	TARGET=production docker compose up

.PHONY: install install-prod lint test test-cov shell static createsuperuser migrations migrate dev build start \
				docker-build-dev docker-build-prod docker-start-dev docker-start-prod
