#!/usr/bin/env bash
set -o errexit

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# Upgrade pip and install wheel
pip install --upgrade pip
pip install wheel

# Install the requirements
pip install --no-cache-dir -r requirements.txt

# Force reinstall scikit-surprise
pip install --no-cache-dir --force-reinstall scikit-surprise

# Run your Django commands
python manage.py collectstatic --no-input
python manage.py migrate