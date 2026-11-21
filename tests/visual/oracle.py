"""The frozen oracle of spec2viz for the parity tests that build their own inputs.

specIR does not import or run spec2viz. What spec2viz answered to each of these tests (revision
`REVISION`) is versioned in `goldens/spec2viz-<REVISION>-oracle.json`, and a test asks for it with
`expect(kind, *args)` (the answer of the test's n-th question) or `frozen(name)` (an input or a list
that spec2viz owned: its CLI tree, its test fixtures, the source of the package it generated a spec for).

The golden is written by `runs/subagents/exec-deskops-e-5ccf277d5e67/record_goldens.py`, which runs these
same tests with spec2viz installed and installs `LIVE`, one function per kind that calls spec2viz;
outside of that script `LIVE` is empty and the answers come from the file."""

from __future__ import annotations

import hashlib
import json
import os
import re
from pathlib import Path
from typing import Any, Callable

HERE = Path(__file__).resolve().parent
REVISION = "2de1056"
GOLDENS = HERE / "goldens" / f"spec2viz-{REVISION}-oracle.json"
#: Set by the recording script only: kind -> function that asks spec2viz live.
LIVE: dict[str, Callable[..., Any]] = {}
#: What the recording script collected: key -> answer.
RECORDED: dict[str, Any] = {}
_counter: dict[str, int] = {}


def plain(value: Any) -> Any:
    """`value` as the JSON the golden holds (tuples are lists, paths are text)."""
    return json.loads(json.dumps(value, default=str))


def scrub(value: Any, *roots: Path) -> Any:
    """`plain(value)` with the temporary roots of the test replaced, so a path is not provenance."""
    text = json.dumps(value, default=str, ensure_ascii=False)
    for root in roots:
        for form in {str(root), str(root.resolve())}:
            text = text.replace(json.dumps(form)[1:-1], "<tmp>")
    return json.loads(text)


def tmp_root(path: Path) -> Path:
    """The `tmp_path` of the test that `path` lives in (the folder under pytest's `pytest-<n>`)."""
    for parent in (path, *path.parents):
        if parent.parent.name.startswith("pytest-"):
            return parent
    return path.parent


def _data() -> dict[str, Any]:
    return json.loads(GOLDENS.read_text(encoding="utf-8"))


def _test_key(kind: str) -> str:
    current = os.environ["PYTEST_CURRENT_TEST"].rsplit(" (", 1)[0].split("::", 1)[1]
    n = _counter[current] = _counter.get(current, 0) + 1
    return f"{current}#{n}:{kind}"


def expect(kind: str, *args: Any, roots: tuple[Path, ...] = (), **kwargs: Any) -> Any:
    """What spec2viz answered at this point of this test."""
    key = _test_key(kind)
    if LIVE:
        RECORDED[key] = scrub(LIVE[kind](*args, **kwargs), *roots)
        if kind in POST:
            RECORDED[key] = POST[kind](RECORDED[key])
    return _data()["answers"][key] if not LIVE else RECORDED[key]


def frozen(name: str, *args: Any) -> Any:
    """An input or a list of spec2viz that does not depend on the test."""
    if LIVE:
        RECORDED[f"frozen:{name}"] = plain(LIVE[name](*args))
        return RECORDED[f"frozen:{name}"]
    return _data()["answers"][f"frozen:{name}"]


def digest(text: str) -> str:
    """The SHA-256 of a page: the golden keeps it, not the page (they are over 100 KB each)."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def page_digest(page: str) -> str:
    """The digest of a catalog page with its view ids' path hash (`sample-1a2b3c4d`) left out: the hash
    is of the config's path, so it changes with each temporary folder."""
    page = re.sub(r"-[0-9a-f]{8}(?![0-9a-f])", "-<hash>", page)
    # the aliases of an atom come from a set, so their order follows PYTHONHASHSEED (in specIR and in spec2viz)
    page = re.sub(r'"aliases": (\[[^\]]*\])', lambda m: '"aliases": ' + json.dumps(sorted(json.loads(m.group(1))), ensure_ascii=False), page)
    # which of a state's two names (`nueva`, `4 nueva`) the atoms are listed under also follows the seed
    return digest(page.replace('"4 nueva"', '"nueva"'))


def unhash(value: Any) -> Any:
    """`value` with the path hash of view ids (`sample-1a2b3c4d`) left out, as `page_digest` does."""
    return json.loads(re.sub(r"-[0-9a-f]{8}(?![0-9a-f])", "-<hash>", json.dumps(value, ensure_ascii=False)))


#: What the golden keeps of an answer, by kind: the digest of a page (the first item), not the page.
POST: dict[str, Callable[[Any], Any]] = {"catalog_page": lambda answer: [page_digest(answer[0]), unhash(answer[1])]}
