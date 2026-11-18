# Copyright (C) 2026 Paul Monday — GNU GPL v3 or later. See LICENSE.
"""
Cuaderno de español — Spanish reference notebook template.
Auto-discovered by generate.py via METADATA.
"""
import io
from dataclasses import dataclass
from datetime import date

from reportlab.pdfgen import canvas as rl_canvas

from core.dimensions import MARGIN, PAGE_H, PAGE_W
from core.style import FONT_BOLD, FONT_NORMAL
from templates.spanish.content.verbs_data import VERBS
from templates.spanish.doc import SECTION_NAMES, Doc, PageRecord
from templates.spanish.pages import draw_contents_page
from templates.spanish.sections import (
    build_phrases, build_verbs, build_vocab, section_entries,
)

_ORDER = ("verbs", "phrases", "vocab")
_BUILDERS = {"verbs": build_verbs, "phrases": build_phrases, "vocab": build_vocab}

METADATA = {
    "name":        "Cuaderno de español",
    "description": "Spanish reference notebook: verbs, phrases & grammar, vocab",
    "output":      "cuaderno-de-espanol.pdf",
    "pages":       0,  # dynamic
    "template_fields": [
        {"name": "sections",     "prompt": "Sections (all or verbs,phrases,vocab)", "default": "all"},
        {"name": "verb_pages",   "prompt": "Blank My Verbs pages",                  "default": "10"},
        {"name": "phrase_pages", "prompt": "Blank My Phrases pages",                "default": "8"},
        {"name": "vocab_pages",  "prompt": "Blank vocab word pages",                "default": "20"},
    ],
    "cover_fields": [
        {"name": "title",    "prompt": "Notebook title",      "default": "Mi cuaderno de español"},
        {"name": "subtitle", "prompt": "Subtitle (optional)", "default": ""},
    ],
}


@dataclass(frozen=True)
class Options:
    sections: tuple
    verb_pages: int
    phrase_pages: int
    vocab_pages: int


def _count(meta, key, default):
    raw = meta.get(key, default)
    try:
        n = int(str(raw).strip())
    except ValueError:
        raise ValueError(f"{key} must be a whole number, got {raw!r}") from None
    if n < 0:
        raise ValueError(f"{key} must be 0 or more, got {n}")
    return n


def parse_options(meta: dict) -> Options:
    raw = str(meta.get("sections", "all") or "all").lower()
    names = [t for t in raw.replace(",", " ").split() if t]
    chosen = set()
    for n in names:
        if n == "all":
            chosen.update(_ORDER)
        elif n in _ORDER:
            chosen.add(n)
        else:
            raise ValueError(f"sections: unknown section {n!r}; expected all or {', '.join(_ORDER)}")
    if not chosen:
        chosen.update(_ORDER)
    return Options(
        sections=tuple(s for s in _ORDER if s in chosen),
        verb_pages=_count(meta, "verb_pages", 10),
        phrase_pages=_count(meta, "phrase_pages", 8),
        vocab_pages=_count(meta, "vocab_pages", 20),
    )


def _edition() -> str:
    return date.today().isoformat()


def draw_cover(c, **meta):
    """Draw the cover page; always carries the edition date."""
    title = meta.get("title") or "Mi cuaderno de español"
    subtitle = meta.get("subtitle") or ""
    sections = meta.get("sections") or _ORDER
    edition = meta.get("edition") or _edition()
    cx = PAGE_W / 2
    c.saveState()
    c.setFillGray(0)
    c.setFont(FONT_BOLD, 22)
    y = PAGE_H - 140
    words = title.split()
    lines, cur = [], ""
    for w in words:
        t = f"{cur} {w}".strip()
        if c.stringWidth(t, FONT_BOLD, 22) > PAGE_W - 2 * MARGIN - 30 and cur:
            lines.append(cur)
            cur = w
        else:
            cur = t
    lines.append(cur)
    for ln in lines:
        c.drawCentredString(cx, y, ln)
        y -= 28
    if subtitle:
        c.setFont(FONT_NORMAL, 11)
        c.setFillGray(0.35)
        c.drawCentredString(cx, y - 2, subtitle)
        y -= 20
    c.setStrokeGray(0.5)
    c.setLineWidth(0.6)
    c.line(cx - 60, y - 6, cx + 60, y - 6)
    y -= 34
    c.setFont(FONT_NORMAL, 9)
    c.setFillGray(0)
    for s in sections:
        c.drawCentredString(cx, y, SECTION_NAMES[s])
        y -= 14
    c.setFont(FONT_NORMAL, 7.5)
    c.setFillGray(0.4)
    c.drawCentredString(cx, MARGIN + 24, f"Edición {edition}")
    c.restoreState()


def _render(c, opts: Options, meta: dict, page_of):
    """Draw the whole notebook on `c`; returns the Doc (log, dests)."""
    edition = _edition()
    doc = Doc(c, edition, page_of=page_of, verbs=VERBS)
    draw_cover(c, **{**meta, "sections": opts.sections, "edition": edition})
    doc.page += 1
    doc.log.append(PageRecord(doc.page, "cover", None, None))
    c.showPage()
    if len(opts.sections) > 1:
        entries = []
        for s in opts.sections:
            entries.append((SECTION_NAMES[s], f"{s}-contents", 0))
            entries += section_entries(s)
        doc.outline("Contents", "contents", 0)
        draw_contents_page(doc, None, "Contents", entries)
    for s in opts.sections:
        _BUILDERS[s](doc, opts)
    return doc


def generate(output_path: str, **meta):
    """Generate the Spanish notebook PDF (two passes so links show page numbers)."""
    opts = parse_options(meta)
    cover = {k: v for k, v in meta.items() if k in ("title", "subtitle")}

    def canvas(target):
        return rl_canvas.Canvas(target, pagesize=(PAGE_W, PAGE_H))

    c1 = canvas(io.BytesIO())
    first = _render(c1, opts, cover, None)
    c1.save()

    c = canvas(output_path)
    c.setTitle(cover.get("title") or "Mi cuaderno de español")
    _render(c, opts, cover, dict(first.dests))
    c.showOutline()
    c.save()
