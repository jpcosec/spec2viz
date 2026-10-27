"""Self-contained HTML viewer for BPMN XML: vendored bpmn-js, legend, metadata and side panel."""

from __future__ import annotations

import html
import json
import re
import xml.etree.ElementTree as ET
from pathlib import Path

from spec2viz.exceptions import RenderError
from spec2viz.renderers.bpmn_palette import (
    DEFAULT_LEGEND_LABELS,
    GATEWAY_TONE,
    TONE_PALETTE,
)

BPMN_NS = "http://www.omg.org/spec/BPMN/20100524/MODEL"
COLOR_NS = "http://www.omg.org/spec/BPMN/non-normative/color/1.0"
VENDOR_DIR = Path(__file__).resolve().parent.parent / "templates" / "vendor" / "bpmn-js"
NODE_TAGS = {"startEvent", "endEvent", "task", "exclusiveGateway", "subProcess"}


def _vendor(name: str) -> str:
    path = VENDOR_DIR / name
    if not path.exists():
        raise RenderError(f"Vendored bpmn-js asset missing: {path}")
    return path.read_text(encoding="utf-8")


def _script_safe(text: str) -> str:
    """Text that can sit inside an inline <script> or <style> element."""
    return re.sub(r"</(script|style)", r"<\\/\1", text, flags=re.IGNORECASE)


def _json_for_script(value) -> str:
    return (json.dumps(value, ensure_ascii=False)
            .replace("<", "\\u003c").replace(">", "\\u003e").replace("&", "\\u0026"))


def _local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def element_info(xml: str) -> dict[str, dict]:
    """label/detail/branches indexed by BPMN element id, read from the generated XML."""
    try:
        root = ET.fromstring(xml.encode("utf-8"))
    except ET.ParseError:
        return {}
    elements: dict[str, ET.Element] = {}
    for el in root.iter():
        tag = _local(el.tag)
        if tag in NODE_TAGS and el.get("id"):
            elements[el.get("id")] = el
    name = {eid: (el.get("name") or eid) for eid, el in elements.items()}
    flows = [el for el in root.iter() if _local(el.tag) == "sequenceFlow"]
    info: dict[str, dict] = {}
    for eid, el in elements.items():
        docs = [d.text for d in el if _local(d.tag) == "documentation" and d.text]
        branches = [
            {
                "label": f.get("name") or "",
                "target": name.get(f.get("targetRef"), f.get("targetRef") or ""),
            }
            for f in flows
            if f.get("sourceRef") == eid
        ]
        info[eid] = {
            "label": el.get("name") or eid,
            "detail": docs[-1] if docs else None,
            "branches": branches,
            "subprocess": _local(el.tag) == "subProcess",
        }
    return info


def _used_legend_keys(xml: str) -> list[str]:
    """Legend entries that the diagram really uses, in palette order (no start/end events)."""
    keys: set[str] = set()
    try:
        root = ET.fromstring(xml)
    except ET.ParseError:
        return [*TONE_PALETTE, "gateway"]
    by_background = {background: tone for tone, (background, _) in TONE_PALETTE.items()}
    for el in root.iter():
        if not _local(el.tag) == "BPMNShape":
            continue
        element_id = el.get("bpmnElement") or ""
        if element_id.startswith(("StartEvent_", "EndEvent_")):
            continue
        background = el.get(f"{{{COLOR_NS}}}background-color")
        if background == GATEWAY_TONE[0]:
            keys.add("gateway")
        elif background in by_background:
            keys.add(by_background[background])
    order = [*TONE_PALETTE, "gateway"]
    return [key for key in order if key in keys]


def _legend_html(xml: str, metadata: dict | None = None) -> str:
    custom = metadata.get("legend") if isinstance(metadata, dict) else None
    custom = custom if isinstance(custom, dict) else {}
    items = []
    for key in _used_legend_keys(xml):
        if key in TONE_PALETTE:
            background, border = TONE_PALETTE[key]
        else:
            background, border = GATEWAY_TONE
        label = custom.get(key) if isinstance(custom.get(key), str) else DEFAULT_LEGEND_LABELS[key]
        items.append(
            f'    <span class="item"><i class="swatch" style="background:{background};border-color:{border}"></i>'
            f"{html.escape(label)}</span>"
        )
    return ('  <div class="legend" aria-label="Leyenda de colores">\n'
            '    <span class="title">Colores:</span>\n' + "\n".join(items) + "\n  </div>")


def _meta_html(metadata: dict | None) -> str:
    """Description and open questions, collapsed into a <details> so they do not take the screen."""
    if not isinstance(metadata, dict):
        return ""
    desc = metadata.get("description")
    questions = metadata.get("preguntas_abiertas")
    if isinstance(questions, str):
        questions = [questions]
    body: list[str] = []
    if desc:
        body.append(f'      <p class="description">{html.escape(str(desc).strip())}</p>')
    if questions:
        items = "\n".join(f"        <li>{html.escape(str(q))}</li>" for q in questions)
        body.append('      <h2>Preguntas abiertas</h2>\n      <ul class="preguntas-abiertas">\n'
                    + items + "\n      </ul>")
    if not body:
        return ""
    return ('    <details class="meta">\n'
            '      <summary>Descripción y preguntas abiertas</summary>\n'
            '      <div class="meta-body">\n' + "\n".join(body) + "\n      </div>\n"
            "    </details>")


HTML_TEMPLATE = """<!DOCTYPE html>
<html lang="es">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>@@TITLE@@</title>
<style>
@@DIAGRAM_CSS@@
</style>
<style>
@@BPMN_CSS@@
</style>
<style>
  html, body { margin: 0; height: 100%; font-family: system-ui, -apple-system, "Segoe UI", Arial, sans-serif; color: #1f2328; background: #fff; }
  body { height: 100vh; display: flex; flex-direction: column; overflow: hidden; }
  header { flex: 0 0 auto; padding: 6px 14px 4px; border-bottom: 1px solid #d0d7de; background: #fff; position: relative; z-index: 5; }
  .row { display: flex; align-items: center; gap: 12px; justify-content: space-between; }
  .row.second { justify-content: flex-start; gap: 16px; margin-top: 2px; }
  h1 { font-size: 16px; margin: 0; white-space: nowrap; overflow: hidden; text-overflow: ellipsis; }
  .toolbar { display: flex; gap: 6px; flex: 0 0 auto; }
  .toolbar button { font: inherit; font-size: 12px; padding: 2px 9px; border: 1px solid #d0d7de; background: #f6f8fa; border-radius: 5px; cursor: pointer; }
  details.meta { flex: 0 0 auto; font-size: 12px; line-height: 1.4; }
  details.meta summary { cursor: pointer; padding: 2px 0; white-space: nowrap; }
  details.meta .meta-body { position: absolute; left: 0; right: 0; top: 100%; max-height: 60vh; overflow: auto; padding: 10px 14px 12px; background: #fff; border-bottom: 1px solid #d0d7de; box-shadow: 0 6px 16px rgba(0, 0, 0, .12); z-index: 20; }
  .meta-body p { margin: 3px 0; font-size: 13px; line-height: 1.45; max-width: 120ch; }
  .meta-body h2 { font-size: 13px; margin: 8px 0 3px; }
  .meta-body ul { margin: 0; padding-left: 20px; font-size: 13px; line-height: 1.45; max-width: 120ch; }
  .legend { flex: 1 1 auto; display: flex; flex-wrap: nowrap; gap: 4px 14px; overflow-x: auto; white-space: nowrap; font-size: 12px; align-items: center; }
  .legend .item { flex: 0 0 auto; display: inline-flex; align-items: center; gap: 5px; }
  .legend .swatch { width: 16px; height: 13px; border-radius: 3px; border: 2px solid #555; box-sizing: border-box; }
  .legend .title { flex: 0 0 auto; font-weight: 600; }
  main { flex: 1 1 auto; min-height: 0; display: flex; }
  #canvas { flex: 1 1 auto; min-height: 0; position: relative; }
  #panel { flex: 0 0 340px; max-width: 340px; border-left: 1px solid #d0d7de; overflow: auto; padding: 12px 14px; font-size: 13px; line-height: 1.45; background: #fbfcfd; box-sizing: border-box; }
  body.panel-collapsed #panel { display: none; }
  #panel h2 { font-size: 14px; margin: 0 0 8px; }
  #panel h3 { font-size: 12px; text-transform: uppercase; letter-spacing: .04em; color: #57606a; margin: 14px 0 5px; }
  #panel p { margin: 0 0 8px; white-space: pre-wrap; }
  #panel ul { margin: 0; padding-left: 18px; }
  #panel li { margin: 3px 0; }
  #panel .muted { color: #57606a; }
  #panel .branch-label { font-weight: 600; }
  #error { color: #b42318; font-size: 12px; white-space: pre-wrap; position: absolute; right: 14px; top: 6px; }
</style>
</head>
<body>
<header>
  <div class="row">
    <h1>@@TITLE@@</h1>
    <div class="toolbar">
      <button type="button" id="fit">Fit</button>
      <button type="button" id="zoom-in">Zoom +</button>
      <button type="button" id="zoom-out">Zoom &minus;</button>
      <button type="button" id="toggle-panel">Detalle</button>
    </div>
  </div>
  <div class="row second">
@@META@@
@@LEGEND@@
  </div>
  <div id="error"></div>
</header>
<main>
  <div id="canvas"></div>
  <aside id="panel" aria-live="polite">
    <h2>Detalle</h2>
    <p class="muted" id="panel-body">Haz clic en una tarea, gateway o subproceso.</p>
  </aside>
</main>
<script>
@@VIEWER_JS@@
</script>
<script>
(function () {
  var xml = @@XML_JSON@@;
  var info = @@INFO_JSON@@;
  var viewer = new BpmnJS({
    container: '#canvas',
    textRenderer: {
      defaultStyle: { fontFamily: 'Arial, sans-serif', fontSize: @@FONT@@, lineHeight: 1.2 },
      externalStyle: { fontFamily: 'Arial, sans-serif', fontSize: @@FONT@@, lineHeight: 1.2 }
    }
  });
  window.bpmnViewer = viewer;
  var MIN_ZOOM = 0.6;  // the initial view never shows the diagram smaller than this
  function fitViewport() {
    viewer.get('canvas').zoom('fit-viewport', 'auto');
  }
  function initialView() {
    fitViewport();
    var canvas = viewer.get('canvas');
    if (canvas.zoom() < MIN_ZOOM) {
      // too big to fit legibly: zoom in and start at the diagram's left edge,
      // with the start event in view, instead of in the middle of the flow
      canvas.zoom(MIN_ZOOM);
      var start = viewer.get('elementRegistry').filter(function (el) {
        return el.type === 'bpmn:StartEvent';
      })[0];
      if (start) {
        var box = canvas.getAbsoluteBBox(start);
        var outer = canvas.viewbox().outer;
        canvas.scroll({ dx: 40 - box.x, dy: Math.round(outer.height * 0.4) - box.y });
      }
    }
  }
  function el(tag, text, cls) {
    var node = document.createElement(tag);
    if (text !== undefined && text !== null) { node.textContent = text; }
    if (cls) { node.className = cls; }
    return node;
  }
  function showInfo(id) {
    var data = info[id];
    var body = document.getElementById('panel-body');
    body.className = '';
    body.textContent = '';
    if (!data) {
      body.className = 'muted';
      body.textContent = 'Sin informacion para este elemento.';
      return;
    }
    body.appendChild(el('p', data.label, 'element-label'));
    if (data.detail) {
      body.appendChild(el('h3', data.subprocess ? 'Detalle del grupo' : 'Detalle'));
      body.appendChild(el('p', data.detail));
    }
    body.appendChild(el('h3', 'Ramas salientes'));
    if (!data.branches.length) {
      body.appendChild(el('p', 'Sin ramas.', 'muted'));
    } else {
      var ul = el('ul');
      data.branches.forEach(function (branch) {
        var li = el('li');
        if (branch.label) { li.appendChild(el('span', branch.label, 'branch-label')); li.appendChild(document.createTextNode(' → ')); }
        li.appendChild(document.createTextNode(branch.target));
        ul.appendChild(li);
      });
      body.appendChild(ul);
    }
  }
  viewer.on('element.click', function (evt) { showInfo(evt.element.id); });
  viewer.on('root.set', function () { try { initialView(); } catch (e) {} });
  viewer.importXML(xml).then(function (result) {
    if (result.warnings && result.warnings.length) { console.warn('bpmn-js import warnings', result.warnings); }
    initialView();
    window.bpmnReady = true;
  }).catch(function (err) {
    document.getElementById('error').textContent = 'Could not render the BPMN diagram: ' + err.message;
    console.error(err);
  });
  document.getElementById('fit').addEventListener('click', fitViewport);
  document.getElementById('zoom-in').addEventListener('click', function () { viewer.get('zoomScroll').stepZoom(1); });
  document.getElementById('zoom-out').addEventListener('click', function () { viewer.get('zoomScroll').stepZoom(-1); });
  document.getElementById('toggle-panel').addEventListener('click', function () {
    document.body.classList.toggle('panel-collapsed');
    setTimeout(function () { viewer.get('canvas').resized(); }, 0);
  });
  window.addEventListener('resize', function () { viewer.get('canvas').resized(); });
})();
</script>
</body>
</html>
"""


def render_bpmn_html(xml: str, title: str, metadata: dict | None = None) -> str:
    """A self-contained page that renders `xml` with the vendored bpmn-js NavigatedViewer."""
    # JSON with `<`, `>` and `&` escaped can never close the script element it lives in
    values = {
        "@@DIAGRAM_CSS@@": _script_safe(_vendor("diagram-js.css")),
        "@@BPMN_CSS@@": _script_safe(_vendor("bpmn-js.css")),
        "@@VIEWER_JS@@": _script_safe(_vendor("bpmn-navigated-viewer.production.min.js")),
        "@@XML_JSON@@": _json_for_script(xml),
        "@@INFO_JSON@@": _json_for_script(element_info(xml)),
        "@@META@@": _meta_html(metadata),
        "@@LEGEND@@": _legend_html(xml, metadata),
        "@@FONT@@": "14",
        "@@TITLE@@": html.escape(title),
    }
    return re.sub("|".join(re.escape(k) for k in values), lambda m: values[m.group(0)], HTML_TEMPLATE)


def provenance_comment(text: str) -> str:
    """`text` as an XML comment (`--` is not allowed inside one)."""
    return "<!-- " + text.replace("--", "- -") + " -->\n"


def with_xml_provenance(xml: str, header: str) -> str:
    """The XML with a provenance comment right after its declaration."""
    decl, sep, rest = xml.partition("\n")
    if not decl.startswith("<?xml"):
        return provenance_comment(header) + xml
    return decl + sep + provenance_comment(header) + rest


__all__ = ["render_bpmn_html", "with_xml_provenance", "element_info", "HTML_TEMPLATE"]
