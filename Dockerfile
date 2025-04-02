# Base image with common settings
FROM python:3.13-slim AS python-base

# Install common dependencies
RUN apt-get update && \
    apt-get install -y curl build-essential libpq-dev && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Create a non-root user with home directory setup
RUN groupadd -r nonroot-user && \
useradd -r -g nonroot-user -d /home/nonroot-user -m nonroot-user && \
mkdir -p /home/nonroot-user/python_dev_questionnaire && \
chown -R nonroot-user:nonroot-user /home/nonroot-user && \
chmod -R 755 /home/nonroot-user

# Set working directory to nonroot-user's home directory
WORKDIR /home/nonroot-user/python_dev_questionnaire

# Install uv to nonroot-user home directory
RUN su nonroot-user -c "curl -LsSf https://astral.sh/uv/install.sh | sh"

# Add uv to PATH
ENV PATH="/home/nonroot-user/.local/bin:$PATH"

# Switch to non-root user
USER nonroot-user


# Production image
FROM python-base AS production

# Copy files and change ownership to nonroot-user
COPY --chown=nonroot-user:nonroot-user ./python_dev_questionnaire ./python_dev_questionnaire
COPY --chown=nonroot-user:nonroot-user ./docker-entrypoint.sh ./
COPY --chown=nonroot-user:nonroot-user ./Makefile ./
COPY --chown=nonroot-user:nonroot-user ./manage.py ./
COPY --chown=nonroot-user:nonroot-user ./pyproject.toml ./
COPY --chown=nonroot-user:nonroot-user ./README.md ./
COPY --chown=nonroot-user:nonroot-user ./uv.lock ./

# Install prod dependencies
RUN make install-prod

# Collect static files
RUN make static

# Script for running migrations and creating Django superuser.
ENTRYPOINT ["./docker-entrypoint.sh"]

# Start the application
CMD make start


# Development image
FROM python-base AS development

# Create an empty .venv dir that will be used as volume in docker-compose-dev.yaml file.
RUN mkdir -p /home/nonroot-user/python_dev_questionnaire/.venv

# Script for installing dependencies, running migrations and creating Django superuser.
# We can not install dependencies in Dockerfile development image because we do not copy application files.
# All needed files are mounted as volumes in docker-compose-dev.yaml file.
ENTRYPOINT ["./docker-entrypoint-dev.sh"]

# Start the application in development mode
CMD make dev
