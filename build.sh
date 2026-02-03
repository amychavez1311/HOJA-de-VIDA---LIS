#!/usr/bin/env bash
# exit on error
set -o errexit

# Limpiar pycache que puede contener referencias a módulos antiguos
find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
find . -type f -name "*.pyc" -delete

pip install -r requirements.txt

python manage.py collectstatic --no-input
python manage.py migrate