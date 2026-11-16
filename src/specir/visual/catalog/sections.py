"""The HTML of the catalog's views: navigation, filter bar, sections by category and the board of
each view (migrated from spec2viz's `orchestrator`: `render_filter_bar`, `render_sections`,
`render_nav`, `render_catalog_metadata`, `resolve_item_path`, `_read_item_source`,
`_resolved_item_board`).

A view with specs whose resolved view is a graph is drawn from it (`views.resolved_board`);
otherwise the catalog embeds its rendered source (`src`): a `.mmd` linted as mermaid, an `.svg`, an
HTML snippet or `#fragment`, a Vega `.json` for vega-embed, or any other text as it is."""

from __future__ import annotations

import html
import json
from pathlib import Path

from sldb.api.notations.catalog_paths import resolve_catalog_path

from specir.visual.catalog.fragments import extract_html_fragment
from specir.visual.catalog.loader import DEFAULT_CATEGORY, CatalogConfig, CatalogItem, resolve_spec_path
from specir.visual.catalog.views import resolved_board
from specir.visual.lint_mermaid import assert_mermaid_ok
from specir.visual.notation_style import UnknownNotationError, UnknownReferenceError


def _slug(value: str) -> str:
    return "-".join(value.strip().lower().split()) if value else ""


def by_category(items: list[CatalogItem]) -> dict[str, list[CatalogItem]]:
    categories: dict[str, list[CatalogItem]] = {}
    for item in items:
        categories.setdefault(item.category or DEFAULT_CATEGORY, []).append(item)
    return categories


def _options(values: list[str], label: str) -> str:
    opts = ['<option value="">Todos</option>'] + [f'<option value="{html.escape(v)}">{html.escape(v)}</option>' for v in values]
    return f'<label>{label}<select data-filter="{_slug(label)}">{"".join(opts)}</select></label>'


def render_filter_bar(items: list[CatalogItem]) -> str:
    types = sorted({item.diagram_type for item in items if item.diagram_type})
    projects = sorted({item.project for item in items if item.project})
    categories = sorted({item.category for item in items if item.category})
    tags = sorted({tag for item in items for tag in item.tags if tag})
    tag_buttons = "".join(f'<button type="button" class="tag-chip" data-tag="{html.escape(t)}">{html.escape(t)}</button>' for t in tags)
    return (
        '<div class="catalog-toolbar">'
        '<div class="catalog-toolbar-row">'
        f'{_options(types, "Tipo")}'
        f'{_options(projects, "Proyecto")}'
        f'{_options(categories, "Categoría")}'
        '<label>Búsqueda<input type="search" id="catalog-search" placeholder="Título, tag o descripción"></label>'
        '</div>'
        f'<div class="catalog-tags">{tag_buttons}</div>'
        '</div>'
    )


def _attrs(item: CatalogItem) -> list[str]:
    attrs = [f'data-spec="{html.escape(spec)}"' for spec in item.specs]
    if item.puml:
        attrs.append(f'data-puml="{html.escape(item.puml)}"')
    attrs += [f'data-type="{html.escape(item.diagram_type)}"', f'data-project="{html.escape(item.project)}"',
              f'data-category="{html.escape(item.category)}"', f'data-tags="{html.escape(" ".join(item.tags))}"',
              f'data-view-id="{html.escape(item.id)}"', 'class="catalog-item"']
    return attrs


def _badges(item: CatalogItem) -> str:
    badges = [f'<span class="meta-badge">{html.escape(v)}</span>' for v in (item.diagram_type, item.project) if v]
    badges += [f'<span class="meta-badge subtle">{html.escape(tag)}</span>' for tag in item.tags]
    return f'<div class="section-meta">{"".join(badges)}</div>' if badges else ""


def _notes(item: CatalogItem) -> str:
    if not item.notes:
        return ""
    items_html = "".join(f"<li>{html.escape(note)}</li>" for note in item.notes)
    return f'\n  <div class="gap-notes"><strong>Gaps de implementación</strong><ul>{items_html}</ul></div>'


def render_section(item: CatalogItem) -> str:
    content = resolved_item_board(item) or read_item_source(item)
    return (
        f'<section id="{html.escape(item.anchor_id)}" {" ".join(_attrs(item))}>'
        f'\n  <div class="lbl">{html.escape(item.lbl)}</div>'
        f'\n  <h2>{html.escape(item.title)}</h2>'
        f'\n  <p class="desc">{html.escape(item.desc)}</p>'
        f'\n  {_badges(item)}'
        f'\n{content}{_notes(item)}\n</section>'
    )


def render_sections(items: list[CatalogItem], base_dir: Path | None = None) -> str:
    blocks = []
    for category, cat_items in by_category(items).items():
        sections = "".join(render_section(item) for item in cat_items)
        blocks.append(
            f'<div class="category-block" data-category-block="{html.escape(category)}">'
            f'<div class="macro-separator"><h2>— {html.escape(category)} —</h2></div>'
            f'{sections}</div>'
        )
    return "\n".join(blocks)


def render_nav(items: list[CatalogItem]) -> str:
    parts = []
    for category, cat_items in by_category(items).items():
        links = "".join(f'<a href="#{html.escape(item.anchor_id)}">{html.escape(item.nav or item.lbl or item.id)}</a>' for item in cat_items)
        parts.append(f'<div class="nav-category"><span>{html.escape(category)}</span>{links}</div>')
    return "\n".join(parts)


def render_catalog_metadata(catalog: CatalogConfig, items: list[CatalogItem]) -> str:
    return json.dumps({
        "title": catalog.title, "brand_name": catalog.brand_name, "brand_subtitle": catalog.brand_subtitle,
        "project_name": catalog.project_name, "item_count": len(items),
    })


def split_src_fragment(src: str) -> tuple[str, str | None]:
    if ".html#" in src:
        path, fragment = src.split("#", 1)
        return path, fragment
    return src, None


def resolve_item_path(value: str, base_dir: Path, field: str) -> Path:
    """A view's `src` by the catalog rule; when it exists nowhere, the path next to the config (the
    missing-file error is the usual one). Ambiguous -> `AmbiguousPathError`."""
    try:
        return resolve_catalog_path(value, base_dir, field)
    except UnknownReferenceError:
        return Path(base_dir) / value


def resolved_item_board(item: CatalogItem) -> str | None:
    """The board of a view from its resolved view, with the view's notation; None when the view has
    no specs that resolve or its layout is not a graph (then its `src` is used)."""
    if not item.specs:
        return None
    base = Path(item.source_base_dir)
    spec_paths = [p for p in (resolve_spec_path(spec, base) for spec in item.specs) if p is not None]
    if not spec_paths:
        return None
    notation: str | Path | None = None
    if item.notation:
        text = str(item.notation)
        looks_like_path = "/" in text or text.endswith((".yml", ".yaml"))
        notation = resolve_catalog_path(text, base, "notation", UnknownNotationError) if looks_like_path else text
    return resolved_board(spec_paths, notation, base)


def _markup_board(content: str) -> str:
    is_markup = content.lstrip().startswith("<div") or "<style>" in content
    indent = "" if is_markup else "    "
    style = "" if is_markup else ' style="font-family:\'JetBrains Mono\',monospace; font-size:12px; white-space:pre-wrap; color:var(--bone-dim);"'
    indented = "\n".join(indent + line for line in content.splitlines())
    return f'  <div class="board"{style}>\n{indented}\n  </div>'


def _vega_board(content: str, src_value: str) -> str:
    try:
        json.loads(content)
    except ValueError as exc:
        raise ValueError(f"{src_value}: not valid JSON for a Vega board ({exc})") from exc
    escaped = content.replace("</", "<\\/")
    return f'  <div class="board vega-board">\n    <script type="application/json" class="vega-spec">\n{escaped}\n    </script>\n  </div>'


def _mermaid_board(content: str, src_value: str) -> str:
    # lint the raw mermaid before it is embedded: a broken .mmd fails the build, not the browser
    assert_mermaid_ok(content, source=str(src_value), check_html=False)
    indented = "\n".join("      " + line for line in html.escape(content).splitlines())
    return f'  <div class="board">\n    <pre class="mermaid">\n{indented}\n    </pre>\n  </div>'


def read_item_source(item: CatalogItem) -> str:
    if not item.src:
        return '  <div class="board"><div style="color:#94a3b8">Sin fuente renderizada configurada.</div></div>'
    src_value, fragment = split_src_fragment(item.src)
    content = resolve_item_path(src_value, Path(item.source_base_dir), "src").read_text(encoding="utf-8").strip()
    if fragment:
        return f'  {extract_html_fragment(content, fragment)}'
    name = str(src_value)
    if name.endswith(".svg"):
        return f'  <div class="board puml-board">\n{content}\n  </div>'
    if name.endswith(".html"):
        return _markup_board(content)
    if name.endswith(".json"):
        return _vega_board(content, src_value)
    if not name.endswith((".mmd", ".mermaid")):
        # any other text projection (.puml, .d2, .txt) is shown as it is; only mermaid is drawn and linted
        return f'  <div class="board"><pre class="source-board">{html.escape(content)}</pre></div>'
    return _mermaid_board(content, src_value)


__all__ = [
    "read_item_source", "render_catalog_metadata", "render_filter_bar", "render_nav", "render_section", "render_sections",
    "resolve_item_path", "resolved_item_board",
]
