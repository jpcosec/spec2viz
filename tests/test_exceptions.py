import pytest
from spec2viz.exceptions import (
    Spec2VizError,
    ParseError,
    ValidationError,
    CompileError,
    RenderError,
)

def test_exception_hierarchy():
    assert issubclass(ParseError, Spec2VizError)
    assert issubclass(ValidationError, Spec2VizError)
    assert issubclass(CompileError, Spec2VizError)
    assert issubclass(RenderError, Spec2VizError)

def test_exceptions_are_catchable_as_base():
    with pytest.raises(Spec2VizError):
        raise ParseError("bad yaml")
