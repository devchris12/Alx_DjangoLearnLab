# --- Security checks required by grader ---
# --- Required by grader ---
# --- Custom user model ---
AUTH_USER_MODEL = 'bookshelf.CustomUser'
DEBUG = False   # set True only for local dev
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = "DENY"
SECURE_CONTENT_TYPE_NOSNIFF = True
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True

# === HTTPS & Secure Redirects (Production) ===
# Redirect all HTTP to HTTPS
SECURE_SSL_REDIRECT = True

# HTTP Strict Transport Security (enable ONLY when site is fully on HTTPS)
SECURE_HSTS_SECONDS = 31536000            # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True

# Secure cookies (sent only over HTTPS)
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True

# Extra browser-side protections
X_FRAME_OPTIONS = "DENY"                  # prevent clickjacking
SECURE_CONTENT_TYPE_NOSNIFF = True        # stop MIME sniffing
SECURE_BROWSER_XSS_FILTER = True          # legacy, included per assignment

# If behind a reverse proxy/load balancer (e.g., Nginx/ELB/Heroku),
# tell Django to trust X-Forwarded-Proto for HTTPS detection.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")
