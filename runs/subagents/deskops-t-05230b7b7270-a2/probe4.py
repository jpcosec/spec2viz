import sys; sys.path.insert(0, "/mnt/ssd/proyectos/SLDB_1/IR/runs/subagents/deskops-t-05230b7b7270-a2")
from probe_lib import *
import re
M="blog/models.py"; V="blog/views.py"; U="blog/urls.py"; S="blog/serializers.py"; Q="sql/blog_0001_initial.sql"
def titles(root): return sorted((d.model_name, d.payload.get("title")) for d in ext(root).values() if d.model_name!="RelationDoc")
def rels(root): return sorted(d.payload["title"] for d in ext(root).values() if d.model_name=="RelationDoc")
# rename table in model+sql
root = new("t_table"); sub(root,M,'"posts"','"entries"'); p=root/Q; p.write_text(p.read_text().replace('"posts"','"entries"')); r=extract(root)
print("TABLE rename:", [t for t in titles(root) if t[0]=="TableDoc"], [x for x in rels(root) if "entries" in x], r.not_derived[:1])
# model rename Post->Article keeping viewset
root = new("t_model")
sub(root,M,"class Post(","class Article("); sub(root,M,"post: Post","post: Article"); sub(root,V,"Post.objects","Article.objects"); sub(root,V,"import Post","import Article"); sub(root,S,"import Post","import Article"); sub(root,S,"model = Post","model = Article")
r=extract(root); print("MODEL rename:", titles(root), rels(root))
# m8 + verified
root = new("t_m8"); extract(root); store=root/".sldb"; pp=package_pythonpath()
w="RelationDoc:edge-op-post-publish--writes--table-posts"; before=docs(root)[w].payload
ver={"verificacion":"verificado","verificado_por":"human:jp","evidencia":"x"}
d=docs(root)["TableDoc:table-posts"]; api.save_document_payload(store,"TableDoc",d.name,{**d.payload,**ver},pp)
sub(root,M,'        self.save(update_fields=["status", "published_at"])\n','')
r=extract(root)
print("M8 writes kept:", w in docs(root), docs(root)[w].payload==before, "in changed:", w in r.changed, r.changed)
d2=docs(root)["TableDoc:table-posts"].payload; print("verified table kept:", d2["verificacion"], d2["verificado_por"], d2["evidencia"])
# change in sql file touching posts table
sub(root,Q,'"title" varchar(200) NOT NULL','"title" varchar(250) NOT NULL')
r=extract(root); print("SQL change: changed=", r.changed); d3=docs(root)["TableDoc:table-posts"].payload; print("verified table after SQL change intact:", d3==d2)
# unverified, changed file -> updated
root = new("t_upd"); extract(root); sub(root,Q,'"title" varchar(200) NOT NULL','"title" varchar(250) NOT NULL'); r=extract(root)
print("unverified updated:", r.changed, "varchar(250)" in docs(root)["TableDoc:table-posts"].payload["description"]); r=extract(root); print("then stable:", r.created, r.changed)
import subprocess
print("edges check rc", subprocess.run([str(BIN/"sldb"),"edges","check","--store",".sldb"],cwd=root,capture_output=True).returncode)
