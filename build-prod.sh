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
make migrate

# Create superuser. Continue on fail.
make createsuperuser || true

echo "Build python-dev-questionnaire completed successfully!"
