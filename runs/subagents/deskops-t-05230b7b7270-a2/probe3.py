import sys; sys.path.insert(0, "/mnt/ssd/proyectos/SLDB_1/IR/runs/subagents/deskops-t-05230b7b7270-a2")
from probe_lib import *
M="blog/models.py"; V="blog/views.py"; U="blog/urls.py"; S="blog/serializers.py"
def titles(root): return sorted((d.model_name, d.payload.get("title")) for d in ext(root).values() if d.model_name!="RelationDoc")
def rels(root): return sorted(d.payload["title"] for d in ext(root).values() if d.model_name=="RelationDoc")
def case(name, edits):
    root = new(name)
    for e in edits: sub(root, *e)
    r = extract(root)
    print(f"=== {name}: created={len(r.created)}"); print(titles(root)); print(rels(root)); print("ND", r.not_derived)
    return root
print(open("/mnt/ssd/proyectos/SLDB_1/IR/tests/fixtures/blog_app/blog/serializers.py").read())
case("m_model", [(M,"Post","Article"),(V,"Post","Article"),(S,"Post","Article")])
case("m_table", [(M,'db_table = "posts"','db_table = "entries"')])
case("m_nometa", [(M,'    class Meta:\n        db_table = "posts"\n\n','')])
case("m_router", [(U,'register("posts"','register("articles"')])
case("m_method", [(V,'methods=["post"]','methods=["put"]')])
case("m_action", [(V,'def publish(self','def release(self'),(V,'post.publish(','post.publish(')])
case("m_pred", [(M,"can_publish","ensure_publishable")])
case("m_pred2", [(M,"can_publish","is_allowed")])
case("m_state", [(M,'PUBLISHED = "published", "Published"','PUBLISHED = "published", "Live"\n        ARCHIVED = "archived", "Archived"')])
