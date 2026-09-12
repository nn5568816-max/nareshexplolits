#!/usr/bin/env bash
set -e
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
export FLASK_SECRET_KEY="replace-with-a-long-random-secret"
export ADMIN_USER="anish"
export ADMIN_PASS="change-this-password"
python app.py
