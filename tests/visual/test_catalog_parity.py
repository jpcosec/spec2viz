"""specIR's catalog against spec2viz's, as the oracle (IR13b; `parity` marker). What spec2viz answered
to each case at revision 2de1056 is in `goldens/spec2viz-2de1056-oracle.json` (`oracle.py`).

- Validating a registry: sldb's `check_catalog` (what `sldb notations sync --catalog --check` runs)
  gives, entry by entry, the same view, spec, error class and message as spec2viz's, over the
  registries of spec2viz's catalog path and notation tests and its own `docs/architecture/vistas.yml`.
- Syncing a registry: `sldb notations sync --catalog` leaves the same documents as `spec2viz catalog
  sync` (IR13a's comparison), and with one failing view neither writes anything.
- Building the catalog: `render_catalog` gives spec2viz's page byte for byte over spec2viz's catalog
  fixtures and the cases of its tests (sources of every kind, stores of stores, `project.yml`,
  fragments, resolved views, atoms from a folder, explicit atoms and refs, atoms of a view's store,
  coverage from a snapshot). One declared difference: the atom and coverage warnings are sldb
  findings (`level`, `code`, `subject`, `what`, `fix`) where spec2viz wrote `{scope, message}`;
  they are compared by their text. So the same views, categories, navigation, atoms per element
  (`ATOMS_EXPLICIT`, `ATOMS_LINKED`, `ATOMS_BY_VIEW`, `ATOMS_DB`, `REFS_EXPLICIT`) and coverage per
  view (`COVERAGE_BY_VIEW`) are embedded."""

from __future__ import annotations

import json
import re
import shutil
import sys
from pathlib import Path

import pytest
import sldb.api as sldb_api
import yaml
from sldb.api.notations import SpecSync, check_catalog, sync_catalog

from specir.visual.catalog import render_catalog
from test_catalog import (
    NOTATION, OWN_NOTATION, RESOLVED_NOTATION, SPECS, _explicit_project, _repo, _resolved_project, _simple, _sources, _two_atoms, _vistas,
    fixture_repo, sldb_cli, spec_docs,
)
from test_sync_generation_parity import _assert_same_store

sys.path.insert(0, str(Path(__file__).resolve().parent))
import oracle  # noqa: E402

pytestmark = pytest.mark.parity

WARNINGS = re.compile(r"window\.SPEC2VIZ_(ATOM|COVERAGE)_WARNINGS = (\[.*?\]); ")


def _ours(entry, exc):
    return (entry["vista"], Path(entry["spec"]).name, type(exc).__name__ if exc else None, str(exc) if exc else None)


def _same_check(config: Path, store: Path | None = None) -> list:
    ours = oracle.scrub([_ours(entry, exc) for entry, exc in check_catalog(config, store)], oracle.tmp_root(config))
    assert ours == oracle.expect("check_catalog", config, store, roots=(oracle.tmp_root(config),))
    return ours


# --- validating a registry ----------------------------------------------------------------------

@pytest.mark.parametrize("view", [
    {"specs": ["flows/lanes.yml"], "notation": "notations/flow-own.yml", "src": "flows/lanes.mmd"},
    {"specs": ["docs/architecture/flows/lanes.yml"], "notation": "docs/architecture/notations/flow-own.yml"},
    {"specs": ["flows/missing.yml"]},
    {"specs": ["flows/lanes.yml"], "notation": "notations/missing.yml"},
    {"specs": ["flows/lanes.yml"], "src": "flows/missing.mmd"},
    {"specs": ["flows/lanes.yml"], "notation": "no-such-notation"},
    {"specs": ["flows/lanes.yml"], "notation": "deployment"},
    {"specs": ["flows/lanes.yml"], "notation": "activity"},
])
def test_check_catalog_reports_what_spec2viz_reports(tmp_path, view):
    root, arch = _repo(tmp_path)
    _same_check(_vistas(arch, **view))


@pytest.mark.parametrize("field", ["specs", "notation", "src"])
def test_check_catalog_reports_ambiguity_like_spec2viz(tmp_path, field):
    root, arch = _repo(tmp_path)
    rel = {"specs": "flows/lanes.yml", "notation": "notations/flow-own.yml", "src": "flows/lanes.mmd"}[field]
    (root / rel).parent.mkdir(parents=True, exist_ok=True)
    (root / rel).write_text((arch / rel).read_text(encoding="utf-8") + "\n# otra copia\n", encoding="utf-8")
    errors = _same_check(_vistas(arch, specs=["flows/lanes.yml"], notation="notations/flow-own.yml", src="flows/lanes.mmd"))
    assert errors[0][2] == "AmbiguousPathError"


def test_check_catalog_of_spec2viz_s_own_registry(tmp_path):
    root = fixture_repo(tmp_path)
    results = _same_check(root / "docs" / "architecture" / "vistas.yml")
    assert len(results) == 11


def test_check_catalog_with_a_store_notation(tmp_path):
    root, arch = _repo(tmp_path)
    sldb_api.init_store(root)
    config = _vistas(arch, specs=["flows/lanes.yml"], notation="flow-own")
    assert _same_check(config, root / ".sldb")[0][2] == "UnknownNotationError"
    (arch / "own.yml").write_text(yaml.safe_dump(OWN_NOTATION), encoding="utf-8")
    assert sldb_cli("notations", "sync", "--notation", arch / "own.yml", "--store", root / ".sldb")[0] == 0
    assert _same_check(config, root / ".sldb")[0][2] is None


# --- syncing a registry -------------------------------------------------------------------------

def _sync_ours(tmp_path: Path, config_rel: str) -> Path:
    root = fixture_repo(tmp_path / "sldb")
    sldb_api.init_store(root)
    sync_catalog(SpecSync(root / ".sldb"), root / config_rel)
    return root


def test_catalog_sync_leaves_what_spec2viz_leaves(tmp_path):
    ours = _sync_ours(tmp_path, "docs/architecture/vistas.yml")
    _assert_same_store(ours, oracle.expect("catalog_sync_documents", tmp_path / "spec2viz", "docs/architecture/vistas.yml", roots=(tmp_path,)))
    assert len(spec_docs(ours / ".sldb")) == 11


def _failing_catalog_root(base: Path) -> tuple[Path, Path]:
    """A synced-nothing repo whose registry has a last view that draws with the wrong type."""
    root = fixture_repo(base)
    sldb_api.init_store(root)
    config = root / "docs" / "architecture" / "vistas.yml"
    data = yaml.safe_load(config.read_text(encoding="utf-8"))
    data["vistas"][-1]["notation"] = "deployment"
    config.write_text(yaml.safe_dump(data, allow_unicode=True), encoding="utf-8")
    return root, config


def _invalid_lines(output: str, root: Path) -> list[str]:
    return [line.replace(str(root), "<root>") for line in output.splitlines() if line.startswith("Invalid:")]


def test_a_failing_view_makes_both_write_nothing(tmp_path):
    root, config = _failing_catalog_root(tmp_path / "sldb")
    rc, output = sldb_cli("notations", "sync", "--catalog", config, "--store", root / ".sldb")
    assert rc == 1 and "NotationMismatchError" in output, output
    assert not spec_docs(root / ".sldb")
    rc_oracle, named, written, invalid = oracle.expect("catalog_sync_failure", tmp_path / "spec2viz", roots=(tmp_path,))
    assert rc_oracle == 1 and named and written == 0  # spec2viz exited 1, named the error and wrote no SpecDoc
    assert _invalid_lines(output, root) == invalid


# --- building the catalog -----------------------------------------------------------------------

def _warnings(page: str) -> tuple[str, list]:
    """The page without its warnings, and the warnings' text (subject or scope, and message)."""
    found = []
    for kind, raw in WARNINGS.findall(page):
        found.append((kind, sorted((w.get("message") or w.get("what"), (w.get("scope") or w.get("subject")).split("#")[0]) for w in json.loads(raw))))
    return WARNINGS.sub(lambda m: f"window.SPEC2VIZ_{m.group(1)}_WARNINGS = <warnings>; ", page), found


def _same_page(config: Path, **options) -> str:
    tmp = oracle.tmp_root(config)
    ours = render_catalog(config, **options)
    ours_page, ours_warnings = _warnings(ours)
    oracle_digest, oracle_warnings = oracle.expect("catalog_page", config, roots=(tmp,), **options)
    assert oracle.page_digest(oracle.scrub(ours_page, tmp)) == oracle_digest
    assert oracle.unhash(oracle.scrub(ours_warnings, tmp)) == oracle_warnings
    return ours


@pytest.mark.parametrize("config", ["docs/architecture/vistas.yml", "examples/catalog/project.yml", "examples/catalog/leaves/architecture-vistas.yml"])
def test_the_catalog_of_spec2viz_s_fixtures_is_spec2viz_s(tmp_path, config):
    root = fixture_repo(tmp_path)
    page = _same_page(root / config)
    assert page.count("<section id=") >= 1


def test_the_catalog_of_a_synced_project_is_spec2viz_s(tmp_path):
    root = fixture_repo(tmp_path)
    sldb_api.init_store(root)
    sync_catalog(SpecSync(root / ".sldb"), root / "docs" / "architecture" / "vistas.yml")
    _same_page(root / "docs" / "architecture" / "vistas.yml")


def test_every_kind_of_source_with_atoms_is_spec2viz_s(tmp_path):
    (tmp_path / "template.html").write_text("<html><body><nav>{{NAV}}</nav><main>{{SECTIONS}}</main><script>window.ATOMS_DB = {{ATOMS_DB}};</script></body></html>", encoding="utf-8")
    _sources(tmp_path)
    (tmp_path / "vistas.yml").write_text("""
template: template.html
vistas:
  - {id: flow, category: Core, title: Flow, lbl: Flow label, desc: Flow desc, src: flow.mmd, specs: [spec-a], puml: flow.puml, notes: [gap one]}
  - {id: picture, category: Core, title: Picture, src: diagram.svg, tags: [x:y]}
  - {id: html-view, category: Extras, title: Html View, src: snippet.html}
  - {id: matrix, category: Extras, title: Matrix, src: matrix.vega.json}
  - {id: deploy, category: Extras, title: Deploy, src: deploy.puml}
""", encoding="utf-8")
    atoms = _two_atoms(tmp_path)
    _same_page(tmp_path / "vistas.yml", atoms_dir=atoms)
    _same_page(tmp_path / "vistas.yml", atoms_dir=atoms, atoms_tags=["stock"])


@pytest.mark.parametrize("atoms_a, atoms_b", [(["atom-uno", "atom-dos"], None), (["atom-uno", "no-existe"], None), (["atom-uno"], ["atom-dos"])])
def test_explicit_atoms_are_spec2viz_s(tmp_path, atoms_a, atoms_b):
    atoms = _explicit_project(tmp_path, atoms_a, atoms_b)
    (atoms / "atom-uno.md").write_text("---\ntitle: Uno\nfive_wh_one_plus: what\nid: atom-uno\n---\nVer [[atom-ruido]].\n", encoding="utf-8")
    _same_page(tmp_path / "vistas.yml", atoms_dir=atoms)


def test_strict_atoms_fail_both(tmp_path):
    atoms = _explicit_project(tmp_path, ["no-existe"], None)
    with pytest.raises(Exception, match="no-existe") as ours:
        render_catalog(tmp_path / "vistas.yml", atoms_dir=atoms, strict_atoms=True)
    oracle_error, oracle_text = oracle.expect("catalog_page_error", tmp_path / "vistas.yml", atoms_dir=atoms, strict_atoms=True, roots=(tmp_path,))
    assert "no-existe" in oracle_text
    assert type(ours.value).__name__ == oracle_error == "UnknownAtomError"


@pytest.mark.parametrize("view_notation", [None, "infra-own.yml"])
def test_resolved_views_are_spec2viz_s(tmp_path, view_notation):
    root, arch = _resolved_project(tmp_path, view_notation)
    page = _same_page(arch / "vistas.yml")
    assert "data-resolved-from" in page


def test_stores_of_stores_and_unique_anchors_are_spec2viz_s(tmp_path):
    (tmp_path / "template.html").write_text("<html><body><aside>{{NAV}}</aside><main>{{FILTERS}}{{SECTIONS}}</main></body></html>", encoding="utf-8")
    for folder in [tmp_path / "alpha" / "docs" / "vistas", tmp_path / "beta" / "docs" / "vistas"]:
        folder.mkdir(parents=True)
        project = folder.parent.parent
        (project / "project.yaml").write_text("project_name: Demo\nclient: sample\n", encoding="utf-8")
        (project / "specs").mkdir()
        (project / "specs" / "same-view.yml").write_text("id: same-view\ntitle: Same\ntype: component\nversion: '1.0'\ndata:\n  nodes: {}\n  edges: []\n", encoding="utf-8")
        (project / "rendered").mkdir()
        (project / "rendered" / "same-view.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
        (folder / "vistas.yml").write_text("template: template.html\nvistas:\n  - id: vista01\n    title: Demo\n    category: Arquitectura\n"
                                           "    specs:\n      - same-view\n    mmd: ../../rendered/same-view.mmd\n", encoding="utf-8")
    (tmp_path / "catalog.yml").write_text("template: template.html\ncategory: Raiz\ntags: [t:1]\nstores:\n  - path: alpha/docs/vistas/vistas.yml\n"
                                          "  - {path: beta/docs/vistas/vistas.yml, project: otro/p, category: Beta, type: component, tags: [d:x]}\n"
                                          "items:\n  - {id: own, title: Propia, desc: un diagrama de secuencia}\n", encoding="utf-8")
    _same_page(tmp_path / "catalog.yml")


def test_a_fragment_and_a_simple_registry_are_spec2viz_s(tmp_path):
    _same_page(_simple(tmp_path, "<html><body>{{NAV}}{{FILTERS}}{{SECTIONS}}</body></html>"))
    (tmp_path / "bundle.html").write_text('<html><body><section id="d1"><div class="board"><pre class="mermaid">graph TD\\nA-->B</pre></div></section></body></html>', encoding="utf-8")
    (tmp_path / "catalog.yml").write_text("template: template.html\nitems:\n  - id: frag\n    title: Fragment\n    src: bundle.html#d1\n    type: component\n", encoding="utf-8")
    _same_page(tmp_path / "catalog.yml")


# --- atoms of a view's store --------------------------------------------------------------------

MODULE = "ir13b_atom_models"
MODELS = '''from pydantic import Field
from sldb import StructuredNLDoc


class AtomDoc(StructuredNLDoc):
    __template__ = "---\\nid: ⸢rev•id⸥\\ntitle: ⸢rev•title⸥\\nfive_wh_one_plus: ⸢rev•five_wh_one_plus⸥\\ntags: ⸢rev,list•tags⸥\\n---\\n\\n⸢rev•answer⸥"
    id: str = Field(description="Atom id.")
    title: str = Field(description="Title.")
    five_wh_one_plus: str = Field(description="The question.")
    tags: list[str] = Field(default_factory=list, description="Tags.")
    answer: str = Field(description="Body.")
'''


def test_atoms_of_the_view_s_store_and_its_refs_are_spec2viz_s(tmp_path, monkeypatch):
    root = tmp_path / "proj"
    root.mkdir()
    (root / f"{MODULE}.py").write_text(MODELS, encoding="utf-8")
    monkeypatch.syspath_prepend(str(root))
    sldb_api.init_store(root)
    assert sldb_cli("models", "add", f"{MODULE}:AtomDoc", "--store", root / ".sldb", "--pythonpath", root)[0] == 0
    for atom_id, title, q in (("atom-runtime", "Runtime", "what"), ("atom-core", "Core", "why")):
        sldb_api.create_document(root / ".sldb", "AtomDoc", f"desk/atoms/{atom_id}.md",
                                 {"id": atom_id, "title": title, "five_wh_one_plus": q, "tags": ["dominio:x"], "answer": f"Cuerpo {atom_id}"}, pythonpath=str(root))
    assert sldb_cli("edges", "rebuild", "--store", root / ".sldb", cwd=root)[0] == 0
    docs = root / "docs"
    docs.mkdir()
    spec = {"id": "arq", "title": "Arq", "type": "component", "version": "1.0",
            "data": {"nodes": {"cli": {"label": "CLI", "atoms": ["atom-core"], "refs": ["AtomDoc:atom-runtime", "AtomDoc:no-existe"]}, "core": {"label": "Core"}}, "edges": []}}
    (docs / "arq.yml").write_text(yaml.safe_dump(spec), encoding="utf-8")
    (docs / "arq.mmd").write_text("graph TD\ncli-->core\n", encoding="utf-8")
    (docs / "vistas.yml").write_text("vistas:\n  - {id: arq, title: Arq, src: arq.mmd, specs: [arq.yml], type: component}\n  - {id: otra, title: Otra, src: arq.mmd}\n", encoding="utf-8")
    monkeypatch.setenv("PYTHONPATH", str(root))
    page = _same_page(docs / "vistas.yml")
    assert "Cuerpo atom-core" in page and '"ref": "AtomDoc:atom-runtime"' in page
