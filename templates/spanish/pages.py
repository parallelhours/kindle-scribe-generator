# Copyright (C) 2026 Paul Monday — GNU GPL v3 or later. See LICENSE.
"""Shared page types: practice, contents, phrase index/entries and fill-in pages."""
import re
import unicodedata

from reportlab.pdfbase.pdfmetrics import stringWidth

from core.dimensions import MARGIN, PAGE_W
from core.style import FONT_BOLD, FONT_NORMAL, GRID_LW, SHADE_HEADER_BG
from templates.spanish.layout import (
    BODY_SIZE, CELL_SIZE, EN_GRAY, FONT_EN, FONT_FOR, HEAD_SIZE, MIN_CELL, LayoutOverflow,
    block_height, draw_block, wrap_rich,
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
        _fit_cell(c, vx + 2, y, mid - 6, entry["verb"], FONT_BOLD, BODY_SIZE)
        _fit_cell(c, mx + 2, y, right, entry.get("en", ""), FONT_EN, BODY_SIZE, EN_GRAY)
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
                    fx = x + pw + j * cw + 2
                    _fit_cell(c, fx, ry, fx + cw - 3, forms[i], FONT_NORMAL, CELL_SIZE)
    # examples
    ey = gt - gh - 4
    exs = list(entry.get("examples", [])) if entry else []
    for k in range(2):
        ly = ey - k * 2 * _EX_PITCH - _EX_PITCH + 3
        _rule(c, x, right, ly)
        _rule(c, x + 10, right, ly - _EX_PITCH)
        _label(c, x + 2, ly - _EX_PITCH + 3, "=", FONT_EN, BODY_SIZE, EN_GRAY)
        if k < len(exs):
            _fit_cell(c, x + 2, ly + 2.5, right, exs[k][0], FONT_NORMAL, BODY_SIZE,
                      strict=True)
            _fit_cell(c, x + 13, ly - _EX_PITCH + 2.5, right, exs[k][1], FONT_EN, BODY_SIZE,
                      EN_GRAY, strict=True)


# --------------------------------------------------------------------------
# Phrase entries: printed and blank share one drawing routine, so a handwritten
# entry on a blank page has exactly the structure of a printed one.
# --------------------------------------------------------------------------
_PH_PITCH = 15.0
_PH_LINES = 7
_PH_GAP = 9.0
_PH_PHRASE_SIZE = 8.5
_PH_CMP_GAP = 5.0
_PH_LABEL_GRAY = 0.35


def _ph_fields(p):
    """(label, label font, label size, label gray, label dx, rule dx, text, text size)."""
    ex = list(p["examples"]) if p else [("", "")] * 2
    fields = [
        ("phrase", FONT_BOLD, CELL_SIZE, _PH_LABEL_GRAY, 0, None,
         f"**{p['es']}**" if p else "", _PH_PHRASE_SIZE),
        ("meaning", FONT_NORMAL, CELL_SIZE, _PH_LABEL_GRAY, 0, None,
         f"~{p['en']}~" if p else "", BODY_SIZE),
        ("when to use", FONT_NORMAL, CELL_SIZE, _PH_LABEL_GRAY, 0, None,
         p["use"] if p else "", BODY_SIZE),
    ]
    for es, en in ex:
        fields.append(("e.g.", FONT_NORMAL, CELL_SIZE, _PH_LABEL_GRAY, 0, 16, es, BODY_SIZE))
        fields.append(("=", FONT_EN, BODY_SIZE, EN_GRAY, 8, 18, f"~{en}~" if en else "",
                       BODY_SIZE))
    return fields


def _ph_plan(p, w):
    """Fields with their wrapped text lines (an empty field still gets one line)."""
    plan = []
    for lab, font, lsize, lgray, ldx, rdx, text, tsize in _ph_fields(p):
        if rdx is None:
            rdx = stringWidth(lab + "  ", font, lsize)
        lines = wrap_rich(text, w - rdx - 3, tsize) if text else []
        plan.append((lab, font, lsize, lgray, ldx, rdx, lines or [[]], tsize))
    return plan


def phrase_entry_height(p, w):
    return _PH_PITCH * sum(len(f[6]) for f in _ph_plan(p, w))


def _draw_phrase_entry(c, x, top, w, p=None):
    right = x + w
    row = 0
    for lab, font, lsize, lgray, ldx, rdx, lines, tsize in _ph_plan(p, w):
        for i, line in enumerate(lines):
            by = top - (row + 1) * _PH_PITCH + 4
            if i == 0:
                _label(c, x + ldx, by, lab, font, lsize, lgray)
            _rule(c, x + rdx, right, by - 2)
            tx = x + rdx + 2
            for style, text in line:
                c.setFont(FONT_FOR[style], tsize)
                c.setFillGray(EN_GRAY if style == "en" else 0)
                c.drawString(tx, by, text)
                tx += stringWidth(text, FONT_FOR[style], tsize)
            c.setFillGray(0)
            row += 1
    return row * _PH_PITCH


def _ph_separator(c, f):
    top = f.take(_PH_GAP)
    _rule(c, f.x, f.x + f.width, top - _PH_GAP / 2 + 1, 0.8, 0.3)


def draw_phrase_blank_page(doc):
    c = doc.c
    f = doc.start_page("fill-phrase", "My Phrases", "phrases")
    c.saveState()
    eh = _PH_PITCH * _PH_LINES
    while f.remaining() >= eh:
        top = f.take(eh)
        _draw_phrase_entry(c, f.x, top, f.width)
        if f.remaining() >= eh + _PH_GAP:
            _ph_separator(c, f)
        else:
            break
    c.restoreState()
    doc.end_page()


_FOLD = str.maketrans("áéíóúüàèìòùâêîôû", "aeiouuaeiouaeiou")


def spanish_sort_key(s: str) -> tuple:
    """Spanish dictionary order: accents and case ignored, ñ after n, and on a tie the
    unaccented word first (aun < aún). Punctuation is ignored."""
    low = s.lower()
    primary, accents = [], []
    for ch in low:
        if ch == "ñ":
            primary.append("n{")  # '{' sorts after every letter: n < ñ < o
            accents.append(0)
        elif ch.isalnum() or ch == " ":
            base = ch.translate(_FOLD)
            primary.append(base)
            accents.append(0 if base == ch else 1)
    return ("".join(primary).strip(), tuple(accents), s)


def _slug(s):
    folded = unicodedata.normalize("NFKD", s.lower())
    folded = "".join(ch for ch in folded if not unicodedata.combining(ch))
    words = re.sub(r"[^a-z0-9 ]+", " ", folded).split()
    return "-".join(words) or "x"


def phrase_dests(names) -> dict:
    """Map each phrase to a unique destination name "p-{slug}" (aun: p-aun, aún: p-aun-2)."""
    out, used = {}, set()
    for name in sorted(names, key=spanish_sort_key):
        base = f"p-{_slug(name)}"
        d, n = base, 2
        while d in used:
            d, n = f"{base}-{n}", n + 1
        used.add(d)
        out[name] = d
    return out


def _initial(s):
    k = spanish_sort_key(s)[0]
    return "Ñ" if k.startswith("n{") else k[:1].upper()


INDEX_ROW_H = 13.0
_INDEX_LETTER_W = 12.0
_INDEX_PHRASE_W = 92.0
_INDEX_PHRASE_MAX = 250.0  # widest phrase (at the minimum size) the index row can hold
_INDEX_TITLE = "A. Connector phrases A–Z"


def draw_phrase_index(doc, phrases):
    """A-Z index: one full-row-height link per phrase to its entry."""
    c = doc.c
    phrases = sorted(phrases, key=lambda p: spanish_sort_key(p["es"]))
    dests = phrase_dests([p["es"] for p in phrases])
    idx, first = 0, True
    while first or idx < len(phrases):
        f = doc.start_page("phrase-index", _INDEX_TITLE if first else f"{_INDEX_TITLE} (cont.)",
                           "phrases", dests=("phrases-index",) if first else ())
        c.saveState()
        prev = None
        while idx < len(phrases) and f.remaining() >= INDEX_ROW_H:
            p = phrases[idx]
            top = f.take(INDEX_ROW_H)
            letter = _initial(p["es"])
            _index_row(doc, f, top, p, dests[p["es"]], letter if letter != prev else "",
                       new_group=prev is not None and letter != prev)
            prev = letter
            idx += 1
        first = False
        c.restoreState()
        doc.end_page()


def _shrink(text, font, width, start, minimum):
    """Largest size from start down to minimum (0.1 pt steps) that fits; else minimum."""
    size = start
    while size > minimum and stringWidth(text, font, size) > width:
        size = round(size - 0.1, 1)
    return size


def _index_row(doc, f, top, p, dest, letter, new_group):
    c = doc.c
    x, right = f.x, f.x + f.width
    bottom = top - INDEX_ROW_H
    base = bottom + 4
    if new_group:
        _rule(c, x, right, top, 0.55, 0.5)
    if letter:
        _label(c, x, base, letter, FONT_BOLD, BODY_SIZE + 1, 0.35)
    px = x + _INDEX_LETTER_W
    # long (e.g. user-added) phrases shrink to the minimum size, then push the meaning
    # column right; the meaning shrinks and, as a last resort, is cut with an ellipsis
    es_size = _shrink(p["es"], FONT_BOLD, _INDEX_PHRASE_W - 4, BODY_SIZE, MIN_CELL)
    if stringWidth(p["es"], FONT_BOLD, es_size) > _INDEX_PHRASE_MAX:
        raise LayoutOverflow(
            f"phrase {p['es'][:60]!r} is too long for the index row "
            f"({stringWidth(p['es'], FONT_BOLD, es_size):.0f}pt at {es_size}pt, "
            f"max {_INDEX_PHRASE_MAX:.0f}pt); shorten it")
    _label(c, px, base, p["es"], FONT_BOLD, es_size)
    mx = max(px + _INDEX_PHRASE_W, px + stringWidth(p["es"], FONT_BOLD, es_size) + 6)
    avail = right - _PNUM_W - mx - 2
    en = p["en"]
    en_size = _shrink(en, FONT_EN, avail, BODY_SIZE, MIN_CELL)
    while len(en) > 1 and stringWidth(en, FONT_EN, en_size) > avail:
        en = en[:-2].rstrip() + "…"
    _label(c, mx, base, en, FONT_EN, en_size, EN_GRAY)
    # full-row-height tap target; pass 1 reserves the page-number space as well
    doc.link((x, bottom, right, top), dest)
    pg = doc.page_of(dest)
    if pg is not None:
        _label(c, right - stringWidth(f"p. {pg}", FONT_NORMAL, BODY_SIZE), base, f"p. {pg}",
               FONT_NORMAL, BODY_SIZE)
    _rule(c, px, right, bottom + 0.5, 0.88, 0.3)


_ENTRY_W = PAGE_W - 2 * MARGIN
_ENTRIES_TITLE = "A. Connector phrases"


def draw_phrase_entries(doc, phrases, comparisons=()) -> None:
    """Printed phrase entries in Spanish alphabetical order, as many per page as fit.
    An entry (with the comparison box that follows it, if any) never splits across pages.
    Each entry gets the destination from phrase_dests (no outline entry)."""
    c = doc.c
    phrases = sorted(phrases, key=lambda p: spanish_sort_key(p["es"]))
    dests = phrase_dests([p["es"] for p in phrases])
    after = {cmp["after"]: cmp["block"] for cmp in comparisons}
    f, drawn = None, 0
    for p in phrases:
        block = after.get(p["es"])
        need = phrase_entry_height(p, _ENTRY_W)
        if block:
            need += _PH_CMP_GAP + block_height(block, _ENTRY_W, doc.verbs)
        if f is None or (_PH_GAP if drawn else 0) + need > f.remaining() + 1e-6:
            if f is not None:
                c.restoreState()
                doc.end_page()
            f = doc.start_page("phrase-entries", _ENTRIES_TITLE, "phrases")
            c.saveState()
            drawn = 0
            if need > f.remaining() + 1e-6:
                raise LayoutOverflow(f"phrase entry {p['es']!r} does not fit on one page")
        if drawn:
            _ph_separator(c, f)
        c.bookmarkPage(dests[p["es"]])
        doc.dests[dests[p["es"]]] = doc.page
        top = f.take(phrase_entry_height(p, f.width))
        _draw_phrase_entry(c, f.x, top, f.width, p)
        if block:
            f.take(_PH_CMP_GAP)
            draw_block(c, f, block, doc)
        drawn += 1
    if f is not None:
        c.restoreState()
        doc.end_page()


# --------------------------------------------------------------------------
# Word page
# --------------------------------------------------------------------------
_ROWS_PER_COL = int((449.28 - 2 * 6 - 14 - 2 - 12 - _WORD_TOP_H) // WORD_PITCH)
WORD_ROWS_PER_PAGE = _ROWS_PER_COL * _WORD_COLS


def word_cell_columns(doc_width, x0):
    """(left, right) text spans of every cell in a word-page row: per column, the
    article box, the word rule and the English rule, in that order."""
    colw = (doc_width - _COL_GAP) / _WORD_COLS
    spans = []
    for col in range(_WORD_COLS):
        x = x0 + col * (colw + _COL_GAP)
        wx = x + _ARTICLE_W + 3
        ex = wx + (colw - _ARTICLE_W - 3) * _WORD_W_FR
        spans += [(x + 1.5, x + _ARTICLE_W - 1.5), (wx, ex - 4), (ex + 1, x + colw)]
    return spans


_WORD_LINE2 = 6.5  # baseline offset of a second text line in a word row


def _fit_cell(c, x, base, right, text, font, start, gray=0.0, strict=False):
    """Draw text in [x, right]: shrink to MIN_CELL, then wrap onto two lines, then
    truncate with an ellipsis as a last resort (never overruns the cell). With
    strict=True, text that would need truncating raises LayoutOverflow instead."""
    width = right - x
    size = _shrink(text, font, width, start, MIN_CELL)
    if stringWidth(text, font, size) <= width + 1e-6:
        _label(c, x, base, text, font, size, gray)
        return
    size = MIN_CELL
    words, first = text.split(), ""
    for i, w in enumerate(words):
        trial = f"{first} {w}".strip()
        if first and stringWidth(trial, font, size) > width:
            rest = " ".join(words[i:])
            break
        first = trial
    else:
        rest = ""
    if strict and (stringWidth(first, font, size) > width
                   or (rest and stringWidth(rest, font, size) > width)):
        raise LayoutOverflow(f"{text[:60]!r} does not fit in {width:.0f}pt on two lines")
    if stringWidth(first, font, size) > width:  # a single unbreakable word
        while first and stringWidth(first + "\u2026", font, size) > width:
            first = first[:-1]
        first += "\u2026"
    while rest and stringWidth(rest, font, size) > width:
        rest = rest[:-2].rstrip() + "\u2026"
    if rest:
        _label(c, x, base + _WORD_LINE2, first, font, size, gray)
        _label(c, x, base, rest, font, size, gray)
    else:
        _label(c, x, base, first, font, size, gray)


def draw_word_page(doc, section, words=None, topic="", date=""):
    c = doc.c
    words = list(words or [])
    if len(words) > WORD_ROWS_PER_PAGE:
        raise ValueError(f"{len(words)} words exceed one page ({WORD_ROWS_PER_PAGE})")
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
        _fit_cell(c, lx + 2, by, f.x + f.width, " - ".join(s for s in (topic, date) if s),
                  FONT_NORMAL, BODY_SIZE)
    nrows = int(f.remaining() // WORD_PITCH)
    if nrows < _ROWS_PER_COL:
        raise LayoutOverflow(f"word page has room for {nrows} rows, needs {_ROWS_PER_COL}")
    nrows = _ROWS_PER_COL
    spans = word_cell_columns(f.width, f.x)
    grid_top = f.y
    idx = 0
    for col in range(_WORD_COLS):
        (ax0, _ax1), (wx, wx1), (ex0, ex1) = spans[3 * col:3 * col + 3]
        x = ax0 - 1.5
        for r in range(nrows):
            ry = grid_top - r * WORD_PITCH
            c.setStrokeGray(0.5)
            c.setLineWidth(GRID_LW)
            c.rect(x, ry - WORD_PITCH + 3, _ARTICLE_W, WORD_PITCH - 6, stroke=1, fill=0)
            _rule(c, wx, wx1 + 1, ry - WORD_PITCH + 3)
            _rule(c, ex0 - 1, ex1, ry - WORD_PITCH + 3)
            if idx < len(words):
                art, wd, en = words[idx]
                _fit_cell(c, ax0 + 0.5, ry - WORD_PITCH + 6.5, _ax1, art, FONT_BOLD, CELL_SIZE)
                _fit_cell(c, wx, ry - WORD_PITCH + 5.5, wx1, wd, FONT_NORMAL, BODY_SIZE)
                _fit_cell(c, ex0, ry - WORD_PITCH + 5.5, ex1, en, FONT_EN, CELL_SIZE + 0.4,
                          EN_GRAY)
            idx += 1
    c.restoreState()
    doc.end_page()
