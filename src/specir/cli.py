"""The `specir` command: the visual layer's CLI, with the taxonomy of spec2viz's (IR13d).

- `diagram` (render, lint, schema) and `catalog` (schema) are IR12's groups
  (`specir.visual.commands`); this module mounts them and adds `catalog build` (IR13b's page, with
  the option to save its annotations through `sldb serve`), the top-level aliases `render`,
  `lint`, `schema` and `build`, and `about`.
- `retirement check` (IR13) is the retirement gate of spec2viz (`specir.visual.retirement`): it audits,
  read-only, the inventory of the coverage matrix plus specIR's repo, and the matrix's accreditation.
- What spec2viz's CLI did that is sldb's has no command here, by design (JP: no wrapper over sldb's
  CLI or API): syncing a spec, a notation, a palette or a catalog (`sldb notations sync --spec`,
  `--notation`, `--palette`, `--catalog [--check]`), generating a spec from a graph or from Python
  (`sldb notations from-graph`), listing notations and palettes (`sldb notations list`), resolving a
  view (`sldb notations view`) and serving the catalog's annotations (`sldb serve`). The table is
  `docs/spec2viz/correspondencia-cli.md`.
- Validating a spec, a notation or a palette is `sldb notations validate <name|path> [--json]`
  (SV-K16, SV-K21, SV-K26, SV-K29): specIR does not define `diagram validate` or `validate`."""

from __future__ import annotations

import sys
from pathlib import Path

import click

from specir.visual.commands import (
    DIAGRAM_RENDERERS,
    _lint_paths,
    _render_paths,
    _write_schema,
    catalog,
    diagram,
)

#: The top-level aliases, each with the group command it stands for (spec2viz's legacy commands).
ALIASES = {"render": "diagram render", "lint": "diagram lint", "schema": "diagram schema",
           "build": "catalog build"}


@click.group(
    help=(
        "specIR CLI: semantic diagram specs -> diagrams -> catalog HTML.\n\n"
        "\b\nTaxonomy:\n"
        "- diagram: semantic diagram specs (render, lint, schema)\n"
        "- catalog: HTML bundles and hierarchical diagram stores (build, schema)\n\n"
        "Top-level aliases (render, lint, schema, build) remain available for compatibility.\n\n"
        "Syncing specs, notations, palettes and catalogs into a store, generating specs from a graph "
        "or from Python, resolving views and serving annotations are sldb's: use `sldb notations ...` "
        "and `sldb serve` directly."
    )
)
@click.version_option(package_name="specir", prog_name="specir")
def main():
    pass


main.add_command(diagram)
main.add_command(catalog)


@main.command("mcp", short_help="Serve sldb's MCP server with specIR's tools loaded.")
@click.option("--store", required=True, type=click.Path(path_type=Path), help="The sldb store to serve.")
@click.option("--level", default=None, type=int, help="Mutability level (default: read-only).")
@click.option("--actor", default=None, help="Actor recorded on writes.")
def mcp(store: Path, level: int | None, actor: str | None):
    """Serve sldb's MCP server on a store with specIR's tools (specir_types, specir_nodes, specir_rules, specir_impact) already loaded."""
    from specir.mcp_extension import serve

    serve(store, level=level, actor=actor)


@main.command("about", short_help="Where diagrams live and how the flow reaches HTML.")
def about():
    """Point to where the diagrams live and the full spec -> HTML flow, with sldb's commands for the store."""
    from sldb.api.notations import find_store

    cwd = Path.cwd()
    store = find_store(cwd)
    click.echo("specir — semantic specs -> diagrams -> catalog HTML (specIR's visual layer over sldb)\n")

    click.echo("Where the diagrams live:")
    click.echo("  spec files       : YAML specs (`type:` one of the eight diagram types) next to their vistas.yml")
    click.echo(f"  store            : {store if store else f'no .sldb store above {cwd}'}")
    click.echo("  specs in a store : SpecDoc documents (`sldb notations list --store <.sldb>`)")
    click.echo("  catalog config   : a vistas.yml registry or a project.yml / diagram-store config\n")

    click.echo("Flow to HTML:")
    click.echo("  1. sldb notations validate <spec.yml>")
    click.echo("  2. specir diagram render   <spec.yml> --out <dir>")
    click.echo("  3. specir diagram lint     <rendered.mmd>")
    click.echo("  4. specir catalog build    --config <vistas.yml> --out <out.html>")
    click.echo("     (build alias = catalog build; --atoms-dir injects window.ATOMS_DB)\n")

    click.echo("Into the store (sldb, used directly):")
    click.echo("  sldb notations sync --spec <spec.yml> --store <.sldb>")
    click.echo("  sldb notations sync --catalog <vistas.yml> [--check] --store <.sldb>")
    click.echo("  sldb notations from-graph --python <src_dir> | --store <.sldb> | --snapshot <graph.json>")
    click.echo("  sldb notations view <SpecDoc id> --store <.sldb>\n")

    click.echo("Save a built catalog's annotations (replaces spec2viz's `catalog serve`):")
    click.echo("  sldb models add specir.visual.catalog.annotations:CatalogAnnotationsDoc --store <.sldb>")
    click.echo("  sldb serve --store <.sldb> --cors --port 8765")
    click.echo("  specir catalog build --config <vistas.yml> --out <out.html> --sldb-url http://127.0.0.1:8765")


# ── catalog build and its alias ─────────────────────────────────────────────────────────────────


def _build_catalog(config: Path, out: Path, base_dir: Path | None, atoms_dir: Path | None, atoms_tags: tuple[str, ...],
                   strict_atoms: bool, annotations: bool, sldb_url: str | None, annotations_doc: str | None):
    from specir.visual.catalog import AnnotationsTarget, build_catalog

    target = AnnotationsTarget(server=sldb_url or "", doc=annotations_doc or "") if (annotations or sldb_url or annotations_doc) else None
    try:
        build_catalog(config, out, base_dir, atoms_dir, list(atoms_tags) or None, strict_atoms, target)
        click.echo(f"Rendered catalog -> {out}")
    except Exception as exc:
        click.echo(f"Error building catalog: {exc}", err=True)
        sys.exit(1)


def _catalog_build_options(function):
    options = [
        click.option("--config", required=True, type=click.Path(exists=True, path_type=Path), help="Path to a legacy vistas.yml registry or a hierarchical diagram store config."),
        click.option("--out", required=True, type=click.Path(path_type=Path), help="HTML file to write."),
        click.option("--base-dir", type=click.Path(exists=True, path_type=Path), help="Base directory for template and vista source paths. Defaults to the config file directory."),
        click.option("--atoms-dir", type=click.Path(exists=True, path_type=Path), help="Directory with W5H1 atom markdown files to inject as window.ATOMS_DB."),
        click.option("--atoms-tag", "atoms_tags", multiple=True, help="Embed only atoms carrying this tag (full `ns:value` or just `value`); repeatable. Default: all atoms."),
        click.option("--strict-atoms", is_flag=True, help="Fail the build if a spec `atoms:` id does not exist among the loaded atoms (default: warning)."),
        click.option("--annotations", is_flag=True, help="Save the page's annotations in an sldb store through `sldb serve`; the server and the document can also come from the page URL (`?sldb=<url>&annotations=<id>`)."),
        click.option("--sldb-url", default=None, help="Base URL of `sldb serve --cors` that keeps the annotations (implies --annotations)."),
        click.option("--annotations-doc", default=None, help="Id of the CatalogAnnotationsDoc that holds them (implies --annotations). Default: derived from the catalog's name."),
    ]
    for option in reversed(options):
        function = option(function)
    return function


@catalog.command("build", short_help="Build catalog HTML from a vistas registry or diagram store.")
@_catalog_build_options
def catalog_build(config: Path, out: Path, base_dir: Path | None, atoms_dir: Path | None, atoms_tags: tuple[str, ...], strict_atoms: bool,
                  annotations: bool, sldb_url: str | None, annotations_doc: str | None):
    """Build a diagram catalog HTML bundle from a vistas registry or diagram store."""
    _build_catalog(config, out, base_dir, atoms_dir, atoms_tags, strict_atoms, annotations, sldb_url, annotations_doc)


@main.command("build", short_help="Build catalog HTML from a vistas registry or diagram store.")
@_catalog_build_options
def build(config: Path, out: Path, base_dir: Path | None, atoms_dir: Path | None, atoms_tags: tuple[str, ...], strict_atoms: bool,
          annotations: bool, sldb_url: str | None, annotations_doc: str | None):
    """Legacy alias for `catalog build`."""
    _build_catalog(config, out, base_dir, atoms_dir, atoms_tags, strict_atoms, annotations, sldb_url, annotations_doc)


# ── the other top-level aliases ─────────────────────────────────────────────────────────────────


@main.command("render", short_help="Render diagram specs to output files.")
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path), metavar="SPEC ...")
@click.option("--out", default=".", show_default=True, type=click.Path(path_type=Path), help="Output directory for rendered files.")
@click.option("--renderer", "--backend", type=click.Choice(DIAGRAM_RENDERERS), default=None, help="Force a renderer instead of using the spec type default.")
def render(paths: list[Path], out: Path, renderer: str | None):
    """Legacy alias for `diagram render`."""
    _render_paths(paths, out, renderer)


@main.command("lint", short_help="Lint rendered mermaid for browser-breaking syntax.")
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path), metavar="SPEC_OR_MMD ...")
def lint_cmd(paths: list[Path]):
    """Legacy alias for `diagram lint`."""
    _lint_paths(paths)


@main.command("schema", short_help="Export JSON Schema for semantic specs.")
@click.option(
    "--type",
    "diagram_type",
    default=None,
    help="Limit the schema to one type: class, sequence, state, component, activity, deployment, component_view_matrix, or diagram-store.",
)
@click.option("--out", type=click.Path(path_type=Path), help="Write the schema to this file instead of stdout.")
def schema(diagram_type: str | None, out: Path | None):
    """Legacy schema entrypoint for diagram specs and diagram stores."""
    _write_schema(diagram_type, out)


@main.group("retirement", short_help="The retirement gate of spec2viz (IR13).")
def retirement():
    """The retirement gate of spec2viz: `docs/spec2viz/gate-de-retiro.md`."""


@retirement.command("check", short_help="Audit the consumers and stores of the inventory and the matrix's accreditation.")
@click.option("--matrix", default=str(Path("docs") / "spec2viz" / "matriz-de-cobertura.md"), show_default=True,
              type=click.Path(exists=True, dir_okay=False, path_type=Path), help="The coverage matrix; its repo is specIR's.")
@click.option("--path", "paths", multiple=True, metavar="NAME=PATH",
              help="Local path of each repo and store of the matrix's inventory (a store's path is its .sldb folder).")
def retirement_check(matrix: Path, paths: tuple[str, ...]):
    """Report every remaining dependency on spec2viz (repo or store, path, line and kind) and every row
    of the matrix not accredited; exit 1 when there is one, 0 when the retirement can be declared.
    Nothing is written."""
    from specir.visual.retirement import InventoryError, check, format_gate_report

    given: dict[str, Path] = {}
    for item in paths:
        name, sep, value = item.partition("=")
        if not sep or not name or not value:
            raise click.UsageError(f"--path takes NAME=PATH, not {item!r}")
        given[name] = Path(value)
    try:
        report = check(matrix, given)
    except InventoryError as exc:
        raise click.UsageError(str(exc)) from exc
    click.echo(format_gate_report(report))
    sys.exit(0 if report.ok else 1)


@main.group("ux", short_help="Extract the interface of a tree (graph_ui).")
def ux():
    """The interface extraction of a tree into a store."""


@ux.command("extract", short_help="Extract the interface nodes of a tree and warn of the skipped files.")
@click.argument("root", type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.option("--store", type=click.Path(path_type=Path), default=None, help="Store path. Default: <ROOT>/.sldb.")
@click.option("--path", "paths", multiple=True, help="Only extract this path relative to ROOT (repeatable).")
@click.option("--strict", is_flag=True, help="Exit 1 if code_facts skipped any file.")
def ux_extract(root: Path, store: Path | None, paths: tuple[str, ...], strict: bool):
    """Run the frontend extraction over ROOT and print a summary. Files `code_facts` skipped (no
    installed grammar) are warned on stderr; with --strict they make the exit code 1."""
    from specir.extract import extract_frontend

    try:
        report = extract_frontend(root, store, list(paths) or None)
    except ValueError as exc:
        click.echo(f"Error extracting: {exc}", err=True)
        sys.exit(1)
    click.echo(f"created: {len(report.created)}, updated: {len(report.changed)}, unchanged: {len(report.unchanged)}, not derived: {len(report.not_derived)}")
    for item in report.not_derived:
        click.echo(f"  not derived: {item}")
    if report.skipped:
        shown = report.skipped[:10]
        more = f" (+{len(report.skipped) - 10} more)" if len(report.skipped) > 10 else ""
        click.echo(f"warning: code_facts skipped {len(report.skipped)} file(s) (no installed grammar or unreadable){more}:", err=True)
        for item in shown:
            click.echo(f"  {item}", err=True)
        if strict:
            sys.exit(1)


@main.group("extract", short_help="Extract nodes from a tree into a store.")
def extract_group():
    """Extractions of code into the nodes of specIR's types."""


@extract_group.command("python-cli", short_help="Extract the CLI, public API, handlers, operations and models of a Python library.")
@click.argument("root", type=click.Path(exists=True, file_okay=False, path_type=Path))
@click.option("--store", type=click.Path(path_type=Path), default=None, help="Store path. Default: <ROOT>/.sldb.")
@click.option("--path", "paths", multiple=True, help="Only extract this path relative to ROOT (repeatable).")
def extract_python_cli_cmd(root: Path, store: Path | None, paths: tuple[str, ...]):
    """Run the Python CLI extraction over ROOT and print a summary. What the facts did not let a rule
    classify is printed as `desconocido` with its reason and counted."""
    from specir.extract import extract_python_cli

    try:
        report = extract_python_cli(root, store, list(paths) or None)
    except ValueError as exc:
        click.echo(f"Error extracting: {exc}", err=True)
        sys.exit(1)
    click.echo(f"created: {len(report.created)}, updated: {len(report.changed)}, unchanged: {len(report.unchanged)}, desconocidos: {len(report.not_derived)}")
    for item in report.not_derived:
        click.echo(f"  {item}")


__all__ = ["ALIASES", "main"]


if __name__ == "__main__":
    main()
