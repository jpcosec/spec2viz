import json
import re
from pathlib import Path

from spec2viz.deskops import SldbAtomResolver, build_atoms_by_view, build_coverage_by_view, build_deskops, parse_atoms, render_deskops


def test_parse_atoms_handles_missing_dir(tmp_path):
    assert parse_atoms(tmp_path / "missing") == "{}"


def test_parse_atoms_builds_index_and_skips_bad_files(tmp_path, capsys):
    atoms_dir = tmp_path / "atoms"
    atoms_dir.mkdir()

    (atoms_dir / "good.md").write_text(
        """---
title: Architecture
five_wh_one_plus: what
id: atom-1
---
Body text.
""",
        encoding="utf-8",
    )
    (atoms_dir / "bad.md").write_text(
        """---
: bad yaml
---
Broken.
""",
        encoding="utf-8",
    )

    payload = json.loads(parse_atoms(atoms_dir))
    assert payload["architecture"]["title"] == "Architecture"
    assert "architecture" in payload["architecture"]["aliases"]
    assert payload["architecture"]["atoms"]["what"]["id"] == "atom-1"
    assert payload["architecture"]["atoms"]["what"]["body"] == "Body text."

    out = capsys.readouterr().out
    assert "Failed to parse atom" in out


def test_render_deskops_renders_mermaid_svg_html_and_notes(tmp_path):
    base = tmp_path
    (base / "template.html").write_text(
        "<html><body><nav>{{NAV}}</nav><main>{{SECTIONS}}</main><script>window.ATOMS_DB = {{ATOMS_DB}};</script></body></html>",
        encoding="utf-8",
    )
    (base / "flow.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    (base / "diagram.svg").write_text("<svg><text>Diagram</text></svg>", encoding="utf-8")
    (base / "snippet.html").write_text("plain html snippet", encoding="utf-8")

    atoms_dir = base / "atoms"
    atoms_dir.mkdir()
    (atoms_dir / "atom.md").write_text(
        """---
title: Runtime
five_wh_one_plus: why
---
Because reasons.
""",
        encoding="utf-8",
    )

    (base / "vistas.yml").write_text(
        """
template: template.html
vistas:
  - id: flow
    category: Core
    title: Flow
    lbl: Flow label
    desc: Flow desc
    src: flow.mmd
    specs: [spec-a, spec-b]
    puml: flow.puml
    notes: [gap one, gap two]
  - id: picture
    category: Core
    title: Picture
    src: diagram.svg
  - id: html-view
    category: Extras
    title: Html View
    src: snippet.html
""",
        encoding="utf-8",
    )

    html = render_deskops(base / "vistas.yml", atoms_dir=atoms_dir)

    assert re.search(r'<a href="#flow-[a-f0-9]{8}">Flow label</a>', html)
    assert 'data-spec="spec-a"' in html
    assert 'data-spec="spec-b"' in html
    assert 'data-puml="flow.puml"' in html
    assert '<pre class="mermaid">' in html
    assert '<div class="board puml-board">' in html
    assert "plain html snippet" in html
    assert "Gaps de implementación" in html
    assert "window.ATOMS_DB = {}" in html
    assert "window.ATOMS_BY_VIEW" in html
    assert "window.COVERAGE_BY_VIEW" in html
    assert "because reasons." in html.lower()


def test_render_deskops_injects_atoms_before_body_when_placeholder_missing(tmp_path):
    base = tmp_path
    (base / "template.html").write_text(
        "<html><body>{{NAV}}{{SECTIONS}}</body></html>", encoding="utf-8"
    )
    (base / "flow.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    (base / "vistas.yml").write_text(
        """
template: template.html
vistas:
  - id: flow
    src: flow.mmd
""",
        encoding="utf-8",
    )

    html = render_deskops(base / "vistas.yml", atoms_dir=base / "missing")
    assert "window.ATOMS_DB = {}" in html
    assert "window.ATOMS_BY_VIEW" in html
    assert "window.COVERAGE_BY_VIEW" in html
    assert html.count("</body>") == 1


def test_build_coverage_by_view_projects_kgdb_payload(tmp_path):
    item = type(
        "Item",
        (),
        {
            "anchor_id": "view-1",
            "source_base_dir": str(tmp_path),
            "src": "docs/view.html#d1",
            "diagram_type": "component",
            "title": "View 1",
            "project": "demo/project",
        },
    )()
    snapshot_path = tmp_path / ".sldb/runtime/knowledge_graph.kg.json"
    snapshot_path.parent.mkdir(parents=True)
    snapshot_path.write_text(
        json.dumps(
            {
                "nodes": [
                    {
                        "identity": {"node_id": "view:view-1", "node_type": "view"},
                        "semantics": {
                            "view_id": "view-1",
                            "diagram_type": "component",
                            "title": "Projected View",
                            "source_ref": "docs/view.html#d1",
                        },
                        "edges": [
                            {
                                "target_id": "diagram_element:view-1:node:runtime",
                                "relation_type": "contains",
                                "metadata": {},
                            }
                        ],
                    },
                    {
                        "identity": {"node_id": "diagram_element:view-1:node:runtime", "node_type": "diagram_element"},
                        "semantics": {
                            "view_id": "view-1",
                            "diagram_type": "component",
                            "element_id": "node:runtime",
                            "element_kind": "node",
                            "label": "Runtime",
                        },
                        "edges": [
                            {
                                "target_id": "facet:what",
                                "relation_type": "expects_facet",
                                "metadata": {"facet": "what", "source_field": "label"},
                            },
                            {
                                "target_id": "atom:runtime",
                                "relation_type": "covers_facet",
                                "metadata": {
                                    "atom_id": "runtime",
                                    "facet": "what",
                                    "score": 1.0,
                                    "match_basis": "title",
                                    "evidence": 'label="Runtime" matched atom.title="Runtime"',
                                },
                            },
                        ],
                    },
                    {
                        "identity": {"node_id": "facet:what", "node_type": "facet"},
                        "semantics": {"facet": "what"},
                        "edges": [],
                    },
                ]
            }
        ),
        encoding="utf-8",
    )

    payload, warnings = build_coverage_by_view([item], kgdb_snapshot_path=snapshot_path)

    assert warnings == []
    assert payload["view-1"]["summary"]["elements_fully_covered"] == 1
    assert payload["view-1"]["elements"][0]["covered_facets"][0]["atom_id"] == "runtime"
    assert payload["view-1"]["elements"][0]["missing_facets"] == []


def test_build_atoms_by_view_uses_store_scoped_payload(monkeypatch, tmp_path):
    item = type("Item", (), {"anchor_id": "view-1", "source_base_dir": str(tmp_path), "src": None})()

    def fake_discover(self, _item):
        return Path("/tmp/store-a")

    def fake_load(self, store_path):
        assert store_path == Path("/tmp/store-a")
        return {"runtime": {"title": "Runtime", "aliases": ["runtime"], "atoms": {"what": {"id": "atom-1", "body": "Body"}}}}

    monkeypatch.setattr(SldbAtomResolver, "_discover_store_for_item", fake_discover)
    monkeypatch.setattr(SldbAtomResolver, "_load_store_payload", fake_load)

    atoms_by_view, warnings = build_atoms_by_view([item])

    assert warnings == []
    assert atoms_by_view == {
        "view-1": {
            "runtime": {"title": "Runtime", "aliases": ["runtime"], "atoms": {"what": {"id": "atom-1", "body": "Body"}}}
        }
    }


def test_build_deskops_writes_output_file(tmp_path):
    base = tmp_path
    (base / "template.html").write_text(
        "<html><body>{{NAV}}{{SECTIONS}}</body></html>", encoding="utf-8"
    )
    (base / "flow.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    config = base / "vistas.yml"
    config.write_text(
        """
template: template.html
vistas:
  - id: flow
    src: flow.mmd
""",
        encoding="utf-8",
    )

    out = base / "architecture.html"
    build_deskops(config, out)

    assert out.exists()
    assert "graph TD" in out.read_text(encoding="utf-8")

