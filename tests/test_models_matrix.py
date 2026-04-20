import yaml
from pathlib import Path
from yaml_charts.models.matrix import MatrixDiagram

FIXTURE = Path("tests/fixtures/matrix.quotation-view.yml")

def test_matrix_loads():
    data = yaml.safe_load(FIXTURE.read_text())
    d = MatrixDiagram.model_validate(data)
    assert d.id == "matrix.quotation-view"
    assert d.type.value == "component_view_matrix"

def test_matrix_views():
    data = yaml.safe_load(FIXTURE.read_text())
    d = MatrixDiagram.model_validate(data)
    assert len(d.data.views) == 1
    view = d.data.views[0]
    assert view.id == "quotation"
    assert len(view.stages) == 5
    assert view.stages[0].id == "browse"

def test_matrix_components():
    data = yaml.safe_load(FIXTURE.read_text())
    d = MatrixDiagram.model_validate(data)
    root = d.data.components[0]
    assert root.name == "QuotationFlow"
    assert root.kind == "core"
    assert root.stages["quotation"] == ["browse", "client", "basket", "validation", "completed"]
    assert len(root.children) == 2

def test_matrix_nested_children():
    data = yaml.safe_load(FIXTURE.read_text())
    d = MatrixDiagram.model_validate(data)
    basket = d.data.components[0].children[1]
    assert basket.name == "Basket"
    assert len(basket.children) == 1
    assert basket.children[0].name == "BasketItem"
