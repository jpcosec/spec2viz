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
const [db, text, explicit] = JSON.parse(process.argv[1]);
globalThis.DB = db;
globalThis.window = { ATOMS_EXPLICIT: explicit || {} };
const nodeEl = { closest: () => ({ id: 'v1' }) };
const hit = findAtomData(text, nodeEl);
console.log(JSON.stringify(hit ? (hit.explicit ? hit.list.map(a => a.id) : hit.title) : null));
"""


def _match(template: Path, db: dict, text: str, explicit: dict | None = None):
    src = template.read_text(encoding="utf-8")
    block = re.search(r"// <atom-match>.*?// </atom-match>", src, re.S)
    assert block, "falta el bloque <atom-match> en el template"
    code = HARNESS % block.group(0)
    out = subprocess.run(
        ["node", "-e", code, json.dumps([db, text, explicit])], capture_output=True, text=True, check=True
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


    def test_explicit_atoms_win_and_all_are_returned(self, template):
        explicit = {"v1": {"producto": {"title": "producto", "explicit": True, "list": [
            {"id": "a1", "title": "T", "question": "what", "body": "x"},
            {"id": "a2", "title": "T", "question": "what", "body": "y"},
        ]}}}
        # "Producto" calzaria por fuzzy con otro atomo; con explicito solo salen los suyos
        assert _match(template, DB, "Producto", explicit) == ["a1", "a2"]

    def test_node_without_explicit_falls_back_to_fuzzy(self, template):
        explicit = {"v1": {"otro": {"title": "otro", "explicit": True, "list": [{"id": "a1", "title": "T", "question": "what", "body": "x"}]}}}
        assert _match(template, DB, "Evaluación de órdenes", explicit) == "Evaluación de órdenes"


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


MD_HARNESS = """
const escapeHtmlUnused = null;
%s
const [body, known] = JSON.parse(process.argv[1]);
console.log(JSON.stringify(renderAtomBody(body, id => known[id] || null)));
"""


def _md(template: Path, body: str, known: dict | None = None) -> str:
    src = template.read_text(encoding="utf-8")
    block = re.search(r"// <atom-md>.*?// </atom-md>", src, re.S)
    assert block
    out = subprocess.run(
        ["node", "-e", MD_HARNESS % block.group(0), json.dumps([body, known or {}])],
        capture_output=True, text=True, check=True,
    )
    return json.loads(out.stdout)


@pytest.mark.skipif(shutil.which("node") is None, reason="requiere node para ejecutar el template")
@pytest.mark.parametrize("template", TEMPLATES, ids=lambda p: p.parent.name)
class TestAtomMarkdown:
    def test_html_is_escaped(self, template):
        html = _md(template, '<script>alert(1)</script> & "x"')
        assert "<script>" not in html and "&lt;script&gt;" in html and "&amp;" in html

    def test_inline_formatting(self, template):
        html = _md(template, "**fuerte** y *suave* y `cod <b>`")
        assert "<strong>fuerte</strong>" in html and "<em>suave</em>" in html and "<code>cod &lt;b&gt;</code>" in html

    def test_paragraphs_breaks_and_lists(self, template):
        html = _md(template, "uno\ndos\n\n- a\n- b")
        assert "<p>uno<br>dos</p>" in html and "<ul><li>a</li><li>b</li></ul>" in html

    def test_external_link_only_safe_schemes(self, template):
        assert 'href="https://x.cl/a"' in _md(template, "[t](https://x.cl/a)")
        assert "<a " not in _md(template, "[t](javascript:alert(1))")

    def test_atom_link_present_and_absent(self, template):
        known = {"a-1": {"id": "a-1", "title": "Plazo <48h>", "question": "what", "body": "x"}}
        html = _md(template, "ver [[a-1]]", known)
        assert 'data-atom-id="a-1"' in html and "Plazo &lt;48h&gt;" in html
        html = _md(template, "ver [[a-9]]", known)
        assert "atom-link-missing" in html and "data-atom-id" not in html and ">a-9<" in html

    def test_predicate_link(self, template):
        known = {"a-1": {"id": "a-1", "title": "Destino", "question": "what", "body": "x"}}
        html = _md(template, "[depende de:: [[a-1]]]", known)
        assert "<em>depende de</em>: <a" in html and ">Destino</a>" in html


@pytest.mark.skipif(shutil.which("node") is None, reason="requiere node para ejecutar el template")
@pytest.mark.parametrize("template", TEMPLATES, ids=lambda p: p.parent.name)
def test_tabs_follow_the_target_atom(template):
    src = template.read_text(encoding="utf-8")
    block = re.search(r"// <atom-md>.*?// </atom-md>", src, re.S).group(0)
    code = block + """
const target = { id: 't', title: 'Etapa', question: 'what' };
console.log(JSON.stringify([atomTabLabels([target], false), atomTabLabels([{question:'how_not',title:'T'}], true)]));
"""
    out = subprocess.run(["node", "-e", code], capture_output=True, text=True, check=True)
    assert json.loads(out.stdout) == [["what"], ["how not · T"]]
    # la navegacion por enlace regenera las pestanas con el atomo destino (no deja las del anterior)
    assert "showAtoms([target], false)" in src
