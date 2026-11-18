# Copyright (C) 2026 Paul Monday — GNU GPL v3 or later. See LICENSE.
"""Layout engine for the Spanish notebook: rich text, frames and blocks."""
import re

from reportlab.pdfbase.pdfmetrics import stringWidth

from core.style import (
    FONT_BOLD, FONT_NORMAL, GRID_LW, SHADE_HEADER_BG, SHADE_INSTRUCTIONS,
)

FONT_EN = "Helvetica-Oblique"
FONT_FOR = {"normal": FONT_NORMAL, "bold": FONT_BOLD, "en": FONT_EN}

BODY_SIZE = 7.5
HEAD_SIZE = 9.5
CELL_SIZE = 6.8
MIN_BODY = 6.5
MIN_CELL = 6.0
EN_GRAY = 0.40
VOS_GRAY = 0.60

_EPS = 1e-6
_CELL_PAD_X = 2.0
_CELL_PAD_Y = 1.5
_BULLET_INDENT = 8.0
_EXAMPLE_INDENT = 6.0
_PERSONS = ["yo", "tú", "él/ella/Ud.", "nosotros", "vosotros", "ellos/Uds."]
_VOS_ROW = 4


class LayoutOverflow(Exception):
    """Content does not fit at the minimum legible size / available space."""


# --------------------------------------------------------------------------
# Rich text
# --------------------------------------------------------------------------
_RICH_RE = re.compile(r"\*\*(.+?)\*\*|~(.+?)~")


def parse_rich(text: str) -> list[tuple[str, str]]:
    out, pos = [], 0
    for m in _RICH_RE.finditer(text):
        if m.start() > pos:
            out.append(("normal", text[pos:m.start()]))
        if m.group(1) is not None:
            out.append(("bold", m.group(1)))
        else:
            out.append(("en", m.group(2)))
        pos = m.end()
    if pos < len(text):
        out.append(("normal", text[pos:]))
    return out


def _bold(chunks):
    return [("bold" if s == "normal" else s, t) for s, t in chunks]


def _w(style, text, size):
    return stringWidth(text, FONT_FOR[style], size)


def _wrap_chunks(chunks, width, size):
    # Build units: whitespace runs and words (words may span style chunks).
    units, word = [], []
    for style, text in chunks:
        for tok in re.findall(r"\s+|\S+", text):
            if tok.isspace():
                if word:
                    units.append(("word", word))
                    word = []
                units.append(("space", style))
            else:
                word.append((style, tok))
    if word:
        units.append(("word", word))

    lines, cur, curw, pending = [], [], 0.0, None
    for kind, val in units:
        if kind == "space":
            if cur:
                pending = (val, " ")
            continue
        ww = sum(_w(s, t, size) for s, t in val)
        if ww > width + _EPS:
            raise LayoutOverflow(f"word too wide ({ww:.1f} > {width:.1f}): {val!r}")
        sw = _w(*pending, size) if pending else 0.0
        if cur and curw + sw + ww > width + _EPS:
            lines.append(cur)
            cur, curw, pending, sw = [], 0.0, None, 0.0
        if cur and pending:
            cur.append(pending)
            curw += sw
        cur.extend(val)
        curw += ww
        pending = None
    if cur:
        lines.append(cur)

    merged = []
    for ln in lines:
        m = []
        for s, t in ln:
            if m and m[-1][0] == s:
                m[-1] = (s, m[-1][1] + t)
            else:
                m.append((s, t))
        merged.append(m)
    return merged


def wrap_rich(text: str, width: float, size: float) -> list[list[tuple[str, str]]]:
    return _wrap_chunks(parse_rich(text), width, size)


def _width_at_1(chunks):
    return sum(_w(s, t, 1.0) for s, t in chunks)


def _fit_from_w1(w1, width, start, minimum, what=""):
    if w1 <= 0:
        return start
    size = min(start, int(width / w1 * 10 + _EPS) / 10.0)
    while size > 0 and w1 * size > width + _EPS:
        size = round(size - 0.1, 1)
    if size < minimum - _EPS:
        raise LayoutOverflow(f"cannot fit {what!r} in {width:.1f}pt at >= {minimum}pt")
    return size


def fit_size(text: str, width: float, start: float, minimum: float) -> float:
    return _fit_from_w1(_width_at_1(parse_rich(text)), width, start, minimum, text)


def _longest_word_w1(chunks):
    best, word = 0.0, 0.0
    for style, text in chunks:
        for tok in re.findall(r"\s+|\S+", text):
            if tok.isspace():
                best, word = max(best, word), 0.0
            else:
                word += _w(style, tok, 1.0)
    return max(best, word)


# --------------------------------------------------------------------------
# Frame
# --------------------------------------------------------------------------
class Frame:
    def __init__(self, x, width, top, bottom):
        self.x, self.width, self.top, self.bottom = x, width, top, bottom
        self.y = top

    def remaining(self) -> float:
        return self.y - self.bottom

    def take(self, h: float) -> float:
        if h > self.remaining() + _EPS:
            raise LayoutOverflow(f"need {h:.1f}pt, only {self.remaining():.1f}pt left")
        top = self.y
        self.y -= h
        return top


# --------------------------------------------------------------------------
# Low-level drawing helpers
# --------------------------------------------------------------------------
def _draw_lines(c, lines, x, top, size, lead, gray=None):
    """Draw wrapped rich lines; returns nothing. Baseline of line i is below top."""
    for i, line in enumerate(lines):
        cx = x
        base = top - i * lead - size * 0.82
        for style, text in line:
            c.setFont(FONT_FOR[style], size)
            c.setFillGray(gray if gray is not None else (EN_GRAY if style == "en" else 0))
            c.drawString(cx, base, text)
            cx += _w(style, text, size)
    c.setFillGray(0)


def _line_w(line, size):
    return sum(_w(s, t, size) for s, t in line)


def _body_lead(size):
    return size + 2.0


def _text_h(text, width, size, bold=False):
    chunks = parse_rich(text)
    lines = _wrap_chunks(_bold(chunks) if bold else chunks, width, size)
    return lines, len(lines) * _body_lead(size)


# --------------------------------------------------------------------------
# Tables (also used by conj and compare)
# --------------------------------------------------------------------------
def _plan_table(header, rows, widths, width):
    ncols = len(header)
    fr = widths if widths else [1.0 / ncols] * ncols
    colw = [f * width for f in fr]

    def plan_cell(text, cw, bold):
        chunks = parse_rich(text)
        if bold:
            chunks = _bold(chunks)
        avail = cw - 2 * _CELL_PAD_X
        size = _fit_from_w1(_longest_word_w1(chunks), avail, CELL_SIZE, MIN_CELL, text)
        lines = _wrap_chunks(chunks, avail, size)
        lead = size + 1.4
        h = max(len(lines), 1) * lead + 2 * _CELL_PAD_Y
        return lines, size, lead, h

    plans, heights = [], []
    for ri, row in enumerate([header] + list(rows)):
        cells = [plan_cell(row[i], colw[i], ri == 0) for i in range(ncols)]
        plans.append(cells)
        heights.append(max(cell[3] for cell in cells))
    return colw, plans, heights


def _table_height(block, width):
    _, _, heights = _plan_table(block["header"], block["rows"], block.get("widths"), width)
    return sum(heights)


def _draw_table(c, x, top, block, width, header_shade=SHADE_HEADER_BG):
    colw, plans, heights = _plan_table(block["header"], block["rows"], block.get("widths"), width)
    gray_rows = set(block.get("gray_rows", []))
    total = sum(heights)
    c.setFillGray(header_shade)
    c.rect(x, top - heights[0], width, heights[0], stroke=0, fill=1)
    c.setFillGray(0)
    c.setStrokeGray(0)
    c.setLineWidth(GRID_LW)
    y = top
    for ri, cells in enumerate(plans):
        cx = x
        gray = VOS_GRAY if (ri - 1) in gray_rows and ri > 0 else None
        for ci, (lines, size, lead, _h) in enumerate(cells):
            _draw_lines(c, lines, cx + _CELL_PAD_X, y - _CELL_PAD_Y, size, lead, gray)
            cx += colw[ci]
        y -= heights[ri]
        c.line(x, y, x + width, y)
    c.line(x, top, x + width, top)
    cx = x
    for cw in colw + [0]:
        c.line(cx, top, cx, top - total)
        cx += cw


def _expand_conj(block, verbs):
    names, tenses = block["verbs"], block["tenses"]
    tables = []

    def cell(v, tense, i):
        val = verbs[v][tense]
        if isinstance(val, str):
            return val if i == 0 else ""
        return val[i]

    if len(names) == 1:
        v = names[0]
        header = [f"**{v}** ~{verbs[v]['en']}~"] + list(tenses)
        rows = [[_PERSONS[i]] + [cell(v, t, i) for t in tenses] for i in range(6)]
        n = len(tenses)
        widths = [0.22] + [0.78 / n] * n
        tables.append({"header": header, "rows": rows, "widths": widths, "gray_rows": [_VOS_ROW]})
    else:
        n = len(names)
        widths = [0.22] + [0.78 / n] * n
        for t in tenses:
            header = [t] + [f"**{v}** ~{verbs[v]['en']}~" for v in names]
            rows = [[_PERSONS[i]] + [cell(v, t, i) for v in names] for i in range(6)]
            tables.append({"header": header, "rows": rows, "widths": widths,
                           "gray_rows": [_VOS_ROW]})
    return tables


_TABLE_GAP = 3.0


def _stack_height(tables, width):
    return sum(_table_height(t, width) for t in tables) + _TABLE_GAP * (len(tables) - 1)


def _compare_table(block):
    return {"header": [block["left"], block["right"]], "rows": block["rows"],
            "widths": [0.5, 0.5], "gray_rows": []}


# --------------------------------------------------------------------------
# Timeline
# --------------------------------------------------------------------------
_TL_H = 26.0
_TL_LINE = 13.0  # line sits this far below the block top
_TL_PAD = 8.0
_TL_ARROW = 6.0


def _timeline_height(block, width):
    h = _TL_H
    cap = block.get("caption")
    if cap:
        _, ch = _text_h(cap, width, BODY_SIZE)
        h += ch + 2
    return h


def _draw_timeline(c, frame_x, top, block, width):
    ly = top - _TL_LINE
    x0, x1 = frame_x + _TL_PAD, frame_x + width - _TL_PAD
    c.setStrokeGray(0)
    c.setFillGray(0)
    c.setLineWidth(0.8)
    c.line(x0, ly, x1 - _TL_ARROW, ly)
    p = c.beginPath()
    p.moveTo(x1, ly)
    p.lineTo(x1 - _TL_ARROW, ly + 2.5)
    p.lineTo(x1 - _TL_ARROW, ly - 2.5)
    p.close()
    c.drawPath(p, stroke=0, fill=1)
    span = (x1 - _TL_ARROW - 4) - x0
    for i, ev in enumerate(sorted(block["events"], key=lambda e: e["pos"])):
        ex = x0 + ev["pos"] * span
        mark = ev.get("mark", "point")
        if mark == "now":
            c.circle(ex, ly, 3.2, stroke=1, fill=1)
        elif mark == "past":
            c.setFillGray(1)
            c.circle(ex, ly, 2.4, stroke=1, fill=1)
            c.setFillGray(0)
        else:
            c.circle(ex, ly, 1.8, stroke=1, fill=1)
        style = "bold" if mark == "now" else "normal"
        chunks = [(style if s == "normal" else s, t) for s, t in parse_rich(ev["label"])]
        lw = sum(_w(s, t, CELL_SIZE) for s, t in chunks)
        lx = min(max(ex - lw / 2, frame_x), frame_x + width - lw)
        base = ly + 5 if i % 2 == 0 else ly - 5 - CELL_SIZE * 0.8
        _draw_lines(c, [chunks], lx, base + CELL_SIZE * 0.82, CELL_SIZE, CELL_SIZE + 1)
    cap = block.get("caption")
    if cap:
        lines, _ = _text_h(cap, width, BODY_SIZE)
        _draw_lines(c, lines, frame_x, top - _TL_H - 1, BODY_SIZE, _body_lead(BODY_SIZE))


# --------------------------------------------------------------------------
# Decision chart
# --------------------------------------------------------------------------
_CH_LABEL_FR = 0.50
_CH_TENSE_FR = 0.62
_NODE_GAP = 4.0


def _chart_plan(block, width):
    label_w = width * _CH_LABEL_FR - _BULLET_INDENT
    tense_w = width * (1 - _CH_TENSE_FR)
    nodes = []
    for node in block["nodes"]:
        qlines, qh = _text_h(node["q"], width, BODY_SIZE, bold=True)
        answers, ah = [], 0.0
        for a in node["answers"]:
            ll = wrap_rich(a["label"], label_w, CELL_SIZE)
            tl = _wrap_chunks(_bold(parse_rich(a["tense"])), tense_w, CELL_SIZE)
            n = max(len(ll), len(tl), 1)
            h = n * (CELL_SIZE + 1.6) + 1.0
            answers.append((a, ll, tl, h))
            ah += h
        nodes.append((qlines, qh, answers, qh + ah + _NODE_GAP))
    return nodes


def _chart_height(block, width):
    return sum(n[3] for n in _chart_plan(block, width))


def _draw_chart(c, ctx, x, top, block, width):
    y = top
    lead = CELL_SIZE + 1.6
    for qlines, qh, answers, nh in _chart_plan(block, width):
        _draw_lines(c, qlines, x, y, BODY_SIZE, _body_lead(BODY_SIZE))
        y -= qh
        for a, ll, tl, h in answers:
            _draw_lines(c, ll, x + _BULLET_INDENT, y, CELL_SIZE, lead)
            tx = x + width * _CH_TENSE_FR
            _draw_lines(c, tl, tx, y, CELL_SIZE, lead)
            # connector arrow drawn as shapes (no glyph arrows in cp1252)
            ay = y - CELL_SIZE * 0.45
            ax0 = x + width * _CH_LABEL_FR + 2
            ax1 = tx - 3
            c.setStrokeGray(0.3)
            c.setLineWidth(0.5)
            c.line(ax0, ay, ax1 - 3, ay)
            p = c.beginPath()
            p.moveTo(ax1, ay)
            p.lineTo(ax1 - 3, ay + 1.6)
            p.lineTo(ax1 - 3, ay - 1.6)
            p.close()
            c.setFillGray(0.3)
            c.drawPath(p, stroke=0, fill=1)
            c.setFillGray(0)
            tw = max(_line_w(ln, CELL_SIZE) for ln in tl) if tl else 0
            rect = (tx, y - h + 0.5, tx + tw, y)
            if ctx.link(rect, a["dest"]):
                for i, ln in enumerate(tl):
                    uy = y - i * lead - CELL_SIZE * 0.82 - 1.0
                    c.setStrokeGray(0)
                    c.line(tx, uy, tx + _line_w(ln, CELL_SIZE), uy)
            y -= h
        y -= _NODE_GAP
    c.setStrokeGray(0)


# --------------------------------------------------------------------------
# xref
# --------------------------------------------------------------------------
_XREF_PAGE_W = 24.0


def _xref_lines(block, width):
    w = width - (_XREF_PAGE_W if block.get("dest") else 0)
    return _text_h(block["text"], w, BODY_SIZE, bold=bool(block.get("dest")))


# --------------------------------------------------------------------------
# Public block API
# --------------------------------------------------------------------------
def block_height(block: dict, width: float, verbs: dict) -> float:
    t = block["type"]
    if t == "heading":
        _, h = _text_h(block["text"], width, HEAD_SIZE, bold=True)
        return h + 4.0
    if t == "text":
        _, h = _text_h(block["text"], width, BODY_SIZE)
        return h + 2.0
    if t == "bullets":
        w = width - _BULLET_INDENT
        return sum(_text_h(it, w, BODY_SIZE)[1] + 1.0 for it in block["items"])
    if t == "example":
        w = width - _EXAMPLE_INDENT
        h = _text_h(block["es"], w, BODY_SIZE)[1] + _text_h(f"~{block['en']}~", w, BODY_SIZE)[1]
        return h + 3.0
    if t == "spacer":
        return float(block["h"])
    if t == "table":
        return _table_height(block, width)
    if t == "conj":
        return _stack_height(_expand_conj(block, verbs), width)
    if t == "compare":
        return _table_height(_compare_table(block), width)
    if t == "timeline":
        return _timeline_height(block, width)
    if t == "chart":
        return _chart_height(block, width)
    if t == "xref":
        return _xref_lines(block, width)[1] + 1.0
    raise ValueError(f"unknown block type {t!r}")


def draw_block(c, frame: Frame, block: dict, ctx) -> None:
    t = block["type"]
    h = block_height(block, frame.width, ctx.verbs)
    top = frame.take(h)
    x, w = frame.x, frame.width
    c.saveState()
    if t == "heading":
        lines, _ = _text_h(block["text"], w, HEAD_SIZE, bold=True)
        _draw_lines(c, lines, x, top, HEAD_SIZE, _body_lead(HEAD_SIZE))
        c.setStrokeGray(0.5)
        c.setLineWidth(0.4)
        c.line(x, top - h + 1.5, x + w, top - h + 1.5)
    elif t == "text":
        lines, _ = _text_h(block["text"], w, BODY_SIZE)
        _draw_lines(c, lines, x, top, BODY_SIZE, _body_lead(BODY_SIZE))
    elif t == "bullets":
        y = top
        for it in block["items"]:
            lines, lh = _text_h(it, w - _BULLET_INDENT, BODY_SIZE)
            c.setFillGray(0)
            c.circle(x + 2.5, y - BODY_SIZE * 0.5 - 0.4, 1.1, stroke=0, fill=1)
            _draw_lines(c, lines, x + _BULLET_INDENT, y, BODY_SIZE, _body_lead(BODY_SIZE))
            y -= lh + 1.0
    elif t == "example":
        iw = w - _EXAMPLE_INDENT
        es, eh = _text_h(block["es"], iw, BODY_SIZE)
        en, nh = _text_h(f"~{block['en']}~", iw, BODY_SIZE)
        c.setStrokeGray(0.6)
        c.setLineWidth(0.8)
        c.line(x + 1.5, top - 0.5, x + 1.5, top - eh - nh - 2.5)
        _draw_lines(c, es, x + _EXAMPLE_INDENT, top, BODY_SIZE, _body_lead(BODY_SIZE))
        _draw_lines(c, en, x + _EXAMPLE_INDENT, top - eh, BODY_SIZE, _body_lead(BODY_SIZE))
    elif t == "spacer":
        pass
    elif t == "table":
        _draw_table(c, x, top, block, w)
    elif t == "conj":
        y = top
        for tb in _expand_conj(block, ctx.verbs):
            _draw_table(c, x, y, tb, w)
            y -= _table_height(tb, w) + _TABLE_GAP
    elif t == "compare":
        _draw_table(c, x, top, _compare_table(block), w, header_shade=SHADE_INSTRUCTIONS)
    elif t == "timeline":
        _draw_timeline(c, x, top, block, w)
    elif t == "chart":
        _draw_chart(c, ctx, x, top, block, w)
    elif t == "xref":
        lines, lh = _xref_lines(block, w)
        dest = block.get("dest")
        _draw_lines(c, lines, x, top, BODY_SIZE, _body_lead(BODY_SIZE))
        if dest:
            lead = _body_lead(BODY_SIZE)
            rect = (x, top - lh, x + w, top)
            if ctx.link(rect, dest):
                c.setStrokeGray(0)
                c.setLineWidth(0.4)
                for i, ln in enumerate(lines):
                    uy = top - i * lead - BODY_SIZE * 0.82 - 1.0
                    c.line(x, uy, x + _line_w(ln, BODY_SIZE), uy)
                pg = ctx.page_of(dest)
                if pg is not None:
                    c.setFont(FONT_NORMAL, CELL_SIZE)
                    c.setFillGray(0)
                    c.drawRightString(x + w, top - BODY_SIZE * 0.82, f"p.{pg}")
    c.restoreState()
