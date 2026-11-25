"""The `specir` command (IR13d): spec2viz's `tests/test_cli.py` ported, the correspondence table and the
agent skill.

- Ported from spec2viz (revision 2de1056), over the same fixtures (`fixtures/spec2viz/`) and on the same
  top-level aliases spec2viz's tests call: `test_validate_*`, `test_render_*`, `test_schema_*`,
  `test_help_mentions_taxonomy_groups_and_renderers`, `test_catalog_schema_stdout`,
  `test_catalog_build_alias_matches_legacy_build` and every `test_build_command*`. The help says
  "Top-level aliases ... remain available" where spec2viz said "Legacy top-level commands remain
  available". The render cases on `diagram render`, the provenance header and the API ones are IR12's
  (`test_render_commands.py`).
- `docs/spec2viz/correspondencia-cli.md` covers exactly the command tree of spec2viz's CLI, and every
  equivalent it names answers `--help` with the options it names (sldb's commands run as a separate
  process; sldb's API functions are called on a builtin).
- `skills/use-specir/SKILL.md` names only commands that exist (each is invoked with `--help`) and no
  spec2viz command."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path

import pytest
from click.testing import CliRunner

from specir.cli import ALIASES, main
from specir.visual.catalog import AnnotationsTarget, render_catalog

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[1]
CORPUS = HERE / "fixtures" / "spec2viz"
FIXTURES = CORPUS / "tests" / "fixtures"
EXAMPLES = CORPUS / "examples"
CORRESPONDENCE = REPO / "docs" / "spec2viz" / "correspondencia-cli.md"
SKILL = REPO / "skills" / "use-specir" / "SKILL.md"
SLDB = str(Path(sys.executable).with_name("sldb"))
runner = CliRunner()

sys.path.insert(0, str(REPO / "tests"))


# ── validate ──────────────────────────────────────────────────────────────────


def test_specir_defines_no_validate_command():
    """SV-K16, SV-K21, SV-K26 and SV-K29 are `sldb notations validate` (specIR retired its own)."""
    assert "validate" not in main.commands and "validate" not in ALIASES
    assert "validate" not in main.commands["diagram"].commands
    for args in (["validate", "x.yml"], ["diagram", "validate", "x.yml"]):
        r = runner.invoke(main, args)
        assert r.exit_code == 2 and "No such command" in r.output
    r = runner.invoke(main, ["--help"])
    assert not re.search(r"^\s+validate\b", r.output, flags=re.M)
    p = subprocess.run([SLDB, "notations", "validate", str(FIXTURES / "state.quotation.yml")], capture_output=True, text=True)
    assert p.returncode == 0, p.stderr
    p = subprocess.run([SLDB, "notations", "validate", str(FIXTURES / "invalid" / "unknown_node.yml")], capture_output=True, text=True)
    assert p.returncode == 1, p.stdout


# ── render (top-level alias) ──────────────────────────────────────────────────


def _render(*args: str):
    return runner.invoke(main, ["render", *args])


@pytest.mark.parametrize(
    ("name", "output"),
    [
        ("sequence.create-quotation.yml", "sequence.create-quotation.puml"),
        ("matrix.quotation-view.yml", "matrix.quotation-view.vega.json"),
        ("state.quotation.yml", "state.quotation.puml"),
        ("activity.validation.yml", "activity.validation.puml"),
        ("deployment.runtime.yml", "deployment.runtime.puml"),
        ("component.quotation.yml", "component.quotation.graph.html"),
    ],
)
def test_render_each_type(tmp_path, name, output):
    """spec2viz's test_render_sequence, _matrix, _state, _activity, _deployment and _component."""
    r = _render(str(FIXTURES / name), "--out", str(tmp_path))
    assert r.exit_code == 0, r.output
    assert (tmp_path / output).exists()


def test_render_override(tmp_path):
    r = _render(str(FIXTURES / "sequence.create-quotation.yml"), "--out", str(tmp_path), "--renderer", "mermaid")
    assert r.exit_code == 0
    assert (tmp_path / "sequence.create-quotation.mmd").exists()


def test_render_backend_alias(tmp_path):
    r = _render(str(FIXTURES / "state.quotation.yml"), "--out", str(tmp_path), "--backend", "mermaid")
    assert r.exit_code == 0
    assert (tmp_path / "state.quotation.mmd").exists()


def test_render_multiple(tmp_path):
    r = _render(str(FIXTURES / "sequence.create-quotation.yml"), str(FIXTURES / "state.quotation.yml"), "--out", str(tmp_path))
    assert r.exit_code == 0
    assert (tmp_path / "sequence.create-quotation.puml").exists()
    assert (tmp_path / "state.quotation.puml").exists()


def test_render_invalid_fails(tmp_path):
    r = _render(str(FIXTURES / "invalid" / "unknown_node.yml"), "--out", str(tmp_path))
    assert r.exit_code != 0


def test_render_d2(tmp_path):
    r = _render(str(FIXTURES / "component.quotation.yml"), "--out", str(tmp_path), "--renderer", "d2")
    assert r.exit_code == 0
    assert (tmp_path / "component.quotation.d2").exists()


def test_render_antonia_html(tmp_path):
    r = _render(str(FIXTURES / "sequence.create-quotation.yml"), "--out", str(tmp_path), "--renderer", "antonia-html")
    assert r.exit_code == 0
    assert (tmp_path / "sequence.create-quotation.html").exists()


def test_render_json_reflection_artifact(tmp_path):
    r = _render(str(EXAMPLES / "reflection" / "canonical.yml"), "--out", str(tmp_path), "--renderer", "json")
    assert r.exit_code == 0
    assert (tmp_path / "canonical.artifact.json").exists()


def test_the_render_alias_writes_what_diagram_render_writes(tmp_path):
    for renderer in ("plantuml", "mermaid", "d2", "graph"):
        a, b = tmp_path / f"alias-{renderer}", tmp_path / f"group-{renderer}"
        spec = str(FIXTURES / "component.quotation.yml")
        assert runner.invoke(main, ["render", spec, "--out", str(a), "--renderer", renderer]).exit_code == 0
        assert runner.invoke(main, ["diagram", "render", spec, "--out", str(b), "--renderer", renderer]).exit_code == 0
        [fa], [fb] = sorted(a.iterdir()), sorted(b.iterdir())
        assert fa.name == fb.name and fa.read_bytes() == fb.read_bytes()


# ── lint (top-level alias) ────────────────────────────────────────────────────


def test_lint_alias_matches_diagram_lint(tmp_path):
    good = tmp_path / "good.mmd"
    good.write_text("graph TD\nA-->B\n", encoding="utf-8")
    bad = tmp_path / "bad.mmd"
    bad.write_text("graph TD\nA[<b>x</b>]-->B\n", encoding="utf-8")
    spec = str(FIXTURES / "state.quotation.yml")
    for args in ([str(good)], [str(bad)], [spec], [str(good), str(bad)]):
        alias, group = runner.invoke(main, ["lint", *args]), runner.invoke(main, ["diagram", "lint", *args])
        assert (alias.exit_code, alias.output) == (group.exit_code, group.output), args
    assert runner.invoke(main, ["lint", str(good)]).exit_code == 0
    assert runner.invoke(main, ["lint", spec]).exit_code == 0


# ── schema ────────────────────────────────────────────────────────────────────


def test_schema_stdout():
    r = runner.invoke(main, ["schema", "--type", "sequence"])
    assert r.exit_code == 0
    assert '"title": "SequenceDiagram"' in r.output


def test_schema_outfile(tmp_path):
    out = tmp_path / "schema.json"
    r = runner.invoke(main, ["schema", "--type", "state", "--out", str(out)])
    assert r.exit_code == 0
    assert out.exists()


def test_schema_diagram_store_stdout():
    r = runner.invoke(main, ["schema", "--type", "diagram-store"])
    assert r.exit_code == 0
    assert '"title": "DiagramStoreEnvelope"' in r.output
    assert '"diagram_store"' in r.output


def test_schema_invalid_type_fails():
    r = runner.invoke(main, ["schema", "--type", "unknown"])
    assert r.exit_code != 0


def test_catalog_schema_stdout():
    r = runner.invoke(main, ["catalog", "schema"])
    assert r.exit_code == 0
    assert '"title": "DiagramStoreEnvelope"' in r.output


# ── help and about ────────────────────────────────────────────────────────────


def test_help_mentions_taxonomy_groups_and_renderers():
    r = runner.invoke(main, ["--help"])
    assert r.exit_code == 0
    assert "diagram" in r.output
    assert "catalog" in r.output
    assert "Top-level aliases (render, lint, schema, build) remain available" in r.output

    r = runner.invoke(main, ["render", "--help"])
    assert r.exit_code == 0
    for name in ["plantuml", "mermaid", "vega", "d2", "antonia-html", "json"]:
        assert name in r.output

    r = runner.invoke(main, ["diagram", "--help"])
    assert r.exit_code == 0
    assert "render" in r.output
    assert "validate" not in r.output
    assert "schema" in r.output

    r = runner.invoke(main, ["catalog", "--help"])
    assert r.exit_code == 0
    assert "build" in r.output
    assert "schema" in r.output


def test_every_alias_stands_for_a_group_command_with_the_same_parameters():
    for alias, target in ALIASES.items():
        group, name = target.split()
        a, g = main.commands[alias], main.commands[group].commands[name]
        assert [p.opts for p in a.params] == [p.opts for p in g.params], alias


def test_about_names_the_commands_of_specir_and_sldb(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    r = runner.invoke(main, ["about"])
    assert r.exit_code == 0, r.output
    assert f"no .sldb store above {tmp_path}" in r.output
    named = {}
    for line in r.output.splitlines():
        line = re.sub(r"^\d\. ", "", line.strip())
        if line.startswith(("specir ", "sldb ")):
            words, options = _command_and_options(line)
            named.setdefault(" ".join(words), set()).update(options)
    assert {"sldb notations validate", "specir diagram render", "specir diagram lint", "specir catalog build",
            "sldb notations sync", "sldb notations from-graph", "sldb notations view", "sldb serve", "sldb models add"} <= set(named)
    assert "spec2viz diagram" not in r.output and "spec2viz catalog" not in r.output
    for command, options in named.items():
        _assert_answers_help(command.split(), sorted(options))


def test_about_shows_the_store_above_the_current_directory(tmp_path, monkeypatch):
    subprocess.run(["timeout", "120", SLDB, "stores", "init", "--path", str(tmp_path)], check=True, capture_output=True)
    (tmp_path / "docs").mkdir()
    monkeypatch.chdir(tmp_path / "docs")
    r = runner.invoke(main, ["about"])
    assert r.exit_code == 0 and f"store            : {tmp_path / '.sldb'}" in r.output


# ── catalog build and its alias ───────────────────────────────────────────────


def test_catalog_build_alias_matches_legacy_build(tmp_path):
    (tmp_path / "template.html").write_text("<html><body>{{NAV}}{{FILTERS}}{{SECTIONS}}</body></html>", encoding="utf-8")
    (tmp_path / "view.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    config = tmp_path / "vistas.yml"
    config.write_text("\ntemplate: template.html\nvistas:\n  - id: sample\n    src: view.mmd\n", encoding="utf-8")

    legacy = tmp_path / "legacy.html"
    grouped = tmp_path / "grouped.html"
    r1 = runner.invoke(main, ["build", "--config", str(config), "--out", str(legacy)])
    r2 = runner.invoke(main, ["catalog", "build", "--config", str(config), "--out", str(grouped)])
    assert r1.exit_code == 0, r1.output
    assert r2.exit_code == 0, r2.output
    assert legacy.read_text(encoding="utf-8") == grouped.read_text(encoding="utf-8")


def test_build_command(tmp_path):
    (tmp_path / "template.html").write_text("<html><body>{{NAV}}{{SECTIONS}}</body></html>", encoding="utf-8")
    (tmp_path / "view.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    config = tmp_path / "vistas.yml"
    config.write_text("\ntemplate: template.html\nvistas:\n  - id: sample\n    src: view.mmd\n", encoding="utf-8")

    out = tmp_path / "out.html"
    r = runner.invoke(main, ["build", "--config", str(config), "--out", str(out)])
    assert r.exit_code == 0
    assert out.exists()
    assert "Rendered catalog" in r.output
    html = out.read_text(encoding="utf-8")
    assert "catalog-search" in html


def test_build_command_supports_store_of_stores(tmp_path):
    root = tmp_path
    child = root / "child"
    child.mkdir()

    (root / "template.html").write_text(
        "<html><head><title>{{CATALOG_TITLE}}</title></head><body><aside>{{NAV}}</aside><main>{{FILTERS}}{{SECTIONS}}</main></body></html>",
        encoding="utf-8",
    )
    (child / "view.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    (child / "spec-component.yml").write_text(
        "id: spec-component\ntitle: Example\ntype: component\nversion: '1.0'\ndata:\n  nodes: {}\n  edges: []\n", encoding="utf-8"
    )
    (child / "vistas.yml").write_text(
        """
template: unused.html
vistas:
  - id: sample
    category: Arquitectura
    title: Sample Diagram
    nav: Sample
    desc: Demo child vista
    src: view.mmd
    specs:
      - spec-component
""",
        encoding="utf-8",
    )
    (root / "catalog.yml").write_text(
        """
template: template.html
title: Repo Catalog
brand_name: Diagram Catalog
stores:
  - path: child/vistas.yml
    project: demo/project
    tags:
      - domain:crm
""",
        encoding="utf-8",
    )

    out = root / "out.html"
    r = runner.invoke(main, ["build", "--config", str(root / "catalog.yml"), "--out", str(out)])
    assert r.exit_code == 0, r.output
    html = out.read_text(encoding="utf-8")
    assert "Repo Catalog" in html
    assert "Diagram Catalog" in html
    assert "catalog-search" in html
    assert 'data-project="demo/project"' in html
    assert 'data-type="component"' in html
    assert "domain:crm" in html
    assert "Sample Diagram" in html


def test_build_command_supports_brand_subtitle_in_builtin_template(tmp_path):
    root = tmp_path
    (root / "view.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    (root / "spec-component.yml").write_text(
        "id: spec-component\ntitle: Example\ntype: component\nversion: '1.0'\ndata:\n  nodes: {}\n  edges: []\n", encoding="utf-8"
    )
    (root / "catalog.yml").write_text(
        "template: missing-template.html\ntitle: Repo Catalog\nbrand_name: Diagram Catalog\nbrand_subtitle: Repo subtitle from config\nvistas:\n  - id: sample\n    category: Arquitectura\n    title: Sample Diagram\n    src: view.mmd\n    specs:\n      - spec-component.yml\n",
        encoding="utf-8",
    )

    out = root / "out.html"
    r = runner.invoke(main, ["build", "--config", str(root / "catalog.yml"), "--out", str(out)])
    assert r.exit_code == 0, r.output
    html = out.read_text(encoding="utf-8")
    assert "Repo subtitle from config" in html
    assert "Visor transversal de diagramas de spec2viz" not in html


def test_build_command_warns_on_local_template_override(tmp_path):
    root = tmp_path
    (root / "template.html").write_text(
        "<html><head><title>{{CATALOG_TITLE}}</title></head><body><aside>{{NAV}}</aside><main>{{FILTERS}}{{SECTIONS}}</main></body></html>",
        encoding="utf-8",
    )
    (root / "view.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    (root / "spec-component.yml").write_text(
        "id: spec-component\ntitle: Example\ntype: component\nversion: '1.0'\ndata:\n  nodes: {}\n  edges: []\n", encoding="utf-8"
    )
    (root / "catalog.yml").write_text(
        "template: template.html\nvistas:\n  - id: sample\n    category: Arquitectura\n    title: Sample Diagram\n    src: view.mmd\n    specs:\n      - spec-component.yml\n",
        encoding="utf-8",
    )

    out = root / "out.html"
    r = runner.invoke(main, ["build", "--config", str(root / "catalog.yml"), "--out", str(out)])
    assert r.exit_code == 0, r.output
    assert "using local catalog template override" in r.output


def test_build_command_supports_project_yml_envelope(tmp_path):
    root = tmp_path
    child = root / "child"
    child.mkdir()

    (root / "template.html").write_text(
        "<html><head><title>{{CATALOG_TITLE}}</title></head><body><aside>{{NAV}}</aside><main>{{FILTERS}}{{SECTIONS}}</main></body></html>",
        encoding="utf-8",
    )
    (child / "view.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    (child / "spec-state.yml").write_text(
        "id: spec-state\ntitle: Example State\ntype: state\nversion: '1.0'\ndata:\n  entity: X\n  initial: a\n  states:\n    - id: a\n      label: A\n  transitions: []\n",
        encoding="utf-8",
    )
    (child / "vistas.yml").write_text(
        """
template: ../template.html
vistas:
  - id: sample-state
    category: Estados
    title: State Diagram
    nav: State
    desc: Demo leaf
    src: view.mmd
    specs:
      - spec-state.yml
""",
        encoding="utf-8",
    )
    (root / "project.yml").write_text(
        """
diagram_store:
  kind: diagram-store
  template: template.html
  title: Project Catalog
  brand_name: Project Brand
  project_name: project/demo
  stores:
    - path: child/vistas.yml
      project: project/demo
      tags:
        - domain:workflow
""",
        encoding="utf-8",
    )

    out = root / "out.html"
    r = runner.invoke(main, ["build", "--config", str(root / "project.yml"), "--out", str(out)])
    assert r.exit_code == 0, r.output
    html = out.read_text(encoding="utf-8")
    assert "Project Catalog" in html
    assert "Project Brand" in html
    assert "project/demo" in html
    assert "domain:workflow" in html
    assert 'data-type="state"' in html


def test_build_command_extracts_types_from_specs_dir_and_makes_anchor_ids_unique(tmp_path):
    root = tmp_path
    (root / "template.html").write_text("<html><body><aside>{{NAV}}</aside><main>{{FILTERS}}{{SECTIONS}}</main></body></html>", encoding="utf-8")

    for folder in [root / "alpha" / "docs" / "vistas", root / "beta" / "docs" / "vistas"]:
        folder.mkdir(parents=True)
        (folder.parent.parent / "project.yaml").write_text("project_name: Demo\nclient: sample\n", encoding="utf-8")
        (folder.parent.parent / "specs").mkdir(exist_ok=True)
        (folder.parent.parent / "specs" / "same-view.yml").write_text(
            "id: same-view\ntitle: Same\ntype: component\nversion: '1.0'\ndata:\n  nodes: {}\n  edges: []\n", encoding="utf-8"
        )
        (folder.parent.parent / "rendered").mkdir(exist_ok=True)
        (folder.parent.parent / "rendered" / "same-view.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
        (folder / "vistas.yml").write_text(
            "template: template.html\nvistas:\n  - id: vista01\n    title: Demo\n    category: Arquitectura\n    specs:\n      - same-view\n    mmd: ../../rendered/same-view.mmd\n",
            encoding="utf-8",
        )

    (root / "catalog.yml").write_text(
        "template: template.html\nstores:\n  - path: alpha/docs/vistas/vistas.yml\n  - path: beta/docs/vistas/vistas.yml\n", encoding="utf-8"
    )

    out = root / "out.html"
    r = runner.invoke(main, ["catalog", "build", "--config", str(root / "catalog.yml"), "--out", str(out)])
    assert r.exit_code == 0, r.output
    html = out.read_text(encoding="utf-8")
    assert html.count('data-type="component"') == 2
    anchor_ids = set(re.findall(r'id="(sample-demo-vista01-[a-f0-9]{8})"', html))
    assert len(anchor_ids) == 2


def test_build_command_extracts_html_section_fragments(tmp_path):
    (tmp_path / "template.html").write_text("<html><body>{{NAV}}{{FILTERS}}{{SECTIONS}}</body></html>", encoding="utf-8")
    (tmp_path / "bundle.html").write_text(
        '<html><body><section id="d1"><div class="board"><pre class="mermaid">graph TD\\nA-->B</pre></div></section></body></html>',
        encoding="utf-8",
    )
    (tmp_path / "catalog.yml").write_text(
        "template: template.html\nitems:\n  - id: frag\n    title: Fragment\n    src: bundle.html#d1\n    type: component\n    category: Arquitectura\n",
        encoding="utf-8",
    )

    out = tmp_path / "out.html"
    r = runner.invoke(main, ["catalog", "build", "--config", str(tmp_path / "catalog.yml"), "--out", str(out)])
    assert r.exit_code == 0, r.output
    html = out.read_text(encoding="utf-8")
    assert "bundle.html#d1" not in html
    assert '<div class="board"><pre class="mermaid">graph TD\\nA-->B</pre></div>' in html


def test_build_command_reports_errors(tmp_path):
    (tmp_path / "template.html").write_text("<html><body>{{NAV}}{{SECTIONS}}</body></html>", encoding="utf-8")
    config = tmp_path / "vistas.yml"
    config.write_text("template: template.html\nvistas: [\n  {id: broken, src: missing.mmd}\n]\n", encoding="utf-8")

    out = tmp_path / "out.html"
    r = runner.invoke(main, ["build", "--config", str(config), "--out", str(out)])
    assert r.exit_code != 0
    assert "Error building catalog" in r.output


def test_catalog_build_embeds_the_annotations_saver_of_ir13b(tmp_path):
    """`--sldb-url`/`--annotations-doc` build the page IR13b's `render_catalog` builds with that target
    (the round trip through a real `sldb serve` is `test_catalog_annotations.py`); without them the page
    is spec2viz's, and `--annotations` alone leaves the server to the page URL."""
    (tmp_path / "view.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    config = tmp_path / "vistas.yml"
    config.write_text("title: Demo\nvistas:\n  - id: sample\n    title: Sample\n    src: view.mmd\n", encoding="utf-8")
    cases = {
        (): None,
        ("--annotations",): AnnotationsTarget(),
        ("--sldb-url", "http://127.0.0.1:8765"): AnnotationsTarget(server="http://127.0.0.1:8765"),
        ("--sldb-url", "http://127.0.0.1:8765", "--annotations-doc", "catalog-annotations-x"): AnnotationsTarget("http://127.0.0.1:8765", "catalog-annotations-x"),
    }
    for i, (args, target) in enumerate(cases.items()):
        out = tmp_path / f"out-{i}.html"
        r = runner.invoke(main, ["catalog", "build", "--config", str(config), "--out", str(out), *args])
        assert r.exit_code == 0, r.output
        page = out.read_text(encoding="utf-8")
        assert page == render_catalog(config, annotations=target), args
        assert ("window.SPECIR_ANNOTATIONS" in page) == (target is not None), args


# ── the correspondence table ──────────────────────────────────────────────────


def correspondence_rows() -> list[list[str]]:
    rows = []
    for line in CORRESPONDENCE.read_text(encoding="utf-8").splitlines():
        if line.startswith("| SV-K"):
            rows.append([cell.strip() for cell in line.strip().strip("|").split("|")])
    return rows


def _command_and_options(text: str) -> tuple[list[str], list[str]]:
    """`specir diagram render --renderer --out` -> (["specir", "diagram", "render"], ["--renderer", "--out"])."""
    words, options, done = [], [], False
    for token in text.split():
        token = token.strip("[]")
        if token.startswith("-"):
            options.append(token)
            done = True
        elif not done and re.fullmatch(r"[a-z][a-z0-9-]*", token):
            words.append(token)
        else:
            done = True
    return words, options


def _assert_answers_help(words: list[str], options: list[str]) -> None:
    if words[0] == "specir":
        r = runner.invoke(main, [*words[1:], "--help"])
        assert r.exit_code == 0, f"{' '.join(words)}: {r.output}"
        output = r.output
    else:
        assert words[0] == "sldb", words
        p = subprocess.run(["timeout", "120", SLDB, *words[1:], "--help"], capture_output=True, text=True)
        assert p.returncode == 0, f"{' '.join(words)}: {p.stderr}"
        output = p.stdout
    for option in options:
        assert re.search(rf"(?<![\w-]){re.escape(option)}(?![\w-])", output), f"{' '.join(words)} has no {option}"


def test_the_table_has_one_row_per_command_id():
    ids = [row[0] for row in correspondence_rows()]
    assert sorted(ids) == [f"SV-K{n:02d}" for n in range(1, 31)]


def test_every_equivalent_of_the_table_answers_its_help():
    import sldb.notations as notations

    checked = 0
    for row in correspondence_rows():
        equivalent = re.match(r"`([^`]+)`", row[3]).group(1)
        if equivalent.startswith("sldb.notations."):
            function = getattr(notations, equivalent.rsplit(".", 1)[1])
            builtins = notations.builtin_notations() if function is notations.load_notation else notations.builtin_palettes()
            assert builtins and all(function(name) for name in builtins), equivalent
        else:
            words, options = _command_and_options(equivalent)
            _assert_answers_help(words, options)
        checked += 1
    assert checked == 30


def test_specir_defines_no_command_the_table_gives_to_sldb():
    for row in correspondence_rows():
        command = re.fullmatch(r"`([^`]+)`", row[1]).group(1)
        if row[3].startswith("`sldb"):
            path = command.split()[1:]
            group = main
            for part in path[:-1]:
                group = group.commands.get(part)
                if group is None:
                    break
            assert group is None or path[-1] not in getattr(group, "commands", {}), f"specir duplicates {command}"


# ── the agent skill ───────────────────────────────────────────────────────────


def skill_commands() -> set[str]:
    """Every `specir ...`/`sldb ...` the skill names: inline code spans and lines of its code blocks."""
    text = SKILL.read_text(encoding="utf-8")
    found = set()
    blocks = re.findall(r"```[a-z]*\n(.*?)```", text, flags=re.DOTALL)
    for block in blocks:
        for line in block.splitlines():
            for part in line.split("->"):
                part = part.strip()
                if part.startswith(("specir ", "sldb ")):
                    found.add(part)
    prose = re.sub(r"```[a-z]*\n.*?```", "", text, flags=re.DOTALL)
    found |= {span for span in re.findall(r"`([^`\n]+)`", prose) if span.startswith(("specir ", "sldb "))}
    return found


def test_the_skill_names_only_commands_that_exist():
    commands = skill_commands()
    assert len(commands) > 20
    seen = set()
    for command in sorted(commands):
        words, options = _command_and_options(command)
        key = (tuple(words), tuple(options))
        if key in seen:
            continue
        seen.add(key)
        _assert_answers_help(words, options)
    named = {" ".join(words) for words, _ in seen}
    assert {"specir about", "specir diagram render", "sldb notations validate", "specir diagram lint", "specir catalog build",
            "specir catalog schema", "sldb notations sync", "sldb notations from-graph", "sldb serve"} <= named


def test_the_skill_names_no_spec2viz_command():
    text = SKILL.read_text(encoding="utf-8")
    assert not re.search(r"(?m)^\s*(python -m )?spec2viz[ .]", text)
    assert not re.search(r"`(python -m )?spec2viz[ .][^`]*`", text)
    assert re.search(r"^name: use-specir$", text, flags=re.MULTILINE)
