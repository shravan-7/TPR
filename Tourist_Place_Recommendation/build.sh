#!/usr/bin/env bash
set -o errexit

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# Upgrade pip and install wheel
pip install --upgrade pip
pip install wheel

# Install numpy and scipy first
pip install --no-cache-dir numpy==1.23.5 scipy==1.9.3

# Install the rest of the requirements
pip install --no-cache-dir -r requirements.txt

# Run your Django commands
python manage.py collectstatic --no-input
python manage.py migrate