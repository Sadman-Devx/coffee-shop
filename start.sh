#!/bin/bash
# Startup script for Railway deployment

# Run migrations
python manage.py migrate --noinput

# Run setup (creates admin user and coffee items)
python manage.py setup_site

# Collect static files
python manage.py collectstatic --noinput

# Start the server
exec gunicorn coffee_site.wsgi

