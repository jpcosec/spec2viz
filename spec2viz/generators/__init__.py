"""Spec generators — produce spec2viz YAML from external sources."""
from __future__ import annotations

from spec2viz.generators.python_ast import generate_python_ast_spec, write_spec

__all__ = ["generate_python_ast_spec", "write_spec"]
