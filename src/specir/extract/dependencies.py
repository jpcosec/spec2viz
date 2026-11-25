"""The dependencies between the pieces of a tree: a piece is a top-level package of a repo, and a piece
depends on another when a module of it imports the other's top-level package.

The imports come from the generic facts of sldb (`attrs.imports` and `attrs.nested_imports` of each
module fact): an absolute import counts, a relative one stays inside the piece, a conditional or
nested one counts. A `depends_on` edge is `observado` (the facts show it as it is) and lists in
`attributes.sitios` the file and line of every import, so a rule over the edge can name them.

Known gap of the facts: they give the module an import belongs to but not its line, and the extractor
reads no code itself, so the site is the importing module's file and the line is reported as `desconocido`
(sldb is asked for it in its inbox)."""

from __future__ import annotations

from pathlib import Path

from sldb.api.code import code_facts

from specir.extract.facts import Fact, Facts
from specir.extract.plan import Planned, edge_name, node_name, sentence
from specir.extract.python_cli import _is_test
from specir.extract.write import ExtractionReport, write_plan
from specir.install import package_pythonpath

RULE = "module-imports-top-level-package-of-another-piece"
PIECE_RULE = "top-level-package-of-the-tree"
RELATION = "depends_on"


def top(module: str) -> str:
    return module.split(".", 1)[0]


def interpret_dependencies(facts: Facts) -> tuple[dict[str, Planned], dict[str, Planned], list[str]]:
    modules = [m for m in facts.of_kind("module") if m["path"].endswith(".py") and not _is_test(m["path"])]
    pieces = {top(m["attrs"]["module"]) for m in modules}
    nodes: dict[str, Planned] = {}
    anchors: dict[str, Fact] = {}
    for module in modules:
        if module["path"].endswith("__init__.py") and "." not in module["attrs"]["module"]:
            anchors[top(module["attrs"]["module"])] = module
    for name in sorted(pieces):
        anchor = anchors.get(name)
        text = sentence(PIECE_RULE, [anchor], derived=False) if anchor else f"Observado por la regla {PIECE_RULE}: paquete de primer nivel {name} del árbol."
        planned = Planned("PieceDoc", node_name("PieceDoc", name), {"title": name, "description": text}, "observado", PIECE_RULE, [anchor] if anchor else [])
        nodes[planned.export_id] = planned
    uses: dict[tuple[str, str], list[Fact]] = {}
    not_derived: list[str] = []
    for module in modules:
        source = top(module["attrs"]["module"])
        imported = [*module["attrs"].get("imports", []), *module["attrs"].get("nested_imports", [])]
        for target in sorted({top(i) for i in imported if not i.startswith(".")} & pieces - {source}):
            not_derived.append(f"desconocido: la línea del import de {target} en {module['path']}; los hechos de sldb traen el módulo que importa pero no la línea (pedido a sldb en su inbox)")
            uses.setdefault((source, target), []).append(module)
    edges: dict[str, Planned] = {}
    for (source, target), sites in sorted(uses.items()):
        src, dst = nodes[f"PieceDoc:{node_name('PieceDoc', source)}"], nodes[f"PieceDoc:{node_name('PieceDoc', target)}"]
        used = list({m["id"]: m for m in sites}.values())
        listed = [f"{m['path']} (línea desconocida)" for m in used]
        name = edge_name(src, RELATION, dst)
        fields = {
            "title": f"{source} {RELATION} {target}", "source_id": src.export_id, "target_id": dst.export_id, "relation_type": RELATION, "condition": "",
            "notes": f"{sentence(RULE, used, derived=False)} Importa en: {'; '.join(listed)}.",
        }
        edges[f"RelationDoc:{name}"] = Planned("RelationDoc", name, fields, "observado", RULE, used, {"sitios": listed})
    return nodes, edges, not_derived


def extract_dependencies(root: str | Path, store: str | Path | None = None, paths: list[str] | None = None) -> ExtractionReport:
    """Extract the pieces (top-level Python packages) under `root` and the `depends_on` edges between
    them into `store` (default `<root>/.sldb`); idempotent. An edge whose import was removed is
    deleted if nobody verified it.

    Raises:
        ValueError: A fact's anchor does not match the fact; nothing is written.
    """
    root = Path(root).resolve()
    store_path = Path(store).resolve() if store is not None else root / ".sldb"
    result = code_facts(root, paths)
    nodes, edges, not_derived = interpret_dependencies(Facts(result["facts"]))
    report = write_plan(store_path, root, package_pythonpath(), list(nodes.values()), list(edges.values()), list(dict.fromkeys(not_derived)), retire=RELATION)
    report.skipped = [s for s in result.get("skipped", []) if s.endswith(".py")]
    return report
