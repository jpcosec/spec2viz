"""The catalog's annotations are saved with `sldb serve` (IR13b, replaces spec2viz's `catalog serve`).

A real store with `CatalogAnnotationsDoc` registered, a real `sldb serve --cors` on a free port
(under `timeout`, closed at the end of each test) and the page's own code run by node: the
template's `annoReadStore`, `annoWriteStore` and `annoLoad`, taken from the built HTML, and the
script the build embeds (`templates/annotations-sldb.js`). Only the DOM is left out (`annoRender`
draws nothing and `localStorage` is a map), because node has none. A reload is a new node process
with an empty `localStorage`: what it shows comes from the store."""

from __future__ import annotations

import json
import os
import re
import shutil
import socket
import subprocess
import sys
import time
import urllib.request
from contextlib import contextmanager
from pathlib import Path
from typing import Iterator

import pytest
import sldb.api as api

from specir.visual.catalog import AnnotationsTarget, build_catalog, register_annotations_model, render_catalog
from specir.visual.catalog.annotations import MODEL_NAME, annotations_id, package_pythonpath

pytestmark = pytest.mark.skipif(shutil.which("node") is None, reason="node runs the page's code")

SLDB = str(Path(sys.executable).with_name("sldb"))
DOC = "catalog-annotations-demo"

HARNESS = """
globalThis.window = globalThis;
globalThis.location = { search: process.argv[2] || '' };
const memory = new Map();
globalThis.localStorage = { getItem: k => memory.get(k) ?? null, setItem: (k, v) => memory.set(k, String(v)), removeItem: k => memory.delete(k) };
for (const [k, v] of Object.entries(JSON.parse(process.env.SEED || '{}'))) memory.set(k, v);
const ANNO_STORE_KEY = 'specir.catalog.annotations.v1';
let annoCache = [];
let renders = 0;
function annoRender() { renders += 1; }
%(template)s
%(injected)s
(async () => {
  const steps = JSON.parse(process.argv[1]);
  await annoLoad();
  for (const step of steps) await annoWriteStore([...annoCache, step]);
  console.log(JSON.stringify({ annoCache, renders, local: JSON.parse(localStorage.getItem(ANNO_STORE_KEY) || '[]'), keys: [...memory.keys()], legacy: memory.get('spec2viz.catalog.annotations.v1') ?? null }));
})();
"""


def _free_port() -> int:
    with socket.socket() as sock:
        sock.bind(("127.0.0.1", 0))
        return sock.getsockname()[1]


@contextmanager
def sldb_serve(root: Path) -> Iterator[str]:
    """`sldb serve --cors` over `root/.sldb` on a free port, under `timeout`; stopped on exit."""
    port = _free_port()
    command = ["timeout", "120", SLDB, "serve", "--store", str(root / ".sldb"), "--pythonpath", package_pythonpath(), "--port", str(port), "--cors"]
    process = subprocess.Popen(command, cwd=root, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
    url = f"http://127.0.0.1:{port}"
    try:
        for _ in range(200):
            try:
                with urllib.request.urlopen(f"{url}/health", timeout=2):
                    break
            except OSError:
                if process.poll() is not None:
                    pytest.fail(f"sldb serve exited: {process.stderr.read()}")
                time.sleep(0.1)
        yield url
    finally:
        process.terminate()
        try:
            process.wait(timeout=10)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()


def _project(tmp_path: Path) -> Path:
    root = tmp_path / "proj"
    root.mkdir()
    api.init_store(root)
    register_annotations_model(root / ".sldb")
    (root / "docs").mkdir()
    (root / "docs" / "flow.mmd").write_text("graph TD\nA-->B\n", encoding="utf-8")
    (root / "docs" / "vistas.yml").write_text("project_name: demo\nvistas:\n  - id: flow\n    title: Flow\n    src: flow.mmd\n", encoding="utf-8")
    return root


def _page_code(page: str) -> tuple[str, str]:
    """The template's three storage functions and the scripts the build embedded for sldb."""
    template = re.search(r"    function annoMigrateLegacy\(\) \{.*?\n    function annoClose", page, re.S).group(0).removesuffix("    function annoClose")
    found = re.search(r"window\.SPECIR_ANNOTATIONS = .*?// </sldb-annotations>", page, re.S)
    return template, found.group(0) if found else ""  # a page without a target has no injected script


def _run(page: str, steps: list[dict], search: str = "", seed: dict | None = None) -> dict:
    template, injected = _page_code(page)
    code = HARNESS % {"template": template, "injected": injected}
    done = subprocess.run(["node", "-e", code, json.dumps(steps), search], capture_output=True, text=True, timeout=60, env={**os.environ, "SEED": json.dumps(seed or {})})
    assert done.returncode == 0, done.stderr
    assert "not saved" not in done.stderr and "not read" not in done.stderr, done.stderr
    return json.loads(done.stdout)


def _note(label: str, text: str) -> dict:
    return {"key": f"flow-x::{label}", "vista": "flow-x", "label": label, "comentario": text, "ts": "2026-11-15 21:00"}


def _stored(url: str, doc: str = DOC) -> list[dict]:
    """What the store holds, read back by `sldb serve` (`GET /document`)."""
    with urllib.request.urlopen(f"{url}/document?id={doc}", timeout=10) as response:
        body = json.load(response)
    assert body["model_name"] == MODEL_NAME
    return body["payload"]["annotations"]


def test_an_annotation_made_on_the_served_catalog_is_saved_and_reappears_on_reload(tmp_path: Path) -> None:
    root = _project(tmp_path)
    with sldb_serve(root) as url:
        page = render_catalog(root / "docs" / "vistas.yml", annotations=AnnotationsTarget(server=url, doc=DOC))
        first = _run(page, [_note("A", "revisar")])
        assert first["annoCache"] == [_note("A", "revisar")]
        assert _stored(url) == [_note("A", "revisar")]
        reloaded = _run(page, [])
        assert reloaded["annoCache"] == [_note("A", "revisar")] and reloaded["local"] == [_note("A", "revisar")]
        again = _run(page, [_note("B", "otra")])
        assert again["annoCache"] == [_note("A", "revisar"), _note("B", "otra")]
        assert _stored(url) == [_note("A", "revisar"), _note("B", "otra")]
    assert "comentario: otra" in next((root / MODEL_NAME).glob("*.md")).read_text(encoding="utf-8")


def test_a_stale_page_merges_with_what_another_page_saved(tmp_path: Path) -> None:
    root = _project(tmp_path)
    with sldb_serve(root) as url:
        page = render_catalog(root / "docs" / "vistas.yml", annotations=AnnotationsTarget(server=url, doc=DOC))
        _run(page, [_note("A", "uno")])
        template, injected = _page_code(page)
        # two pages loaded the same version; the second one saves after the first: its guard is stale (409)
        code = (HARNESS.split("(async () => {")[0] % {"template": template, "injected": injected}) + """
(async () => {
  const other = sldbAnnotationsStore(sldbAnnotationsConfig(window.SPECIR_ANNOTATIONS, ''), fetch);
  await annoLoad();
  const seen = await other.read();
  await annoWriteStore([...annoCache, %s]);
  const saved = await other.write([...seen, %s]);
  console.log(JSON.stringify(saved));
})();
""" % (json.dumps(_note("B", "dos")), json.dumps(_note("C", "tres")))
        done = subprocess.run(["node", "-e", code], capture_output=True, text=True, timeout=60)
        assert done.returncode == 0, done.stderr
        assert json.loads(done.stdout) == [_note("A", "uno"), _note("B", "dos"), _note("C", "tres")]
        assert _stored(url) == [_note("A", "uno"), _note("B", "dos"), _note("C", "tres")]


def test_the_page_url_names_the_server_and_the_document(tmp_path: Path) -> None:
    root = _project(tmp_path)
    with sldb_serve(root) as url:
        page = render_catalog(root / "docs" / "vistas.yml", annotations=AnnotationsTarget())
        _run(page, [_note("A", "por url")], search=f"?sldb={url}/&annotations=otro-doc")
        assert _stored(url, "otro-doc") == [_note("A", "por url")]


def test_without_a_target_the_page_is_spec2viz_s_and_keeps_annotations_in_the_browser(tmp_path: Path) -> None:
    root = _project(tmp_path)
    page = render_catalog(root / "docs" / "vistas.yml")
    assert "SPECIR_ANNOTATIONS" not in page and "sldb-annotations" not in page
    out = build_catalog(root / "docs" / "vistas.yml", tmp_path / "out.html", annotations=AnnotationsTarget(server="http://127.0.0.1:1"))
    assert '"doc": "catalog-annotations-demo"' in out.read_text(encoding="utf-8")


def test_the_model_registers_once_and_the_id_is_one_sldb_serve_accepts(tmp_path: Path) -> None:
    root = _project(tmp_path)
    register_annotations_model(root / ".sldb")
    assert api.is_model_registered(root / ".sldb", MODEL_NAME)
    assert annotations_id("Mi Catálogo / v2") == "catalog-annotations-Mi-Cat-logo-v2"
    assert re.fullmatch(r"[a-zA-Z0-9][a-zA-Z0-9_-]{0,159}", annotations_id("x" * 300))


LEGACY = "spec2viz.catalog.annotations.v1"
NEW = "specir.catalog.annotations.v1"


def _local_page(tmp_path: Path) -> str:
    root = _project(tmp_path)
    return render_catalog(root / "docs" / "vistas.yml")


def test_annotations_saved_under_spec2vizs_key_move_to_specirs_key(tmp_path: Path) -> None:
    page = _local_page(tmp_path)
    assert page.count(LEGACY) == 1 and NEW in page
    old = [_note("A", "vieja")]
    out = _run(page, [_note("B", "nueva")], seed={LEGACY: json.dumps(old)})
    assert out["annoCache"] == [*old, _note("B", "nueva")]
    assert out["keys"] == [NEW] and out["legacy"] is None


def test_when_both_keys_exist_the_new_wins_and_the_old_is_dropped(tmp_path: Path) -> None:
    page = _local_page(tmp_path)
    out = _run(page, [], seed={LEGACY: json.dumps([_note("A", "vieja")]), NEW: json.dumps([_note("C", "nueva")])})
    assert out["annoCache"] == [_note("C", "nueva")]
    assert out["keys"] == [NEW]


def test_an_invalid_old_value_is_left_untouched(tmp_path: Path) -> None:
    page = _local_page(tmp_path)
    out = _run(page, [], seed={LEGACY: "{not json"})
    assert out["annoCache"] == [] and out["legacy"] == "{not json" and NEW not in out["keys"]
