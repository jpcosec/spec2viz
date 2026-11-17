import sys; sys.path.insert(0, "/mnt/ssd/proyectos/SLDB_1/IR/runs/subagents/deskops-t-05230b7b7270-a2")
from probe_lib import *
from sldb.api.code import code_facts
import re
root = new("anch"); extract(root)
facts = {}
for f in code_facts(root)["facts"]:
    mod=f["attrs"]["module"]; n="" if f["id"]==mod else f["id"].removeprefix(mod+".")
    facts[f"code:{f['path']}::{n}"]=f
d=docs(root); anchors={v.name:v for v in d.values() if v.model_name=="CodeAnchorDoc"}
print("anchors", len(anchors))
bad=0
for a in anchors.values():
    f=facts[a.payload["ref"]]; c=a.payload["claim"]
    ok = f["source_hash"] in c and f["path"] in c and f"líneas {f['span']['start_line']}-{f['span']['end_line']}" in c and a.payload["seen"]==f["fingerprints"]
    bad+= not ok
print("anchor mismatches", bad)
for k,v in ext(root).items():
    p=v.payload; t=p.get("description") or p.get("notes"); names=re.findall(r"\[(anchor-[0-9a-f]{16})\]",t)
    f=p.get("attributes") or p
    assert names and set(names)<=set(anchors), k
    print(k.split(":")[0], f["origen"], f["verificacion"], repr(f["evidencia"]), len(set(names)), "rule" , re.search(r"regla (\S+)", t).group(1))
