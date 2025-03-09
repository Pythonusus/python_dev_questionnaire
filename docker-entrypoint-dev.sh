#!/usr/bin/env bash

# Exit on error
set -o errexit

# Installing dependencies during entrypoint script, because
# we do not copy application files to development image.
# Mounted volumes are used instead, so we cannot install dependencies during build.
make install

# Migrations should be made during development and added to version control.
# During build we will only apply them to the database.
echo "Applying database migrations..."
make migrate

# Create Django superuser if needed. Continue on fail.
echo "Creating Django superuser if it doesn't exist..."
make createsuperuser || true

echo "Entrypoint script finished successfully!"

# Execute the command passed to docker run
exec "$@"
