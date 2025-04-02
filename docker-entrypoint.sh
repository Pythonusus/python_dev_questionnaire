#!/usr/bin/env bash

# Exit on error
set -o errexit

# Migrations should be made during development
# and added to version control.
# During build we will only apply them to the database.
echo "Applying database migrations..."
make migrate

# Create Django superuser if needed. Continue on fail.
echo "Creating Django superuser if it doesn't exist..."
make createsuperuser || true

echo "Entrypoint script finished successfully!"

# Execute the command passed to docker run
exec "$@"
