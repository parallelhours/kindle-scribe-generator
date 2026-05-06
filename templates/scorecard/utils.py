# Copyright (C) 2026 Paul Monday — GNU GPL v3 or later. See LICENSE.
# Re-export shared constants so template.py can use a single `import utils as U`
from core.dimensions import PAGE_W, PAGE_H, MARGIN          # noqa: F401
from core.style import (                                     # noqa: F401
    BORDER_LW, GRID_LW, SUBCELL_LW, DIAMOND_LW,
    SHADE_INSTRUCTIONS, SHADE_HEADER_BG,
    COLOR_BLACK, COLOR_LABEL_GRAY,
    FONT_NORMAL, FONT_BOLD,
)

# ── Lineup page column widths (pt) ───────────────────────────────────────────
# Content width: PAGE_W - 2*MARGIN = 324.96 pt
COL_NUM    = 14
COL_LINEUP = 68.96
COL_POS    = 16
COL_INNING = 18      # each of innings 1–10
COL_AB     = 12
COL_R      = 10
COL_H      = 10
COL_RBI    = 14

LINEUP_COLS = (
    [COL_NUM, COL_LINEUP, COL_POS]
    + [COL_INNING] * 10
    + [COL_AB, COL_R, COL_H, COL_RBI]
)  # 17 columns, sum ≈ 324.96 pt

LINEUP_COL_LABELS = (
    ["#", "Line Up", "Pos"]
    + [str(i) for i in range(1, 11)]
    + ["AB", "R", "H", "RBI"]
)

# ── Row heights (pt) ─────────────────────────────────────────────────────────
ROW_TEAM_LABEL = 18
ROW_HEADER     = 12
ROW_STARTER    = 30   # 9 starters
ROW_SUB        = 20.5 # 4 substitutes (remaining rows become summary section)
DIVIDER_H      = 4    # gap between starters and subs


def col_x_positions():
    """Return the left-edge x coordinate for each of the 17 lineup columns."""
    x = MARGIN
    positions = []
    for w in LINEUP_COLS:
        positions.append(x)
        x += w
    return positions


def draw_diamond(c, x, y, w, h):
    """Draw a scoring diamond cell.

    Args:
        c: ReportLab canvas
        x: left edge of cell (pt)
        y: bottom edge of cell (pt) — ReportLab origin is bottom-left
        w: cell width (pt)
        h: cell height (pt)
    """
    labels = ["1B", "2B", "3B", "HR", "BB"]
    label_col_w = 6.5
    label_font_size = 2.8
    line_h = (h - 2.0) / len(labels)
    c.setFont(FONT_NORMAL, label_font_size)
    c.setFillColorRGB(*COLOR_LABEL_GRAY)
    for i, lbl in enumerate(labels):
        ly = y + h - 1.5 - (i + 0.7) * line_h
        c.drawString(x + 0.8, ly, lbl)
    c.setFillColorRGB(*COLOR_BLACK)

    dx = x + label_col_w
    dw = w - label_col_w
    cx = dx + dw / 2
    cy = y + h / 2
    d = min(dw, h) * 0.44

    p = c.beginPath()
    p.moveTo(cx,     cy + d)
    p.lineTo(cx + d, cy)
    p.lineTo(cx,     cy - d)
    p.lineTo(cx - d, cy)
    p.close()
    c.setLineWidth(DIAMOND_LW)
    c.drawPath(p, stroke=1, fill=0)
