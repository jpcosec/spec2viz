from spec2viz.models.base import DiagramType, Metadata, Style, BaseDiagram


def test_diagram_type_values():
    assert DiagramType.sequence == "sequence"
    assert DiagramType.component_view_matrix == "component_view_matrix"


def test_metadata_optional_fields():
    m = Metadata()
    assert m.author is None
    assert m.description is None


def test_style_defaults():
    s = Style()
    assert s.theme == "default"
    assert s.kinds == {}
