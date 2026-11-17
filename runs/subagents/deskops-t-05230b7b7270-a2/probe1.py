import sys; sys.path.insert(0, "/mnt/ssd/proyectos/SLDB_1/IR/runs/subagents/deskops-t-05230b7b7270-a2")
from probe_lib import *
root = new("base"); r = extract(root)
print("CREATED", len(r.created)); [print(" ", x) for x in r.created]
print("NOT_DERIVED"); [print(" ", x) for x in r.not_derived]
print("DOCS tipos:", sorted({d.model_name for d in ext(root).values()}))
base = summary(root)
for t in base: print(t)
# provenance
for k, d in ext(root).items():
    f = d.payload.get("attributes") or d.payload
    assert f["origen"] in ("observado","derivado") and f["verificacion"]=="sin_verificar" and not f["evidencia"] and not f["verificado_por"], k
print("provenance ok")
# idempotence
before = digest(root); r2 = extract(root); print("IDEMP", digest(root)==before, len(r2.created), len(r2.changed), len(r2.unchanged))
