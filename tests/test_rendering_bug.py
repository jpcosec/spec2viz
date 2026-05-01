from pathlib import Path
from spec2viz import render_to_file

def test_direct_render_to_file(tmp_path):
    # Setup
    fixture_dir = tmp_path / "fixtures"
    fixture_dir.mkdir()
    fixture_path = fixture_dir / "canonical.yml"
    fixture_path.write_text("""
id: canonical-arch
title: Canonical Architecture
type: component
version: "1.0"
data:
  nodes:
    core: {label: Core, kind: internal}
    api: {label: API, kind: boundary}
  edges:
    - {from: api, to: core, relation: uses}
""")

    out_dir = tmp_path / "out"
    
    # The call that is failing in the CLI
    output_path = render_to_file(fixture_path, out=out_dir, renderer="mermaid")
    
    assert output_path.exists()
    assert "graph TD" in output_path.read_text()
    assert "core" in output_path.read_text()
    assert "api" in output_path.read_text()
