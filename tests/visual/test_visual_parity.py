"""Parity of specIR's compilers with spec2viz over the whole corpus (tests/visual/parity.py).

For every spec of spec2viz (its fixtures, invalid ones included, its examples and its architecture
specs): loading and validating it with sldb (D3) gives the same typed error (class and text) as
spec2viz, and a valid spec compiles in specIR to an IR structurally equivalent to spec2viz's
(`specir.visual.normalize`). The saved oracle (`parity.GOLDENS`) always runs; the live oracle
(spec2viz itself) runs when spec2viz is installed and is skipped otherwise."""

from __future__ import annotations

import pytest

from parity import CORPUS, goldens, spec2viz_outcome, specir_outcome
from specir.visual.normalize import differences

TYPES = {"ActivityIR", "ClassIR", "ComponentIR", "DeploymentIR", "EnforcementArtifact", "MatrixIR", "SequenceIR", "StateIR"}


def _explain(found: dict, expected: dict) -> str:
    if found["error"] != expected["error"]:
        return f"error {found['error']} != {expected['error']}"
    return "; ".join(differences(found["ir"], expected["ir"])[:10])


@pytest.mark.parametrize("rel", CORPUS)
def test_specir_matches_the_saved_oracle(rel: str) -> None:
    expected = goldens()[rel]
    found = specir_outcome(rel)
    assert found == expected, _explain(found, expected)


@pytest.mark.parity
@pytest.mark.parametrize("rel", CORPUS)
def test_specir_matches_spec2viz(rel: str) -> None:
    pytest.importorskip("spec2viz")
    expected = spec2viz_outcome(rel)
    found = specir_outcome(rel)
    assert found == expected, _explain(found, expected)


@pytest.mark.parity
def test_the_saved_oracle_is_spec2viz_last_run() -> None:
    pytest.importorskip("spec2viz")
    saved = goldens()
    assert sorted(saved) == CORPUS
    stale = [rel for rel in CORPUS if spec2viz_outcome(rel) != saved[rel]]
    assert not stale, f"rewrite the goldens with `python tests/visual/parity.py`: {stale}"


def test_the_corpus_covers_the_eight_diagram_types_and_typed_errors() -> None:
    saved = goldens()
    compiled = {outcome["ir"]["__type__"] for outcome in saved.values() if outcome["ir"]}
    assert compiled == TYPES
    errors = {outcome["error"][0] for outcome in saved.values() if outcome["error"]}
    assert {"ParseError", "ValidationError"} <= errors, errors
    assert len(CORPUS) == 44
