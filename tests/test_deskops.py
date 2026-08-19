import json
import re
from pathlib import Path

from spec2viz.deskops import build_deskops, parse_atoms, render_deskops


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
    assert '<div class="mermaid">' in html
    assert '<div class="board puml-board">' in html
    assert "plain html snippet" in html
    assert "Gaps de implementación" in html
    assert "window.ATOMS_DB" in html
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
    assert html.count("</body>") == 1


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
