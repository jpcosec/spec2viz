from __future__ import annotations

from dataclasses import dataclass, field
from pathlib import Path
import html
import json
import yaml


def _slug(value: str) -> str:
    return "-".join(value.strip().lower().split()) if value else ""


def _string_list(value) -> list[str]:
    if not value:
        return []
    if isinstance(value, str):
        return [value]
    return [str(v) for v in value if str(v).strip()]


@dataclass
class CatalogItem:
    id: str
    title: str
    desc: str = ""
    category: str = "Otras Vistas"
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


@dataclass
class CatalogConfig:
    template: str
    title: str = "spec2viz Catalog"
    brand_name: str = "spec2viz Catalog"
    project_name: str = "spec2viz"
    html_artifact: str = ""
    items: list[CatalogItem] = field(default_factory=list)


class CatalogLoader:
    def __init__(self):
        self._visited: set[Path] = set()

    def load(self, config_path: Path) -> CatalogConfig:
        config_path = config_path.resolve()
        if config_path in self._visited:
            raise ValueError(f"Recursive store reference detected: {config_path}")
        self._visited.add(config_path)
        try:
            return self._load_store(config_path)
        finally:
            self._visited.remove(config_path)

    def _load_store(self, config_path: Path) -> CatalogConfig:
        raw = yaml.safe_load(config_path.read_text(encoding="utf-8")) or {}
        base_dir = config_path.parent

        if "diagram_store" in raw and isinstance(raw["diagram_store"], dict):
            data = raw["diagram_store"]
        else:
            data = raw

        if "vistas" in data:
            return self._load_legacy_vistas(config_path, data)

        template = data.get("template", "template.html")
        catalog = CatalogConfig(
            template=template,
            title=data.get("title") or data.get("catalog_title") or "spec2viz Catalog",
            brand_name=data.get("brand_name") or data.get("title") or "spec2viz Catalog",
            project_name=data.get("project_name") or data.get("project") or "spec2viz",
            html_artifact=data.get("html_artifact", ""),
        )

        default_project = data.get("project", "")
        default_category = data.get("category", "Otras Vistas")
        default_tags = _string_list(data.get("tags"))
        default_type = data.get("type", "")

        for item in data.get("items", []):
            catalog.items.append(
                self._make_item(
                    item=item,
                    base_dir=base_dir,
                    store_path=config_path,
                    default_project=default_project,
                    default_category=default_category,
                    default_tags=default_tags,
                    default_type=default_type,
                )
            )

        for store_entry in data.get("stores", []):
            child_path, overrides = self._normalize_store_entry(store_entry, base_dir)
            child_catalog = self.load(child_path)
            if not catalog.html_artifact and child_catalog.html_artifact:
                catalog.html_artifact = child_catalog.html_artifact
            for child_item in child_catalog.items:
                catalog.items.append(self._apply_overrides(child_item, overrides))

        return catalog

    def _load_legacy_vistas(self, config_path: Path, data: dict) -> CatalogConfig:
        base_dir = config_path.parent
        catalog = CatalogConfig(
            template=data["template"],
            title=data.get("title") or data.get("brand_name") or "spec2viz Catalog",
            brand_name=data.get("brand_name") or data.get("title") or "spec2viz Catalog",
            project_name=data.get("project_name") or data.get("project") or "spec2viz",
            html_artifact=data.get("html_artifact", ""),
        )
        for view in data.get("vistas", []):
            catalog.items.append(
                self._make_item(
                    item=view,
                    base_dir=base_dir,
                    store_path=config_path,
                    default_project=data.get("project", ""),
                    default_category="Otras Vistas",
                    default_tags=_string_list(data.get("tags")),
                    default_type="",
                )
            )
        return catalog

    def _make_item(
        self,
        item: dict,
        base_dir: Path,
        store_path: Path,
        default_project: str,
        default_category: str,
        default_tags: list[str],
        default_type: str,
    ) -> CatalogItem:
        specs = _string_list(item.get("specs"))
        project = item.get("project") or default_project
        diagram_type = item.get("type") or default_type or self._infer_diagram_type(specs, base_dir)
        tags = list(dict.fromkeys(default_tags + _string_list(item.get("tags"))))
        if project and not any(tag.startswith("project:") for tag in tags):
            tags.append(f"project:{project}")
        if diagram_type and not any(tag.startswith("type:") for tag in tags):
            tags.append(f"type:{diagram_type}")

        src = item.get("src") or item.get("mmd")
        return CatalogItem(
            id=item["id"],
            title=item.get("title", item["id"]),
            desc=item.get("desc", ""),
            category=item.get("category") or default_category,
            nav=item.get("nav", item.get("lbl", item["id"])),
            lbl=item.get("lbl", ""),
            src=src,
            specs=specs,
            puml=item.get("puml"),
            notes=_string_list(item.get("notes")),
            project=project,
            diagram_type=diagram_type,
            tags=tags,
            store_path=str(store_path),
            source_base_dir=str(base_dir),
        )

    def _normalize_store_entry(self, store_entry, base_dir: Path) -> tuple[Path, dict]:
        if isinstance(store_entry, str):
            return (base_dir / store_entry).resolve(), {}
        if not isinstance(store_entry, dict) or "path" not in store_entry:
            raise ValueError("Store entries must be a relative path or an object with 'path'.")
        path = (base_dir / str(store_entry["path"])) .resolve()
        overrides = {k: v for k, v in store_entry.items() if k != "path"}
        return path, overrides

    def _apply_overrides(self, item: CatalogItem, overrides: dict) -> CatalogItem:
        project = overrides.get("project") or item.project
        category = overrides.get("category") or item.category
        diagram_type = overrides.get("type") or item.diagram_type
        tags = list(dict.fromkeys(item.tags + _string_list(overrides.get("tags"))))
        if project and not any(tag == f"project:{project}" for tag in tags):
            tags.append(f"project:{project}")
        if diagram_type and not any(tag == f"type:{diagram_type}" for tag in tags):
            tags.append(f"type:{diagram_type}")
        return CatalogItem(
            id=item.id,
            title=item.title,
            desc=item.desc,
            category=category,
            nav=item.nav,
            lbl=item.lbl,
            src=item.src,
            specs=item.specs,
            puml=item.puml,
            notes=item.notes,
            project=project,
            diagram_type=diagram_type,
            tags=tags,
            store_path=item.store_path,
            source_base_dir=item.source_base_dir,
        )

    def _infer_diagram_type(self, specs: list[str], base_dir: Path) -> str:
        for spec in specs:
            spec_path = self._resolve_spec_path(spec, base_dir)
            if not spec_path:
                continue
            try:
                data = yaml.safe_load(spec_path.read_text(encoding="utf-8")) or {}
            except Exception:
                continue
            diagram_type = data.get("type")
            if diagram_type:
                return str(diagram_type)
        return ""

    def _resolve_spec_path(self, spec: str, base_dir: Path) -> Path | None:
        candidates: list[Path] = []
        spec_path = Path(spec)
        if spec_path.suffix:
            candidates.append(base_dir / spec_path)
        else:
            for root in [base_dir, *base_dir.parents[:4]]:
                candidates.append(root / f"{spec}.yml")
                candidates.append(root / f"{spec}.yaml")
        for candidate in candidates:
            if candidate.exists():
                return candidate.resolve()
        return None


def load_catalog(config_path: Path) -> CatalogConfig:
    return CatalogLoader().load(config_path)


def render_filter_bar(items: list[CatalogItem]) -> str:
    types = sorted({item.diagram_type for item in items if item.diagram_type})
    projects = sorted({item.project for item in items if item.project})
    categories = sorted({item.category for item in items if item.category})
    tags = sorted({tag for item in items for tag in item.tags if tag})

    def options(values: list[str], label: str) -> str:
        opts = ['<option value="">Todos</option>']
        for value in values:
            esc = html.escape(value)
            opts.append(f'<option value="{esc}">{esc}</option>')
        return f'<label>{label}<select data-filter="{_slug(label)}">{"".join(opts)}</select></label>'

    tag_buttons = "".join(
        f'<button type="button" class="tag-chip" data-tag="{html.escape(tag)}">{html.escape(tag)}</button>'
        for tag in tags
    )

    return (
        '<div class="catalog-toolbar">'
        '<div class="catalog-toolbar-row">'
        f'{options(types, "Tipo")}'
        f'{options(projects, "Proyecto")}'
        f'{options(categories, "Categoría")}'
        '<label>Búsqueda<input type="search" id="catalog-search" placeholder="Título, tag o descripción"></label>'
        '</div>'
        f'<div class="catalog-tags">{tag_buttons}</div>'
        '</div>'
    )


def render_sections(items: list[CatalogItem], base_dir: Path | None = None) -> str:
    categories: dict[str, list[CatalogItem]] = {}
    for item in items:
        categories.setdefault(item.category or "Otras Vistas", []).append(item)

    blocks: list[str] = []
    for category, cat_items in categories.items():
        sections: list[str] = []
        for item in cat_items:
            content = _read_item_source(item)
            attrs = []
            for spec in item.specs:
                attrs.append(f'data-spec="{html.escape(spec)}"')
            if item.puml:
                attrs.append(f'data-puml="{html.escape(item.puml)}"')
            attrs.append(f'data-type="{html.escape(item.diagram_type)}"')
            attrs.append(f'data-project="{html.escape(item.project)}"')
            attrs.append(f'data-category="{html.escape(item.category)}"')
            attrs.append(f'data-tags="{html.escape(" ".join(item.tags))}"')
            attrs.append('class="catalog-item"')

            badges = []
            if item.diagram_type:
                badges.append(f'<span class="meta-badge">{html.escape(item.diagram_type)}</span>')
            if item.project:
                badges.append(f'<span class="meta-badge">{html.escape(item.project)}</span>')
            for tag in item.tags:
                badges.append(f'<span class="meta-badge subtle">{html.escape(tag)}</span>')
            badges_html = f'<div class="section-meta">{"".join(badges)}</div>' if badges else ""

            notes_html = ""
            if item.notes:
                items_html = "".join(f"<li>{html.escape(note)}</li>" for note in item.notes)
                notes_html = f'\n  <div class="gap-notes"><strong>Gaps de implementación</strong><ul>{items_html}</ul></div>'

            sections.append(
                f'<section id="{html.escape(item.id)}" {" ".join(attrs)}>'
                f'\n  <div class="lbl">{html.escape(item.lbl)}</div>'
                f'\n  <h2>{html.escape(item.title)}</h2>'
                f'\n  <p class="desc">{html.escape(item.desc)}</p>'
                f'\n  {badges_html}'
                f'\n{content}{notes_html}\n</section>'
            )

        blocks.append(
            f'<div class="category-block" data-category-block="{html.escape(category)}">'
            f'<div class="macro-separator"><h2>— {html.escape(category)} —</h2></div>'
            f'{"".join(sections)}'
            '</div>'
        )
    return "\n".join(blocks)


def render_nav(items: list[CatalogItem]) -> str:
    categories: dict[str, list[CatalogItem]] = {}
    for item in items:
        categories.setdefault(item.category or "Otras Vistas", []).append(item)

    parts: list[str] = []
    for category, cat_items in categories.items():
        links = "".join(
            f'<a href="#{html.escape(item.id)}">{html.escape(item.nav or item.lbl or item.id)}</a>'
            for item in cat_items
        )
        parts.append(f'<div class="nav-category"><span>{html.escape(category)}</span>{links}</div>')
    return "\n".join(parts)


def render_catalog_metadata(catalog: CatalogConfig, items: list[CatalogItem]) -> str:
    payload = {
        "title": catalog.title,
        "brand_name": catalog.brand_name,
        "project_name": catalog.project_name,
        "item_count": len(items),
    }
    return json.dumps(payload)


def _read_item_source(item: CatalogItem) -> str:
    if not item.src:
        return '  <div class="board"><div style="color:#94a3b8">Sin fuente renderizada configurada.</div></div>'
    src = Path(item.source_base_dir) / item.src
    content = src.read_text(encoding="utf-8").strip()
    if str(item.src).endswith(".svg"):
        return f'  <div class="board puml-board">\n{content}\n  </div>'
    if str(item.src).endswith(".html"):
        is_markup = content.lstrip().startswith("<div") or "<style>" in content
        indent = "" if is_markup else "    "
        style = "" if is_markup else ' style="font-family:\'JetBrains Mono\',monospace; font-size:12px; white-space:pre-wrap; color:var(--bone-dim);"'
        indented = "\n".join(indent + line for line in content.splitlines())
        return f'  <div class="board"{style}>\n{indented}\n  </div>'
    indented = "\n".join("      " + line for line in content.splitlines())
    return f'  <div class="board">\n    <div class="mermaid">\n{indented}\n    </div>\n  </div>'
