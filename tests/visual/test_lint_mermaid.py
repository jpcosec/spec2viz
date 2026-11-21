"""The mermaid linter of specIR (SV-D01), migrated from `spec2viz.linters.mermaid`.

- `tests/test_mermaid_mmdc.py` of spec2viz (revision 2de1056) ported case by case: the real-engine
  (mmdc) cases skip when mermaid-cli is not installed, as in spec2viz; the regex cases force the
  engine off (`SPECIR_MMDC=0`, and spec2viz's `SPEC2VIZ_MMDC=0` still works).
- The same findings as spec2viz on the lint fixtures (`render_parity.lint_cases`: spec2viz's lint
  texts and the mermaid of every spec of the corpus), with and without the raw-angle-bracket rule:
  against the saved goldens.
- `diagram lint` reports a clean spec, a clean `.mmd` and a broken `.mmd` as spec2viz's did."""

from __future__ import annotations

import sys
from pathlib import Path

import pytest
from click.testing import CliRunner

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))

import render_parity  # noqa: E402

from specir.cli import main  # noqa: E402
from specir.visual.exceptions import RenderError  # noqa: E402
from specir.visual.lint_mermaid import MermaidLintError, assert_mermaid_ok, lint_mermaid, mmdc_path  # noqa: E402

_MMDC = mmdc_path() is not None
requires_mmdc = pytest.mark.skipif(not _MMDC, reason="mmdc (mermaid-cli) not installed")

BROKEN = {name: render_parity.LINT_TEXTS[name] for name in ("paren-edge-label", "brace-edge-label", "nested-quotes", "html-entity-seq")}
CLEAN = {name: render_parity.LINT_TEXTS[name] for name in ("simple-graph", "quoted-paren-edge", "sequence-ok")}


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


# ── same findings as spec2viz ───────────────────────────────────────────────────────────────────


def test_lint_goldens_cover_the_fixtures_and_flag_the_bad_ones():
    goldens = render_parity.lint_goldens()
    assert sorted(goldens) == sorted(render_parity.lint_cases())
    flagged = {name for name, found in goldens.items() if found["check_html"]}
    assert {"invalid-return-arrow", "raw-angle-brackets", "bad-return-arrow", "empty-decision"} <= flagged
    assert any(name.startswith("mermaid:") for name in goldens)


def test_specir_finds_what_the_goldens_say(monkeypatch):
    monkeypatch.setenv("SPECIR_MMDC", "0")
    assert render_parity.lint_findings(lint_mermaid) == render_parity.lint_goldens()


def test_assert_mermaid_ok_raises_a_render_error(monkeypatch):
    monkeypatch.setenv("SPECIR_MMDC", "0")
    assert_mermaid_ok(CLEAN["sequence-ok"])
    with pytest.raises(MermaidLintError, match=r"Mermaid lint failed in x\.mmd \(2 issue\(s\)\)") as caught:
        assert_mermaid_ok(render_parity.LINT_TEXTS["invalid-return-arrow"], source="x.mmd")
    assert isinstance(caught.value, RenderError)


# ── diagram lint ────────────────────────────────────────────────────────────────────────────────


def test_diagram_lint_command(tmp_path, monkeypatch):
    monkeypatch.setenv("SPECIR_MMDC", "0")
    runner = CliRunner()
    spec = render_parity.parity.FIXTURES / "tests" / "fixtures" / "sequence.create-quotation.yml"
    ok = runner.invoke(main, ["diagram", "lint", str(spec)])
    assert ok.exit_code == 0 and "sequence.create-quotation.yml: OK" in ok.output
    good = tmp_path / "good.mmd"
    good.write_text(CLEAN["simple-graph"], encoding="utf-8")
    bad = tmp_path / "bad.mmd"
    bad.write_text(render_parity.LINT_TEXTS["invalid-return-arrow"], encoding="utf-8")
    result = runner.invoke(main, ["diagram", "lint", str(good), str(bad)])
    assert result.exit_code == 1
    assert "good.mmd: OK" in result.output and "bad.mmd: 2 issue(s)" in result.output and "<<--" in result.output
