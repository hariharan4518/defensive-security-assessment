# Secure Authentication Lab

## Project Overview

This project demonstrates a basic secure authentication system developed using Python and Flask.

## Features

* User registration and login.
* Secure password hashing using Werkzeug.
* Server-side input validation.
* Parameterized SQL queries to prevent SQL injection.
* Login rate limiting to reduce brute-force attacks.
* Generic error messages for failed login attempts.
* Session management and logout.
* Session timeout.
* HTTPOnly and SameSite cookie settings.

## Technologies Used

* Python
* Flask
* SQLite
* Werkzeug

## Security Testing

The following tests were performed:

1. Successful user registration.
2. Successful login with valid credentials.
3. Rejection of duplicate usernames.
4. Rejection of incorrect passwords.
5. Rate limiting after repeated failed login attempts.
6. Logout and session access verification.

## How to Run

1. Install Python.

2. Install dependencies using:

   `pip install -r requirements.txt`

3. Set the SECRET_KEY environment variable.

4. Run the application:

   `python app.py`

5. Open `http://127.0.0.1:5000` in your browser.

## Note

This is an educational authentication project intended for local demonstration, not production deployment.
