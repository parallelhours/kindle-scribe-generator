# Copyright (C) 2026 Paul Monday — GNU GPL v3 or later. See LICENSE.
from reportlab.pdfgen import canvas as rl_canvas
from core import dimensions as D
from core import style as S

METADATA = {
    "name":        "Weekly Planner",
    "description": "Daily planner — one page per day with schedule, tasks, and brain dump (default 7 days)",
    "output":      "weekly-activity-notebook.pdf",
    "pages":       7,
    "template_fields": [
        {"name": "first_day", "prompt": "First day (Monday/Sunday)", "default": "Monday"},
        {"name": "days",      "prompt": "Number of days",            "default": "7"},
    ],
}

_DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

# ── Layout constants ──────────────────────────────────────────────────────────
_CW          = D.PAGE_W - 2 * D.MARGIN          # 324.96 pt
_HEADER_H    = 26.0
_BRAIN_H     = 110.0
_BODY_H      = D.PAGE_H - 2 * D.MARGIN - _HEADER_H - _BRAIN_H   # ≈ 301.28 pt

_LEFT_FRAC   = 0.55
_LCW         = _CW * _LEFT_FRAC                 # ≈ 178.73 pt
_RCW         = _CW - _LCW                       # ≈ 146.23 pt

_SEC_HDR_H   = 12.0
_TOP3_ROWS   = 3
_TODO_ROWS   = 6
_PERS_ROWS   = 4
_TOTAL_ROWS  = _TOP3_ROWS + _TODO_ROWS + _PERS_ROWS    # 13
_ROW_H       = (_BODY_H - 3 * _SEC_HDR_H) / _TOTAL_ROWS   # ≈ 20.41 pt

_N_SLOTS     = 17       # 5 am … 9 pm inclusive
_START_HOUR  = 5
_SLOT_H      = (_BODY_H - _SEC_HDR_H) / _N_SLOTS          # ≈ 17.02 pt

_BRAIN_HDR_H = 14.0
_VIBE_H      = 14.0
_FACE_R      = 4.5
_FACE_GAP    = 3.0

# Grayscale fills
_FILL_DARK   = 0.17
_FILL_MID    = 0.30
_FILL_LIGHT  = 0.55

# Line weights / sizes
_BOX_SZ      = 7.0
_BOX_LW      = 0.8
_LINE_LW     = 0.3
_GRID_LW     = 0.5


def _resolve_start(first_day: str) -> int:
    name = first_day.capitalize()
    return _DAYS.index(name) if name in _DAYS else 0


def generate(output_path: str, **meta) -> None:
    first_day = meta.get("first_day", "Monday")
    days = int(meta.get("days", 7))
    start = _resolve_start(first_day)
    c = rl_canvas.Canvas(output_path, pagesize=(D.PAGE_W, D.PAGE_H))
    for i in range(days):
        day_name = _DAYS[(start + i) % 7].upper()
        _draw_page(c, day_name)
        c.showPage()
    c.save()


def _draw_header(c, day_name: str) -> None:
    top = D.PAGE_H - D.MARGIN
    bot = top - _HEADER_H
    c.setFillGray(_FILL_DARK)
    c.rect(D.MARGIN, bot, _CW, _HEADER_H, stroke=0, fill=1)
    c.setFillGray(1)
    c.setFont(S.FONT_BOLD, 11)
    c.drawCentredString(D.PAGE_W / 2, bot + (_HEADER_H - 11) / 2, day_name)
    c.setFillGray(0)


def _draw_column_border(c) -> None:
    body_top = D.PAGE_H - D.MARGIN - _HEADER_H   # ≈ 417.28
    body_bot = D.MARGIN + _BRAIN_H                # ≈ 116.0
    div_x    = D.MARGIN + _LCW

    c.setLineWidth(S.BORDER_LW)
    c.setStrokeGray(0.2)
    c.rect(D.MARGIN, body_bot, _CW, _BODY_H, stroke=1, fill=0)
    c.setLineWidth(_GRID_LW)
    c.line(div_x, body_bot, div_x, body_top)
    c.setLineWidth(1)
    c.setStrokeGray(0)


def _draw_page(c, day_name: str) -> None:
    _draw_header(c, day_name)
    _draw_column_border(c)
    _draw_left_column(c)
    _draw_right_column(c)
    _draw_brain_dump(c)


def _draw_section_header(c, label: str, x: float, y_top: float, width: float,
                         fill_gray: float = _FILL_MID) -> None:
    """Draw a section header bar with centered label."""
    bot = y_top - _SEC_HDR_H
    c.setFillGray(fill_gray)
    c.rect(x, bot, width, _SEC_HDR_H, stroke=0, fill=1)
    c.setFillGray(1)
    c.setFont(S.FONT_BOLD, 6.5)
    c.drawCentredString(x + width / 2, bot + (_SEC_HDR_H - 6.5) / 2 + 0.5, label)
    c.setFillGray(0)


def _draw_checkbox_row(c, x_left: float, x_right: float,
                       row_top: float, row_h: float) -> None:
    """Draw a single checkbox row with checkbox, line, and bottom divider."""
    cy    = row_top - row_h / 2          # vertical center
    box_x = x_left + 4.0
    box_y = cy - _BOX_SZ / 2

    c.setLineWidth(_BOX_LW)
    c.setStrokeGray(0.3)
    c.roundRect(box_x, box_y, _BOX_SZ, _BOX_SZ, 1, stroke=1, fill=0)

    c.setLineWidth(_LINE_LW)
    c.setStrokeGray(0.65)
    c.line(box_x + _BOX_SZ + 3.5, cy, x_right - 4.0, cy)

    # Faint row separator
    c.setLineWidth(0.2)
    c.setStrokeGray(0.85)
    c.line(x_left, row_top - row_h, x_right, row_top - row_h)
    c.setLineWidth(1)
    c.setStrokeGray(0)


def _draw_left_column(c) -> None:
    """Draw left column with three task sections: TOP 3, TO-DO, PERSONAL."""
    lx       = D.MARGIN
    rx       = D.MARGIN + _LCW
    body_top = D.PAGE_H - D.MARGIN - _HEADER_H   # ≈ 417.28

    sections = [
        ("TOP 3",    _TOP3_ROWS),
        ("TO-DO",    _TODO_ROWS),
        ("PERSONAL", _PERS_ROWS),
    ]

    y = body_top
    for label, n_rows in sections:
        _draw_section_header(c, label, lx, y, _LCW)
        y -= _SEC_HDR_H
        for _ in range(n_rows):
            _draw_checkbox_row(c, lx, rx, y, _ROW_H)
            y -= _ROW_H


def _draw_right_column(c) -> None:
    rx       = D.MARGIN + _LCW           # left edge of right column
    rx_end   = D.PAGE_W - D.MARGIN       # right edge
    body_top = D.PAGE_H - D.MARGIN - _HEADER_H   # ≈ 417.28

    _draw_section_header(c, "SCHEDULE", rx, body_top, _RCW, fill_gray=_FILL_LIGHT)

    slots_top  = body_top - _SEC_HDR_H
    time_col_w = 22.0
    line_x1    = rx + time_col_w
    line_x2    = rx_end - 2.0

    for i in range(_N_SLOTS):
        hour = _START_HOUR + i
        if hour < 12:
            label = f"{hour} am"
        elif hour == 12:
            label = "12 pm"
        else:
            label = f"{hour - 12} pm"

        slot_top = slots_top - i * _SLOT_H
        slot_mid = slot_top - _SLOT_H / 2

        c.setFont(S.FONT_NORMAL, 6.5)
        c.setFillGray(0.55)
        c.drawRightString(rx + time_col_w - 2.0, slot_mid - 2.5, label)
        c.setFillGray(0)

        c.setLineWidth(_LINE_LW)
        c.setStrokeGray(0.68)
        c.line(line_x1, slot_mid, line_x2, slot_mid)

        c.setLineWidth(0.2)
        c.setStrokeGray(0.87)
        c.line(rx + 2, slot_top - _SLOT_H, rx_end - 2, slot_top - _SLOT_H)
        c.setLineWidth(1)
        c.setStrokeGray(0)


def _draw_face(c, cx: float, cy: float, mood: int) -> None:
    """Draw a simple mood face. mood: 0 = very sad, 4 = very happy."""
    r  = _FACE_R
    lw = 0.6

    c.setLineWidth(lw)
    c.setStrokeGray(0.35)
    c.setFillGray(1.0)
    c.circle(cx, cy, r, stroke=1, fill=1)

    # Eyes
    c.setFillGray(0.3)
    eye_y = cy + r * 0.28
    c.circle(cx - r * 0.32, eye_y, r * 0.13, stroke=0, fill=1)
    c.circle(cx + r * 0.32, eye_y, r * 0.13, stroke=0, fill=1)

    # Mouth — bezier for sad/happy, line for neutral
    mx1 = cx - r * 0.42
    mx2 = cx + r * 0.42
    my  = cy - r * 0.22
    ctrl_dy = [-2.4, -1.1, 0.0, 1.1, 2.4][mood]

    c.setLineWidth(lw)
    c.setStrokeGray(0.35)
    if ctrl_dy == 0.0:
        c.line(mx1, my, mx2, my)
    else:
        ctrl_y = my + ctrl_dy
        c.bezier(mx1, my, cx - r * 0.18, ctrl_y, cx + r * 0.18, ctrl_y, mx2, my)

    c.setFillGray(0)
    c.setStrokeGray(0)


def _draw_brain_dump(c) -> None:
    brain_top = D.MARGIN + _BRAIN_H    # ≈ 116.0
    brain_bot = D.MARGIN               # 6.0
    lx  = D.MARGIN
    rx  = D.PAGE_W - D.MARGIN

    # Outer border
    c.setLineWidth(S.BORDER_LW)
    c.setStrokeGray(0.2)
    c.rect(lx, brain_bot, _CW, _BRAIN_H, stroke=1, fill=0)

    # Header bar
    hdr_bot = brain_top - _BRAIN_HDR_H
    c.setFillGray(_FILL_DARK)
    c.rect(lx, hdr_bot, _CW, _BRAIN_HDR_H, stroke=0, fill=1)
    c.setFillGray(1)
    c.setFont(S.FONT_BOLD, 7)
    c.drawString(lx + 5, hdr_bot + (_BRAIN_HDR_H - 7) / 2 + 0.5, "BRAIN DUMP")
    c.setFont(S.FONT_NORMAL, 5.5)
    c.setFillGray(0.8)
    c.drawRightString(rx - 5, hdr_bot + (_BRAIN_HDR_H - 5.5) / 2 + 0.5,
                      "sketch  \xb7  capture  \xb7  offload")
    c.setFillGray(0)

    # Vibe Check strip — rule line above, label + 5 faces right-aligned
    vibe_top = brain_bot + _VIBE_H
    c.setLineWidth(0.3)
    c.setStrokeGray(0.68)
    c.line(lx + 2, vibe_top, rx - 2, vibe_top)
    c.setStrokeGray(0)

    face_total_w = 5 * (2 * _FACE_R) + 4 * _FACE_GAP   # 5 faces + gaps
    strip_right  = rx - 5
    face_left    = strip_right - face_total_w
    strip_cy     = brain_bot + _VIBE_H / 2

    label = "VIBE CHECK"
    c.setFont(S.FONT_BOLD, 6.5)
    label_w = c.stringWidth(label, S.FONT_BOLD, 6.5)
    c.setFillGray(0.35)
    c.drawString(face_left - 6.0 - label_w, strip_cy - 3.0, label)
    c.setFillGray(0)

    for i in range(5):
        face_cx = face_left + i * (2 * _FACE_R + _FACE_GAP) + _FACE_R
        _draw_face(c, face_cx, strip_cy, i)
    c.setLineWidth(1)
