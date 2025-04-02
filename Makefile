# Installs dependencies using uv package manager.
install:
	uv sync

# Installs only prod dependencies using uv package manager.
install-prod:
	uv sync --no-dev

# Runs ruff linter with the config from pyproject.toml.
lint:
	uv run ruff check --config pyproject.toml python_dev_questionnaire

# Runs ruff linter with the config from pyproject.toml and fixes the issues.
format:
	uv run ruff check --config pyproject.toml --fix python_dev_questionnaire

lint-html:
	uv run djlint python_dev_questionnaire/templates --lint

format-html:
	uv run djlint python_dev_questionnaire/templates --reformat

# Running tests with DEBUG=False to keep env similar to production.
test:
	DEBUG=False uv run pytest -vv

# Runs tests with coverage. Generates XML and HTML reports in default directories.
# XML report (coverage.xml) and HTML report (htmlcov/) will be in the project root.
test-cov:
	DEBUG=False COVERAGE_FILE=coverage/.coverage uv run -m pytest \
		--cov=python_dev_questionnaire \
		--cov-config=pyproject.toml \
		--cov-report=xml:coverage/coverage.xml \
		--cov-report=html:coverage/html \
		--cov-report=term

# Test coverage for CI actions. Only XML report and raw coverage data is needed.
test-cov-ci:
	DEBUG=False COVERAGE_FILE=coverage/.coverage uv run -m pytest \
		--cov=python_dev_questionnaire \
		--cov-config=pyproject.toml \
		--cov-report=xml:coverage/coverage.xml

# Starts the shell with the django project loaded using IPython.
shell:
	uv run python manage.py shell_plus

# Installs pre-commit hooks.
pre-commit:
	uv run pre-commit install

static:
	uv run python manage.py collectstatic --noinput

# Creates a superuser with credentials from .env file.
createsuperuser:
	uv run python manage.py createsuperuser --noinput

migrations:
	uv run python manage.py makemigrations

migrate:
	uv run python manage.py migrate

# Starts the server in development mode.
dev:
	uv run python manage.py runserver 0.0.0.0:$${PORT:-5050}

# Used for deploy without docker.
build:
	./build.sh

# Starts the server in production mode.
start:
	DEBUG=False uv run gunicorn -w 5 -b 0.0.0.0:$${PORT:-8000} python_dev_questionnaire.wsgi

# Create coverage directory on host with proper permissions if doesn't exist.
mk-coverage-dir:
	if [ ! -d "coverage" ]; then \
		mkdir -p coverage/html; \
		chmod -R 777 coverage; \
	fi

# Collects static before building because we use staticfiles volume for development.
# No static collection in Dockerfile development image.
# Coverage directory is created on host with proper permissions.
docker-build-dev: static mk-coverage-dir
	docker compose -f compose.yaml -f compose.dev.yaml build

# Static collection is in Dockerfile production image because we want to
# collect static files inside the container in production.
docker-build-prod:
	docker compose build

# Starts the containers in development mode.
# Since it can be used without compose build command,
# we also collect static files before starting.
# Same with coverage directory.
docker-start-dev: static mk-coverage-dir
	docker compose -f compose.yaml -f compose.dev.yaml up

# Starts the containers in production mode.
docker-start-prod:
	docker compose up

# Shows logs of the running containers.
docker-logs:
	docker compose logs -f

# Stops the containers.
docker-stop:
	docker compose stop

# Stops and removes the containers.
docker-down:
	docker compose down

# Installs dependencies inside the container.
# Used for dev container after modifying project dependencies.
docker-install:
	docker compose exec web uv sync

# Applies migrations inside the container.
# Used for dev container after modifying migrations.
docker-migrate:
	docker compose exec web uv run python manage.py migrate

docker-test:
	docker compose exec web make test

# Runs tests with coverage inside the container.
docker-test-cov:
	docker compose exec -T web make test-cov

# Runs tests with coverage inside the container.
# Only coverage.xml is needed for CI.
docker-test-cov-ci:
	docker compose exec -T web make test-cov-ci

# Starts interactive shell inside the container with the django project loaded using IPython.
docker-ipython:
	docker compose exec web make shell

# Starts interactive bash terminal inside the container.
docker-shell:
	docker compose exec web bash

.PHONY: install install-prod lint lint-html format format-html test test-cov test-cov-ci \
        shell pre-commit static createsuperuser migrations migrate dev build start \
        docker-build-dev docker-build-prod mk-coverage-dir docker-start-dev docker-start-prod \
        docker-stop docker-down docker-install docker-migrate \
        docker-test docker-test-cov docker-test-cov-ci docker-ipython docker-shell
