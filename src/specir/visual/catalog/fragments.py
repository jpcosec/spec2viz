"""One element of an HTML artifact, by id or by class, as the catalog embeds a `src: x.html#id`
(migrated from spec2viz's `orchestrator`: `_ElementByIdExtractor`, `_ElementByClassExtractor`,
`_extract_html_fragment`)."""

from __future__ import annotations

from html.parser import HTMLParser


class _ElementExtractor(HTMLParser):
    """The markup of the first element `wanted(attrs)` accepts, as written."""

    def __init__(self, keep_decl: bool):
        super().__init__(convert_charrefs=False)
        self.depth = 0
        self.capturing = False
        self.parts: list[str] = []
        self.keep_decl = keep_decl

    def wanted(self, attrs: dict[str, str | None]) -> bool:
        raise NotImplementedError

    def handle_starttag(self, tag, attrs):
        if not self.capturing and self.wanted(dict(attrs)):
            self.capturing, self.depth = True, 1
            self.parts.append(self.get_starttag_text())
            return
        if self.capturing:
            self.depth += 1
            self.parts.append(self.get_starttag_text())

    def handle_startendtag(self, tag, attrs):
        if self.capturing:
            self.parts.append(self.get_starttag_text())

    def handle_endtag(self, tag):
        if self.capturing:
            self.parts.append(f"</{tag}>")
            self.depth -= 1
            self.capturing = self.depth != 0

    def _keep(self, text: str) -> None:
        if self.capturing:
            self.parts.append(text)

    def handle_data(self, data):
        self._keep(data)

    def handle_comment(self, data):
        self._keep(f"<!--{data}-->")

    def handle_entityref(self, name):
        self._keep(f"&{name};")

    def handle_charref(self, name):
        self._keep(f"&#{name};")

    def handle_decl(self, decl):
        if self.keep_decl:
            self._keep(f"<!{decl}>")

    def get_html(self) -> str:
        return "".join(self.parts).strip()


class ElementByIdExtractor(_ElementExtractor):
    def __init__(self, target_id: str):
        super().__init__(keep_decl=True)
        self.target_id = target_id

    def wanted(self, attrs):
        return attrs.get("id") == self.target_id


class ElementByClassExtractor(_ElementExtractor):
    def __init__(self, class_name: str):
        super().__init__(keep_decl=False)
        self.class_name = class_name

    def wanted(self, attrs):
        return self.class_name in set((attrs.get("class") or "").split())


def extract_html_fragment(content: str, fragment: str) -> str:
    """The `.board` inside the element `#fragment` (or the element itself if it has none)."""
    extractor = ElementByIdExtractor(fragment)
    extractor.feed(content)
    element_html = extractor.get_html()
    if not element_html:
        raise ValueError(f"HTML fragment '#{fragment}' not found in source artifact.")
    board = ElementByClassExtractor("board")
    board.feed(element_html)
    return board.get_html() or element_html


__all__ = ["ElementByClassExtractor", "ElementByIdExtractor", "extract_html_fragment"]
