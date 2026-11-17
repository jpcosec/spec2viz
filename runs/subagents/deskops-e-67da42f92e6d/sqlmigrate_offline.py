"""Run Django's real `sqlmigrate` with the PostgreSQL backend and no server (IR08 fixture SQL).

What is patched is only what needs a live server: the server version (16), the applied-migrations
table (none applied) and the transaction calls (autocommit, no-ops), as sldb B2 did (runs/subagents/20261116-exec-b2sql-c1 of sldb). The SQL comes from Django's PostgreSQL
schema editor exactly as with a server. Usage (cwd = tests/fixtures/blog_app):
    python sqlmigrate_offline.py blog 0001
"""
import os
import sys

sys.path.insert(0, os.getcwd())
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "blogsite.settings")
import django  # noqa: E402

django.setup()
from django.core.management import call_command  # noqa: E402
from django.db import connection  # noqa: E402
from django.db.migrations.recorder import MigrationRecorder  # noqa: E402

connection.__dict__["pg_version"] = 160000
connection.ensure_connection = lambda: None
connection.get_autocommit = lambda: True
connection.set_autocommit = lambda *a, **k: None
connection.commit = lambda: None
connection.rollback = lambda: None
MigrationRecorder.applied_migrations = lambda self: {}
MigrationRecorder.has_table = lambda self: False

call_command("sqlmigrate", *sys.argv[1:])
