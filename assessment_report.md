# Defensive Security Assessment Capstone

## 1. Project Information

**Project:** Secure Authentication Lab  
**Assessment Type:** Defensive Security Assessment  
**Application:** Python Flask Web Application  
**Database:** SQLite  
**Assessment Scope:** Local application only

## 2. Scope and Authorization

The assessment was conducted on my own locally developed Flask authentication application.

The assessment covered:
- Application configuration
- User authentication
- Password security
- Input validation
- Login rate limiting
- Third-party dependencies
- Security logging

No external systems or unauthorized targets were tested.

## 3. Security Tests Performed

### Test 1: Application Configuration

- Secret key loaded from environment variable.
- HTTPOnly cookie enabled.
- SameSite cookie protection enabled.
- Session timeout configured to 15 minutes.
- Debug mode disabled.

**Result:** Passed for local assessment.

### Test 2: Authentication Security

- Tested valid login.
- Tested invalid password.
- Verified generic authentication error messages.
- Verified logout functionality.
- Verified session clearing.

**Result:** Passed.

### Test 3: Password Security

Passwords are stored using Werkzeug password hashing rather than plaintext storage.

**Result:** Passed.

### Test 4: Login Rate Limiting

Tested repeated incorrect login attempts.

The application blocks further attempts after five failures within 60 seconds.

**Result:** Passed.

### Test 5: Input Validation

Username length and password length restrictions were implemented.

Parameterized SQL queries are used to reduce SQL injection risk.

**Result:** Implemented.

### Test 6: Dependency Security

Used pip-audit to scan installed Python dependencies.

The scan reported zero known vulnerabilities at the time of testing.

**Result:** Passed.

### Test 7: Security Logging

Implemented logging for:
- Successful login attempts
- Failed login attempts
- Rate-limit events
- User registration
- Logout events

Verified that security.log was generated.

**Result:** Passed.

## 4. Findings and Recommendations

### Finding 1: Secure Cookie Configuration

The Secure cookie option is disabled for local HTTP testing.

**Recommendation:** Enable Secure cookies when deploying through HTTPS.

### Finding 2: CSRF Protection

CSRF protection has not yet been implemented.

**Recommendation:** Add CSRF tokens to registration and login forms before production deployment.

### Finding 3: Rate Limiting Storage

The current rate limiter stores attempts in application memory.

**Recommendation:** Use persistent shared storage for production deployment.

## 5. Security Improvements

The following improvements were implemented:

- Password hashing
- Parameterized SQL queries
- Input validation
- Login rate limiting
- Session management
- Secure configuration practices
- Security event logging
- Dependency vulnerability scanning

## 6. Conclusion

The defensive security assessment was performed on a locally developed Flask authentication application.

The application was tested for authentication security, configuration, password handling, input validation, dependency vulnerabilities, rate limiting, and security logging.

Several security improvements were implemented and verified.

Additional protections, including CSRF protection and production-grade rate limiting, are recommended before deployment.

**Assessment Status:** Completed for local lab scope, with production improvements identified.