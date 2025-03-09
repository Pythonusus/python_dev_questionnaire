# Base image with common settings
FROM python:3.13-slim AS python-base

# Create a non-root user with home directory setup
RUN groupadd -r nonroot-user && \
    useradd -r -g nonroot-user -d /home/nonroot-user -m nonroot-user && \
    mkdir -p /home/nonroot-user/app && \
    chown -R nonroot-user:nonroot-user /home/nonroot-user && \
    chmod -R 755 /home/nonroot-user

# Add uv to PATH
ENV PATH="/home/nonroot-user/.local/bin:$PATH"

# Set working directory to nonroot-user's home directory
WORKDIR /home/nonroot-user/app

# Install uv to nonroot-user home directory
RUN apt-get update && \
    apt-get install -y curl build-essential libpq-dev && \
    su nonroot-user -c "curl -LsSf https://astral.sh/uv/install.sh | sh" && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Switch to non-root user
USER nonroot-user

# Copy files
COPY . .


# Production image
FROM python-base AS production

# Install prod dependencies, collect static files,
# Apply migrations, create app superuser if it doesn't exist
RUN make build-prod

CMD make start


# Development image
FROM python-base AS development


# Install prod dependencies, collect static files,
# Apply migrations, create superuser if it doesn't exist
RUN make build-dev

CMD make dev
