import sys, copy
sys.path.insert(0, "tests/visual")
from specir.visual.notation_style import NotationSpec, load_notation
import specir.visual.notation_style as ns, sldb
print("sldb", sldb.__file__)
spec = load_notation("statechart")
d = spec.model_dump(); d["diagram_type"]="mindmap"
for src, data in (("load_notation(statechart)+mindmap", d),):
    try: NotationSpec.model_validate(data); print("NO ERROR")
    except Exception as e: print(src, "->", type(e).__name__, str(e))
