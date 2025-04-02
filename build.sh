#!/usr/bin/env bash

# Exit on error
set -o errexit

# Install only production dependencies
make install-prod

# Collect static files
make static

# Migrations should be made during development
# and added to version control.
# During build we will only apply them to the database.
# Apply migrations
echo "Applying database migrations..."
make migrate

# Create Django superuser. Continue on fail.
echo "Creating Django superuser if it doesn't exist..."
make createsuperuser || true

echo "Build python-dev-questionnaire completed successfully!"
