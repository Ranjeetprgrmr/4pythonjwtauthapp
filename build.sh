#!/usr/bin/env bash
# Exit on error
set -o errexit

# Install system dependencies required for psycopg2
apt-get update
apt-get install -y libpq-dev gcc python3-dev

# Install Python packages
pip install -r requirements.txt

# Convert static asset files
python manage.py collectstatic --no-input

# Apply any outstanding database migrations
python manage.py migrate