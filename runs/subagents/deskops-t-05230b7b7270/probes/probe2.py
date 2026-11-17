"""Verified docs survive a re-extraction after a source change that moves anchors; stale-edge check."""
import sys, tempfile, shutil
from pathlib import Path
sys.path[:0] = ["/mnt/ssd/proyectos/SLDB_1/IR/tests", "/mnt/ssd/proyectos/SLDB_1/IR/tests/extract"]
import sldb.api as api
from specir.extract import extract
from specir.install import package_pythonpath
from extraction import new_project, documents, extracted
base = Path(tempfile.mkdtemp(dir="/dev/shm", prefix="probe2-"))
r = new_project(base, "x"); extract(r)
store, pp = r / ".sldb", package_pythonpath()
V = {"verificacion": "verificado", "verificado_por": "human:tester", "evidencia": "visto"}
docs = documents(r)
nodes = ["TableDoc:table-posts", "ApiOperationDoc:api-post-posts-id-publish", "DomainOperationDoc:op-post-publish", "DomainEntityDoc:entity-post", "HandlerDoc:handler-postviewset-publish"]
for k in nodes:
    d = docs[k]; api.save_document_payload(store, d.model_name, d.name, {**d.payload, **V, "title": d.payload["title"] + " (editado)"}, pp)
rels = [k for k in docs if k.startswith("RelationDoc:")]
for k in rels:
    d = docs[k]; api.save_document_payload(store, "RelationDoc", d.name, {**d.payload, "notes": d.payload["notes"] + " NOTA", "attributes": {**d.payload["attributes"], **V}}, pp)
kept = {k: documents(r)[k].payload for k in [*nodes, *rels]}
def edit(rel, a, b):
    p = r / rel; t = p.read_text(); assert a in t; p.write_text(t.replace(a, b))
edit("blog/models.py", "        self.published_at = timezone.now()\n", "        self.published_at = timezone.now()\n        self.status = self.Status.PUBLISHED\n")
edit("blog/views.py", "class PostViewSet", "# c1\n# c2\nclass PostViewSet")
edit("sql/blog_0001_initial.sql", '"body" text NOT NULL', '"body" text NOT NULL, "extra" text NULL')
before_n = len(documents(r))
rep = extract(r)
print("changed:", *rep.changed, sep="\n  "); print("created:", *rep.created, sep="\n  "); print("unchanged:", *rep.unchanged, sep="\n  ")
print("not_derived:", *rep.not_derived, sep="\n  ")
after = documents(r)
print("verified preserved:", {k: after[k].payload == v for k, v in kept.items()})
print("doc count before/after", before_n, len(after))
rep2 = extract(r); print("2nd run changed:", rep2.changed, "created:", rep2.created)
print("preserved 2nd:", all(documents(r)[k].payload == v for k, v in kept.items()))
shutil.rmtree(base)
