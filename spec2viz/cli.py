from __future__ import annotations

import json
import sys
from pathlib import Path

import click

from spec2viz import json_schema, load, render_to_file, validate, write_json_schema
from spec2viz.exceptions import Spec2VizError


DIAGRAM_RENDERERS = ["plantuml", "mermaid", "vega", "d2", "antonia-html", "tree", "graph", "json"]


def _render_paths(paths: list[Path], out: Path, renderer: str | None):
    for path in paths:
        try:
            output = render_to_file(path, out=out, renderer=renderer)
            click.echo(f"Rendered {path.name} -> {output}")
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


def _build_catalog(config: Path, out: Path, base_dir: Path | None, atoms_dir: Path | None):
    from spec2viz.deskops import build_deskops

    try:
        build_deskops(config, out, base_dir, atoms_dir)
        click.echo(f"Rendered deskops architecture -> {out}")
    except Exception as exc:
        click.echo(f"Error building deskops: {exc}", err=True)
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
    help="Limit the schema to one type: sequence, state, component, activity, deployment, or matrix.",
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
    help="Limit the schema to one type: sequence, state, component, activity, deployment, matrix, or diagram-store.",
)
@click.option("--out", type=click.Path(path_type=Path), help="Write the schema to this file instead of stdout.")
def schema(diagram_type: str | None, out: Path | None):
    """Legacy schema entrypoint for diagram specs and diagram stores."""
    _write_schema(diagram_type, out)


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
def catalog_build(config: Path, out: Path, base_dir: Path | None, atoms_dir: Path | None):
    """Build a diagram catalog HTML bundle from a vistas registry or diagram store."""
    _build_catalog(config, out, base_dir, atoms_dir)


@main.command("build", short_help="Build catalog HTML from a vistas registry or diagram store.")
@click.option("--config", required=True, type=click.Path(exists=True, path_type=Path), help="Path to a legacy vistas.yml registry or a hierarchical diagram store config.")
@click.option("--out", required=True, type=click.Path(path_type=Path), help="HTML file to write.")
@click.option("--base-dir", type=click.Path(exists=True, path_type=Path), help="Base directory for template and vista source paths. Defaults to the config file directory.")
@click.option("--atoms-dir", type=click.Path(exists=True, path_type=Path), help="Directory with W5H1 atom markdown files to inject as window.ATOMS_DB.")
def build(config: Path, out: Path, base_dir: Path | None, atoms_dir: Path | None):
    """Legacy alias for `catalog build`."""
    _build_catalog(config, out, base_dir, atoms_dir)


if __name__ == "__main__":
    main()
