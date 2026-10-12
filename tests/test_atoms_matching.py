"""Asociacion nodo<->atomo (template) y alcance de los atomos embebidos (deskops)."""
import json
import re
import shutil
import subprocess
from pathlib import Path

import pytest
from click.testing import CliRunner

from spec2viz.cli import main
from spec2viz.deskops import filter_atoms_payload, parse_atoms, split_shared_atoms

ROOT = Path(__file__).resolve().parents[1]
TEMPLATES = [ROOT / "spec2viz" / "templates" / "default.html", ROOT / "docs" / "architecture" / "template.html"]

HARNESS = """
const norm = (str) => str ? str.trim().toLowerCase().replace(/\\s+/g, ' ') : '';
const getViewAtomsDb = () => DB;
%s
const [db, text] = JSON.parse(process.argv[1]);
globalThis.DB = db;
const hit = findAtomData(text, null);
console.log(JSON.stringify(hit ? hit.title : null));
"""


def _match(template: Path, db: dict, text: str):
    src = template.read_text(encoding="utf-8")
    block = re.search(r"// <atom-match>.*?// </atom-match>", src, re.S)
    assert block, "falta el bloque <atom-match> en el template"
    code = HARNESS % block.group(0)
    out = subprocess.run(
        ["node", "-e", code, json.dumps([db, text])], capture_output=True, text=True, check=True
    )
    return json.loads(out.stdout)


def _entry(title, aliases=None):
    return {"title": title, "aliases": aliases or [], "atoms": {"what": {"id": "a", "body": "b"}}}


DB = {
    "evaluacion de ordenes": _entry("Evaluación de órdenes", ["evaluacion de ordenes", "evaluacion", "ordenes"]),
    "homologacion de producto": _entry("Homologación de producto", ["homologacion de producto", "homologacion", "producto"]),
}


@pytest.mark.skipif(shutil.which("node") is None, reason="requiere node para ejecutar el template")
@pytest.mark.parametrize("template", TEMPLATES, ids=lambda p: p.parent.name)
class TestTemplateMatching:
    def test_one_shared_word_is_not_a_match(self, template):
        # antes: una palabra de 3+ letras en comun bastaba (bestScore >= 10)
        assert _match(template, DB, "Cerrar producto vencido") is None
        assert _match(template, DB, "Revisar ordenes") is None

    def test_unrelated_node_has_no_atom(self, template):
        assert _match(template, DB, "Enviar correo al cliente") is None

    def test_exact_title_matches_ignoring_accents_punctuation_case(self, template):
        assert _match(template, DB, "Evaluación de órdenes") == "Evaluación de órdenes"
        assert _match(template, DB, "HOMOLOGACION DE PRODUCTO (R1)") == "Homologación de producto"

    def test_phrase_contained_matches(self, template):
        assert _match(template, DB, "Paso: homologacion de producto nuevo") == "Homologación de producto"

    def test_two_shared_tokens_matching_most_of_the_alias(self, template):
        assert _match(template, DB, "Evaluacion ordenes") == "Evaluación de órdenes"


def _two_atoms(tmp_path):
    d = tmp_path / "atoms"
    d.mkdir()
    for i, (title, tags) in enumerate([("Uno", ["dominio:oc"]), ("Dos", ["dominio:stock"])]):
        (d / f"a{i}.md").write_text(
            f"---\ntitle: {title}\nfive_wh_one_plus: what\nid: a{i}\ntags: {json.dumps(tags)}\n---\nCuerpo {i}.\n",
            encoding="utf-8",
        )
    return d


def test_filter_atoms_payload_by_full_tag_or_value(tmp_path):
    payload = json.loads(parse_atoms(_two_atoms(tmp_path)))
    assert set(filter_atoms_payload(payload, ["dominio:oc"])) == {"uno"}
    assert set(filter_atoms_payload(payload, ["stock"])) == {"dos"}
    assert set(filter_atoms_payload(payload, None)) == {"uno", "dos"}
    assert filter_atoms_payload(payload, ["nada"]) == {}


def test_split_shared_atoms_emits_repeated_payload_once():
    p = {"x": {"title": "X", "atoms": {}}}
    shared, rest = split_shared_atoms({"v1": p, "v2": p, "v3": {}, "v4": {"y": {}}})
    assert shared == p
    assert set(rest) == {"v3", "v4"}
    assert split_shared_atoms({"v1": p}) == ({}, {"v1": p})


def test_catalog_build_embeds_atoms_once_and_honors_atoms_tag(tmp_path):
    atoms = _two_atoms(tmp_path)
    (tmp_path / "f.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    cfg = tmp_path / "vistas.yml"
    cfg.write_text(
        "vistas:\n"
        + "".join(f"  - id: v{i}\n    title: V{i}\n    src: f.mmd\n    type: mermaid\n" for i in range(3)),
        encoding="utf-8",
    )
    runner = CliRunner()

    def build(*extra):
        out = tmp_path / "o.html"
        res = runner.invoke(main, ["catalog", "build", "--config", str(cfg), "--out", str(out), "--atoms-dir", str(atoms), *extra])
        assert res.exit_code == 0, res.output
        return out.read_text(encoding="utf-8")

    html = build()
    assert html.count("Cuerpo 0.") == 1 and html.count("Cuerpo 1.") == 1  # una vez, no una por vista
    html = build("--atoms-tag", "dominio:oc")
    assert "Cuerpo 0." in html and "Cuerpo 1." not in html
