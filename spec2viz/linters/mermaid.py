"""Mermaid output linter.

Catches syntax that parses server-side but breaks the mermaid.js parser in the
browser. Each rule maps a regex to a human explanation so the failure names the
exact line and the fix, instead of a blank diagram at view time.

Scope: sequenceDiagram, flowchart/graph, stateDiagram. The linter is
conservative: it only flags patterns known to hard-fail mermaid rendering.
"""

from __future__ import annotations

import os
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass
from pathlib import Path

from spec2viz.exceptions import RenderError


class MermaidLintError(RenderError):
    """Rendered mermaid text contains a browser-breaking construct."""


@dataclass(frozen=True)
class _Rule:
    name: str
    pattern: re.Pattern[str]
    message: str


# First non-empty line declares the diagram kind.
_HEADER_KINDS = (
    "sequenceDiagram",
    "flowchart",
    "graph",
    "stateDiagram",
    "stateDiagram-v2",
    "classDiagram",
    "erDiagram",
    "journey",
    "gantt",
    "pie",
)

# Valid mermaid sequence arrows. Anything else between two participants that
# looks like an arrow is almost always a renderer bug.
_VALID_SEQ_ARROWS = ("->>", "-->>", "->", "-->", "-x", "--x", "-)", "--)")

_RULES: tuple[_Rule, ...] = (
    _Rule(
        name="invalid-return-arrow",
        # "A<<--B" or "A <<-- B": the reversed dashed arrow is not mermaid.
        pattern=re.compile(r"\S\s*<<--\s*\S"),
        message=(
            "invalid sequence arrow '<<--'. Mermaid return arrows are '-->>'. "
            "Use kind: return -> '-->>' (dashed, forward)."
        ),
    ),
    _Rule(
        name="raw-angle-brackets",
        # Unescaped <...> inside a message/label is parsed as HTML by mermaid
        # and silently drops or breaks the node. Only fires outside of a
        # recognised arrow token.
        pattern=re.compile(r"(?<![-<>x)])<(?!<)[^<>\n]*>"),
        message=(
            "raw '<...>' in a label/message is parsed as HTML by mermaid and "
            "breaks the diagram. Escape as '&lt;...&gt;' or drop the brackets."
        ),
    ),
    _Rule(
        name="empty-label-braces",
        pattern=re.compile(r"\{\s*\"\"\s*\}|\{\s*\}"),
        message="empty decision node label '{}' is not renderable.",
    ),
)


def mmdc_path() -> str | None:
    """Return the mermaid-cli binary path if available, else None.

    Honors SPEC2VIZ_MMDC to point at a specific binary. Set SPEC2VIZ_MMDC=0
    (or 'off'/'false') to force-disable the real-parser check.
    """
    override = os.environ.get("SPEC2VIZ_MMDC")
    if override in {"0", "off", "false", "no"}:
        return None
    if override:
        return override if (Path(override).exists() or shutil.which(override)) else None
    return shutil.which("mmdc")


def _mmdc_check(text: str) -> list[str]:
    """Parse the mermaid text with the real mermaid-cli engine.

    Returns a list of problems (empty = clean). If mmdc is not installed the
    check is skipped and returns []. This is the source of truth: it catches
    browser-breaking syntax the regex heuristics miss (unescaped '()', '{}',
    nested quotes, HTML entities, etc.).
    """
    binary = mmdc_path()
    if not binary:
        return []
    with tempfile.TemporaryDirectory() as td:
        src = Path(td) / "diagram.mmd"
        out = Path(td) / "diagram.svg"
        src.write_text(text, encoding="utf-8")
        try:
            proc = subprocess.run(
                [binary, "-i", str(src), "-o", str(out)],
                capture_output=True,
                text=True,
                timeout=60,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:  # pragma: no cover
            return [f"mmdc could not run ({exc}); skipping real-parser check."]
        if proc.returncode == 0 and out.exists():
            return []
        detail = _extract_mmdc_error(proc.stdout, proc.stderr)
        return [f"mermaid engine (mmdc) rejected the diagram:\n    {detail}"]


def _extract_mmdc_error(stdout: str, stderr: str) -> str:
    blob = "\n".join(p for p in (stdout, stderr) if p).strip()
    lines = [ln for ln in blob.splitlines() if ln.strip()]
    picked = [ln.strip() for ln in lines if re.search(r"error|parse|expecting", ln, re.I)]
    chosen = picked or lines
    return "\n    ".join(chosen[:6]) or "unknown mmdc failure"


def _looks_like_sequence(text: str) -> bool:
    for line in text.splitlines():
        s = line.strip()
        if s:
            return s.startswith("sequenceDiagram")
    return False


def _check_sequence_arrows(text: str) -> list[str]:
    """Flag sequence message lines whose arrow token is not valid mermaid."""
    problems: list[str] = []
    msg_re = re.compile(r"^\s*(\w+)\s*([-<>x()]{2,4})\s*(\w+)\s*:")
    for i, line in enumerate(text.splitlines(), 1):
        m = msg_re.match(line)
        if not m:
            continue
        arrow = m.group(2)
        if arrow not in _VALID_SEQ_ARROWS:
            problems.append(
                f"line {i}: invalid sequence arrow '{arrow}'. "
                f"Valid arrows: {', '.join(_VALID_SEQ_ARROWS)}."
            )
    return problems


def lint_mermaid(text: str, *, check_html: bool = True) -> list[str]:
    """Return a list of human-readable problems. Empty list means clean.

    check_html controls the raw-angle-bracket rule. Pass check_html=False when
    the caller will HTML-escape the content before embedding (e.g. the deskops
    build wraps mermaid in <pre> and escapes '<' to '&lt;' itself), so raw
    '<...>' in labels is safe in that path. Leave it True for standalone .mmd
    output that a mermaid engine parses verbatim.

    Does not raise; callers decide whether to raise MermaidLintError.
    """
    problems: list[str] = []
    lines = text.splitlines()

    for rule in _RULES:
        if rule.name == "raw-angle-brackets" and not check_html:
            continue
        for i, line in enumerate(lines, 1):
            if rule.pattern.search(line):
                problems.append(f"line {i}: {rule.message}\n    -> {line.strip()}")

    if _looks_like_sequence(text):
        problems.extend(_check_sequence_arrows(text))

    problems.extend(_mmdc_check(text))

    return problems


def assert_mermaid_ok(
    text: str, *, source: str | None = None, check_html: bool = True
) -> None:
    """Raise MermaidLintError if the mermaid text has breaking constructs."""
    problems = lint_mermaid(text, check_html=check_html)
    if problems:
        where = f" in {source}" if source else ""
        joined = "\n  - ".join(problems)
        raise MermaidLintError(
            f"Mermaid lint failed{where} ({len(problems)} issue(s)):\n  - {joined}"
        )
