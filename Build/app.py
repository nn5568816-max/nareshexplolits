import os
import sqlite3
from datetime import datetime, date
from functools import wraps

from flask import Flask, abort, flash, redirect, render_template, request, session, url_for, jsonify

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "osint_api.db")

app = Flask(__name__)
app.secret_key = os.environ.get("FLASK_SECRET_KEY", "change-this-secret-key")

ADMIN_USER = os.environ.get("ADMIN_USER", "anish")
ADMIN_PASS = os.environ.get("ADMIN_PASS", "anish123")


def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    conn = get_db()
    conn.execute("""
        CREATE TABLE IF NOT EXISTS api_keys (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            key_text TEXT UNIQUE NOT NULL,
            service_type TEXT DEFAULT 'number',
            daily_limit INTEGER DEFAULT 100,
            used_today INTEGER DEFAULT 0,
            total_used INTEGER DEFAULT 0,
            last_used TEXT DEFAULT '',
            expiry_date TEXT DEFAULT '',
            created_at TEXT DEFAULT CURRENT_TIMESTAMP,
            active INTEGER DEFAULT 1
        )
    """)
    conn.execute("""
        CREATE TABLE IF NOT EXISTS usage_logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            api_key_id INTEGER NOT NULL,
            query TEXT,
            used_at TEXT DEFAULT CURRENT_TIMESTAMP
        )
    """)
    conn.commit()
    conn.close()


def login_required(view):
    @wraps(view)
    def wrapped(*args, **kwargs):
        if not session.get("admin_logged"):
            return redirect(url_for("login"))
        return view(*args, **kwargs)
    return wrapped


def is_expired(expiry):
    if not expiry:
        return False
    try:
        return datetime.strptime(expiry, "%Y-%m-%d").date() < date.today()
    except ValueError:
        return False


def key_usage(conn, key_id):
    today = date.today().isoformat()
    today_count = conn.execute(
        "SELECT COUNT(*) FROM usage_logs WHERE api_key_id=? AND date(used_at)=?",
        (key_id, today)
    ).fetchone()[0]
    total_count = conn.execute(
        "SELECT COUNT(*) FROM usage_logs WHERE api_key_id=?",
        (key_id,)
    ).fetchone()[0]
    return today_count, total_count


@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get("admin_logged"):
        return redirect(url_for("dashboard"))

    login_error = None
    if request.method == "POST":
        username = request.form.get("login_user", "")
        password = request.form.get("login_pass", "")
        if username == ADMIN_USER and password == ADMIN_PASS:
            session.clear()
            session["admin_logged"] = True
            return redirect(url_for("dashboard"))
        login_error = "Invalid credentials"

    return render_template("login.html", login_error=login_error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))


@app.route("/")
@login_required
def dashboard():
    conn = get_db()
    keys = conn.execute("SELECT * FROM api_keys ORDER BY id DESC").fetchall()
    total_usage = conn.execute("SELECT COUNT(*) FROM usage_logs").fetchone()[0]
    today_usage = conn.execute(
        "SELECT COUNT(*) FROM usage_logs WHERE date(used_at)=date('now')"
    ).fetchone()[0]
    active_keys = sum(1 for k in keys if k["active"])

    rows = []
    for key in keys:
        today_count, total_count = key_usage(conn, key["id"])
        rows.append({
            "id": key["id"],
            "key_text": key["key_text"],
            "daily_limit": key["daily_limit"],
            "today": today_count,
            "total": total_count,
            "created_at": key["created_at"],
            "expiry_date": key["expiry_date"],
            "active": key["active"],
            "expired": is_expired(key["expiry_date"]),
        })

    conn.close()

    return render_template(
        "dashboard.html",
        keys=rows,
        total_usage=total_usage,
        today_usage=today_usage,
        active_keys=active_keys,
        base_url=request.host_url.rstrip("/"),
    )


@app.post("/key/create")
@login_required
def create_key():
    key_text = request.form.get("key_text", "").strip()
    try:
        daily_limit = max(0, int(request.form.get("daily_limit", "100")))
    except ValueError:
        daily_limit = 100
    expiry_date = request.form.get("expiry_date", "").strip()

    if not key_text:
        flash("Key text required", "error")
        return redirect(url_for("dashboard") + "#create-section")

    conn = get_db()
    try:
        cur = conn.execute(
            """INSERT INTO api_keys
               (key_text, service_type, daily_limit, expiry_date, active)
               VALUES (?, 'number', ?, ?, 1)""",
            (key_text, daily_limit, expiry_date),
        )
        conn.commit()
        flash("API Key created successfully!", "success")
    except sqlite3.IntegrityError:
        flash("That API key already exists.", "error")
    finally:
        conn.close()

    return redirect(url_for("dashboard") + "#keys-section")


@app.post("/key/edit")
@login_required
def edit_key():
    try:
        key_id = int(request.form.get("id", "0"))
        daily_limit = max(0, int(request.form.get("daily_limit", "0")))
    except ValueError:
        flash("Invalid key data.", "error")
        return redirect(url_for("dashboard"))

    expiry_date = request.form.get("expiry_date", "").strip()
    conn = get_db()
    conn.execute(
        "UPDATE api_keys SET daily_limit=?, expiry_date=? WHERE id=?",
        (daily_limit, expiry_date, key_id),
    )
    conn.commit()
    conn.close()

    flash("API Key updated successfully!", "success")
    return redirect(url_for("dashboard") + "#keys-section")


@app.post("/key/toggle")
@login_required
def toggle_key():
    try:
        key_id = int(request.form.get("id", "0"))
    except ValueError:
        abort(400)

    conn = get_db()
    row = conn.execute("SELECT active FROM api_keys WHERE id=?", (key_id,)).fetchone()
    if row:
        new_status = 0 if row["active"] else 1
        conn.execute("UPDATE api_keys SET active=? WHERE id=?", (new_status, key_id))
        conn.commit()
        flash("Key status updated!", "success")
    conn.close()

    return redirect(url_for("dashboard") + "#keys-section")


@app.post("/key/delete")
@login_required
def delete_key():
    try:
        key_id = int(request.form.get("id", "0"))
    except ValueError:
        abort(400)

    conn = get_db()
    conn.execute("DELETE FROM usage_logs WHERE api_key_id=?", (key_id,))
    conn.execute("DELETE FROM api_keys WHERE id=?", (key_id,))
    conn.commit()
    conn.close()

    flash("Key deleted successfully!", "success")
    return redirect(url_for("dashboard") + "#keys-section")


@app.post("/reset-daily")
@login_required
def reset_daily():
    # Keep the legacy used_today field synchronized for compatibility.
    conn = get_db()
    conn.execute("UPDATE api_keys SET used_today=0")
    conn.commit()
    conn.close()
    flash("Daily usage reset successfully!", "success")
    return redirect(url_for("dashboard"))


@app.get("/api.py")
def demo_api():
    """
    Demo-only endpoint. It intentionally returns sample data and does not
    perform reverse lookup, tracking, identification, or personal-data lookup.
    """
    key_text = request.args.get("key", "").strip()
    number = request.args.get("num", "").strip()

    if not key_text or not number:
        return jsonify({"error": "key and num are required"}), 400

    if not number.isdigit() or len(number) != 10:
        return jsonify({"error": "Number must be 10 digits"}), 400

    conn = get_db()
    key = conn.execute(
        "SELECT * FROM api_keys WHERE key_text=?", (key_text,)
    ).fetchone()

    if not key:
        conn.close()
        return jsonify({"error": "Invalid API key"}), 401

    if not key["active"]:
        conn.close()
        return jsonify({"error": "API key is inactive"}), 403

    if is_expired(key["expiry_date"]):
        conn.close()
        return jsonify({"error": "API key has expired"}), 403

    today_count, _ = key_usage(conn, key["id"])
    if key["daily_limit"] > 0 and today_count >= key["daily_limit"]:
        conn.close()
        return jsonify({"error": "Daily limit exceeded"}), 429

    now = datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")
    conn.execute(
        "INSERT INTO usage_logs (api_key_id, query, used_at) VALUES (?, ?, ?)",
        (key["id"], number, now),
    )
    conn.execute(
        """UPDATE api_keys
           SET used_today=used_today+1,
               total_used=total_used+1,
               last_used=?
           WHERE id=?""",
        (now, key["id"]),
    )
    conn.commit()
    conn.close()

    return jsonify({
        "success": True,
        "demo": True,
        "number": number,
        "message": "Sample/dummy data only. No real-person information is returned.",
    })


@app.errorhandler(404)
def not_found(_):
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    init_db()
    app.run(host="127.0.0.1", port=int(os.environ.get("PORT", "5000")), debug=False)
