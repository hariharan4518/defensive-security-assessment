from flask import (
    Flask, request, redirect, session,
    render_template_string, flash, url_for
)
from werkzeug.security import generate_password_hash, check_password_hash
from datetime import timedelta
import sqlite3
import os
import time
import logging

# --------------------------------
# FLASK CONFIGURATION
# --------------------------------

app = Flask(__name__)

app.secret_key = os.environ.get("SECRET_KEY")

if not app.secret_key:
    raise RuntimeError("SECRET_KEY environment variable is not set")

app.permanent_session_lifetime = timedelta(minutes=15)

app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"
app.config["SESSION_COOKIE_SECURE"] = False  # Local HTTP testing only


# --------------------------------
# SECURITY LOGGING
# --------------------------------

logging.basicConfig(
    filename="security.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)


# --------------------------------
# DATABASE CONFIGURATION
# --------------------------------

DATABASE = "users.db"


def get_db_connection():
    return sqlite3.connect(DATABASE)


def initialize_database():
    conn = get_db_connection()

    conn.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            username TEXT UNIQUE NOT NULL,
            password_hash TEXT NOT NULL
        )
    """)

    conn.commit()
    conn.close()


initialize_database()


# --------------------------------
# RATE LIMITING
# --------------------------------

login_attempts = {}

MAX_ATTEMPTS = 5
TIME_WINDOW = 60


def is_rate_limited(ip):
    current_time = time.time()

    if ip not in login_attempts:
        login_attempts[ip] = []

    login_attempts[ip] = [
        attempt for attempt in login_attempts[ip]
        if current_time - attempt < TIME_WINDOW
    ]

    return len(login_attempts[ip]) >= MAX_ATTEMPTS


def record_failed_attempt(ip):
    if ip not in login_attempts:
        login_attempts[ip] = []

    login_attempts[ip].append(time.time())


# --------------------------------
# HOME PAGE
# --------------------------------

@app.route("/")
def home():
    return render_template_string("""
        <h2>Secure Authentication Lab</h2>
        <a href="/register">Register</a>
        <br><br>
        <a href="/login">Login</a>
    """)


# --------------------------------
# REGISTRATION
# --------------------------------

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form.get("username", "").strip()
        password = request.form.get("password", "")

        if not username or len(username) > 30:
            flash("Username must contain 1 to 30 characters.")
            return redirect(url_for("register"))

        if len(password) < 8 or len(password) > 128:
            flash("Password must contain 8 to 128 characters.")
            return redirect(url_for("register"))

        password_hash = generate_password_hash(password)

        conn = get_db_connection()

        try:
            conn.execute(
                """
                INSERT INTO users (username, password_hash)
                VALUES (?, ?)
                """,
                (username, password_hash)
            )

            conn.commit()

        except sqlite3.IntegrityError:
            flash("Username already exists.")
            return redirect(url_for("register"))

        finally:
            conn.close()

        logger.info("New user registered: %s", username)

        flash("Registration successful. Please login.")
        return redirect(url_for("login_page"))

    return render_template_string("""
        <h2>Register</h2>

        <form method="POST">
            Username:
            <input type="text" name="username" required>
            <br><br>

            Password:
            <input type="password" name="password" required>
            <br><br>

            <button type="submit">Register</button>
        </form>

        {% for message in get_flashed_messages() %}
            <p>{{ message }}</p>
        {% endfor %}

        <a href="/login">Login</a>
    """)


# --------------------------------
# LOGIN PAGE
# --------------------------------

@app.route("/login", methods=["GET"])
def login_page():

    return render_template_string("""
        <h2>Secure Login</h2>

        <form method="POST" action="/login">
            Username:
            <input type="text" name="username" required>
            <br><br>

            Password:
            <input type="password" name="password" required>
            <br><br>

            <button type="submit">Login</button>
        </form>

        {% for message in get_flashed_messages() %}
            <p>{{ message }}</p>
        {% endfor %}

        <a href="/register">Register</a>
    """)


# --------------------------------
# LOGIN AUTHENTICATION
# --------------------------------

@app.route("/login", methods=["POST"])
def login():

    username = request.form.get("username", "").strip()
    password = request.form.get("password", "")

    ip = request.remote_addr or "unknown"

    if is_rate_limited(ip):

        logger.warning(
            "Rate limit exceeded from IP: %s", ip
        )

        flash("Too many attempts. Try again later.")
        return redirect(url_for("login_page"))

    conn = get_db_connection()

    try:
        cursor = conn.cursor()

        cursor.execute(
            """
            SELECT username, password_hash
            FROM users
            WHERE username = ?
            """,
            (username,)
        )

        user = cursor.fetchone()

    finally:
        conn.close()

    if user and check_password_hash(user[1], password):

        session.clear()
        session.permanent = True
        session["username"] = username

        login_attempts.pop(ip, None)

        logger.info(
            "Successful login for username: %s from IP: %s",
            username, ip
        )

        return redirect(url_for("dashboard"))

    record_failed_attempt(ip)

    logger.warning(
        "Failed login for username: %s from IP: %s",
        username, ip
    )

    flash("Invalid username or password.")
    return redirect(url_for("login_page"))


# --------------------------------
# DASHBOARD
# --------------------------------

@app.route("/dashboard")
def dashboard():

    if "username" not in session:
        return redirect(url_for("login_page"))

    return render_template_string("""
        <h2>Welcome to Secure Dashboard</h2>

        <p>Logged in as: {{ username }}</p>

        <a href="/logout">Logout</a>
    """, username=session["username"])


# --------------------------------
# LOGOUT
# --------------------------------

@app.route("/logout")
def logout():

    username = session.get("username")

    session.clear()

    logger.info("User logged out: %s", username)

    flash("You have been logged out.")

    return redirect(url_for("login_page"))


# --------------------------------
# RUN APPLICATION
# --------------------------------

if __name__ == "__main__":

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )