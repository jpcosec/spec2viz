# Vendored bpmn-js

- Package: `bpmn-js` 18.31.1 (npm), the latest stable release on 2026-10-22
- Source: https://registry.npmjs.org/bpmn-js/-/bpmn-js-18.31.1.tgz
  (integrity `sha512-Hc7LzrgwfcBRUAdI/380Q2v1MJ115atGEVGadawLfDbHdo+r+IkmNj8fuYPFmWglUYt1KYIaC46OeX16HGTKQw==`,
  checked before extracting; no package scripts were run)
- Project: https://github.com/bpmn-io/bpmn-js, https://bpmn.io
- License: the bpmn.io license, copied verbatim in `LICENSE` (MIT-style, plus: the bpmn.io watermark that links
  back to https://bpmn.io must not be removed, changed or visually overlapped)

Files copied unchanged from the package's `dist/`:

| file | from |
| --- | --- |
| `bpmn-navigated-viewer.production.min.js` | `dist/bpmn-navigated-viewer.production.min.js` |
| `diagram-js.css` | `dist/assets/diagram-js.css` |
| `bpmn-js.css` | `dist/assets/bpmn-js.css` |
| `LICENSE` | `LICENSE` |

The `bpmn-font` icon font of `dist/assets/` is not vendored: it only draws the modeler's palette and context
pad, which the NavigatedViewer does not have. `spec2viz.renderers.bpmn.render_bpmn_html` inlines these files
into every `.bpmn.html`, so the page works offline from `file://`.

To upgrade: download the new tarball into an empty temp dir, verify its integrity against `npm view bpmn-js
dist.integrity`, extract it without running anything, copy the same four files and update this README.
