"""Generator that scans a Python project AST and produces a spec2viz component spec."""
from __future__ import annotations

import ast
from pathlib import Path

import yaml


def _sanitize_id(module_path: str) -> str:
    """Convert a dotted module path to a safe node identifier."""
    return module_path.replace(".", "_").replace("-", "_")


def _scan_module(pyfile: Path, src_root: Path) -> tuple[list[dict], list[dict]]:
    """Extract elements and relations from a single Python module."""
    rel = pyfile.relative_to(src_root)
    mod_id = str(rel.with_suffix("")).replace("/", ".")
    safe_id = f"module_{_sanitize_id(mod_id)}"

    elements = [{"id": safe_id, "kind": "module", "label": mod_id}]
    relations = []

    try:
        tree = ast.parse(pyfile.read_text(encoding="utf-8"))
    except SyntaxError:
        return elements, relations

    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.ClassDef):
            cls_id = f"class_{_sanitize_id(mod_id)}_{node.name}"
            elements.append({"id": cls_id, "kind": "class", "label": node.name})
            relations.append({"source": safe_id, "target": cls_id, "kind": "defines"})

    for node in ast.walk(tree):
        if not isinstance(node, ast.ImportFrom):
            continue
        if node.module is None:
            continue
        target_id = f"module_{_sanitize_id(node.module)}"
        relations.append({"source": safe_id, "target": target_id, "kind": "imports"})

    return elements, relations


def generate_python_ast_spec(
    src_dir: Path,
    *,
    project_id: str = "project",
    title: str = "Python AST Architecture",
    root_package: str | None = None,
) -> dict:
    """Scan all .py files under src_dir and return a spec2viz-compatible dict."""
    all_elements: list[dict] = []
    all_relations: list[dict] = []

    for pyfile in sorted(src_dir.rglob("*.py")):
        if pyfile.name == "__init__.py":
            continue
        if root_package and not _module_matches(pyfile, src_dir, root_package):
            continue
        elements, relations = _scan_module(pyfile, src_dir)
        all_elements.extend(elements)
        all_relations.extend(relations)

    return _build_spec(project_id, title, all_elements, all_relations)


def _module_matches(pyfile: Path, src_dir: Path, root_package: str) -> bool:
    """Check if a file belongs to the given root package."""
    rel = str(pyfile.relative_to(src_dir))
    return rel.startswith(root_package.replace(".", "/"))


def _build_spec(
    project_id: str, title: str, elements: list[dict], relations: list[dict]
) -> dict:
    """Assemble the final spec2viz YAML structure."""
    seen_ids = {el["id"] for el in elements}
    _register_missing_nodes(elements, relations, seen_ids)

    nodes = {}
    for el in elements:
        nodes[el["id"]] = {"label": el["label"], "kind": el["kind"]}

    edges = [
        {"from": r["source"], "to": r["target"], "relation": r["kind"]}
        for r in relations
    ]

    return {
        "id": project_id,
        "title": title,
        "type": "component",
        "version": "1.0",
        "data": {"nodes": nodes, "edges": edges},
    }


def _register_missing_nodes(
    elements: list[dict], relations: list[dict], seen_ids: set[str]
) -> None:
    """Auto-register nodes referenced in edges but not yet declared."""
    for rel in relations:
        target = rel["target"]
        if target not in seen_ids:
            label = target.split("_")[-1]
            elements.append({"id": target, "kind": "external", "label": label})
            seen_ids.add(target)


def write_spec(spec: dict, output_path: Path) -> None:
    """Write a spec2viz spec dict to a YAML file."""
    output_path.parent.mkdir(parents=True, exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        yaml.dump(spec, f, sort_keys=False, allow_unicode=True)
