from __future__ import annotations

import json
import sys
from pathlib import Path

import click

from spec2viz import json_schema, load, render_to_file, validate, write_json_schema
from spec2viz.exceptions import Spec2VizError


DIAGRAM_RENDERERS = ["plantuml", "mermaid", "vega", "d2", "antonia-html", "tree", "graph", "bpmn", "json"]


def _render_paths(paths: list[Path], out: Path, renderer: str | None):
    for path in paths:
        try:
            output = render_to_file(path, out=out, renderer=renderer)
            click.echo(f"Rendered {path.name} -> {output}")
            if renderer == "bpmn":
                click.echo(f"Rendered {path.name} -> {output.with_name(output.name + '.html')}")
        except Spec2VizError as exc:
            click.echo(f"Error: {exc}", err=True)
            sys.exit(1)


def _validate_paths(paths: list[Path]):
    for path in paths:
        try:
            diagram = load(path)
            validate(diagram)
            click.echo(f"{path.name}: OK")
        except Spec2VizError as exc:
            click.echo(f"{path.name}: ERROR: {exc}", err=True)
            sys.exit(1)


def _lint_paths(paths: list[Path]):
    """Lint mermaid text files (.mmd) or render specs to mermaid then lint."""
    from spec2viz.linters.mermaid import lint_mermaid

    had_issue = False
    for path in paths:
        try:
            if path.suffix == ".mmd":
                text = path.read_text(encoding="utf-8")
            else:
                from spec2viz import compile_ir, load
                from spec2viz.renderers import render

                text = render(compile_ir(load(path)), "mermaid")
            problems = lint_mermaid(text)
        except Spec2VizError as exc:
            click.echo(f"{path.name}: ERROR: {exc}", err=True)
            had_issue = True
            continue
        if problems:
            had_issue = True
            click.echo(f"{path.name}: {len(problems)} issue(s)", err=True)
            for p in problems:
                click.echo(f"  - {p}", err=True)
        else:
            click.echo(f"{path.name}: OK")
    if had_issue:
        sys.exit(1)


def _write_schema(diagram_type: str | None, out: Path | None):
    if out:
        write_json_schema(out, diagram_type=diagram_type)
        click.echo(f"Wrote schema to {out}")
    else:
        click.echo(json.dumps(json_schema(diagram_type), indent=2))


def _build_catalog(config: Path, out: Path, base_dir: Path | None, atoms_dir: Path | None, atoms_tags: tuple[str, ...] = (), strict_atoms: bool = False):
    from spec2viz.deskops import build_deskops

    try:
        build_deskops(config, out, base_dir, atoms_dir, list(atoms_tags) or None, strict_atoms)
        click.echo(f"Rendered catalog -> {out}")
    except Exception as exc:
        click.echo(f"Error building catalog: {exc}", err=True)
        sys.exit(1)


@click.group(
    help=(
        "spec2viz CLI.\n\n"
        "Taxonomy:\n"
        "- diagram: semantic diagram specs (render, validate, schema)\n"
        "- catalog: HTML bundles and hierarchical diagram stores (build, schema)\n\n"
        "Legacy top-level commands remain available for compatibility."
    )
)
def main():
    pass


@main.command("about", short_help="Where diagrams live and how the flow reaches HTML.")
def about():
    """Point to where the diagrams live and the full spec -> HTML flow."""
    pkg_root = Path(__file__).resolve().parent.parent
    examples = pkg_root / "examples"
    click.echo("spec2viz — semantic specs -> diagrams -> catalog HTML\n")

    click.echo("Where the diagrams live:")
    click.echo(f"  package examples : {examples}")
    if examples.is_dir():
        for sub in sorted(p for p in examples.iterdir() if p.is_dir()):
            specs = sorted(
                list(sub.rglob("*.yml")) + list(sub.rglob("*.yaml"))
            )
            if specs:
                rel = ", ".join(s.relative_to(examples).as_posix() for s in specs[:3])
                click.echo(f"    - {sub.name:<11} {rel}")
    click.echo("  catalog config   : examples/catalog/project.yml\n")

    click.echo("Flow to HTML:")
    click.echo("  1. diagram validate <spec.yml>")
    click.echo("  2. diagram render   <spec.yml> --out <dir>")
    click.echo("  3. diagram lint     <rendered.mmd>")
    click.echo("  4. catalog build    --config <vistas.yml> --out <out.html>")
    click.echo("     (build alias = catalog build; --atoms-dir injects window.ATOMS_DB)\n")

    click.echo("Serve a built catalog:")
    click.echo("  catalog serve --html <out.html> --port 8000")


@main.group(help="Work with semantic diagram specs.")
def diagram():
    pass


@main.group(help="Declarative visual vocabularies: NotationDoc, GlyphDoc and LinkDoc as store documents.")
def notation():
    pass


@notation.command("list", short_help="List the builtin notations.")
def notation_list():
    """One line per builtin notation: name, diagram type, glyph and link counts."""
    from spec2viz.notation import builtin_notations, load_notation

    for name in builtin_notations():
        spec = load_notation(name)
        click.echo(f"{name}: {spec.diagram_type} ({spec.level}), {len(spec.glyphs)} glyphs, {len(spec.links)} links, layout {spec.layout.get('kind')}")


@notation.command("validate", short_help="Validate notation YAML files (or builtin names).")
@click.argument("names", nargs=-1, required=True, metavar="NAME_OR_PATH ...")
def notation_validate(names: tuple[str, ...]):
    """Check each notation's grammar: ids, enumerations, default glyphs, relations the diagram
    type emits, `where` predicates in the `sldb find --where` grammar, builtin shapes, and the
    optional style against its palette: palette kinds, colors (token or `#rrggbb`) and icons of
    the declared set. Errors name their type (UnknownShapeError, UnknownKindError,
    InvalidColorError, UnknownIconError)."""
    from spec2viz.exceptions import ValidationError
    from spec2viz.notation import load_notation

    failed = False
    for name in names:
        try:
            spec = load_notation(name)
        except ValidationError as exc:
            click.echo(f"Invalid: {type(exc).__name__}: {exc}", err=True)
            failed = True
            continue
        click.echo(f"Valid: {spec.name} ({spec.diagram_type}; glyphs: {', '.join(g.id for g in spec.glyphs)}; links: {', '.join(l.id for l in spec.links)})")
    if failed:
        sys.exit(1)


@main.group(short_help="List, validate and sync palettes (colors, icons and reference shapes per kind).")
def palette():
    """Palettes: per-kind fill, stroke, icon and reference shape, as data. `default` is builtin."""


@palette.command("list", short_help="List the builtin palettes.")
def palette_list():
    """One line per builtin palette: name, kinds and icon set."""
    from spec2viz.palette import builtin_palettes, load_palette

    for name in builtin_palettes():
        spec = load_palette(name)
        click.echo(f"{name}: {len(spec.kinds)} kinds ({', '.join(spec.kinds)}), icons {spec.icon_set.name} {spec.icon_set.version} ({len(spec.icon_set.icons)})")


@palette.command("validate", short_help="Validate palette YAML files (or builtin names): colors, icons, shapes and WCAG contrast.")
@click.argument("names", nargs=-1, required=True, metavar="NAME_OR_PATH ...")
def palette_validate(names: tuple[str, ...]):
    """Check each palette: `#rrggbb` colors and tokens, icons of the declared set, builtin shapes,
    strokes >= 3:1 against each theme background, text >= 4.5:1 on each fill, and a distinct
    (shape, icon) per kind so colour is never the only cue. Errors name their type."""
    from spec2viz.exceptions import ValidationError
    from spec2viz.palette import load_palette

    failed = False
    for name in names:
        try:
            spec = load_palette(name)
        except ValidationError as exc:
            click.echo(f"Invalid: {type(exc).__name__}: {exc}", err=True)
            failed = True
            continue
        click.echo(f"Valid: {spec.name} ({len(spec.kinds)} kinds, {len(spec.colors)} color tokens, {len(spec.icon_set.icons)} icons)")
    if failed:
        sys.exit(1)


@palette.command("sync", short_help="Write palettes into an sldb store as PaletteDoc.")
@click.argument("names", nargs=-1, required=True, metavar="NAME_OR_PATH ...")
@click.option("--store", required=True, type=click.Path(exists=True, path_type=Path), help="The `.sldb` store to write into.")
@click.option("--pythonpath", help="Project path the store's models import from.")
def palette_sync(names: tuple[str, ...], store: Path, pythonpath: str | None):
    """Write each palette as `PaletteDoc:<name>` under `sldb/palettes/`. `notation sync` already
    writes the palette a styled notation uses; this is for a palette on its own."""
    from spec2viz.sldb_sync import PaletteSync

    for name in names:
        try:
            report = PaletteSync(store, pythonpath).sync(name)
        except Exception as exc:
            click.echo(f"Error syncing palette {name}: {type(exc).__name__}: {exc}", err=True)
            sys.exit(1)
        click.echo(f"Synced palette {report.spec_id} ({len(report.created)} created, {len(report.updated)} updated)")


@notation.command("sync", short_help="Write notations into an sldb store.")
@click.argument("names", nargs=-1, required=True, metavar="NAME_OR_PATH ...")
@click.option("--store", required=True, type=click.Path(exists=True, path_type=Path), help="The `.sldb` store to write into.")
@click.option("--pythonpath", help="Project path the store's models import from.")
@click.option("--strict", is_flag=True, help="Exit 1 when the notation names a model the store does not register or the edge index reports errors.")
def notation_sync(names: tuple[str, ...], store: Path, pythonpath: str | None, strict: bool):
    """Write each notation as `NotationDoc:<name>`, one `GlyphDoc:<name>.<glyph>` and one
    `LinkDoc:<name>.<link>` under `<root>/sldb/notations/<name>/`, creating the
    RelationTypeDocs it names, then rebuild and check the edge index."""
    from spec2viz.sldb_sync import NotationSync, format_notation_report

    sync = NotationSync(Path(store), pythonpath=pythonpath)
    failed = False
    for name in names:
        try:
            report = sync.sync(name)
        except Exception as exc:
            click.echo(f"Error syncing notation {name}: {exc}", err=True)
            sys.exit(1)
        click.echo(format_notation_report(report))
        failed = failed or bool(report.problems)
    if strict and failed:
        sys.exit(1)


@notation.command("view", short_help="Resolve a spec's view (glyph per node, link per relation) as JSON.")
@click.argument("spec_ref", metavar="SPEC_REF")
@click.option("--store", required=True, type=click.Path(exists=True, path_type=Path), help="The `.sldb` store to read.")
@click.option("--pythonpath", help="Project path the store's models import from.")
@click.option("--out", type=click.Path(path_type=Path), help="Write the JSON here instead of stdout.")
def notation_view(spec_ref: str, store: Path, pythonpath: str | None, out: Path | None):
    """Apply docs/notation-contract.md to `SpecDoc:<id>` (or `<id>`): which glyph, markers, label
    and compartments each node gets and which link each relation gets. This is the one
    interpreter of the contract; a surface serves this and draws."""
    import json

    from spec2viz.notation_view import ViewError, resolve_view

    try:
        view = resolve_view(Path(store), spec_ref, pythonpath)
    except ViewError as exc:
        click.echo(f"Error: {exc}", err=True)
        sys.exit(1)
    text = json.dumps(view, ensure_ascii=False, indent=2)
    if out:
        out.write_text(text + "\n", encoding="utf-8")
        click.echo(f"Wrote {out}")
    else:
        click.echo(text)


@main.group(help="Work with diagram catalogs, vistas registries, and hierarchical stores.")
def catalog():
    pass


@diagram.command("render", short_help="Render diagram specs to output files.")
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path), metavar="SPEC ...")
@click.option("--out", default=".", show_default=True, type=click.Path(path_type=Path), help="Output directory for rendered files.")
@click.option(
    "--renderer",
    "--backend",
    type=click.Choice(DIAGRAM_RENDERERS),
    default=None,
    help="Force a renderer instead of using the spec type default.",
)
def diagram_render(paths: list[Path], out: Path, renderer: str | None):
    """Render one or more semantic diagram spec files."""
    _render_paths(paths, out, renderer)


@main.command("render", short_help="Render diagram specs to output files.")
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path), metavar="SPEC ...")
@click.option("--out", default=".", show_default=True, type=click.Path(path_type=Path), help="Output directory for rendered files.")
@click.option(
    "--renderer",
    "--backend",
    type=click.Choice(DIAGRAM_RENDERERS),
    default=None,
    help="Force a renderer instead of using the spec type default.",
)
def render(paths: list[Path], out: Path, renderer: str | None):
    """Legacy alias for `diagram render`."""
    _render_paths(paths, out, renderer)


@diagram.command("generate", short_help="Generate a component spec from Python source AST.")
@click.argument("src_dir", type=click.Path(exists=True, path_type=Path), metavar="SRC_DIR")
@click.option("--out", default="architecture.spec.yaml", show_default=True, type=click.Path(path_type=Path), help="Output spec YAML file.")
@click.option("--id", "project_id", default=None, help="Project identifier for the spec. Defaults to directory name.")
@click.option("--title", default=None, help="Human-readable title. Defaults to '<project> AST Architecture'.")
@click.option("--package", default=None, help="Root package to filter (e.g. 'sldb'). Scans all if omitted.")
def diagram_generate(src_dir: Path, out: Path, project_id: str | None, title: str | None, package: str | None):
    """Scan Python source files and generate a spec2viz component diagram spec."""
    from spec2viz.generators import generate_python_ast_spec, write_spec

    pid = project_id or src_dir.resolve().parent.name
    ttl = title or f"{pid} AST Architecture"
    spec = generate_python_ast_spec(src_dir, project_id=pid, title=ttl, root_package=package)
    write_spec(spec, out)
    click.echo(f"Generated {out} ({len(spec['data']['nodes'])} nodes, {len(spec['data']['edges'])} edges)")


@diagram.command("from-graph", short_help="Compile an sldb graph (snapshot JSON or store index) into a component spec.")
@click.argument("graph_json", required=False, type=click.Path(exists=True, dir_okay=False, path_type=Path), metavar="[GRAPH_JSON]")
@click.option("--store", type=click.Path(exists=True, file_okay=False, path_type=Path), help="Read the edge index of this .sldb (or project) dir via sldb.api instead of a JSON file.")
@click.option("--node-type", "node_types", multiple=True, help="Node type to keep (document, model, semantic_tag, ...); repeatable. Default: document, model.")
@click.option("--model", "models", multiple=True, help="Keep only documents of this model (e.g. AtomDoc); repeatable.")
@click.option("--relation", "relations", multiple=True, help="Keep only these relations; repeatable. Overrides the default exclusions.")
@click.option("--exclude-relation", "exclude_relations", multiple=True, help="Drop this relation; repeatable. Default: structural relations (has_section, tagged_as, ...).")
@click.option("--drop-isolated", is_flag=True, help="Drop nodes left without edges after filtering.")
@click.option("--module-prefix", "module_prefixes", multiple=True, help="Keep only Python nodes of this module or below (sldb's python-source graph: `sldb.selfdoc`); repeatable. Edges and nesting with an end outside the scope are dropped.")
@click.option("--id", "spec_id", default=None, help="Spec id. Defaults to the file stem or 'sldb-graph'.")
@click.option("--title", default=None, help="Spec title. Defaults to '<id> graph'.")
@click.option("--out", type=click.Path(path_type=Path), help="Write the YAML spec here instead of stdout.")
def diagram_from_graph(
    graph_json: Path | None,
    store: Path | None,
    node_types: tuple[str, ...],
    models: tuple[str, ...],
    relations: tuple[str, ...],
    exclude_relations: tuple[str, ...],
    drop_isolated: bool,
    module_prefixes: tuple[str, ...],
    spec_id: str | None,
    title: str | None,
    out: Path | None,
):
    """Compile an sldb graph into a spec2viz component diagram spec.

    GRAPH_JSON is a node-link file from `sldb graph snapshot save` or sldb's Python
    source graph (`sldb selfdoc python-sync`, `.sldb/runtime/graphs/python-source.graph.json`);
    `--store` reads the store's edge index instead. `contains` relations nest nodes, every
    other relation becomes an edge with its name as it comes. Python nodes take their label
    from the code (`ast.name` / `ast.module`) and their kind from the declared
    `semantics.kind` or the AST class; `--module-prefix` scopes them without leaving any
    dangling edge or nesting.
    """
    import yaml

    from spec2viz.graph_import import component_spec_from_graph, load_node_link_graph, load_store_index

    if (graph_json is None) == (store is None):
        raise click.UsageError("Pass exactly one of GRAPH_JSON or --store.")
    attrs = None
    try:
        if store is not None:
            nodes, edges = load_store_index(store)
            source, default_id = f"store {store}", "sldb-graph"
        else:
            nodes, edges, attrs = load_node_link_graph(graph_json)
            source, default_id = f"file {graph_json}", graph_json.stem
    except ImportError as exc:
        click.echo(f"Error: --store needs the sldb package ({exc})", err=True)
        sys.exit(1)
    except Exception as exc:
        click.echo(f"Error reading graph: {exc}", err=True)
        sys.exit(1)

    sid = spec_id or default_id
    spec = component_spec_from_graph(
        nodes,
        edges,
        node_types=node_types,
        models=models,
        relations=relations,
        exclude_relations=exclude_relations or None,
        drop_isolated=drop_isolated,
        spec_id=sid,
        title=title or f"{sid} graph",
        source=source,
        attrs=attrs,
        module_prefixes=module_prefixes,
    )
    text = yaml.safe_dump(spec, sort_keys=False, allow_unicode=True)
    if out:
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(text, encoding="utf-8")
        click.echo(f"Generated {out} ({len(spec['data']['nodes'])} nodes, {len(spec['data']['edges'])} edges)")
    else:
        click.echo(text, nl=False)


@diagram.command("sync", short_help="Materialize spec nodes and edges as sldb documents.")
@click.argument("paths", nargs=-1, required=True, type=click.Path(exists=True, path_type=Path), metavar="SPEC ...")
@click.option("--store", type=click.Path(exists=True, path_type=Path), help="The `.sldb` store to write into. Defaults to the nearest `.sldb` above the first spec.")
@click.option("--out", type=click.Path(path_type=Path), help="Directory for the generated markdown. Defaults to `<spec dir>/sldb/<spec id>`.")
@click.option("--pythonpath", help="Project path the store's models import from.")
@click.option("--strict", is_flag=True, help="Exit 1 when a `refs:`/`atoms:` target does not exist or the edge index reports errors.")
@click.option("--notation", default=None, help="Notation to draw the spec with: a builtin name, a YAML path, or `none`. Defaults to the diagram type's builtin (uml-class, statechart) if it has one.")
def diagram_sync(paths: list[Path], store: Path | None, out: Path | None, pythonpath: str | None, strict: bool, notation: str | None):
    """Write each spec into an sldb store: `SpecDoc:<id>`, one `SpecNodeDoc:<id>.<element>` per
    element and one `RelationDoc` per edge, then rebuild and check the edge index.

    `refs:` and `atoms:` of the elements become `references` edges and `contains:` becomes
    `contains`, so the store's documents hang from the diagram and the catalog shows the
    relations back on each node. Documents of a previous sync that left the spec are deleted.

    The spec's notation (NotationDoc, GlyphDoc, LinkDoc) is synced with it and referenced
    from `SpecDoc.notation`, so a surface such as graph_ui can draw the spec from the store.
    """
    from spec2viz.sldb_sync import SpecSync, find_store, format_report

    store_path = store or find_store(paths[0].resolve().parent)
    if store_path is None:
        click.echo("Error: no `.sldb` store found above the spec; pass --store.", err=True)
        sys.exit(1)
    sync = SpecSync(Path(store_path), pythonpath=pythonpath, out_dir=out)
    failed = False
    for path in paths:
        try:
            report = sync.sync(path, notation=notation)
        except Exception as exc:
            click.echo(f"Error syncing {path}: {exc}", err=True)
            sys.exit(1)
        click.echo(format_report(report))
        failed = failed or bool(report.problems)
    if strict and failed:
        sys.exit(1)


@diagram.command("validate", short_help="Validate semantic diagram spec files.")
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path), metavar="SPEC ...")
def diagram_validate(paths: list[Path]):
    """Validate one or more semantic diagram spec files."""
    _validate_paths(paths)


@main.command("validate", short_help="Validate semantic diagram spec files.")
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path), metavar="SPEC ...")
def validate_cmd(paths: list[Path]):
    """Legacy alias for `diagram validate`."""
    _validate_paths(paths)


@diagram.command("lint", short_help="Lint rendered mermaid for browser-breaking syntax.")
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path), metavar="SPEC_OR_MMD ...")
def diagram_lint(paths: list[Path]):
    """Lint .mmd files, or render specs to mermaid and lint the result."""
    _lint_paths(paths)


@main.command("lint", short_help="Lint rendered mermaid for browser-breaking syntax.")
@click.argument("paths", nargs=-1, type=click.Path(exists=True, path_type=Path), metavar="SPEC_OR_MMD ...")
def lint_cmd(paths: list[Path]):
    """Legacy alias for `diagram lint`."""
    _lint_paths(paths)


@diagram.command("schema", short_help="Export JSON Schema for semantic diagram specs.")
@click.option(
    "--type",
    "diagram_type",
    default=None,
    help="Limit the schema to one type: class, sequence, state, component, activity, deployment, or component_view_matrix.",
)
@click.option("--out", type=click.Path(path_type=Path), help="Write the schema to this file instead of stdout.")
def diagram_schema(diagram_type: str | None, out: Path | None):
    """Export JSON Schema for all diagram spec types or one diagram type."""
    _write_schema(diagram_type, out)


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


@catalog.command("sync", short_help="Sync every spec of a vistas.yml into an sldb store, with notation and catalog metadata.")
@click.option("--config", required=True, type=click.Path(exists=True, path_type=Path), help="The vistas.yml registry whose specs are synced.")
@click.option("--store", type=click.Path(exists=True, path_type=Path), help="The `.sldb` store to write into. Defaults to the nearest `.sldb` above the config.")
@click.option("--pythonpath", help="Project path the store's models import from.")
@click.option("--strict", is_flag=True, help="Exit 1 when a `refs:`/`atoms:` target does not exist or the edge index reports errors.")
def catalog_sync(config: Path, store: Path | None, pythonpath: str | None, strict: bool):
    """The catalog on graph_ui: each spec listed in the registry is synced like `diagram sync`
    (nodes, edges, its diagram type's notation) and its `SpecDoc` carries the registry's
    `category`, `nav` and `desc`, so a surface lists the specs by category and draws each one
    with `notation view`. The HTML bundle (`catalog build`) is the static export of the same data.
    """
    from spec2viz.sldb_sync import SpecSync, check_catalog, find_store, format_report, sync_catalog

    store_path = store or find_store(config.resolve().parent)
    if store_path is None:
        click.echo("Error: no `.sldb` store found above the config; pass --store.", err=True)
        sys.exit(1)
    # todo o nada: una notacion inexistente o de otro tipo frena el sync antes de escribir
    # el sync no lee `src` (es la fuente de `catalog build`): un src que falta no lo frena
    problems = [(entry, exc) for entry, exc in check_catalog(config, Path(store_path), pythonpath, include_src=False) if exc is not None]
    for entry, exc in problems:
        click.echo(f"Invalid: {entry['vista'] or entry['spec']}: {type(exc).__name__}: {exc}", err=True)
    if problems:
        sys.exit(1)
    try:
        reports = sync_catalog(SpecSync(Path(store_path), pythonpath=pythonpath), config)
    except Exception as exc:
        click.echo(f"Error syncing catalog: {exc}", err=True)
        sys.exit(1)
    failed = False
    for report in reports:
        click.echo(format_report(report))
        failed = failed or bool(report.problems)
    if strict and failed:
        sys.exit(1)


@catalog.command("validate", short_help="Validate a vistas.yml: specs exist and validate, notations resolve to the right type.")
@click.option("--config", required=True, type=click.Path(exists=True, path_type=Path), help="The vistas.yml registry to check.")
@click.option("--store", type=click.Path(exists=True, path_type=Path), help="The `.sldb` store a notation name resolves against. Defaults to the nearest `.sldb` above the config, if any.")
@click.option("--pythonpath", help="Project path the store's models import from.")
def catalog_validate(config: Path, store: Path | None, pythonpath: str | None):
    """Check every view of the registry without writing: each listed spec exists and validates,
    and its `notation:` (a path relative to the vistas.yml, a builtin name or a NotationDoc of the
    store; absent = the builtin of the spec's type) resolves and draws that spec's diagram type.
    Errors name their type (UnknownNotationError, NotationMismatchError, UnknownReferenceError...)."""
    from spec2viz.sldb_sync import check_catalog, find_store

    store_path = store or find_store(config.resolve().parent)
    failed = False
    for entry, exc in check_catalog(config, Path(store_path) if store_path else None, pythonpath):
        name = entry["vista"] or str(entry["spec"])
        if exc is None:
            click.echo(f"Valid: {name}: {Path(entry['spec']).name}" + (f" (notation {entry['notation']})" if entry["notation"] else ""))
        else:
            click.echo(f"Invalid: {name}: {type(exc).__name__}: {exc}", err=True)
            failed = True
    if failed:
        sys.exit(1)


@catalog.command("schema", short_help="Export JSON Schema for hierarchical diagram stores.")
@click.option("--out", type=click.Path(path_type=Path), help="Write the schema to this file instead of stdout.")
def catalog_schema(out: Path | None):
    """Export JSON Schema for diagram-store / project.yml configs."""
    _write_schema("diagram-store", out)


@catalog.command("serve", short_help="Serve catalog locally with auto-save for annotations.")
@click.option("--html", required=True, type=click.Path(exists=True, path_type=Path), help="Path to the built architecture.html to serve.")
@click.option("--port", default=8000, show_default=True, type=int, help="Port to serve on.")
def catalog_serve(html: Path, port: int):
    """Serve the built catalog and provide a POST endpoint to auto-save annotations."""
    import http.server
    import socketserver
    
    class Handler(http.server.SimpleHTTPRequestHandler):
        def do_GET(self):
            if self.path == '/' or self.path.startswith('/index'):
                self.send_response(200)
                self.send_header('Content-type', 'text/html')
                self.end_headers()
                content = html.read_text(encoding='utf-8')
                script = '''<script>
                // Auto-save logic overrides annoWriteStore
                if (typeof annoWriteStore === "function") {
                    const _oldAnnoWriteStore = annoWriteStore;
                    window.annoWriteStore = function(items) {
                        _oldAnnoWriteStore(items);
                        fetch('/api/annotations', {
                            method: 'POST',
                            headers: {'Content-Type': 'application/json'},
                            body: JSON.stringify(items)
                        }).then(r => console.log('Auto-saved to disk', r.status));
                    };
                }
                </script></body>'''
                content = content.replace('</body>', script)
                self.wfile.write(content.encode('utf-8'))
            else:
                self.send_response(404)
                self.end_headers()

        def do_POST(self):
            if self.path == '/api/annotations':
                content_len = int(self.headers.get('Content-Length', 0))
                post_body = self.rfile.read(content_len)
                try:
                    data = json.loads(post_body)
                    out_path = html.parent / 'comentarios-arquitectura.json'
                    out_path.write_text(json.dumps(data, indent=2), encoding='utf-8')
                    self.send_response(200)
                    self.end_headers()
                except Exception as e:
                    click.echo(f"Error saving: {e}")
                    self.send_response(400)
                    self.end_headers()
            else:
                self.send_response(404)
                self.end_headers()

    with socketserver.TCPServer(("127.0.0.1", port), Handler) as httpd:
        click.echo(f"🚀 Serving catalog at http://localhost:{port}")
        click.echo(f"💾 Auto-saving annotations to: {html.parent / 'comentarios-arquitectura.json'}")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            click.echo("\nStopping server...")

@catalog.command("build", short_help="Build catalog HTML from a vistas registry or diagram store.")
@click.option("--config", required=True, type=click.Path(exists=True, path_type=Path), help="Path to a legacy vistas.yml registry or a hierarchical diagram store config.")
@click.option("--out", required=True, type=click.Path(path_type=Path), help="HTML file to write.")
@click.option("--base-dir", type=click.Path(exists=True, path_type=Path), help="Base directory for template and vista source paths. Defaults to the config file directory.")
@click.option("--atoms-dir", type=click.Path(exists=True, path_type=Path), help="Directory with W5H1 atom markdown files to inject as window.ATOMS_DB.")
@click.option("--atoms-tag", "atoms_tags", multiple=True, help="Embed only atoms carrying this tag (full `ns:value` or just `value`); repeatable. Default: all atoms.")
@click.option("--strict-atoms", is_flag=True, help="Fail the build if a spec `atoms:` id does not exist among the loaded atoms (default: warning).")
def catalog_build(config: Path, out: Path, base_dir: Path | None, atoms_dir: Path | None, atoms_tags: tuple[str, ...], strict_atoms: bool):
    """Build a diagram catalog HTML bundle from a vistas registry or diagram store."""
    _build_catalog(config, out, base_dir, atoms_dir, atoms_tags, strict_atoms)


@main.command("build", short_help="Build catalog HTML from a vistas registry or diagram store.")
@click.option("--config", required=True, type=click.Path(exists=True, path_type=Path), help="Path to a legacy vistas.yml registry or a hierarchical diagram store config.")
@click.option("--out", required=True, type=click.Path(path_type=Path), help="HTML file to write.")
@click.option("--base-dir", type=click.Path(exists=True, path_type=Path), help="Base directory for template and vista source paths. Defaults to the config file directory.")
@click.option("--atoms-dir", type=click.Path(exists=True, path_type=Path), help="Directory with W5H1 atom markdown files to inject as window.ATOMS_DB.")
@click.option("--atoms-tag", "atoms_tags", multiple=True, help="Embed only atoms carrying this tag (full `ns:value` or just `value`); repeatable. Default: all atoms.")
@click.option("--strict-atoms", is_flag=True, help="Fail the build if a spec `atoms:` id does not exist among the loaded atoms (default: warning).")
def build(config: Path, out: Path, base_dir: Path | None, atoms_dir: Path | None, atoms_tags: tuple[str, ...], strict_atoms: bool):
    """Legacy alias for `catalog build`."""
    _build_catalog(config, out, base_dir, atoms_dir, atoms_tags, strict_atoms)


if __name__ == "__main__":
    main()
