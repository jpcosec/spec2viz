from pathlib import Path
import yaml

import json
import re

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
    if base_dir is None:
        base_dir = config_path.parent
    reg = yaml.safe_load(config_path.read_text(encoding="utf-8"))
    
    tpl_path = base_dir / reg["template"]
    tpl = tpl_path.read_text(encoding="utf-8")

    categories = {}
    for v in reg.get("vistas", []):
        cat = v.get("category", "Otras Vistas")
        if cat not in categories:
            categories[cat] = []
        categories[cat].append(v)

    nav = ""
    sections = []
    
    for cat, vistas in categories.items():
        nav += f'<div class="nav-category"><span>{cat}</span>'
        nav += "".join(f'<a href="#{v["id"]}">{v.get("nav", v.get("lbl", v["id"]))}</a>' for v in vistas)
        nav += "</div>\n"
        
        sections.append(f'<div class="macro-separator"><h2>— {cat} —</h2></div>')
        for v in vistas:
            src = v.get("src") or v.get("mmd")
            content = (base_dir / src).read_text(encoding="utf-8").strip() if src else ""
            
            attrs = ""
            specs = v.get("specs") or []
            if specs:
                attrs += " " + " ".join(f'data-spec="{s}"' for s in specs)
            puml = v.get("puml")
            if puml:
                attrs += f' data-puml="{puml}"'
            
            if src and str(src).endswith(".svg"):
                board_content = f"""  <div class="board puml-board">
{content}
  </div>"""
            elif src and str(src).endswith(".html"):
                is_markup = content.lstrip().startswith("<div") or "<style>" in content
                indent = "" if is_markup else "    "
                style = "" if is_markup else " style=\"font-family:'JetBrains Mono',monospace; font-size:12px; white-space:pre-wrap; color:var(--bone-dim);\""
                indented = "\n".join(indent + line for line in content.splitlines())
                board_content = f"""  <div class="board"{style}>
{indented}
  </div>"""
            else:
                indented = "\n".join("      " + line for line in content.splitlines())
                board_content = f"""  <div class="board">
    <div class="mermaid">
{indented}
    </div>
  </div>"""

            notes = v.get("notes") or []
            notes_html = ""
            if notes:
                items = "".join(f"<li>{n}</li>" for n in notes)
                notes_html = f"""\n  <div class="gap-notes"><strong>Gaps de implementación</strong><ul>{items}</ul></div>"""

            sections.append(
                f'''<section id="{v["id"]}"{attrs}>
  <div class="lbl">{v.get("lbl", "")}</div>
  <h2>{v.get("title", v["id"])}</h2>
  <p class="desc">{v.get("desc", "")}</p>
{board_content}{notes_html}
</section>'''
            )

    html = tpl.replace("{{NAV}}", nav).replace("{{SECTIONS}}", "\n".join(sections))
    
    atoms_json = parse_atoms(atoms_dir) if atoms_dir else "{}"
    if "{{ATOMS_DB}}" in html:
        html = html.replace("{{ATOMS_DB}}", atoms_json)
    else:
        # Inject before </body> if template doesn't have the tag
        injection = f"\n<script>window.ATOMS_DB = {atoms_json};</script>\n</body>"
        html = html.replace("</body>", injection)
        
    return html

def build_deskops(config_path: Path, out_path: Path, base_dir: Path | None = None, atoms_dir: Path | None = None):
    html = render_deskops(config_path, base_dir, atoms_dir)
    out_path.write_text(html, encoding="utf-8")
