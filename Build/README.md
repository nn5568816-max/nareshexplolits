# Number Info API — Flask conversion

This project converts the supplied PHP admin panel to a ready-to-run Flask + SQLite application.

## Requirements
- Python 3.10+
- pip

## Run

### Windows
Run:
    run.bat

Or manually:
    python -m venv .venv
    .venv\Scripts\activate
    pip install -r requirements.txt
    python app.py

### Linux/macOS
Run:
    chmod +x run.sh
    ./run.sh

The dashboard will be available at:
    http://127.0.0.1:5000/login

## Configuration

Set these environment variables before starting:

- FLASK_SECRET_KEY — a long random session secret
- ADMIN_USER — administrator username
- ADMIN_PASS — administrator password
- PORT — optional Flask port (default 5000)

For development, the application falls back to the values from the original PHP file, but change them before deployment.

## Database

SQLite database:
    osint_api.db

Tables:
- api_keys
- usage_logs

The database is created automatically on first start.

## Demo API

The included `/api.py` endpoint is deliberately demo-only. It validates keys, limits and expiry and records usage, but returns only sample metadata. It does not perform reverse lookup, tracking, identification, or retrieval of private information.

Example:
    /api.py?key=YOUR_KEY&num=9876543210

## Production notes

Use a production WSGI server such as Gunicorn or Waitress behind HTTPS. Do not expose the Flask development server directly to the public internet. Rotate the default credentials and set a strong secret key.
