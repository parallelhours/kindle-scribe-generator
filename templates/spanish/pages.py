# Copyright (C) 2026 Paul Monday — GNU GPL v3 or later. See LICENSE.
"""Shared page types: practice, contents and fill-in pages."""
from reportlab.pdfbase.pdfmetrics import stringWidth

from core.style import FONT_BOLD, FONT_NORMAL, GRID_LW, SHADE_HEADER_BG
from templates.spanish.layout import (
    BODY_SIZE, CELL_SIZE, EN_GRAY, FONT_EN, HEAD_SIZE,
)

_RULE_GRAY = 0.65
_PERSONS5 = ["yo", "tú", "él/ella/Ud.", "nosotros", "ellos/Uds."]
_TENSES5 = ["present", "preterite", "imperfect", "future", "subjunctive"]

PRACTICE_PITCH = 16.0
WORD_PITCH = 18.0
_WORD_TOP_H = 20.0
_WORD_COLS = 2
_COL_GAP = 8.0
_ARTICLE_W = 16.0
_WORD_W_FR = 0.45


def _rule(c, x0, x1, y, gray=_RULE_GRAY, lw=0.4):
    c.setStrokeGray(gray)
    c.setLineWidth(lw)
    c.line(x0, y, x1, y)


def _label(c, x, y, text, font=FONT_NORMAL, size=CELL_SIZE, gray=0.0):
    c.setFont(font, size)
    c.setFillGray(gray)
    c.drawString(x, y, text)
    c.setFillGray(0)


# --------------------------------------------------------------------------
# Practice
# --------------------------------------------------------------------------
def draw_practice_page(doc, section, topic_id, topic_title):
    c = doc.c
    f = doc.start_page("practice", f"Practice: {topic_title}", section, topic_id)
    c.saveState()
    total = f.remaining()
    notes_h = total * 0.45
    _label(c, f.x, f.y - HEAD_SIZE, "Notes", FONT_BOLD, HEAD_SIZE)
    f.take(HEAD_SIZE + 4)
    n_notes = int((notes_h - HEAD_SIZE - 4) // PRACTICE_PITCH)
    for _ in range(n_notes):
        top = f.take(PRACTICE_PITCH)
        _rule(c, f.x, f.x + f.width, top - PRACTICE_PITCH + 2)
    f.take(min(6, f.remaining()))
    n = 1
    while f.remaining() >= 2 * PRACTICE_PITCH:
        top = f.take(PRACTICE_PITCH)
        _label(c, f.x, top - PRACTICE_PITCH + 4, f"{n}.", FONT_BOLD, CELL_SIZE + 0.7)
        _rule(c, f.x + 12, f.x + f.width, top - PRACTICE_PITCH + 2)
        top = f.take(PRACTICE_PITCH)
        _label(c, f.x + 12, top - PRACTICE_PITCH + 4, "=", FONT_EN, BODY_SIZE, EN_GRAY)
        _rule(c, f.x + 22, f.x + f.width, top - PRACTICE_PITCH + 2)
        n += 1
    c.restoreState()
    doc.end_page()


# --------------------------------------------------------------------------
# Contents
# --------------------------------------------------------------------------
CONTENTS_ROW_H = 14.0
_PNUM_W = 26.0
_LEVEL_INDENT = 10.0


def draw_contents_page(doc, section, title, entries):
    c = doc.c
    dest = f"{section}-contents" if section else "contents"
    idx, first = 0, True
    while first or idx < len(entries):
        t = title if first else f"{title} (cont.)"
        f = doc.start_page("contents", t, section, dests=(dest,) if first else ())
        first = False
        c.saveState()
        while idx < len(entries) and f.remaining() >= CONTENTS_ROW_H:
            label, d, level = entries[idx]
            top = f.take(CONTENTS_ROW_H)
            _contents_row(doc, f, top, label, d, level)
            idx += 1
        c.restoreState()
        doc.end_page()


def _contents_row(doc, f, top, label, dest, level):
    c = doc.c
    x = f.x + level * _LEVEL_INDENT
    right = f.x + f.width
    base = top - CONTENTS_ROW_H + 4
    font = FONT_BOLD if level == 0 else FONT_NORMAL
    size = BODY_SIZE
    # full-height row rect for a generous tap target
    linked = doc.link((f.x, top - CONTENTS_ROW_H, right, top), dest)
    pg = doc.page_of(dest)
    # pass 1 (no page map) must lay out like pass 2, so space is always reserved
    known = linked and (pg is not None or doc._page_of is None)
    gray = 0.0 if known else 0.6
    c.setFont(font, size)
    c.setFillGray(gray)
    c.drawString(x, base, label)
    lw = stringWidth(label, font, size)
    if known and pg is not None:
        c.setFont(FONT_NORMAL, size)
        c.drawRightString(right, base, f"p. {pg}")
        c.setFillGray(0.5)
        dots_x0 = x + lw + 4
        dots_x1 = right - _PNUM_W
        c.setFont(FONT_NORMAL, size)
        dw = stringWidth(". ", FONT_NORMAL, size)
        dx = dots_x0
        while dx + dw <= dots_x1:
            c.drawString(dx, base, ".")
            dx += dw
    c.setFillGray(0)


# --------------------------------------------------------------------------
# My Verbs (layout B)
# --------------------------------------------------------------------------
_VERB_HEAD_H = 20.0
_GRID_HEAD_H = 13.0
_GRID_ROW_H = 17.0
_EX_PITCH = 15.0


def draw_my_verbs_page(doc, filled=None):
    c = doc.c
    filled = list(filled or [])[:2]
    kind = "added-verbs" if filled else "fill-verb"
    title = "My Verbs (added)" if filled else "My Verbs"
    f = doc.start_page(kind, title, "verbs")
    c.saveState()
    block_h = (f.remaining() - 8) / 2
    for i in range(2):
        entry = filled[i] if i < len(filled) else None
        top = f.take(block_h)
        _verb_block(c, f.x, top, f.width, entry)
        if i == 0:
            f.take(min(8, f.remaining()))
    c.restoreState()
    doc.end_page()


def _verb_block(c, x, top, w, entry):
    right = x + w
    # header: verb ____ / means ____
    y = top - _VERB_HEAD_H + 5
    _label(c, x, y, "verb", FONT_BOLD, BODY_SIZE)
    vx = x + stringWidth("verb ", FONT_BOLD, BODY_SIZE)
    mid = x + w * 0.42
    _label(c, mid, y, "means", FONT_BOLD, BODY_SIZE)
    mx = mid + stringWidth("means ", FONT_BOLD, BODY_SIZE)
    _rule(c, vx, mid - 6, y - 1.5, 0.3, 0.5)
    _rule(c, mx, right, y - 1.5, 0.3, 0.5)
    if entry:
        _label(c, vx + 2, y, entry["verb"], FONT_BOLD, BODY_SIZE)
        _label(c, mx + 2, y, entry.get("en", ""), FONT_EN, BODY_SIZE, EN_GRAY)
    # grid
    gt = top - _VERB_HEAD_H
    pw = w * 0.2
    cw = (w - pw) / 5
    gh = _GRID_HEAD_H + 5 * _GRID_ROW_H
    c.setFillGray(SHADE_HEADER_BG)
    c.rect(x, gt - _GRID_HEAD_H, w, _GRID_HEAD_H, stroke=0, fill=1)
    c.setFillGray(0)
    c.setStrokeGray(0)
    c.setLineWidth(GRID_LW)
    for r in range(7):
        yy = gt - (0 if r == 0 else _GRID_HEAD_H + (r - 1) * _GRID_ROW_H)
        if r == 6:
            yy = gt - gh
        c.line(x, yy, right, yy)
    c.line(x, gt - gh, right, gt - gh)
    for k in range(7):
        cx = x if k == 0 else x + pw + (k - 1) * cw
        if k == 6:
            cx = right
        c.line(cx, gt, cx, gt - gh)
    for j, t in enumerate(_TENSES5):
        _label(c, x + pw + j * cw + 2, gt - _GRID_HEAD_H + 3.5, t, FONT_BOLD, CELL_SIZE)
    for i, p in enumerate(_PERSONS5):
        ry = gt - _GRID_HEAD_H - (i + 1) * _GRID_ROW_H + 5
        _label(c, x + 2, ry, p, FONT_NORMAL, CELL_SIZE)
        if entry:
            for j, t in enumerate(_TENSES5):
                forms = entry.get("forms", {}).get(t)
                if forms and i < len(forms) and forms[i]:
                    size = CELL_SIZE
                    while size > 6.0 and stringWidth(forms[i], FONT_NORMAL, size) > cw - 3:
                        size = round(size - 0.1, 1)
                    _label(c, x + pw + j * cw + 2, ry, forms[i], FONT_NORMAL, size)
    # examples
    ey = gt - gh - 4
    exs = list(entry.get("examples", [])) if entry else []
    for k in range(2):
        ly = ey - k * 2 * _EX_PITCH - _EX_PITCH + 3
        _rule(c, x, right, ly)
        _rule(c, x + 10, right, ly - _EX_PITCH)
        _label(c, x + 2, ly - _EX_PITCH + 3, "=", FONT_EN, BODY_SIZE, EN_GRAY)
        if k < len(exs):
            _label(c, x + 2, ly + 2.5, exs[k][0], FONT_NORMAL, BODY_SIZE)
            _label(c, x + 13, ly - _EX_PITCH + 2.5, exs[k][1], FONT_EN, BODY_SIZE, EN_GRAY)


# --------------------------------------------------------------------------
# Phrase blank
# --------------------------------------------------------------------------
_PH_PITCH = 15.0
_PH_LINES = 7
_PH_GAP = 9.0


def draw_phrase_blank_page(doc):
    c = doc.c
    f = doc.start_page("fill-phrase", "My Phrases", "phrases")
    c.saveState()
    eh = _PH_PITCH * _PH_LINES
    while f.remaining() >= eh:
        top = f.take(eh)
        x, right = f.x, f.x + f.width
        labels = [("phrase", FONT_BOLD), ("meaning", FONT_NORMAL), ("when to use", FONT_NORMAL)]
        for i, (lab, font) in enumerate(labels):
            by = top - (i + 1) * _PH_PITCH + 4
            _label(c, x, by, lab, font, CELL_SIZE, 0.35)
            lx = x + stringWidth(lab + "  ", font, CELL_SIZE)
            _rule(c, lx, right, by - 2)
        for k in range(2):
            by = top - (3 + 2 * k + 1) * _PH_PITCH + 4
            _label(c, x, by, "e.g.", FONT_NORMAL, CELL_SIZE, 0.35)
            _rule(c, x + 16, right, by - 2)
            by -= _PH_PITCH
            _label(c, x + 8, by, "=", FONT_EN, BODY_SIZE, EN_GRAY)
            _rule(c, x + 18, right, by - 2)
        if f.remaining() >= eh + _PH_GAP:
            f.take(_PH_GAP)
            _rule(c, x, right, top - eh - _PH_GAP / 2 + 1, 0.8, 0.3)
        else:
            break
    c.restoreState()
    doc.end_page()


# --------------------------------------------------------------------------
# Word page
# --------------------------------------------------------------------------
_ROWS_PER_COL = int((449.28 - 2 * 6 - 14 - 2 - 12 - _WORD_TOP_H) // WORD_PITCH)
WORD_ROWS_PER_PAGE = _ROWS_PER_COL * _WORD_COLS


def draw_word_page(doc, section, words=None, topic="", date=""):
    c = doc.c
    words = list(words or [])
    kind = "added-words" if words else "fill-word"
    title = "Vocab (added)" if words else "Vocab"
    f = doc.start_page(kind, title, section)
    c.saveState()
    top = f.take(_WORD_TOP_H)
    by = top - _WORD_TOP_H + 6
    _label(c, f.x, by, "Topic / lesson date", FONT_BOLD, BODY_SIZE)
    lx = f.x + stringWidth("Topic / lesson date  ", FONT_BOLD, BODY_SIZE)
    _rule(c, lx, f.x + f.width, by - 2, 0.3, 0.5)
    if topic or date:
        _label(c, lx + 2, by, " - ".join(s for s in (topic, date) if s), FONT_NORMAL, BODY_SIZE)
    nrows = min(_ROWS_PER_COL, int(f.remaining() // WORD_PITCH))
    colw = (f.width - _COL_GAP) / _WORD_COLS
    grid_top = f.y
    idx = 0
    for col in range(_WORD_COLS):
        x = f.x + col * (colw + _COL_GAP)
        for r in range(nrows):
            ry = grid_top - r * WORD_PITCH
            c.setStrokeGray(0.5)
            c.setLineWidth(GRID_LW)
            c.rect(x, ry - WORD_PITCH + 3, _ARTICLE_W, WORD_PITCH - 6, stroke=1, fill=0)
            wx = x + _ARTICLE_W + 3
            ex = wx + (colw - _ARTICLE_W - 3) * _WORD_W_FR
            _rule(c, wx, ex - 3, ry - WORD_PITCH + 3)
            _rule(c, ex, x + colw, ry - WORD_PITCH + 3)
            if idx < len(words):
                art, wd, en = words[idx]
                _label(c, x + 2, ry - WORD_PITCH + 6.5, art, FONT_BOLD, CELL_SIZE)
                _label(c, wx, ry - WORD_PITCH + 5.5, wd, FONT_NORMAL, BODY_SIZE)
                _label(c, ex + 1, ry - WORD_PITCH + 5.5, en, FONT_EN, CELL_SIZE + 0.4, EN_GRAY)
            idx += 1
    c.restoreState()
    doc.end_page()
