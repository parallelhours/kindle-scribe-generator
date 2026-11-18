# Copyright (C) 2026 Paul Monday — GNU GPL v3 or later. See LICENSE.
"""Doc wrapper: page chrome, destinations, outline, links and page log."""
from dataclasses import dataclass

from core.dimensions import MARGIN, PAGE_H, PAGE_W
from core.style import FONT_BOLD, FONT_NORMAL
from templates.spanish.layout import Frame

HEADER_H = 14.0
FOOTER_H = 12.0
_TITLE_SIZE = 9.0
_SMALL_SIZE = 6.5

SECTION_NAMES = {"verbs": "Verbos", "phrases": "Frases", "vocab": "Vocabulario"}


@dataclass
class PageRecord:
    page: int
    kind: str
    section: str | None
    topic_id: str | None


class Doc:
    def __init__(self, c, edition: str, page_of: dict | None = None, verbs: dict | None = None):
        self.c = c
        self.edition = edition
        self._page_of = page_of
        self.verbs = verbs if verbs is not None else {}
        self.log: list[PageRecord] = []
        self.dests: dict[str, int] = {}
        self.links: list[tuple[tuple, str]] = []
        self.page = 0

    def page_of(self, dest):
        return self._page_of.get(dest) if self._page_of is not None else None

    def link(self, rect, dest) -> bool:
        self.links.append((tuple(rect), dest))
        if self._page_of is None:
            return True
        if dest not in self._page_of:
            return False
        self.c.linkRect("", dest, rect, relative=0, thickness=0)
        return True

    def outline(self, title: str, dest: str, level: int) -> None:
        self.c.addOutlineEntry(title, dest, level=level, closed=level == 0)

    def start_page(self, kind, title, section, topic_id=None, dests=()) -> Frame:
        c = self.c
        self.page += 1
        n = self.page
        for d in dests:
            c.bookmarkPage(d)
            self.dests[d] = n
        self.log.append(PageRecord(n, kind, section, topic_id))

        left, right = MARGIN, PAGE_W - MARGIN
        base = PAGE_H - MARGIN - _TITLE_SIZE
        c.saveState()
        c.setFillGray(0)
        c.setFont(FONT_BOLD, _TITLE_SIZE)
        c.drawString(left, base, title)
        if section:
            rx = right
            if kind != "contents":
                label = "contents"
                lw = c.stringWidth(label, FONT_NORMAL, _SMALL_SIZE)
                c.setFont(FONT_NORMAL, _SMALL_SIZE)
                c.drawRightString(rx, base, label)
                if self.link((rx - lw, base - 2, rx, base + _SMALL_SIZE), f"{section}-contents"):
                    c.setStrokeGray(0)
                    c.setLineWidth(0.4)
                    c.line(rx - lw, base - 1.2, rx, base - 1.2)
                rx -= lw + 6
            c.setFont(FONT_NORMAL, _SMALL_SIZE)
            c.setFillGray(0.4)
            c.drawRightString(rx, base, SECTION_NAMES.get(section, section))
        c.setStrokeGray(0.5)
        c.setLineWidth(0.4)
        c.line(left, PAGE_H - MARGIN - HEADER_H + 2, right, PAGE_H - MARGIN - HEADER_H + 2)
        c.setFillGray(0.4)
        c.setFont(FONT_NORMAL, _SMALL_SIZE)
        c.drawCentredString(PAGE_W / 2, MARGIN + 2, f"Edición {self.edition} · {n}")
        c.restoreState()

        return Frame(left, right - left, PAGE_H - MARGIN - HEADER_H - 2, MARGIN + FOOTER_H)

    def end_page(self) -> None:
        self.c.showPage()
