"""The retirement gate of spec2viz (IR13): who still depends on spec2viz, and which rows of the coverage
matrix are not accredited yet.

The universe audited is exactly the «Inventario de consumidores» of
`docs/spec2viz/matriz-de-cobertura.md` (its repos and its `store <path>` rows) plus specIR's own repo,
the one that holds the matrix. Each one is read from the local path given for it; nothing is written.

What counts as a dependency (and nothing else):

- `importación`: `import spec2viz…`/`from spec2viz… import` in Python code, and the dynamic forms
  `importorskip("spec2viz…")`/`import_module("spec2viz…")`;
- `dependencia declarada`: spec2viz as a requirement in `pyproject.toml`, `setup.cfg`, `setup.py`,
  `requirements*.txt` or a CI file (`.github/**/*.yml`, `.gitlab-ci.yml`);
- `invocación del comando`: a Python call whose command is `spec2viz` (`run("spec2viz", …)`,
  `subprocess.run(["spec2viz", …])`, `os.system("spec2viz …")`, `shutil.which("spec2viz")`), and
  `spec2viz <subcommand>` in a shell script, a Makefile or a CI file;
- `habilidad de agente`: a `SKILL.md` (or a file under a skill's `references/`) that tells an agent to run
  `spec2viz <subcommand>` (as inline code or in a fenced block), or a skill named after spec2viz
  (`name: use-spec2viz`);
- `modelo registrado`: `spec2viz.sldb_models` in a store's `store.yaml`, `core/store_index.yaml` or
  `core/models/*.yaml`.

Mentions in prose, documentation, comments, docstrings, changelogs and desk documents do not count.

The matrix is accredited when every `SV-*` row has an entry in its «Acreditación (IR13)» table whose
state is `cumplida` and that cites at least one test (`tests/….py`)."""

from __future__ import annotations

import ast
import re
from dataclasses import dataclass, field
from pathlib import Path

#: The audited repo that is always there: the one that holds the matrix.
SPECIR = "IR"
MATRIX = Path("docs") / "spec2viz" / "matriz-de-cobertura.md"
INVENTORY_HEADING = "## Inventario de consumidores"
ACCREDITATION_HEADING = "## Acreditación (IR13)"
DONE = "cumplida"

IMPORT = "importación"
DECLARED = "dependencia declarada"
INVOCATION = "invocación del comando"
SKILL = "habilidad de agente"
MODEL = "modelo registrado"

SKIP_DIRS = {".git", ".venv", "venv", "node_modules", "__pycache__", "build", "dist", ".sldb", ".tox",
             ".mypy_cache", ".pytest_cache", ".ruff_cache", "site-packages"}
SUBCOMMANDS = "about|build|catalog|diagram|lint|notation|palette|render|schema|validate"
#: `spec2viz <subcommand>` at a command position of a shell line.
SHELL_CALL = re.compile(rf"(?:^|[\s;&|(`\"'$])spec2viz\s+(?:{SUBCOMMANDS})\b")
#: spec2viz as a requirement: `spec2viz>=0.1`, `"spec2viz"`, `egg=spec2viz`, `pip install spec2viz`.
REQUIREMENT = re.compile(
    r"egg=spec2viz\b"
    r"|pip\s+install\b.*(?<![\w./-])spec2viz(?![\w-])"
    r"|[\"']spec2viz\s*(?:\[[^\]]*\])?\s*(?:[<>=!~]=?[^\"']*)?(?:@[^\"']*)?(?:;[^\"']*)?[\"']"
    r"|^\s*spec2viz\s*(?:\[[^\]]*\])?\s*(?:[<>=!~]=?|@|;|=|$)")
#: `spec2viz <subcommand>` as code in a skill: inline code, or any line of a fenced block.
SKILL_CALL = re.compile(rf"`spec2viz\s+(?:{SUBCOMMANDS})\b")
#: Calls whose first argument is a string but that run nothing (string, path and regex methods).
NOT_A_RUN = {"startswith", "endswith", "split", "rsplit", "replace", "find", "rfind", "index", "count", "partition",
             "rpartition", "strip", "lstrip", "rstrip", "join", "format", "get", "removeprefix", "removesuffix",
             "search", "match", "fullmatch", "compile", "sub", "findall", "glob", "rglob", "joinpath", "append"}
CI_NAMES = {".gitlab-ci.yml", ".travis.yml", "azure-pipelines.yml", "Jenkinsfile"}
CONFIG_NAMES = {"pyproject.toml", "setup.cfg", "setup.py", "tox.ini", "Pipfile"}


class InventoryError(ValueError):
    """The paths given do not match the inventory of the matrix."""


@dataclass(frozen=True, order=True)
class Dependency:
    owner: str
    path: str
    line: int
    kind: str
    text: str = field(compare=False)

    def __str__(self) -> str:
        return f"{self.owner}\t{self.path}:{self.line}\t{self.kind}\t{self.text}"


@dataclass
class Report:
    repos: list[str]
    stores: list[str]
    dependencies: list[Dependency]
    open_rows: list[str]

    @property
    def ok(self) -> bool:
        return not self.dependencies and not self.open_rows


# --- the matrix ----------------------------------------------------------------------------------


def _section(text: str, heading: str) -> list[str]:
    lines = text.splitlines()
    try:
        start = lines.index(heading)
    except ValueError:
        return []
    body = []
    for line in lines[start + 1:]:
        if line.startswith("## "):
            break
        body.append(line)
    return body


def _cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.strip().strip("|").split("|")]


def _table_rows(lines: list[str]) -> list[list[str]]:
    rows = [_cells(line) for line in lines if line.startswith("|")]
    return [row for row in rows[2:] if row and not set(row[0]) <= set("-: ")] if rows else []


def inventory(text: str) -> tuple[list[str], list[str]]:
    """The repos and the stores of the inventory, in order of first appearance."""
    repos: list[str] = []
    stores: list[str] = []
    for row in _table_rows(_section(text, INVENTORY_HEADING)):
        first = row[0]
        store = re.match(r"store\s+`([^`]+)`", first)
        name = store.group(1) if store else first.split()[0].strip("`")
        target = stores if store else repos
        if name and name not in target:
            target.append(name)
    if not repos and not stores:
        raise InventoryError(f"the matrix has no «{INVENTORY_HEADING[3:]}» table")
    return repos, stores


def matrix_rows(text: str) -> list[str]:
    return [_cells(line)[0] for line in text.splitlines() if line.startswith("| SV-")]


def accreditation(text: str) -> dict[str, tuple[str, str]]:
    """Each row id of the accreditation table with its state and the evidence it cites."""
    entries = {}
    for row in _table_rows(_section(text, ACCREDITATION_HEADING)):
        if len(row) >= 3:
            entries[row[0].strip("`")] = (row[1].lower(), row[2])
    return entries


def open_rows(text: str) -> list[str]:
    """The rows of the matrix that are not `cumplida` with a cited test, each with why."""
    entries = accreditation(text)
    problems = []
    for row in matrix_rows(text):
        state, evidence = entries.get(row, ("", ""))
        if not state:
            problems.append(f"{row}: sin entrada en la acreditación")
        elif state != DONE:
            problems.append(f"{row}: {state}")
        elif not re.search(r"tests/[\w./-]+\.py", evidence):
            problems.append(f"{row}: cumplida sin prueba citada")
    return problems


# --- dependencies --------------------------------------------------------------------------------


def _is_spec2viz_module(name: str | None) -> bool:
    return bool(name) and name.split(".")[0] == "spec2viz"


def _command_of(node: ast.expr) -> bool:
    """Whether an argument of a call names the spec2viz command."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value == "spec2viz" or node.value.startswith("spec2viz ")
    if isinstance(node, (ast.List, ast.Tuple)) and node.elts:
        head = node.elts[0]
        return isinstance(head, ast.Constant) and head.value == "spec2viz"
    return False


def _python(owner: str, rel: str, source: str) -> list[Dependency]:
    lines = source.splitlines()
    try:
        tree = ast.parse(source)
    except SyntaxError:
        return [Dependency(owner, rel, n, IMPORT, line.strip()) for n, line in enumerate(lines, 1)
                if re.match(r"\s*(import|from)\s+spec2viz\b", line)]
    found = []

    def add(node: ast.AST, kind: str) -> None:
        found.append(Dependency(owner, rel, node.lineno, kind, lines[node.lineno - 1].strip()))

    for node in ast.walk(tree):
        if isinstance(node, ast.Import) and any(_is_spec2viz_module(a.name) for a in node.names):
            add(node, IMPORT)
        elif isinstance(node, ast.ImportFrom) and not node.level and _is_spec2viz_module(node.module):
            add(node, IMPORT)
        elif isinstance(node, ast.Call) and node.args:
            func = node.func.attr if isinstance(node.func, ast.Attribute) else getattr(node.func, "id", "")
            first = node.args[0]
            if func in ("importorskip", "import_module", "__import__"):
                if isinstance(first, ast.Constant) and isinstance(first.value, str) and _is_spec2viz_module(first.value):
                    add(node, IMPORT)
            elif func not in NOT_A_RUN and _command_of(first):
                add(node, INVOCATION)
    return found


def _lines(owner: str, rel: str, source: str, pattern: re.Pattern, kind: str, comment: str = "#") -> list[Dependency]:
    return [Dependency(owner, rel, n, kind, line.strip()) for n, line in enumerate(source.splitlines(), 1)
            if not line.lstrip().startswith(comment) and pattern.search(line)]


def _skill(owner: str, rel: str, source: str) -> list[Dependency]:
    found, fenced = [], False
    for n, line in enumerate(source.splitlines(), 1):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        named = n < 10 and re.match(r"name:\s*\S*spec2viz", line)  # the skill itself is spec2viz's (use-spec2viz)
        if named or (SHELL_CALL if fenced else SKILL_CALL).search(line):
            found.append(Dependency(owner, rel, n, SKILL, line.strip()))
    return found


def _is_skill(rel: Path) -> bool:
    return rel.name == "SKILL.md" or ("skills" in rel.parts and "references" in rel.parts and rel.suffix == ".md")


def _is_ci(rel: Path) -> bool:
    return rel.name in CI_NAMES or (rel.parts[:1] == (".github",) and rel.suffix in (".yml", ".yaml"))


def scan_repo(owner: str, root: Path) -> list[Dependency]:
    """Every dependency on spec2viz in the repo at `root`, read-only."""
    found: list[Dependency] = []
    for path in sorted(_files(root)):
        rel = path.relative_to(root)
        name = rel.name
        kinds = []
        if name.endswith(".py"):
            kinds.append("python")
        if name in CONFIG_NAMES - {"setup.py"} or re.match(r"requirements.*\.(txt|in)$", name):
            kinds.append("config")
        if _is_ci(rel):
            kinds += ["config", "shell"]
        if name.endswith(".sh") or name in ("Makefile", "makefile", "justfile", "Justfile"):
            kinds.append("shell")
        if _is_skill(rel):
            kinds.append("skill")
        if not kinds:
            continue
        try:
            source = path.read_text(encoding="utf-8")
        except (UnicodeDecodeError, OSError):
            continue
        if "spec2viz" not in source:
            continue
        rel_s = rel.as_posix()
        if "python" in kinds:
            found += _python(owner, rel_s, source)
            if name == "setup.py":
                found += _lines(owner, rel_s, source, REQUIREMENT, DECLARED)
        if "config" in kinds:
            found += _lines(owner, rel_s, source, REQUIREMENT, DECLARED)
        if "shell" in kinds:
            found += _lines(owner, rel_s, source, SHELL_CALL, INVOCATION)
        if "skill" in kinds:
            found += _skill(owner, rel_s, source)
    return sorted(set(found))


def _files(root: Path):
    stack = [root]
    while stack:
        directory = stack.pop()
        try:
            entries = list(directory.iterdir())
        except OSError:
            continue
        for entry in entries:
            if entry.is_symlink():
                continue
            if entry.is_dir():
                if entry.name not in SKIP_DIRS:
                    stack.append(entry)
            elif entry.is_file():
                yield entry


def scan_store(owner: str, store: Path) -> list[Dependency]:
    """The models of `spec2viz.sldb_models` registered in the store at `store` (its `.sldb` folder)."""
    files = [store / "store.yaml", store / "core" / "store_index.yaml", *sorted((store / "core" / "models").glob("*.yaml"))]
    found = []
    for path in files:
        if path.is_file():
            source = path.read_text(encoding="utf-8")
            found += _lines(owner, path.relative_to(store).as_posix(), source, re.compile(r"spec2viz\.sldb_models\b"), MODEL)
    return found


# --- the gate ------------------------------------------------------------------------------------


def check(matrix: Path, paths: dict[str, Path]) -> Report:
    """Audit the inventory of `matrix` (its repos and stores at `paths`) plus specIR's repo.

    `paths` maps each name of the inventory to its local path; specIR's repo is the one that holds
    the matrix and needs no path. A name outside the inventory, or a name of it without a path, is an
    `InventoryError`."""
    text = matrix.read_text(encoding="utf-8")
    repos, stores = inventory(text)
    specir_root = matrix.resolve().parents[len(MATRIX.parts) - 1]
    if SPECIR not in repos:
        repos.append(SPECIR)
    expected = (set(repos) - {SPECIR}) | set(stores)
    unknown = sorted(set(paths) - expected - {SPECIR})
    if unknown:
        raise InventoryError(f"not in the inventory of {matrix.name}: {', '.join(unknown)}")
    missing = sorted(expected - set(paths))
    if missing:
        raise InventoryError(f"no path given for: {', '.join(missing)}")
    roots = {name: Path(paths.get(name, specir_root)) for name in [*repos, *stores]}
    absent = sorted(name for name, root in roots.items() if not root.is_dir())
    if absent:
        raise InventoryError(f"path not found for: {', '.join(f'{n}={roots[n]}' for n in absent)}")
    dependencies = [dep for name in repos for dep in scan_repo(name, roots[name])]
    dependencies += [dep for name in stores for dep in scan_store(name, roots[name])]
    return Report(repos, stores, dependencies, open_rows(text))


def format_report(report: Report) -> str:
    lines = [f"audited repos: {', '.join(report.repos)}", f"audited stores: {', '.join(report.stores) or '-'}"]
    lines += [f"dependencies: {len(report.dependencies)}"] + [f"  {dep}" for dep in report.dependencies]
    lines += [f"rows not accredited: {len(report.open_rows)}"] + [f"  {row}" for row in report.open_rows]
    lines.append("gate: " + ("passed, the retirement can be declared" if report.ok else "failed, the retirement is not declared"))
    return "\n".join(lines)


__all__ = ["Dependency", "InventoryError", "Report", "accreditation", "check", "format_report", "inventory",
           "matrix_rows", "open_rows", "scan_repo", "scan_store"]
