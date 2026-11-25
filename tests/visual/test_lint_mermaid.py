"""The mermaid linter of specIR (SV-D01), migrated from `spec2viz.linters.mermaid`.

- `tests/test_mermaid_mmdc.py` of spec2viz (revision 2de1056) ported case by case: the real-engine
  (mmdc) cases skip when mermaid-cli is not installed, as in spec2viz; the regex cases force the
  engine off (`SPECIR_MMDC=0`, and spec2viz's `SPEC2VIZ_MMDC=0` still works).
- The regex rules flag the broken lint fixtures and leave the clean ones alone.
- `diagram lint` reports a clean spec, a clean `.mmd` and a broken `.mmd` as spec2viz's did."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from click.testing import CliRunner

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

from specir.cli import main  # noqa: E402
from specir.visual.exceptions import RenderError  # noqa: E402
from specir.visual.lint_mermaid import MermaidLintError, assert_mermaid_ok, lint_mermaid, mmdc_path  # noqa: E402

_MMDC = mmdc_path() is not None
requires_mmdc = pytest.mark.skipif(not _MMDC, reason="mmdc (mermaid-cli) not installed")

LINT_TEXTS = {
    "paren-edge-label": "graph TD\n    a -->|ask (paso 2)| b\n",
    "brace-edge-label": "graph TD\n    a -->|fetch {id}| b\n",
    "nested-quotes": 'flowchart TD\n    e["mostrar "msg" fin"]\n',
    "html-entity-seq": "sequenceDiagram\n    A->>B: show &lt;name&gt;\n",
    "simple-graph": "graph TD\n    a --> b\n",
    "quoted-paren-edge": 'graph TD\n    a -->|"ask (paso 2)"| b\n',
    "sequence-ok": "sequenceDiagram\n    A->>B: hello\n",
    "invalid-return-arrow": "sequenceDiagram\n    A<<--B: reply",
    "raw-angle-brackets": "sequenceDiagram\n    A->>B: GET path?x=<id>",
    "bad-return-arrow": "sequenceDiagram\n    A<<--B: bad\n",
    "empty-decision": "flowchart TD\n    d{}\n",
}

BROKEN = {name: LINT_TEXTS[name] for name in ("paren-edge-label", "brace-edge-label", "nested-quotes", "html-entity-seq")}
CLEAN = {name: LINT_TEXTS[name] for name in ("simple-graph", "quoted-paren-edge", "sequence-ok")}


# ── tests/test_mermaid_mmdc.py ──────────────────────────────────────────────────────────────────


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


@pytest.mark.parametrize("variable", ["SPECIR_MMDC", "SPEC2VIZ_MMDC"])
def test_mmdc_disabled_skips_engine(monkeypatch, variable):
    # With the engine forced off, a paren edge label passes the regex-only pass.
    monkeypatch.delenv("SPECIR_MMDC", raising=False)
    monkeypatch.setenv(variable, "0")
    assert mmdc_path() is None
    assert lint_mermaid(BROKEN["paren-edge-label"]) == []


def test_regex_rules_still_fire_without_engine(monkeypatch):
    # The pre-existing heuristics must keep working when the engine is off.
    monkeypatch.setenv("SPECIR_MMDC", "0")
    problems = lint_mermaid("sequenceDiagram\n    A<<--B: bad\n")
    assert any("<<--" in p for p in problems)


# ── the findings of the regex rules ───────────────────────────────────────────────────────────────────


def test_the_regex_rules_flag_the_bad_fixtures_and_only_those(monkeypatch):
    monkeypatch.setenv("SPECIR_MMDC", "0")
    flagged = {name for name, text in LINT_TEXTS.items() if lint_mermaid(text, check_html=True)}
    assert {"invalid-return-arrow", "raw-angle-brackets", "bad-return-arrow", "empty-decision"} <= flagged
    assert not flagged & {"simple-graph", "quoted-paren-edge", "sequence-ok"}


def test_assert_mermaid_ok_raises_a_render_error(monkeypatch):
    monkeypatch.setenv("SPECIR_MMDC", "0")
    assert_mermaid_ok(CLEAN["sequence-ok"])
    with pytest.raises(MermaidLintError, match=r"Mermaid lint failed in x\.mmd \(2 issue\(s\)\)") as caught:
        assert_mermaid_ok(LINT_TEXTS["invalid-return-arrow"], source="x.mmd")
    assert isinstance(caught.value, RenderError)


# ── diagram lint ────────────────────────────────────────────────────────────────────────────────


def test_diagram_lint_command(tmp_path, monkeypatch):
    monkeypatch.setenv("SPECIR_MMDC", "0")
    runner = CliRunner()
    spec = HERE / "fixtures" / "spec2viz" / "tests" / "fixtures" / "sequence.create-quotation.yml"
    ok = runner.invoke(main, ["diagram", "lint", str(spec)])
    assert ok.exit_code == 0 and "sequence.create-quotation.yml: OK" in ok.output
    good = tmp_path / "good.mmd"
    good.write_text(CLEAN["simple-graph"], encoding="utf-8")
    bad = tmp_path / "bad.mmd"
    bad.write_text(LINT_TEXTS["invalid-return-arrow"], encoding="utf-8")
    result = runner.invoke(main, ["diagram", "lint", str(good), str(bad)])
    assert result.exit_code == 1
    assert "good.mmd: OK" in result.output and "bad.mmd: 2 issue(s)" in result.output and "<<--" in result.output
