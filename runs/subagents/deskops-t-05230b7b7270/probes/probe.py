"""Tester probes: mutation, provenance vs code_facts, idempotence, verified-doc preservation. Run from IR root."""
import json, re, shutil, subprocess, sys, tempfile
from pathlib import Path
sys.path[:0] = ["/mnt/ssd/proyectos/SLDB_1/IR/tests", "/mnt/ssd/proyectos/SLDB_1/IR/tests/extract"]
import sldb.api as api
from sldb.api.code import code_facts
from sldb.api.anchors import check_anchors
from specir.extract import extract
from specir.install import package_pythonpath
from extraction import new_project, documents, extracted
from conftest import tree_digest

def summary(root):
    d = extracted(root)
    out = {}
    for k, doc in sorted(d.items()):
        p = doc.payload
        out[k] = p.get("title") if doc.model_name != "RelationDoc" else (p["source_id"], p["relation_type"], p["target_id"])
    return out

def edit(root, rel, pairs):
    p = root / rel; t = p.read_text()
    for old, new in pairs:
        assert old in t, (rel, old); t = t.replace(old, new)
    p.write_text(t)

base = Path(tempfile.mkdtemp(dir="/dev/shm", prefix="probe-"))
print("BASE", base)
# --- baseline
r0 = new_project(base, "base"); rep0 = extract(r0); S0 = summary(r0)
print("== baseline", len(S0), "created", len(rep0.created)); 
for k, v in S0.items(): print("  ", k, v)
print("not_derived:", *rep0.not_derived, sep="\n  ")

# --- provenance vs code_facts
facts = {f"code:{f['path']}::" + ("" if f["id"] == f["attrs"]["module"] else f["id"].removeprefix(f["attrs"]["module"] + ".")): f for f in code_facts(r0)["facts"]}
anchors = {d.payload["ref"]: d for d in documents(r0).values() if d.model_name == "CodeAnchorDoc"}
bad = 0
for ref, a in anchors.items():
    f = facts[ref]
    c = a.payload["claim"]
    ok = f["path"] in c and f"líneas {f['span']['start_line']}-{f['span']['end_line']}" in c and f["source_hash"] in c and a.payload["seen"] == f["fingerprints"]
    bad += not ok
print("== anchors", len(anchors), "mismatching", bad)
# every node/edge: referenced anchors exist; edges: attributes.anchors
for k, doc in extracted(r0).items():
    p = doc.payload; txt = p.get("description") or p.get("notes")
    names = set(re.findall(r"\[(anchor-[0-9a-f]{16})\]", txt))
    held = {d.name for d in anchors.values()}
    assert names and names <= held, k
    fld = p["attributes"] if doc.model_name == "RelationDoc" else p
    assert fld["origen"] in ("observado", "derivado") and fld["verificacion"] == "sin_verificar" and not fld["evidencia"] and not fld["verificado_por"], k
    # does description name a rule?
    print("  ", k, fld["origen"], "|", txt[:90])
    # names refer to file:line that match facts
    for m in re.finditer(r"(\S+\.(?:py|sql)):(\d+) (\S+) \[(anchor-\w+)\]", txt):
        path, line, sym, an = m.groups()
        ref = next(a.payload["ref"] for a in anchors.values() if a.name == an)
        f = facts[ref]; assert f["path"] == path and str(f["span"]["start_line"]) == line, (k, m.group(0))
print("provenance OK")

# --- idempotence
before = tree_digest(r0 / ".sldb", r0 / "specir"); rep = extract(r0)
print("== second run identical:", tree_digest(r0 / ".sldb", r0 / "specir") == before, "created", rep.created, "changed", rep.changed, "unchanged", len(rep.unchanged))

# --- mutation 1: rename model, table, router prefix, action method
r1 = new_project(base, "m1")
edit(r1, "blog/models.py", [("class Post(", "class Article("), ("post: Post", "post: Article"), ('db_table = "posts"', 'db_table = "entries"')])
edit(r1, "blog/serializers.py", [("import Post", "import Article"), ("model = Post", "model = Article")])
edit(r1, "blog/views.py", [("import Post\n", "import Article\n"), ("Post.objects", "Article.objects")])
edit(r1, "blog/urls.py", [('register("posts"', 'register("stories"')])
edit(r1, "blog/views.py", [('methods=["post"]', 'methods=["put"]')])
edit(r1, "sql/blog_0001_initial.sql", [('"posts"', '"entries"'), ("posts_author", "entries_author")])
rep1 = extract(r1); S1 = summary(r1)
print("== mutation1 (Post->Article, posts->entries, prefix->stories, post->put)")
for k, v in S1.items(): print("  ", k, v)
print("not_derived:", *rep1.not_derived, sep="\n  ")
t = {d.payload.get("title") for d in extracted(r1).values() if d.model_name != "RelationDoc"}
assert "PUT /stories/{id}/publish" in t and "entries" in t and "Article" in t and "Article.publish" in t, t
print("mutation1 OK: titles", sorted(t))

# --- mutation 2: no Meta.db_table => <app>_<model> fallback; table renamed blog_post
r2 = new_project(base, "m2")
edit(r2, "blog/models.py", [("    class Meta:\n        db_table = \"posts\"\n\n", "")])
edit(r2, "sql/blog_0001_initial.sql", [('"posts"', '"blog_post"'), ("posts_author", "blog_post_author")])
rep2 = extract(r2); S2 = summary(r2)
print("== mutation2 (no Meta.db_table; table blog_post)"); [print("  ", k, v) for k, v in S2.items() if "persisted_in" in str(v) or "writes" in str(v) or k.startswith("TableDoc")]
print("not_derived:", *rep2.not_derived, sep="\n  ")
# --- mutation 3: rename can_publish -> ensure_publishable (no prefix), and -> is_allowed
for nm in ("ensure_publishable", "may_publish_post"):
    r3 = new_project(base, "m3" + nm); edit(r3, "blog/models.py", [("can_publish", nm)]); extract(r3)
    print("== mutation3", nm, "policies:", sorted(d.payload["title"] for d in extracted(r3).values() if d.model_name == "PolicyDoc"),
          "governed_by:", sum(1 for d in extracted(r3).values() if d.model_name == "RelationDoc" and d.payload["relation_type"] == "governed_by"))
# --- mutation 4: remove the router exposure and the register
r4 = new_project(base, "m4"); edit(r4, "blog/urls.py", [("urlpatterns = router.urls", "urlpatterns = []")]); rep4 = extract(r4)
print("== mutation4 no router.urls:", [k for k in extracted(r4) if k.startswith("ApiOperationDoc")], rep4.not_derived[:3])
# --- mutation 5: include prefix
r5 = new_project(base, "m5"); edit(r5, "blogsite/urls.py", [('path("", include', 'path("api/v1/", include')]); extract(r5)
print("== mutation5 prefix:", [d.payload["title"] for d in extracted(r5).values() if d.model_name == "ApiOperationDoc"])
# --- mutation 6: trailing_slash default
r6 = new_project(base, "m6"); edit(r6, "blog/urls.py", [("SimpleRouter(trailing_slash=False)", "SimpleRouter()")]); extract(r6)
print("== mutation6 slash:", [d.payload["title"] for d in extracted(r6).values() if d.model_name == "ApiOperationDoc"])

# --- verified preservation + changed file
r7 = new_project(base, "m7"); extract(r7)
store, pp = r7 / ".sldb", package_pythonpath()
V = {"verificacion": "verificado", "verificado_por": "human:tester", "evidencia": "visto"}
docs = documents(r7)
nodes = ["TableDoc:table-posts", "ApiOperationDoc:api-post-posts-id-publish", "DomainOperationDoc:op-post-publish"]
for k in nodes:
    d = docs[k]; api.save_document_payload(store, d.model_name, d.name, {**d.payload, **V, "title": d.payload["title"] + " (editado a mano)"}, pp)
rel = [k for k in docs if k.startswith("RelationDoc:") and "executes" in k][0]
d = docs[rel]; api.save_document_payload(store, "RelationDoc", d.name, {**d.payload, "notes": d.payload["notes"] + " NOTA", "attributes": {**d.payload["attributes"], **V}}, pp)
kept = {k: documents(r7)[k].payload for k in [*nodes, rel]}
edit(r7, "blog/models.py", [("self.published_at = timezone.now()", "self.published_at = timezone.now()  # touched")])
edit(r7, "sql/blog_0001_initial.sql", [('"body" text', '"body" text')])  # no-op
rep7 = extract(r7)
print("== m7 changed:", rep7.changed); print("   created:", rep7.created)
after = documents(r7)
print("   verified preserved:", all(after[k].payload == v for k, v in kept.items()), "| all still present:", all(k in after for k in kept))
rep7b = extract(r7)
print("   2nd run after verify: created", rep7b.created, "changed", rep7b.changed)
print("   verified preserved again:", all(documents(r7)[k].payload == v for k, v in kept.items()))
# delete fixture file entirely? changed file with node disappearing
r8 = new_project(base, "m8"); extract(r8)
edit(r8, "blog/models.py", [("        self.save(update_fields=[\"status\", \"published_at\"])\n", "")])
rep8 = extract(r8); print("== m8 removed self.save: changed", rep8.changed, "| writes edge still in store:", any("writes" in k for k in extracted(r8)))
shutil.rmtree(base)
