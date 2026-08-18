from pathlib import Path
import yaml

import json
import re

from spec2viz.orchestrator import (
    load_catalog,
    render_catalog_metadata,
    render_filter_bar,
    render_nav,
    render_sections,
)


def parse_atoms(atoms_dir: Path) -> str:
    if not atoms_dir or not atoms_dir.exists():
        return "{}"

    atoms_db = {}
    for md_file in atoms_dir.glob("*.md"):
        content = md_file.read_text(encoding="utf-8")
        parts = re.split(r'^---\s*$', content, maxsplit=2, flags=re.MULTILINE)
        if len(parts) >= 3:
            try:
                fm = yaml.safe_load(parts[1])
                body = parts[2].strip()
                title = fm.get("title")
                question = fm.get("five_wh_one_plus")
                if title and question:
                    title_norm = title.strip().lower()
                    if title_norm not in atoms_db:
                        atoms_db[title_norm] = {"title": title.strip(), "atoms": {}}
                    atoms_db[title_norm]["atoms"][question.strip().lower()] = {
                        "id": fm.get("id", md_file.stem),
                        "body": body
                    }
            except Exception as e:
                print(f"Failed to parse atom {md_file}: {e}")
    return json.dumps(atoms_db)


def render_deskops(config_path: Path, base_dir: Path | None = None, atoms_dir: Path | None = None) -> str:
    catalog = load_catalog(config_path)
    if base_dir is None:
        base_dir = config_path.parent

    tpl_path = base_dir / catalog.template
    tpl = tpl_path.read_text(encoding="utf-8")

    nav = render_nav(catalog.items)
    filters = render_filter_bar(catalog.items)
    sections = render_sections(catalog.items, base_dir)

    html = tpl.replace("{{NAV}}", nav)
    html = html.replace("{{FILTERS}}", filters)
    html = html.replace("{{SECTIONS}}", sections)
    html = html.replace("{{PROJECT_NAME}}", catalog.project_name)
    html = html.replace("{{BRAND_NAME}}", catalog.brand_name)
    html = html.replace("{{CATALOG_TITLE}}", catalog.title)
    html = html.replace("{{CATALOG_METADATA}}", render_catalog_metadata(catalog, catalog.items))

    if "{{FILTERS}}" not in tpl and "{{SECTIONS}}" in tpl:
        html = html.replace(sections, filters + sections, 1)

    atoms_json = parse_atoms(atoms_dir) if atoms_dir else "{}"
    if "{{ATOMS_DB}}" in html:
        html = html.replace("{{ATOMS_DB}}", atoms_json)
    else:
        injection = (
            f"\n<script>window.ATOMS_DB = {atoms_json}; "
            f"window.SPEC2VIZ_CATALOG = {render_catalog_metadata(catalog, catalog.items)};</script>\n</body>"
        )
        html = html.replace("</body>", injection)

    if "window.SPEC2VIZ_CATALOG" not in html:
        html = html.replace(
            "</body>",
            f"\n<script>window.SPEC2VIZ_CATALOG = {render_catalog_metadata(catalog, catalog.items)};</script>\n</body>",
        )

    return html


def build_deskops(config_path: Path, out_path: Path, base_dir: Path | None = None, atoms_dir: Path | None = None):
    html = render_deskops(config_path, base_dir, atoms_dir)
    out_path.write_text(html, encoding="utf-8")
