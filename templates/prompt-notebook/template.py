# Copyright (C) 2026 Paul Monday — GNU GPL v3 or later. See LICENSE.
from datetime import date as _date
from math import ceil

from reportlab.pdfgen import canvas as rl_canvas

from core import dimensions as D
from core import style as S


METADATA = {
    "name":        "Prompt Notebook",
    "description": "Structured prompt notebook using CO-STAR+ or P.R.O.M.P.T. framework",
    "output":      "prompt-notebook.pdf",
    "pages":       5,
    "cover_fields": [
        {"name": "title", "prompt": "Notebook title", "default": "Prompt Notebook"},
        {"name": "date",  "prompt": "Date",           "default": _date.today().isoformat()},
    ],
    "template_fields": [
        {"name": "count",     "prompt": "Number of prompts",               "default": "1"},
        {"name": "layout",    "prompt": "Layout (compact/expanded)",       "default": "compact"},
        {"name": "framework", "prompt": "Framework (co-star/prompt)",      "default": "co-star"},
    ],
}


# ── Framework definitions ──────────────────────────────────────────────────────

_CO_STAR = (
    ("C", "Context",     "Background, situation, and constraints"),
    ("O", "Objective",   "The specific task or goal"),
    ("S", "Style",       "Structural approach (technical, conversational, academic)"),
    ("T", "Tone",        "Emotional quality (formal, urgent, encouraging)"),
    ("A", "Audience",    "Who will read or use the output"),
    ("R", "Response",    "Exact format, structure, and length of the output"),
    ("E", "Examples",    "Few-shot samples showing what you want"),
)

_PROMPT_FW = (
    ("P", "Persona",     "Who is the AI acting as? (senior engineer, tutor, editor)"),
    ("R", "Request",     "What exactly do you want done? (the objective)"),
    ("O", "Outline",     "How should the output look? (format, structure, length)"),
    ("M", "Material",    "What context does the AI need? (background, constraints)"),
    ("P", "Preference",  "What's the style, tone, and audience level?"),
    ("T", "Test",        "How will you verify success? (examples, checks, tests)"),
)

_FRAMEWORKS = {"co-star": (_CO_STAR, "CO-STAR+"), "prompt": (_PROMPT_FW, "P.R.O.M.P.T.")}

_CO_STAR_EXAMPLES = (
    "e.g. I\u2019m a tech lead on a mobile payment app finishing Q2 sprint.",
    "e.g. Write a status update email for stakeholders ahead of the demo.",
    "e.g. Professional email with sections: shipped, blocked, next steps.",
    "e.g. Confident and transparent \u2014 celebrate wins, flag risks honestly.",
    "e.g. VP of Product, Eng Director, PM team \u2014 needs the headline fast.",
    "e.g. 3\u20134 paragraphs, bullet points for blockers, max 250 words.",
    "e.g. Start: \u2018Hi team, here\u2019s where we stand for the Q2 demo\u2026\u2019",
)

_PROMPT_EXAMPLES = (
    "e.g. You are a senior security engineer specializing in Python web apps.",
    "e.g. Review this DRF viewset for security vulnerabilities.",
    "e.g. List findings by severity with vulnerable code, issue, and fix.",
    "e.g. The viewset handles user registration via email, password, profile.",
    "e.g. Thorough but concise \u2014 assume reader is a mid-level Django dev.",
    "e.g. Verify you caught SQL injection, CSRF, and password storage issues.",
)

_CO_STAR_ASSEMBLED = (
    "I\u2019m a tech lead on a team building a mobile payment app finishing Q2 sprint. "
    "Write a status update email for stakeholders ahead of the demo. "
    "Use a professional email format with clear sections for what shipped, "
    "what\u2019s blocked, and next steps. "
    "Keep the tone confident and transparent \u2014 celebrate wins but flag risks honestly. "
    "The audience is the VP of Product, Eng Director, and PM team "
    "\u2014 they need the headline fast. "
    "Format as 3\u20134 paragraphs with bullet points for blockers, max 250 words. "
    "Here\u2019s a starting point: \u2018Hi team, here\u2019s where we stand for the Q2 demo.\u2019"
)

_PROMPT_ASSEMBLED = (
    "You are a senior security engineer who specializes in Python web applications. "
    "Review this Django REST Framework viewset for security vulnerabilities. "
    "List findings by severity (Critical, High, Medium, Low). "
    "For each finding, show the vulnerable code, explain the issue, and provide a fix. "
    "The viewset handles user registration \u2014 email, password, and profile data "
    "\u2014 in a Django project using TokenAuth. "
    "Be thorough but concise. Assume the reader is a mid-level Django developer. "
    "Use clear, direct language. "
    "Verify you caught SQL injection, missing CSRF, and password storage issues, "
    "and check that fix code is syntactically valid Python."
)


# ── Layout constants ──────────────────────────────────────────────────────────

_CW = D.PAGE_W - 2 * D.MARGIN
_GAP = 4.0
_LINE_SPACING = 11.0


# ── Helpers ────────────────────────────────────────────────────────────────────

def _get_framework(fw: str):
    tup = _FRAMEWORKS.get(fw, _FRAMEWORKS["co-star"])
    return tup[0]


def _get_framework_name(fw: str) -> str:
    tup = _FRAMEWORKS.get(fw, _FRAMEWORKS["co-star"])
    return tup[1]


def _get_examples(fw: str):
    return _CO_STAR_EXAMPLES if fw == "co-star" else _PROMPT_EXAMPLES


def _get_assembled(fw: str):
    return _CO_STAR_ASSEMBLED if fw == "co-star" else _PROMPT_ASSEMBLED


def _calc_page_count(count: int, layout: str, framework: str) -> int:
    n = len(_get_framework(framework))
    if layout == "compact":
        return 1 + count
    return 1 + count * ceil(n / 2)


def _draw_footer(c, label: str, page: int, total: int) -> None:
    c.setFont(S.FONT_NORMAL, 5)
    c.setFillGray(0.45)
    c.drawCentredString(D.PAGE_W / 2, 3, f"Page {page} \u2014 {label}")
    c.setFillGray(0)


def _wrap_draw(c, text, x, y, max_w, font, size, leading):
    c.setFont(font, size)
    words = text.split()
    lines = []
    cur = ""
    for w in words:
        test = cur + (" " if cur else "") + w
        if c.stringWidth(test, font, size) <= max_w:
            cur = test
        else:
            lines.append(cur)
            cur = w
    lines.append(cur)
    for line in lines:
        c.drawString(x, y, line)
        y -= leading
    return y


def _writing_lines(c, x, y, w, h) -> None:
    if h < _LINE_SPACING:
        return
    c.setLineWidth(0.2)
    c.setStrokeGray(0.78)
    n = int(h / _LINE_SPACING)
    for i in range(1, n + 1):
        ly = y + h - i * _LINE_SPACING
        if ly > y + 1:
            c.line(x + 3, ly, x + w - 3, ly)
    c.setStrokeGray(0)


def _card_bg(c, x, y, w, h, r=2) -> None:
    c.setFillGray(0.97)
    c.setStrokeGray(0.55)
    c.setLineWidth(0.3)
    c.roundRect(x, y, w, h, r, stroke=1, fill=1)


def _letter_badge(c, x, y, sz, letter) -> None:
    c.setFillGray(0.2)
    c.roundRect(x, y, sz, sz, 1.5, stroke=0, fill=1)
    c.setFillGray(1)
    c.setFont(S.FONT_BOLD, sz * 0.55)
    c.drawCentredString(x + sz / 2, y + (sz - sz * 0.55) / 2 + 0.5, letter)
    c.setFillGray(0)


def _header_fields(c, top: float, prompt_num: int) -> float:
    c.setFont(S.FONT_NORMAL, 6)
    c.setFillGray(0.4)
    c.drawString(D.MARGIN, top - 8, f"Prompt {prompt_num}")
    c.drawString(D.MARGIN + 60, top - 8, "Date: ____________________")
    c.drawString(D.MARGIN + 175, top - 8, "Project: ________________")
    c.drawString(D.MARGIN, top - 18, "Title: ")
    c.line(D.MARGIN + 24, top - 21, D.PAGE_W - D.MARGIN, top - 21)
    c.setStrokeGray(0)
    c.setFillGray(0)
    return top - 24


def _component_card(c, letter, name, desc, x, y, w, h) -> None:
    _card_bg(c, x, y, w, h)

    hdr_h = 14
    hdr_bot = y + h - hdr_h
    badge_sz = 10
    bx = x + 3
    by = hdr_bot + (hdr_h - badge_sz) / 2
    _letter_badge(c, bx, by, badge_sz, letter)

    c.setFont(S.FONT_BOLD, 6)
    c.drawString(bx + badge_sz + 3, hdr_bot + hdr_h - 7.5, name)
    c.setFont(S.FONT_NORMAL, 4.5)
    c.setFillGray(0.5)
    c.drawString(bx + badge_sz + 3, hdr_bot + hdr_h - 14, desc)
    c.setFillGray(0)

    wh = hdr_bot - 2 - (y + 2)
    if wh > 6:
        _writing_lines(c, x, y + 2, w, wh)


# ── Cover ──────────────────────────────────────────────────────────────────────

def draw_cover(c, title="Prompt Notebook", date="", **_):
    c.setFillGray(0.15)
    c.rect(0, 0, D.PAGE_W, D.PAGE_H, stroke=0, fill=1)
    c.setFillGray(1)
    c.setFont(S.FONT_BOLD, 18)
    c.drawCentredString(D.PAGE_W / 2, D.PAGE_H * 0.6, title)
    c.setFont(S.FONT_NORMAL, 10)
    c.setFillGray(0.7)
    c.drawCentredString(D.PAGE_W / 2, D.PAGE_H * 0.6 - 22, date)
    c.setFillGray(0.4)
    c.setFont(S.FONT_NORMAL, 7)
    c.drawCentredString(D.PAGE_W / 2, D.PAGE_H * 0.4,
                        "Kindle Scribe \u2014 Prompt Notebook")
    c.setFillGray(0)


# ── Overview page ──────────────────────────────────────────────────────────────

def _draw_overview(c, framework: str) -> None:
    top = D.PAGE_H - D.MARGIN
    fw_name = _get_framework_name(framework)
    components = _get_framework(framework)
    examples = _get_examples(framework)
    assembled = _get_assembled(framework)

    # ── Title bar ──
    c.setFillGray(0.15)
    c.rect(D.MARGIN, top - 26, _CW, 26, stroke=0, fill=1)
    c.setFillGray(1)
    c.setFont(S.FONT_BOLD, 11)
    c.drawString(D.MARGIN + 6, top - 18, f"{fw_name} Prompt Framework")
    c.setFillGray(0)

    c.setFont(S.FONT_NORMAL, 5.5)
    c.setFillGray(0.45)
    c.drawString(D.MARGIN + 6, top - 32,
                 "Fill in each section, then read how they assemble into a prompt below.")
    c.setFillGray(0)

    # ── Table column widths ──
    col_l_w = 14
    col_n_w = 46
    col_d_w = 126
    col_gap = 2
    col_e_w = _CW - col_l_w - col_n_w - col_d_w - col_gap * 3
    col_ws = [col_l_w, col_n_w, col_d_w, col_e_w]
    col_xs = [D.MARGIN]
    for w in col_ws[:-1]:
        col_xs.append(col_xs[-1] + w + col_gap)
    headers = ["", "Component", "Definition", "Example"]

    # ── Table header row ──
    tbl_top = top - 38
    hdr_h = 11
    c.setFillGray(0.2)
    c.rect(D.MARGIN, tbl_top - hdr_h, _CW, hdr_h, stroke=0, fill=1)
    c.setFillGray(1)
    c.setFont(S.FONT_BOLD, 5)
    for lbl, cx, cw in zip(headers, col_xs, col_ws):
        if lbl:
            c.drawString(cx + 2, tbl_top - hdr_h + 3, lbl)
    c.setFillGray(0)

    # ── Data rows ──
    row_h = 33
    y = tbl_top - hdr_h

    for i, (letter, comp_name, desc) in enumerate(components):
        row_bot = y - row_h
        ex = examples[i]

        if i % 2 == 0:
            c.setFillGray(0.97)
            c.rect(D.MARGIN, row_bot, _CW, row_h, stroke=0, fill=1)

        c.setStrokeGray(0.55)
        c.setLineWidth(0.25)
        for cx, cw in zip(col_xs, col_ws):
            c.rect(cx, row_bot, cw, row_h, stroke=1, fill=0)

        _letter_badge(c, col_xs[0] + 2, row_bot + (row_h - 10) / 2, 10, letter)

        name_baseline = row_bot + row_h - 8
        c.setFont(S.FONT_BOLD, 5.5)
        c.drawString(col_xs[1] + 3, name_baseline, comp_name)

        c.setFont(S.FONT_NORMAL, 5)
        c.setFillGray(0.5)
        _wrap_draw(c, desc, col_xs[2] + 3, name_baseline,
                   col_d_w - 6, S.FONT_NORMAL, 5, 6.5)
        _wrap_draw(c, ex, col_xs[3] + 3, name_baseline,
                   col_e_w - 6, S.FONT_NORMAL, 5, 6.5)
        c.setFillGray(0)

        y = row_bot

    # ── Assembled prompt box ──
    box_top = y - 4
    box_bot = D.MARGIN
    box_h = box_top - box_bot

    c.setFillGray(0.95)
    c.setStrokeGray(0.4)
    c.setLineWidth(0.4)
    c.rect(D.MARGIN, box_bot, _CW, box_h, stroke=1, fill=1)

    ahdr_h = 14
    ahdr_bot = box_top - ahdr_h
    c.setFillGray(0.2)
    c.rect(D.MARGIN, ahdr_bot, _CW, ahdr_h, stroke=0, fill=1)
    c.setFillGray(1)
    c.setFont(S.FONT_BOLD, 6.5)
    c.drawString(D.MARGIN + 4, ahdr_bot + 4, "Assembled prompt:")
    c.setFillGray(0)

    text_top = ahdr_bot - 3
    _wrap_draw(c, assembled, D.MARGIN + 4, text_top,
               _CW - 8, S.FONT_NORMAL, 5, 7)
    c.setFillGray(0)


# ── Prompt pages ───────────────────────────────────────────────────────────────

def _draw_compact_prompt(c, prompt_num: int, framework: str) -> None:
    components = _get_framework(framework)
    top = D.PAGE_H - D.MARGIN
    hdr_bot = _header_fields(c, top, prompt_num)

    y_start = hdr_bot - _GAP
    avail = y_start - D.MARGIN
    n = len(components)
    card_h = (avail - _GAP * (n - 1)) / n

    for i, (letter, comp_name, desc) in enumerate(components):
        y = y_start - i * (card_h + _GAP) - card_h
        _component_card(c, letter, comp_name, desc, D.MARGIN, y, _CW, card_h)


def _draw_expanded_prompt(c, prompt_num: int, framework: str,
                          start_page: int, total: int) -> int:
    components = _get_framework(framework)
    n = len(components)
    pages_needed = ceil(n / 2)

    for pg in range(pages_needed):
        top = D.PAGE_H - D.MARGIN
        if pg == 0:
            hdr_bot = _header_fields(c, top, prompt_num)
            y_start = hdr_bot - _GAP - 2
        else:
            y_start = top - 2

        comps = components[pg * 2: pg * 2 + 2]
        page_avail = y_start - D.MARGIN
        n_comps = len(comps)
        card_h = (page_avail - _GAP * (n_comps - 1)) / n_comps

        for j, (letter, comp_name, desc) in enumerate(comps):
            y = y_start - j * (card_h + _GAP) - card_h
            _component_card(c, letter, comp_name, desc, D.MARGIN, y, _CW, card_h)

        _draw_footer(c, f"Prompt {prompt_num}", start_page + pg, total)
        c.showPage()

    return pages_needed


# ── Entry point ────────────────────────────────────────────────────────────────

def generate(output_path: str, **meta) -> None:
    title = meta.pop("title", None)
    date_ = meta.pop("date", None)
    has_cover = title is not None or date_ is not None

    count = int(meta.get("count", 1))
    layout = meta.get("layout", "expanded")
    framework = meta.get("framework", "co-star")

    total = _calc_page_count(count, layout, framework)
    if has_cover:
        total += 1

    c = rl_canvas.Canvas(output_path, pagesize=(D.PAGE_W, D.PAGE_H))

    page = 1
    if has_cover:
        draw_cover(c, title=title or "Prompt Notebook", date=date_ or "")
        c.showPage()
        page += 1

    _draw_overview(c, framework)
    _draw_footer(c, "Overview", page, total)
    c.showPage()
    page += 1

    for pn in range(1, count + 1):
        if layout == "compact":
            _draw_compact_prompt(c, pn, framework)
            _draw_footer(c, f"Prompt {pn}", page, total)
            c.showPage()
            page += 1
        else:
            used = _draw_expanded_prompt(c, pn, framework, page, total)
            page += used

    c.save()
