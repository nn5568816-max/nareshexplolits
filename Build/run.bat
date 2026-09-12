@echo off
python -m venv .venv
call .venv\Scripts\activate
python -m pip install --upgrade pip
pip install -r requirements.txt
set FLASK_SECRET_KEY=replace-with-a-long-random-secret
set ADMIN_USER=anish
set ADMIN_PASS=change-this-password
python app.py
