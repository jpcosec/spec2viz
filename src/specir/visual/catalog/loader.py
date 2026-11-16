"""The registry of a catalog: a `vistas.yml`, a hierarchical diagram store or a `project.yml`
envelope, loaded into the flat list of views the HTML catalog draws (migrated from spec2viz's
`orchestrator`: `CatalogItem`, `CatalogConfig`, `CatalogLoader`, `load_catalog`).

Every relative path follows sldb's catalog rule (`sldb.api.notations.catalog_paths`): next to
the config first, then from the repository root, ambiguous when both exist. A spec id without an
extension keeps the inherited search (`<id>.yml` or `specs/<id>.yml` in the config's folder or
its ancestors). The models of the envelope are sldb's (`DiagramStoreEnvelope`, D3)."""

from __future__ import annotations

import hashlib
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

import yaml
from sldb.api.notations.catalog_paths import resolve_catalog_path

from specir.visual.notation_style import UnknownReferenceError

DEFAULT_TITLE = "spec2viz Catalog"
DEFAULT_SUBTITLE = "Visor transversal de diagramas de spec2viz"
DEFAULT_PROJECT_NAME = "spec2viz"
DEFAULT_CATEGORY = "Otras Vistas"

#: Words of a view's title, description or labels that name its diagram type, when no spec says it.
TYPE_HINTS = (
    (("component diagram", "diagrama de componentes", "componentes", "arquitectura logica de componentes"), "component"),
    (("deployment diagram", "diagrama de despliegue", "topologia de despliegue", "despliegue"), "deployment"),
    (("sequence diagram", "diagrama de secuencia", "secuencia", "interacciones"), "sequence"),
    (("state diagram", "state uml", "state diagram-v2", "diagrama de estados", "estados", "ciclo de vida"), "state"),
    (("activity diagram", "actividad", "flujo de atencion", "flujo"), "activity"),
    (("diagrama de clases", "class diagram", "clases"), "class"),
    (("casos de uso", "use case"), "use-case"),
)


def safe_token(value: str) -> str:
    if not value:
        return ""
    normalized = unicodedata.normalize("NFKD", value).encode("ascii", "ignore").decode("ascii")
    return re.sub(r"[^a-z0-9]+", "-", normalized.lower()).strip("-")


def normalize_text(value: str) -> str:
    return unicodedata.normalize("NFKD", value or "").encode("ascii", "ignore").decode("ascii").lower()


def string_list(value) -> list[str]:
    if not value:
        return []
    if isinstance(value, str):
        return [value]
    return [str(v) for v in value if str(v).strip()]


@dataclass
class CatalogItem:
    """One view of the catalog, with the store (config) that declares it."""

    id: str
    anchor_id: str
    title: str
    desc: str = ""
    category: str = DEFAULT_CATEGORY
    nav: str = ""
    lbl: str = ""
    src: str | None = None
    specs: list[str] = field(default_factory=list)
    puml: str | None = None
    notes: list[str] = field(default_factory=list)
    project: str = ""
    diagram_type: str = ""
    tags: list[str] = field(default_factory=list)
    store_path: str = ""
    source_base_dir: str = ""
    notation: str | None = None  # the view's `notation:` (a path, a builtin name or one of the store)


@dataclass
class CatalogConfig:
    """The catalog's page (template, title, brand) and its views, flattened."""

    template: str
    title: str = DEFAULT_TITLE
    brand_name: str = DEFAULT_TITLE
    brand_subtitle: str = DEFAULT_SUBTITLE
    project_name: str = DEFAULT_PROJECT_NAME
    html_artifact: str = ""
    items: list[CatalogItem] = field(default_factory=list)


def _page(data: dict, template: str, title_keys: tuple[str, ...]) -> CatalogConfig:
    return CatalogConfig(
        template=template,
        title=next((data.get(k) for k in title_keys if data.get(k)), None) or DEFAULT_TITLE,
        brand_name=data.get("brand_name") or data.get("title") or DEFAULT_TITLE,
        brand_subtitle=data.get("brand_subtitle") or DEFAULT_SUBTITLE,
        project_name=data.get("project_name") or data.get("project") or DEFAULT_PROJECT_NAME,
        html_artifact=data.get("html_artifact", ""),
    )


def resolve_spec_path(spec: str, base_dir: Path) -> Path | None:
    """A spec with an extension follows the catalog rule (next to the config, then the repo root;
    `AmbiguousPathError` when both exist), then the inherited `specs/` folder; an id without an
    extension keeps the inherited search (`<id>.yml` or `specs/<id>.yml` in the config or its
    ancestors)."""
    spec_path = Path(spec)
    roots = [base_dir, *base_dir.parents[:6]]
    if spec_path.suffix:
        try:
            return resolve_catalog_path(spec, base_dir, "spec")
        except UnknownReferenceError:
            pass  # the inherited `specs/` folder, below
        candidates = [c for root in roots for c in (root / spec_path, root / "specs" / spec_path)]
    else:
        names = (f"{spec}.yml", f"{spec}.yaml", f"specs/{spec}.yml", f"specs/{spec}.yaml")
        candidates = [root / name for root in roots for name in names]
    return next((c.resolve() for c in candidates if c.exists()), None)


def find_project_file(base_dir: Path) -> Path | None:
    for root in [base_dir, *base_dir.parents[:6]]:
        for name in ("project.yaml", "project.yml"):
            if (root / name).exists():
                return (root / name).resolve()
    return None


def find_monorepo_root(start: Path, depth: int | None = None) -> Path | None:
    """The nearest ancestor with a README.md and a `projects/` or `software/` folder."""
    chain = [start, *start.parents] if depth is None else [start, *start.parents[:depth]]
    for root in chain:
        if (root / "README.md").exists() and ((root / "projects").exists() or (root / "software").exists()):
            return root.resolve()
    return None


def _project_from_file(project_file: Path) -> str | None:
    try:
        data = yaml.safe_load(project_file.read_text(encoding="utf-8")) or {}
    except Exception:
        return None
    client = str(data.get("client") or "").strip()
    project_name = str(data.get("project_name") or "").strip()
    if client and project_name:
        return f"{client}/{project_name}"
    return project_name or project_file.parent.resolve().name


def infer_project(base_dir: Path) -> str | None:
    """The project of a config: its folder relative to the monorepo root, or what its
    `project.yml` names (`client/project_name`), or the folder's name."""
    project_file = find_project_file(base_dir)
    if not project_file:
        return None
    project_dir = project_file.parent.resolve()
    root = find_monorepo_root(project_dir, depth=8)
    if root and project_dir.is_relative_to(root):
        return project_dir.relative_to(root).as_posix()
    return _project_from_file(project_file)


def infer_diagram_type(specs: list[str], base_dir: Path) -> str:
    for spec in specs:
        spec_path = resolve_spec_path(spec, base_dir)
        if not spec_path:
            continue
        try:
            data = yaml.safe_load(spec_path.read_text(encoding="utf-8")) or {}
        except Exception:
            continue
        if data.get("type"):
            return str(data["type"])
    return ""


def infer_diagram_type_from_item(item: dict) -> str:
    text = normalize_text(" ".join(str(item.get(key, "")) for key in ["title", "desc", "lbl", "nav", "category", "id"]))
    return next((kind for needles, kind in TYPE_HINTS if any(n in text for n in needles)), "")


def make_anchor_id(item_id: str, project: str | None, store_path: Path) -> str:
    digest = hashlib.md5(str(store_path.resolve()).encode("utf-8")).hexdigest()[:8]
    return "-".join(part for part in (safe_token(project or ""), safe_token(item_id), digest) if part)


def _with_tags(tags: list[str], project: str, diagram_type: str, exact: bool) -> list[str]:
    def has(prefix: str, value: str) -> bool:
        return any(tag == f"{prefix}{value}" if exact else tag.startswith(prefix) for tag in tags)

    if project and not has("project:", project):
        tags.append(f"project:{project}")
    if diagram_type and not has("type:", diagram_type):
        tags.append(f"type:{diagram_type}")
    return tags


@dataclass
class _Defaults:
    project: str
    category: str
    tags: list[str]
    diagram_type: str


def make_item(item: dict, base_dir: Path, store_path: Path, defaults: _Defaults) -> CatalogItem:
    specs = string_list(item.get("specs"))
    project = item.get("project") or defaults.project or infer_project(base_dir)
    diagram_type = item.get("type") or defaults.diagram_type or infer_diagram_type(specs, base_dir) or infer_diagram_type_from_item(item)
    tags = _with_tags(list(dict.fromkeys(defaults.tags + string_list(item.get("tags")))), project, diagram_type, exact=False)
    return CatalogItem(
        id=item["id"], anchor_id=make_anchor_id(item["id"], project, store_path), title=item.get("title", item["id"]),
        desc=item.get("desc", ""), category=item.get("category") or defaults.category, nav=item.get("nav", item.get("lbl", item["id"])),
        lbl=item.get("lbl", ""), src=item.get("src") or item.get("mmd"), specs=specs, puml=item.get("puml"),
        notes=string_list(item.get("notes")), project=project or "", diagram_type=diagram_type, tags=tags,
        store_path=str(store_path), source_base_dir=str(base_dir), notation=item.get("notation"),
    )


def apply_overrides(item: CatalogItem, overrides: dict) -> CatalogItem:
    """A child store's view with the `project`, `category`, `type` and `tags` of its parent's entry."""
    project = overrides.get("project") or item.project
    diagram_type = overrides.get("type") or item.diagram_type
    tags = _with_tags(list(dict.fromkeys(item.tags + string_list(overrides.get("tags")))), project, diagram_type, exact=True)
    return CatalogItem(
        **{**item.__dict__, "anchor_id": make_anchor_id(item.id, project, Path(item.store_path)), "category": overrides.get("category") or item.category,
           "project": project, "diagram_type": diagram_type, "tags": tags},
    )


def normalize_store_entry(store_entry, base_dir: Path) -> tuple[Path, dict]:
    if isinstance(store_entry, str):
        return (base_dir / store_entry).resolve(), {}
    if not isinstance(store_entry, dict) or "path" not in store_entry:
        raise ValueError("Store entries must be a relative path or an object with 'path'.")
    return (base_dir / str(store_entry["path"])).resolve(), {k: v for k, v in store_entry.items() if k != "path"}


class CatalogLoader:
    """Loads a registry and the stores it includes, refusing a store that includes itself."""

    def __init__(self):
        self._visited: set[Path] = set()

    def load(self, config_path: Path) -> CatalogConfig:
        config_path = Path(config_path).resolve()
        if config_path in self._visited:
            raise ValueError(f"Recursive store reference detected: {config_path}")
        self._visited.add(config_path)
        try:
            return self._load_store(config_path)
        finally:
            self._visited.remove(config_path)

    def _load_store(self, config_path: Path) -> CatalogConfig:
        raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
        data = raw["diagram_store"] if isinstance(raw.get("diagram_store"), dict) else raw
        if "vistas" in data:
            return self._load_vistas(config_path, data)
        catalog = _page(data, data.get("template", "template.html"), ("title", "catalog_title"))
        base_dir = config_path.parent
        defaults = _Defaults(data.get("project") or infer_project(base_dir) or "", data.get("category", DEFAULT_CATEGORY),
                             string_list(data.get("tags")), data.get("type", ""))
        catalog.items += [make_item(item, base_dir, config_path, defaults) for item in data.get("items", [])]
        for store_entry in data.get("stores", []):
            self._include(catalog, *normalize_store_entry(store_entry, base_dir))
        return catalog

    def _include(self, catalog: CatalogConfig, child_path: Path, overrides: dict) -> None:
        child = self.load(child_path)
        if not catalog.html_artifact and child.html_artifact:
            catalog.html_artifact = child.html_artifact
        catalog.items += [apply_overrides(item, overrides) for item in child.items]

    def _load_vistas(self, config_path: Path, data: dict) -> CatalogConfig:
        catalog = _page(data, data.get("template", "template.html"), ("title", "brand_name"))
        base_dir = config_path.parent
        defaults = _Defaults(data.get("project") or infer_project(base_dir) or "", DEFAULT_CATEGORY, string_list(data.get("tags")), "")
        catalog.items += [make_item(view, base_dir, config_path, defaults) for view in data.get("vistas", [])]
        return catalog


def load_catalog(config_path: Path) -> CatalogConfig:
    return CatalogLoader().load(config_path)


__all__ = [
    "CatalogConfig", "CatalogItem", "CatalogLoader", "infer_project", "load_catalog", "make_anchor_id", "resolve_spec_path",
]
