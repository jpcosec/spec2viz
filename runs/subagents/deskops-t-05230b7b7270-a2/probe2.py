import sys; sys.path.insert(0, "/mnt/ssd/proyectos/SLDB_1/IR/runs/subagents/deskops-t-05230b7b7270-a2")
from probe_lib import *
def run(name, edits, show=True):
    root = new(name)
    for e in edits: sub(root, *e)
    r = extract(root)
    print(f"=== {name}: created={len(r.created)}")
    return root, r
def titles(root): return sorted((d.model_name, d.payload.get("title")) for d in ext(root).values() if d.model_name!="RelationDoc")
def rels(root): return sorted(d.payload["title"] for d in ext(root).values() if d.model_name=="RelationDoc")
# M1: rename model Post->Article (all refs in models/views/serializers) and table
M = "blog/models.py"
root, r = run("m_model", [(M,"class Post(","class Article("),(M,"post: Post","post: Article"),("blog/views.py","from blog.models import Post","from blog.models import Article as Post")])
print(titles(root)); print(rels(root)); print(r.not_derived)
