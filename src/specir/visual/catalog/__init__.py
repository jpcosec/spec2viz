"""specIR's HTML catalog of diagrams (IR13b): the visual part of spec2viz's catalog.

- `loader`: the registry (`vistas.yml`, hierarchical diagram stores, `project.yml` envelope) as a
  flat list of views; paths by sldb's catalog rule (`sldb.api.notations.catalog_paths`).
- `sections`, `views`, `fragments`: the HTML of the views, drawn from sldb's resolved view
  (`resolve_view`) with IR12's `view_to_mermaid`, or from their rendered source.
- `atoms`: a view as sldb's `SpecView` and the atoms the page embeds; the matching and the coverage
  are `sldb.api.matching` (D4), called directly.
- `annotations`: the store document of the page's annotations and the script that saves them with
  `sldb serve` (which replaces spec2viz's `catalog serve`).
- `build`: the page (`render_catalog`, `build_catalog`).

Syncing and validating a catalog are sldb's, used directly: `sldb.api.notations.sync_catalog` and
`check_catalog`, or `sldb notations sync --catalog [--check]` (D1)."""

from specir.visual.catalog.annotations import AnnotationsTarget, CatalogAnnotationsDoc, annotations_id, register_annotations_model
from specir.visual.catalog.atoms import CatalogAtoms, catalog_atoms, spec_view, split_shared_atoms
from specir.visual.catalog.build import build_catalog, render_catalog
from specir.visual.catalog.loader import CatalogConfig, CatalogItem, CatalogLoader, load_catalog
from specir.visual.catalog.sections import render_catalog_metadata, render_filter_bar, render_nav, render_sections, resolve_item_path
from specir.visual.catalog.views import resolved_board, resolved_views

__all__ = [
    "AnnotationsTarget", "CatalogAnnotationsDoc", "CatalogAtoms", "CatalogConfig", "CatalogItem", "CatalogLoader",
    "annotations_id", "build_catalog", "catalog_atoms", "load_catalog", "register_annotations_model", "render_catalog",
    "render_catalog_metadata", "render_filter_bar", "render_nav", "render_sections", "resolve_item_path", "resolved_board",
    "resolved_views", "spec_view", "split_shared_atoms",
]
