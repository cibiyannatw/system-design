import os


def _bool(env_key, default="False"):
    """Parse a 'True'/'False' style env var into an actual Python bool."""
    return os.getenv(env_key, default).strip().lower() in ("true", "1", "yes")


class Config:
    """
    Single config class for trunk-based, multi-instance deployment.

    There is no DevelopmentConfig/ProductionConfig split and no FLASK_ENV
    file-switching logic. The same code + same class runs everywhere.
    What differs is WHICH values os.getenv() finds at runtime:

    - Local machine: values come from `.env.local` (gitignored, personal).
    - Cloud instances (Dev service / Prod service): values are injected
      directly by the platform dashboard - each service has its own set
      of environment variables, completely independent of git branches.

    The defaults below only apply when nothing is set at all (bare local
    run with no .env.local) - they are NOT "dev" values, just safe
    fallbacks so the app doesn't crash.
    """

    ENVIRONMENT = os.getenv("ENVIRONMENT", "local")
    DEBUG = _bool("DEBUG", "True")

    APP_NAME = os.getenv("APP_NAME", "My Flask App (LOCAL)")
    APP_VERSION = os.getenv("APP_VERSION", "0.0.0-local")

    DATABASE_HOST = os.getenv("DATABASE_HOST", "localhost")
    DATABASE_NAME = os.getenv("DATABASE_NAME", "local_database")

    API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000")

    # --- Secrets ---
    # No fallback values on purpose. These must be set on each cloud
    # instance's dashboard (Dev service vars, Prod service vars). Locally,
    # put personal/test values in .env.local if you need them.
    SECRET_KEY = os.getenv("SECRET_KEY")
    DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
    API_KEY = os.getenv("API_KEY")

    # --- Feature flags ---
    # Toggle per instance via env vars on each service's dashboard.
    FEATURES = {
        "analytics": _bool("FEATURE_ANALYTICS"),
        "email_notifications": _bool("FEATURE_EMAIL_NOTIFICATIONS"),
        "advanced_search": _bool("FEATURE_ADVANCED_SEARCH"),
        "debug_mode": _bool("FEATURE_DEBUG_MODE", "True"),
    }

    # --- Demo data ---
    # In a real app this would come from a database. total_users /
    # active_sessions are env-driven here purely to demonstrate that the
    # same code shows different numbers on Dev vs Prod instances.
    SAMPLE_DATA = {
        "users": [
            {"id": 1, "name": "Demo User 1", "email": "user1@example.com"},
            {"id": 2, "name": "Demo User 2", "email": "user2@example.com"},
        ],
        "stats": {
            "total_users": int(os.getenv("TOTAL_USERS", "2")),
            "active_sessions": int(os.getenv("ACTIVE_SESSIONS", "1")),
            "environment": ENVIRONMENT,
        },
    }
