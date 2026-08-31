"""Output linters for spec2viz renderers.

Linters run on rendered text (not on the IR) to catch syntax that the
browser-side diagram engine would reject. This closes the gap where a spec
validates fine but the produced .mmd/.html fails to parse at view time.
"""

from __future__ import annotations

from spec2viz.linters.mermaid import MermaidLintError, lint_mermaid

__all__ = ["MermaidLintError", "lint_mermaid"]
