"""Tests for the real-engine (mmdc) mermaid lint pass.

These verify that lint_mermaid uses the mermaid-cli parser as source of truth
when available, catching browser-breaking syntax the regex heuristics miss,
while degrading gracefully to a pure-regex pass when mmdc is absent.
"""
from __future__ import annotations

import pytest

from spec2viz.linters.mermaid import lint_mermaid, mmdc_path

_MMDC = mmdc_path() is not None
requires_mmdc = pytest.mark.skipif(not _MMDC, reason="mmdc (mermaid-cli) not installed")


# Patterns that the regex heuristics pass but the real mermaid parser rejects.
BROKEN = {
    "paren-edge-label": "graph TD\n    a -->|ask (paso 2)| b\n",
    "brace-edge-label": "graph TD\n    a -->|fetch {id}| b\n",
    "nested-quotes": 'flowchart TD\n    e["mostrar "msg" fin"]\n',
    "html-entity-seq": "sequenceDiagram\n    A->>B: show &lt;name&gt;\n",
}

CLEAN = {
    "simple-graph": "graph TD\n    a --> b\n",
    "quoted-paren-edge": 'graph TD\n    a -->|"ask (paso 2)"| b\n',
    "sequence-ok": "sequenceDiagram\n    A->>B: hello\n",
}


@requires_mmdc
@pytest.mark.parametrize("case", BROKEN)
def test_mmdc_catches_broken(case):
    problems = lint_mermaid(BROKEN[case])
    assert problems, f"{case}: expected mmdc to reject but lint was clean"
    assert any("mmdc" in p for p in problems)


@requires_mmdc
@pytest.mark.parametrize("case", CLEAN)
def test_mmdc_passes_clean(case):
    assert lint_mermaid(CLEAN[case]) == []


def test_mmdc_disabled_skips_engine(monkeypatch):
    # With the engine forced off, a paren edge label passes the regex-only pass.
    monkeypatch.setenv("SPEC2VIZ_MMDC", "0")
    assert lint_mermaid(BROKEN["paren-edge-label"]) == []


def test_regex_rules_still_fire_without_engine(monkeypatch):
    # The pre-existing heuristics must keep working when the engine is off.
    monkeypatch.setenv("SPEC2VIZ_MMDC", "0")
    problems = lint_mermaid("sequenceDiagram\n    A<<--B: bad\n")
    assert any("<<--" in p for p in problems)
