"""Settings of the example blog: Django REST Framework over PostgreSQL.

The fixture is read statically by specIR's extractor (IR08); it is never served. The database
settings name PostgreSQL so that `manage.py sqlmigrate` writes the Postgres dialect (sql/README.md).
"""

import os

SECRET_KEY = "fixture-only-not-a-secret"
DEBUG = False
ALLOWED_HOSTS: list[str] = []
ROOT_URLCONF = "blogsite.urls"
USE_TZ = True
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

INSTALLED_APPS = [
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "rest_framework",
    "blog",
]

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": os.environ.get("BLOG_DB_NAME", "blog"),
        "USER": os.environ.get("BLOG_DB_USER", "blog"),
        "HOST": os.environ.get("BLOG_DB_HOST", "localhost"),
    }
}

REST_FRAMEWORK = {
    "DEFAULT_PERMISSION_CLASSES": ["rest_framework.permissions.IsAuthenticated"],
}
