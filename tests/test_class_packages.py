"""Paquetes UML en diagramas de clase: anidados, con estilo por kind, validados con errores tipados."""
import shutil
import subprocess
from pathlib import Path

import pytest

from spec2viz.compilers import compile_ir
from spec2viz.exceptions import StructureError, UnknownReferenceError
from spec2viz.loader import load
from spec2viz.renderers.class_diagram import render_mermaid_class, render_plantuml_class
from spec2viz.validator import validate

SPEC = Path(__file__).parent / "fixtures" / "class.packages.yml"


def _ir():
    diagram = load(SPEC)
    validate(diagram)
    return compile_ir(diagram)


def test_ir_knows_paths_and_owners():
    ir = _ir()
    assert ir.package_path("billing") == ["core", "billing"] and ir.package_of("Invoice") == "billing"
    assert ir.package_of("AuditLog") == "shared"


def test_mermaid_namespaces_by_path_and_colors_classes_by_package_kind():
    out = render_mermaid_class(_ir())
    lines = [l.strip() for l in out.splitlines()]
    assert "namespace Core.Billing {" in lines and "namespace Core.Identity {" in lines and "namespace Shared {" in lines
    assert "namespace Core {" not in lines  # sin clases propias, el paquete raiz no abre namespace vacio
    assert "classDef pkg0 fill:#fff1c2,stroke:#7a5c00" in lines and 'cssClass "Invoice,Payment" pkg0' in lines
    assert "classDef pkg1 fill:#dbebf4,stroke:#0072b2" in lines and 'cssClass "User" pkg1' in lines
    assert not any("AuditLog" in l for l in lines if l.startswith("cssClass"))


def test_plantuml_nests_packages_with_their_fill():
    out = render_plantuml_class(_ir())
    assert 'package "Core" as core {\n    package "Billing" as billing #fff1c2 {\n        class "Invoice" as Invoice {' in out
    assert 'package "Shared" as shared {' in out


def test_without_packages_the_output_is_unchanged():
    diagram = load(SPEC)
    diagram.data.packages = {}
    diagram.style = None
    out = render_mermaid_class(compile_ir(diagram))
    assert "namespace" not in out and "classDef" not in out


@pytest.mark.parametrize("mutate, error, message", [
    (lambda d: d.data.packages["shared"].contains.append("Ghost"), UnknownReferenceError, "unknown class or package 'Ghost'"),
    (lambda d: d.data.packages["shared"].contains.append("shared"), StructureError, "contains itself"),
    (lambda d: d.data.packages["shared"].contains.append("Invoice"), StructureError, "Class 'Invoice' is contained by both"),
    (lambda d: d.data.packages["shared"].contains.append("billing"), StructureError, "Package 'billing' is contained by both"),
    (lambda d: d.data.packages["billing"].contains.append("core"), StructureError, "cycle"),
    (lambda d: d.data.packages["shared"].contains.remove("AuditLog"), StructureError, "Orphan class"),
])
def test_typed_validation(mutate, error, message):
    diagram = load(SPEC)
    mutate(diagram)
    with pytest.raises(error, match=message):
        validate(diagram)


def test_package_id_cannot_be_a_class_id():
    from spec2viz.models.class_diagram import ClassPackage

    diagram = load(SPEC)
    diagram.data.packages["User"] = ClassPackage(contains=[])
    with pytest.raises(StructureError, match="both a class and a package"):
        validate(diagram)


@pytest.mark.skipif(shutil.which("mmdc") is None, reason="mmdc not installed")
def test_real_mermaid_engine_accepts_the_packages(tmp_path):
    source = tmp_path / "p.mmd"
    source.write_text(render_mermaid_class(_ir()), encoding="utf-8")
    result = subprocess.run(["mmdc", "-i", str(source), "-o", str(tmp_path / "p.svg"), "-q"], capture_output=True, text=True, timeout=120)
    assert result.returncode == 0, result.stderr[-400:]


sldb_api = pytest.importorskip("sldb.api")


def test_sync_nests_packages_and_styles_them_by_kind(tmp_path):
    from spec2viz.notation_view import resolve_view
    from spec2viz.sldb_sync import SpecSync

    sldb_api.init_store(tmp_path)
    (tmp_path / "docs").mkdir()
    spec = shutil.copy(SPEC, tmp_path / "docs" / "packages.yml")
    report = SpecSync(tmp_path / ".sldb").sync(Path(spec))
    assert report.problems == []
    view = resolve_view(tmp_path / ".sldb", "class.packages")
    assert view["skipped"] == []
    nodes = {n["element"]: n for n in view["nodes"]}
    assert nodes["billing"]["glyph"] == "GlyphDoc:uml-class.package" and nodes["billing"]["shape"] == "package"
    assert nodes["Invoice"]["glyph"] == "GlyphDoc:uml-class.class"
    assert nodes["billing"]["style"]["fill"] == {"light": "#fff1c2", "dark": "#3d3200"} and nodes["billing"]["style"]["source"]["fill"] == "spec"
    assert nodes["identity"]["style"]["stroke"]["light"] == "#0072b2" and nodes["core"]["style"] == {}
    nest = {(l["source"].rsplit(".", 1)[-1], l["target"].rsplit(".", 1)[-1]) for l in view["links"] if l["relation"] == "contains"}
    assert nest == {("core", "billing"), ("core", "identity"), ("billing", "Invoice"), ("billing", "Payment"), ("identity", "User"), ("shared", "AuditLog")}
    assert all(l["draw"] == "nest" for l in view["links"] if l["relation"] == "contains")
