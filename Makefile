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

test:
	uv run pytest

# Runs tests with coverage. Generates XML and HTML reports in coverage/ directory.
# XML report is used for CI. HTML report is used to view the coverage locally.
test-cov:
	uv run pytest --cov=python_dev_questionnaire --cov-report=xml --cov-report=html

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

# Collects static before building because we use staticfiles volume for development.
# No static collection in Dockerfile development image.
docker-build-dev: static
	docker compose -f compose.yaml -f compose.dev.yaml build

# Static collection is in Dockerfile production image because we want to
# collect static files inside the container in production.
docker-build-prod:
	docker compose build

# Starts the containers in development mode.
# Since it can be used without compose build command,
#we also collect static files before starting.
docker-start-dev: static
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

# Starts interactive shell inside the container
# with the django project loaded using IPython.
docker-ipython:
	docker compose exec web make shell

# Starts interactive bash terminal inside the container.
docker-shell:
	docker compose exec web bash

.PHONY: install install-prod lint lint-html format format-html test test-cov shell static createsuperuser migrations migrate dev build start \
				docker-build-dev docker-build-prod docker-start-dev docker-start-prod docker-stop docker-down docker-install docker-migrate docker-ipython docker-shell
