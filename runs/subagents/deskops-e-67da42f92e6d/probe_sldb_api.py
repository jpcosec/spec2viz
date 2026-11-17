"""IR08 probe: what sldb's public API (sldb.api, sldb.api.anchors) gives over the blog fixture.

Read-only. It asks, for each element of the backend and data half of the publish chain, whether
sldb.api gives the fact the mapping needs. It imports nothing outside sldb.api.
"""
import json
from pathlib import Path

import sldb.api as api
from sldb.api.anchors import record_anchor

ROOT = Path(__file__).resolve().parents[3] / "tests" / "fixtures" / "blog_app"
SQL = "sql/blog_0001_initial.sql"

print("sldb.api names about code facts:", sorted(n for n in api.__all__ if any(k in n.lower() for k in ("code", "fact", "scan", "symbol", "anchor"))))
for ref in [
    "code:blog/views.py::PostViewSet", "code:blog/views.py::PostViewSet.publish", "code:blog/urls.py::",
    "code:blog/models.py::Post", "code:blog/models.py::Post.publish", "code:blog/models.py::can_publish",
    "code:blog/models.py::Post.Status", "code:blog/models.py::Post.status", "code:blog/serializers.py::PostSerializer",
    f"code:{SQL}::posts", f"code:{SQL}::posts.status", f"code:{SQL}::posts.author_id", f"code:{SQL}::posts.id",
    f"code:{SQL}::posts_author_id_099b8aca", f"code:{SQL}::posts_author_id_099b8aca_fk_auth_user_id",
]:
    try:
        block = record_anchor(ROOT, ref)
        print("OK  ", ref, json.dumps({"kind": block["kind"], "keys": sorted(block), "seen": sorted(block["seen"])}))
    except Exception as error:  # noqa: BLE001 - the probe reports what fails
        print("FAIL", ref, type(error).__name__, error)
