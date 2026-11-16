"""The self-contained HTML catalog of a registry (migrated from spec2viz's `deskops.render_deskops`
and `build_deskops`): the template (a local override next to the config, or the packaged
`templates/default.html` of IR12) filled with the navigation, the filter bar, the sections and the
page metadata, and the atoms of each view right before `</body>`.

With an `AnnotationsTarget` the page also reads and saves its annotations with `sldb serve`
(`annotations.py`); without one it is what spec2viz built."""

from __future__ import annotations

import sys
from importlib import resources
from pathlib import Path

from specir.visual.catalog.annotations import AnnotationsTarget, annotations_script
from specir.visual.catalog.atoms import atoms_script, catalog_atoms
from specir.visual.catalog.loader import CatalogConfig, load_catalog
from specir.visual.catalog.sections import render_catalog_metadata, render_filter_bar, render_nav, render_sections


def catalog_template(catalog: CatalogConfig, base_dir: Path) -> str:
    """The local template the config names, if it exists; otherwise the packaged one."""
    local = base_dir / catalog.template if catalog.template else None
    if local and local.exists():
        print(f"specir: using local catalog template override: {local}", file=sys.stderr)
        return local.read_text(encoding="utf-8")
    return resources.files("specir.visual").joinpath("templates", "default.html").read_text(encoding="utf-8")


def _fill(template: str, catalog: CatalogConfig, base_dir: Path) -> str:
    nav, filters, sections = render_nav(catalog.items), render_filter_bar(catalog.items), render_sections(catalog.items, base_dir)
    values = {
        "{{NAV}}": nav, "{{FILTERS}}": filters, "{{SECTIONS}}": sections, "{{PROJECT_NAME}}": catalog.project_name,
        "{{BRAND_NAME}}": catalog.brand_name, "{{BRAND_SUBTITLE}}": catalog.brand_subtitle, "{{CATALOG_TITLE}}": catalog.title,
        "{{CATALOG_METADATA}}": render_catalog_metadata(catalog, catalog.items),
    }
    page = template
    for marker, value in values.items():
        page = page.replace(marker, value)
    if "{{FILTERS}}" not in template and "{{SECTIONS}}" in template:
        page = page.replace(sections, filters + sections, 1)
    return page


def render_catalog(
    config_path: Path,
    base_dir: Path | None = None,
    atoms_dir: Path | None = None,
    atoms_tags: list[str] | None = None,
    strict_atoms: bool = False,
    annotations: AnnotationsTarget | None = None,
) -> str:
    """The catalog's HTML. `strict_atoms` turns an unknown `atoms:`/`refs:` id into sldb's
    `UnknownAtomError`; otherwise it is a warning on stderr and in the page."""
    catalog = load_catalog(config_path)
    base_dir = base_dir if base_dir is not None else config_path.parent
    page = _fill(catalog_template(catalog, base_dir), catalog, base_dir)
    atoms = catalog_atoms(catalog.items, atoms_dir, atoms_tags, strict_atoms)
    page = page.replace("{{ATOMS_DB}}", "{}")
    tail = atoms_script(atoms, render_catalog_metadata(catalog, catalog.items))
    if annotations is not None:
        tail = annotations_script(annotations, catalog.title, catalog.project_name) + tail
    return page.replace("</body>", tail)


def build_catalog(config_path: Path, out_path: Path, base_dir: Path | None = None, atoms_dir: Path | None = None,
                  atoms_tags: list[str] | None = None, strict_atoms: bool = False, annotations: AnnotationsTarget | None = None) -> Path:
    """Writes the catalog's HTML to `out_path`."""
    out_path.write_text(render_catalog(config_path, base_dir, atoms_dir, atoms_tags, strict_atoms, annotations), encoding="utf-8")
    return out_path


__all__ = ["build_catalog", "catalog_template", "render_catalog"]
