#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install production and development dependencies
make install

# Static collection is not needed as we are using staticfiles volume
# Collect static outside the Docker container before running the build

# Migrations should be made during development
# and added to version control.
# During build we will only apply them to the database.
# Apply migrations
make migrate

# Create superuser. Continue on fail.
make createsuperuser || true

echo "Build python-dev-questionnaire completed successfully!"
