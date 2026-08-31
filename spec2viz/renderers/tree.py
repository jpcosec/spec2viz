"""Tree renderer: collapsible hierarchical HTML from ComponentIR."""

from __future__ import annotations
import json
from spec2viz.ir import ComponentIR, ComponentNode
from spec2viz.exceptions import RenderError


class TreeRenderer:
    """Renders a ComponentIR as a standalone interactive collapsible tree HTML."""

    def render(self, ir) -> str:
        if not isinstance(ir, ComponentIR):
            raise RenderError(f"TreeRenderer cannot render {type(ir).__name__}")
        return self._build_html(ir)

    def _build_html(self, ir: ComponentIR) -> str:
        tree_data = self._build_tree(ir)
        edge_data = self._build_edge_map(ir)
        node_labels = {n.id: n.label for n in ir.nodes}
        node_kinds = {n.id: n.kind for n in ir.nodes}
        return HTML_TEMPLATE.format(
            title=ir.title,
            tree_json=json.dumps(tree_data, indent=2),
            edges_json=json.dumps(edge_data),
            labels_json=json.dumps(node_labels),
            kinds_json=json.dumps(node_kinds),
        )

    def _build_tree(self, ir: ComponentIR) -> dict:
        """Build a nested tree from flat node IDs using their hierarchy."""
        root = {"name": "sldb", "type": "root", "children": []}
        lookup = {n.id: n for n in ir.nodes}

        for node in ir.nodes:
            parts = node.id.split("_")
            current = root
            path = []
            for i, part in enumerate(parts):
                path.append(part)
                full_id = "_".join(path)
                # Check if this intermediate level has a module node
                existing = self._find_child(current, full_id)
                if existing:
                    current = existing
                else:
                    entry = {
                        "name": full_id,
                        "label": lookup.get(full_id, ComponentNode(id=full_id, label=part, kind="module")).label,
                        "type": lookup.get(full_id, ComponentNode(id=full_id, label=part, kind="module")).kind,
                        "children": [],
                    }
                    current["children"].append(entry)
                    current = entry

        self._deduplicate_leaves(root)
        return root

    def _find_child(self, parent: dict, name: str) -> dict | None:
        for c in parent.get("children", []):
            if c["name"] == name:
                return c
        return None

    def _deduplicate_leaves(self, node: dict) -> None:
        """Remove leaf nodes that are just the parent path repeated (e.g.
        module_cli_commands is both a leaf and a parent)."""
        children = node.get("children", [])
        if not children:
            return
        # If a child has no children and its name == parent name (same depth), skip it
        children[:] = [c for c in children if c.get("children") or c["name"] != node["name"]]
        for c in children:
            self._deduplicate_leaves(c)

    def _build_edge_map(self, ir: ComponentIR) -> dict:
        """Build a dict of node_id -> {imports: [target_ids], imported_by: [source_ids]}."""
        edge_map: dict[str, dict[str, list[str]]] = {}
        for n in ir.nodes:
            edge_map[n.id] = {"imports": [], "imported_by": []}
        for e in ir.edges:
            if e.from_ in edge_map and e.to in edge_map:
                edge_map[e.from_]["imports"].append(e.to)
                edge_map[e.to]["imported_by"].append(e.from_)
        return edge_map


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>{title} — Collapsible Tree</title>
<style>
*{{margin:0;padding:0;box-sizing:border-box}}
body{{font-family:'Segoe UI',system-ui,sans-serif;background:#0a0a0f;color:#f5f0e8;display:flex;height:100vh;overflow:hidden}}
aside{{width:400px;min-width:400px;border-right:1px solid rgba(212,165,116,.2);overflow-y:auto;padding:16px;background:#12121a}}
main{{flex:1;overflow-y:auto;padding:24px}}
.tree-toggle{{cursor:pointer;user-select:none;display:inline-flex;align-items:center;gap:4px}}
.tree-toggle:hover{{color:#d4a574}}
.tree-icon{{display:inline-block;width:16px;text-align:center;color:#d4a574;font-size:12px}}
.node-name{{color:#f5f0e8}}
.node-name:hover{{color:#d4a574}}
.node-kind{{color:rgba(245,240,232,.4);font-size:11px;margin-left:6px}}
ul{{list-style:none;padding-left:16px}}
li{{padding:2px 0}}
li.selected>.tree-toggle>.node-name{{color:#d4a574;font-weight:600}}
.class{{color:#7ec8e3}}
.module{{color:rgba(245,240,232,.7)}}
.external{{color:rgba(245,240,232,.35)}}
.core{{color:#7ec8e3}}
.database{{color:#e3b37e}}
.boundary{{color:rgba(245,240,232,.45)}}
.badge{{font-size:10px;padding:1px 6px;border-radius:8px;margin-left:6px;background:rgba(212,165,116,.15);color:#d4a574}}
#detail-panel{{background:#161621;border:1px solid rgba(212,165,116,.2);border-radius:12px;padding:20px;margin-bottom:16px}}
#detail-panel h3{{font-size:11px;text-transform:uppercase;letter-spacing:.15em;color:#d4a574;margin-bottom:8px}}
#detail-panel p{{margin:4px 0;font-size:13px}}
.dep-list{{display:flex;flex-wrap:wrap;gap:6px;margin-top:8px}}
.dep-tag{{font-size:11px;padding:2px 8px;border-radius:6px;background:rgba(212,165,116,.1);color:rgba(245,240,232,.8);cursor:pointer}}
.dep-tag:hover{{background:rgba(212,165,116,.3);color:#f5f0e8}}
.empty-state{{color:rgba(245,240,232,.4);font-size:13px;font-style:italic}}
.search-box{{width:100%;padding:8px 12px;background:#0a0a0f;border:1px solid rgba(212,165,116,.2);border-radius:8px;color:#f5f0e8;font-size:13px;margin-bottom:12px;outline:none}}
.search-box:focus{{border-color:#d4a574}}
#tree-root{{font-size:13px;line-height:1.6}}
#title-bar{{font-family:'JetBrains Mono',monospace;font-size:10px;letter-spacing:.15em;text-transform:uppercase;color:#d4a574;margin-bottom:16px;padding-bottom:12px;border-bottom:1px solid rgba(212,165,116,.15)}}
.count{{color:rgba(245,240,232,.35);font-size:11px;margin-left:4px}}
</style>
</head>
<body>
<aside>
<div id="title-bar">📁 {title}</div>
<input class="search-box" id="search" placeholder="Filter nodes..." oninput="filterTree(this.value)">
<div id="tree-root"></div>
</aside>
<main>
<div id="detail-panel">
<h3>🔍 Node Detail</h3>
<p class="empty-state">Click a node in the tree to see its dependencies</p>
</div>
<div id="edge-info" style="color:rgba(245,240,232,.4);font-size:12px"></div>
</main>
<script>
const TREE = {tree_json};
const EDGES = {edges_json};
const LABELS = {labels_json};
const KINDS = {kinds_json};

function treeHTML(node, depth) {{
    const hasKids = node.children && node.children.length > 0;
    const label = LABELS[node.name] || node.label || node.name.split('_').pop();
    const kind = KINDS[node.name] || node.type || 'module';
    const kindClass = kind === 'class' ? 'class' : kind === 'module' ? 'module' : kind === 'external' ? 'external' : kind;
    const count = hasKids ? `<span class="count">${{node.children.length}}</span>` : '';
    const cl = kindClass;
    let html = `<li><div class="tree-toggle" onclick="toggle(this)" data-path="${{node.name}}">`;
    if (hasKids) {{
        html += `<span class="tree-icon">▸</span>`;
    }} else {{
        html += `<span class="tree-icon" style="color:transparent">▸</span>`;
    }}
    html += `<span class="node-name ${{cl}}">${{label}}</span>${{count}}<span class="node-kind">${{kind}}</span>`;
    html += `</div>`;
    if (hasKids) {{
        html += `<ul style="display:none">`;
        for (const c of node.children) {{
            html += treeHTML(c, depth + 1);
        }}
        html += `</ul>`;
    }}
    html += `</li>`;
    return html;
}}

function toggle(el) {{
    const ul = el.nextElementSibling;
    const icon = el.querySelector('.tree-icon');
    if (ul && ul.tagName === 'UL') {{
        const showing = ul.style.display !== 'none';
        ul.style.display = showing ? 'none' : 'block';
        icon.textContent = showing ? '▸' : '▾';
    }}
    showDetail(el.dataset.path);
}}

function showDetail(nodeId) {{
    // Remove selected class
    document.querySelectorAll('.selected').forEach(el => el.classList.remove('selected'));
    const toggles = document.querySelectorAll(`[data-path="${{nodeId}}"]`);
    toggles.forEach(t => t.parentElement.classList.add('selected'));

    const panel = document.getElementById('detail-panel');
    const label = LABELS[nodeId] || nodeId.split('_').pop();
    const kind = KINDS[nodeId] || 'module';
    const deps = EDGES[nodeId];
    if (!deps) {{
        panel.innerHTML = `<h3>🔍 ${{label}}</h3><p class="empty-state">No dependency data</p>`;
        return;
    }}
    let html = `<h3>🔍 ${{label}} <span style="font-weight:400;color:rgba(245,240,232,.4)">(${{kind}})</span></h3>`;
    html += `<p><strong>ID:</strong> <code style="color:#d4a574">${{nodeId}}</code></p>`;
    if (deps.imports.length > 0) {{
        html += `<p><strong>Imports:</strong></p><div class="dep-list">`;
        for (const t of deps.imports) {{
            const tl = LABELS[t] || t.split('_').pop();
            html += `<span class="dep-tag" onclick="showDetail('${{t}}')">${{tl}}</span>`;
        }}
        html += `</div>`;
    }} else {{
        html += `<p><strong>Imports:</strong> <span class="empty-state">none</span></p>`;
    }}
    if (deps.imported_by.length > 0) {{
        html += `<p style="margin-top:12px"><strong>Imported by:</strong></p><div class="dep-list">`;
        for (const t of deps.imported_by) {{
            const tl = LABELS[t] || t.split('_').pop();
            html += `<span class="dep-tag" onclick="showDetail('${{t}}')">${{tl}}</span>`;
        }}
        html += `</div>`;
    }} else {{
        html += `<p style="margin-top:12px"><strong>Imported by:</strong> <span class="empty-state">none</span></p>`;
    }}
    panel.innerHTML = html;
}}

function filterTree(query) {{
    const items = document.querySelectorAll('#tree-root li');
    const q = query.toLowerCase();
    items.forEach(li => {{
        const name = li.querySelector('.node-name');
        if (!name) return;
        const matches = !q || name.textContent.toLowerCase().includes(q);
        li.style.display = matches ? '' : 'none';
        if (matches && q) {{
            // auto-expand parents
            let p = li.parentElement;
            while (p && p.id !== 'tree-root') {{
                if (p.tagName === 'UL') {{
                    p.style.display = 'block';
                    const prev = p.previousElementSibling;
                    if (prev) {{
                        const icon = prev.querySelector('.tree-icon');
                        if (icon) icon.textContent = '▾';
                    }}
                }}
                p = p.parentElement;
            }}
        }}
    }});
}}

// Initialize
document.getElementById('tree-root').innerHTML = `<ul>${{treeHTML(TREE, 0)}}</ul>`;
// Auto-expand first level
document.querySelectorAll('#tree-root > ul > li > ul').forEach(ul => {{
    ul.style.display = 'block';
    const icon = ul.previousElementSibling?.querySelector('.tree-icon');
    if (icon) icon.textContent = '▾';
}});
</script>
</body>
</html>"""