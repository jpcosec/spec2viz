import pytest
from yaml_charts.exceptions import (
    YamlChartsError,
    ParseError,
    ValidationError,
    CompileError,
    RenderError,
)

def test_exception_hierarchy():
    assert issubclass(ParseError, YamlChartsError)
    assert issubclass(ValidationError, YamlChartsError)
    assert issubclass(CompileError, YamlChartsError)
    assert issubclass(RenderError, YamlChartsError)

def test_exceptions_are_catchable_as_base():
    with pytest.raises(YamlChartsError):
        raise ParseError("bad yaml")
