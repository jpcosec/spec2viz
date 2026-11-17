import shutil, subprocess, sys, json, hashlib
from pathlib import Path
import sldb.api as api
from specir.install import package_pythonpath
from specir.extract import extract
FIX = Path("/mnt/ssd/proyectos/SLDB_1/IR/tests/fixtures/blog_app")
BIN = Path(sys.executable).parent
def new(name):
    root = Path("/dev/shm/t05") / name
    shutil.rmtree(root, ignore_errors=True)
    shutil.copytree(FIX, root, ignore=shutil.ignore_patterns("__pycache__"))
    subprocess.run([str(BIN/"sldb"), "stores", "init", "--path", str(root)], cwd=root, check=True, capture_output=True)
    subprocess.run([sys.executable, "-m", "specir.install", "--store", str(root/".sldb")], cwd=root, check=True, capture_output=True)
    return root
def docs(root):
    return {f"{d.model_name}:{d.name}": d for d in api.load_runtime_documents(root/".sldb", package_pythonpath())}
def ext(root):
    return {k: d for k, d in docs(root).items() if d.model_name not in ("CodeAnchorDoc",) and (d.payload.get("origen") or (d.payload.get("attributes") or {}).get("origen"))}
def digest(root):
    out = {}
    for base in (root/".sldb", root/"specir"):
        for p in sorted(base.rglob("*")):
            if p.is_file() and "cache" not in str(p).lower(): out[str(p)] = hashlib.sha256(p.read_bytes()).hexdigest()
    return out
def sub(root, rel, old, new_):
    p = root/rel; t = p.read_text(); assert old in t, (rel, old); p.write_text(t.replace(old, new_))
def summary(root):
    e = ext(root)
    return sorted((k, d.payload.get("title"), d.payload.get("route"), d.payload.get("method"), d.payload.get("source_id"), d.payload.get("target_id")) for k, d in e.items())
