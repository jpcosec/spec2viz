import sys, yaml, tempfile, pathlib
sys.path.insert(0, "tests/visual")
import test_notations_parity as t
from specir.visual.notation_style import load_notation, NotationSpec
d = t._with(diagram_type="mindmap")
p = pathlib.Path(tempfile.mkdtemp(dir="/dev/shm/ir13j")) / "mm.yml"
p.write_text(yaml.safe_dump(d), encoding="utf-8")
for label, fn in (("load_notation", lambda: load_notation(p)), ("NotationSpec.model_validate", lambda: NotationSpec.model_validate(d))):
    try:
        fn(); print(label, "NO ERROR")
    except Exception as e:
        print(label, type(e).__module__, type(e).__name__); print(str(e)); print("---")
