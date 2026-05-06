# Copyright (C) 2026 Paul Monday — GNU GPL v3 or later. See LICENSE.
import math
from reportlab.pdfgen import canvas as rl_canvas
from templates.scorecard import utils as U

METADATA = {
    "name": "Baseball Scorecard",
    "description": "6-page baseball scoring sheet optimized for Kindle Scribe",
    "output": "2026-05-06-mets-rockies.pdf",
    "pages": 6,
    "cover_fields": [
        {"name": "title",    "prompt": "Document title",    "default": "Baseball Scorecard"},
        {"name": "visitor",  "prompt": "Visiting team",     "default": ""},
        {"name": "home",     "prompt": "Home team",         "default": ""},
        {"name": "date",     "prompt": "Date (YYYY-MM-DD)", "default": ""},
        {"name": "ballpark", "prompt": "Ballpark",          "default": ""},
    ],
}


def generate(output_path: str, **meta) -> None:
    """Generate the scorecard PDF at output_path.

    Pass cover keyword args (title, visitor, home, date, ballpark) to prepend
    a cover page before the 6 scorecard pages.
    """
    c = rl_canvas.Canvas(output_path, pagesize=(U.PAGE_W, U.PAGE_H))

    if meta:
        draw_cover(c, **meta)
        c.showPage()

    draw_page1(c);  c.showPage()
    draw_page2(c);  c.showPage()
    for _ in range(4):
        draw_lineup_page(c)
        c.showPage()

    c.save()


# ── Cover page ────────────────────────────────────────────────────────────────

def draw_cover(c, title="Baseball Scorecard", visitor="", home="", date="",
               ballpark="", **_):
    """Draw a styled cover page."""
    cx = U.PAGE_W / 2
    banner_h = 20

    # Full-page light background
    c.setFillGray(0.96)
    c.rect(0, 0, U.PAGE_W, U.PAGE_H, stroke=0, fill=1)

    # Top dark banner with document title
    c.setFillGray(0.12)
    c.rect(0, U.PAGE_H - banner_h, U.PAGE_W, banner_h, stroke=0, fill=1)
    c.setFillGray(1)
    c.setFont(U.FONT_BOLD, 6.5)
    c.drawCentredString(cx, U.PAGE_H - banner_h + 7,
                        (title or "Baseball Scorecard").upper())
    c.setFillGray(0)

    # "BASEBALL SCORECARD" title block
    title_y = U.PAGE_H - banner_h - 32
    c.setFont(U.FONT_BOLD, 22)
    c.drawCentredString(cx, title_y, "BASEBALL")
    c.setFont(U.FONT_BOLD, 13)
    c.drawCentredString(cx, title_y - 20, "SCORECARD")

    # Rule under title
    rule_y = title_y - 30
    c.setLineWidth(0.6)
    c.setStrokeGray(0.4)
    c.line(U.MARGIN + 20, rule_y, U.PAGE_W - U.MARGIN - 20, rule_y)
    c.setStrokeGray(0)
    c.setLineWidth(U.GRID_LW)

    # Field diagram — larger scale, no legend
    d, R_out = 50, 115
    cr = d * 0.22
    hp_y = rule_y - R_out * 0.9 - cr - 18
    _draw_field_diagram(c, cx, hp_y, d=d, R_out=R_out)

    # Separator below catcher
    catcher_bottom = hp_y - 2 * cr  # center - radius - radius
    sep_y = catcher_bottom - 14
    c.setLineWidth(0.6)
    c.setStrokeGray(0.4)
    c.line(U.MARGIN + 20, sep_y, U.PAGE_W - U.MARGIN - 20, sep_y)
    c.setStrokeGray(0)
    c.setLineWidth(U.GRID_LW)

    # Teams
    teams_y = sep_y - 18
    if visitor or home:
        v = (visitor or "VISITOR").upper()
        h = (home or "HOME").upper()
        c.setFont(U.FONT_BOLD, 11)
        c.drawCentredString(cx, teams_y, f"{v}  vs  {h}")
    else:
        c.setFont(U.FONT_NORMAL, 9)
        c.setFillColorRGB(*U.COLOR_LABEL_GRAY)
        c.drawCentredString(cx, teams_y, "VISITOR  vs  HOME")
        c.setFillColorRGB(*U.COLOR_BLACK)

    # Date
    if date:
        c.setFont(U.FONT_BOLD, 8)
        c.drawCentredString(cx, teams_y - 18, date)

    # Ballpark
    if ballpark:
        c.setFont(U.FONT_NORMAL, 7)
        c.setFillColorRGB(*U.COLOR_LABEL_GRAY)
        c.drawCentredString(cx, teams_y - 34, ballpark)
        c.setFillColorRGB(*U.COLOR_BLACK)

    # Bottom dark banner
    c.setFillGray(0.12)
    c.rect(0, 0, U.PAGE_W, banner_h, stroke=0, fill=1)
    c.setFillGray(0)
    c.setStrokeGray(0)
    c.setLineWidth(U.GRID_LW)


# ── Lineup page ───────────────────────────────────────────────────────────────

def draw_lineup_page(c):
    """Draw one team's lineup scoring page (used for pages 3–6)."""
    content_w = U.PAGE_W - 2 * U.MARGIN
    xs = U.col_x_positions()
    top_y = U.PAGE_H - U.MARGIN

    # Team label row
    row_bot = top_y - U.ROW_TEAM_LABEL
    c.setLineWidth(U.BORDER_LW)
    c.rect(U.MARGIN, row_bot, content_w, U.ROW_TEAM_LABEL, stroke=1, fill=0)
    c.setFont(U.FONT_BOLD, 7)
    c.drawString(U.MARGIN + 2, row_bot + U.ROW_TEAM_LABEL * 0.35, "Team:")
    top_y = row_bot

    # Column header row
    row_bot = top_y - U.ROW_HEADER
    c.setFillGray(U.SHADE_HEADER_BG)
    c.rect(U.MARGIN, row_bot, content_w, U.ROW_HEADER, stroke=0, fill=1)
    c.setFillGray(0)
    c.setLineWidth(U.GRID_LW)
    c.rect(U.MARGIN, row_bot, content_w, U.ROW_HEADER, stroke=1, fill=0)
    c.setFont(U.FONT_BOLD, 5.5)
    for label, x, w in zip(U.LINEUP_COL_LABELS, xs, U.LINEUP_COLS):
        c.drawCentredString(x + w / 2, row_bot + U.ROW_HEADER * 0.3, label)
    top_y = row_bot

    # 9 starter rows
    for _ in range(9):
        _draw_batter_row(c, top_y, U.ROW_STARTER, xs)
        top_y -= U.ROW_STARTER

    # Substitutes divider
    top_y -= U.DIVIDER_H / 2
    c.setLineWidth(U.GRID_LW)
    c.setDash([3, 3])
    c.line(U.MARGIN, top_y, U.PAGE_W - U.MARGIN, top_y)
    c.setDash()
    c.setFont(U.FONT_NORMAL, 5)
    c.setFillColorRGB(*U.COLOR_LABEL_GRAY)
    c.drawCentredString(U.PAGE_W / 2, top_y + 1, "substitutes")
    c.setFillColorRGB(*U.COLOR_BLACK)
    top_y -= U.DIVIDER_H / 2

    # 4 substitute rows
    for _ in range(4):
        _draw_batter_row(c, top_y, U.ROW_SUB, xs)
        top_y -= U.ROW_SUB

    # Summary: Inning Totals + Pitcher section
    _draw_summary_rows(c, top_y, xs)


def _draw_batter_row(c, top_y, row_h, xs):
    row_bot = top_y - row_h
    for i, (x, w) in enumerate(zip(xs, U.LINEUP_COLS)):
        c.setLineWidth(U.GRID_LW)
        c.rect(x, row_bot, w, row_h, stroke=1, fill=0)
        if 3 <= i <= 12:
            U.draw_diamond(c, x, row_bot, w, row_h)


def _draw_summary_rows(c, top_y, xs):
    """Draw INNING TOTALS row and pitcher summary section."""
    content_w = U.PAGE_W - 2 * U.MARGIN

    # INNING TOTALS row
    row_h = 15
    row_bot = top_y - row_h
    label_w = xs[3] - xs[0]
    c.setLineWidth(U.GRID_LW)
    c.rect(xs[0], row_bot, label_w, row_h, stroke=1, fill=0)
    c.setFont(U.FONT_BOLD, 5.5)
    c.drawString(xs[0] + 2, row_bot + row_h * 0.58, "INNING")
    c.drawString(xs[0] + 2, row_bot + row_h * 0.2, "TOTALS")

    sub_w = 9
    sub_h = row_h / 2
    sub_x = xs[3] - 2 * sub_w - 3
    for row_i, (lbl_a, lbl_b) in enumerate([("R", "H"), ("E", "L")]):
        sy = row_bot + sub_h * (1 - row_i)
        for col_i, lbl in enumerate([lbl_a, lbl_b]):
            c.setLineWidth(U.GRID_LW)
            c.rect(sub_x + col_i * sub_w, sy, sub_w, sub_h, stroke=1, fill=0)
            c.setFont(U.FONT_BOLD, 4.5)
            c.drawCentredString(sub_x + col_i * sub_w + sub_w / 2, sy + sub_h * 0.3, lbl)

    for i in range(3, 17):
        c.setLineWidth(U.GRID_LW)
        c.rect(xs[i], row_bot, U.LINEUP_COLS[i], row_h, stroke=1, fill=0)
    top_y = row_bot

    # Pitcher section
    p_lr_w, p_no_w = 14, 16
    p_era_w, p_ip_w = 22, 20
    p_stat_w = 16
    p_p_w, p_bf_w = 16, 20
    p_name_w = content_w - p_lr_w - p_no_w - p_era_w - p_ip_w - 6 * p_stat_w - p_p_w - p_bf_w
    pitcher_widths = [p_lr_w, p_no_w, p_name_w, p_era_w, p_ip_w,
                      p_stat_w, p_stat_w, p_stat_w, p_stat_w, p_stat_w, p_stat_w,
                      p_p_w, p_bf_w]
    pitcher_labels = ["L/R", "No", "Pitcher", "ERA", "IP",
                      "H", "R", "ER", "BB", "SO", "HR", "P", "BF"]
    p_row_h = 9

    row_bot = top_y - p_row_h
    c.setFillGray(U.SHADE_HEADER_BG)
    c.rect(U.MARGIN, row_bot, content_w, p_row_h, stroke=0, fill=1)
    c.setFillGray(0)
    x = U.MARGIN
    for lbl, w in zip(pitcher_labels, pitcher_widths):
        c.setLineWidth(U.GRID_LW)
        c.rect(x, row_bot, w, p_row_h, stroke=1, fill=0)
        c.setFont(U.FONT_BOLD, 4.5)
        c.drawCentredString(x + w / 2, row_bot + p_row_h * 0.3, lbl)
        x += w
    top_y = row_bot

    for _ in range(3):
        row_bot = top_y - p_row_h
        x = U.MARGIN
        for w in pitcher_widths:
            c.setLineWidth(U.GRID_LW)
            c.rect(x, row_bot, w, p_row_h, stroke=1, fill=0)
            x += w
        top_y = row_bot


# ── Page 1: Game header ───────────────────────────────────────────────────────

def draw_page1(c):
    """Draw the game header page."""
    content_w = U.PAGE_W - 2 * U.MARGIN
    top_y = U.PAGE_H - U.MARGIN

    # Title
    c.setFont(U.FONT_BOLD, 11)
    c.drawCentredString(U.PAGE_W / 2, top_y - 10, "BASEBALL SCORECARD")
    top_y -= 16
    c.setLineWidth(U.BORDER_LW)
    c.line(U.MARGIN, top_y, U.PAGE_W - U.MARGIN, top_y)
    top_y -= 2

    # Info grid
    info_rows = [
        ("Notes:", None),
        ("☐  Visitor:", "Start Time:"),
        ("☐  Home:",    "End Time:"),
        ("Date:",       "Time of Game:"),
        ("Scorer:",     "Attendance:"),
        ("Wind:",       "Weather:"),
    ]
    row_h = 16
    for left_label, right_label in info_rows:
        row_bot = top_y - row_h
        if right_label is None:
            c.setLineWidth(U.GRID_LW)
            c.rect(U.MARGIN, row_bot, content_w, row_h, stroke=1, fill=0)
            c.setFont(U.FONT_NORMAL, 6)
            c.drawString(U.MARGIN + 2, row_bot + row_h * 0.35, left_label)
        else:
            half = content_w / 2
            c.setLineWidth(U.GRID_LW)
            c.rect(U.MARGIN, row_bot, half, row_h, stroke=1, fill=0)
            c.setFont(U.FONT_NORMAL, 6)
            c.drawString(U.MARGIN + 2, row_bot + row_h * 0.35, left_label)
            c.rect(U.MARGIN + half, row_bot, half, row_h, stroke=1, fill=0)
            c.drawString(U.MARGIN + half + 2, row_bot + row_h * 0.35, right_label)
        top_y = row_bot
    top_y -= 3

    # Instructions box (bottom of page)
    instructions_h = 62
    inst_y = U.MARGIN
    c.setFillGray(U.SHADE_INSTRUCTIONS)
    c.rect(U.MARGIN, inst_y, content_w, instructions_h, stroke=0, fill=1)
    c.setFillGray(0)
    c.setLineWidth(U.GRID_LW)
    c.rect(U.MARGIN, inst_y, content_w, instructions_h, stroke=1, fill=0)
    c.setFont(U.FONT_BOLD, 6.5)
    c.drawString(U.MARGIN + 4, inst_y + instructions_h - 10, "How to use this template:")
    lines = [
        "Copy a fresh template for each game. Fill in each page as the game progresses:",
        "  •  Page 1 (Game Header): Complete before first pitch — teams, date, scorer, weather",
        "  •  Page 2 (Game Summary): Complete after the final out — inning totals, pitcher lines, umpires",
        "  •  Page 3 (Visiting Team): Score the visiting team's at-bats inning by inning",
        "  •  Page 4 (Home Team): Score the home team's at-bats inning by inning",
        "  •  Pages 5–6 (Extra Lineup): Add for extra innings or if a team bats through the order twice",
    ]
    c.setFont(U.FONT_NORMAL, 5.5)
    line_y = inst_y + instructions_h - 20
    for line in lines:
        c.drawString(U.MARGIN + 4, line_y, line)
        line_y -= 8

    # Field reference + notes area
    notes_h = top_y - inst_y - instructions_h - 6
    notes_y = inst_y + instructions_h + 6
    c.setLineWidth(U.GRID_LW)
    c.rect(U.MARGIN, notes_y, content_w, notes_h, stroke=1, fill=0)
    _draw_field_reference(c, U.MARGIN, notes_y, content_w, notes_h)


def _draw_field_diagram(c, cx, hp_y, d=40, R_out=95):
    """Draw field fan, infield, pitcher's mound, baselines, and position circles."""
    R_inf = R_out * 0.579
    n_pts = 24
    cr = d * 0.22

    b1  = (cx + d * 0.707, hp_y + d * 0.707)
    b3  = (cx - d * 0.707, hp_y + d * 0.707)
    b2  = (cx, hp_y + d * 1.414)
    pit = (cx, hp_y + d * 0.85)

    def fan_path(r, a0=30, a1=150):
        pts = []
        for i in range(n_pts + 1):
            a = math.radians(a0 + (a1 - a0) * i / n_pts)
            pts.append((cx + r * math.cos(a), hp_y + r * math.sin(a)))
        return pts

    # Outfield fan
    c.setFillGray(0.86)
    c.setStrokeGray(0.55)
    c.setLineWidth(0.6)
    p = c.beginPath()
    p.moveTo(cx, hp_y)
    for px, py in fan_path(R_out):
        p.lineTo(px, py)
    p.close()
    c.drawPath(p, stroke=1, fill=1)

    # Infield dirt overlay
    c.setFillGray(0.76)
    p2 = c.beginPath()
    p2.moveTo(cx, hp_y)
    for px, py in fan_path(R_inf):
        p2.lineTo(px, py)
    p2.close()
    c.drawPath(p2, stroke=0, fill=1)

    # Pitcher's mound
    c.setFillGray(0.66)
    c.circle(pit[0], pit[1], d * 0.17, stroke=0, fill=1)

    # Diamond baselines
    c.setStrokeGray(0.35)
    c.setLineWidth(0.7)
    p3 = c.beginPath()
    p3.moveTo(cx, hp_y)
    p3.lineTo(*b1)
    p3.lineTo(*b2)
    p3.lineTo(*b3)
    p3.close()
    c.drawPath(p3, stroke=1, fill=0)

    # Position circles
    positions = [
        (1, pit[0], pit[1]),
        (2, cx, hp_y - d * 0.22),
        (3, b1[0], b1[1]),
        (4, cx + d * 0.38, hp_y + d * 1.15),
        (5, b3[0], b3[1]),
        (6, cx - d * 0.38, hp_y + d * 1.15),
        (7, cx - R_out * 0.56, hp_y + R_out * 0.72),
        (8, cx, hp_y + R_out * 0.9),
        (9, cx + R_out * 0.56, hp_y + R_out * 0.72),
    ]
    for num, px, py in positions:
        c.setFillGray(1)
        c.setStrokeGray(0.3)
        c.setLineWidth(0.6)
        c.circle(px, py, cr, stroke=1, fill=1)
        c.setFillGray(0.1)
        c.setFont(U.FONT_BOLD, cr * 1.35)
        c.drawCentredString(px, py - cr * 0.42, str(num))

    c.setFillGray(0)
    c.setStrokeGray(0)
    c.setLineWidth(U.GRID_LW)


def _draw_field_reference(c, box_x, box_y, box_w, box_h):
    """Draw baseball field diagram + position legend inside a bounding box."""
    d = 40
    R_out = 95
    cr = d * 0.22

    cx = box_x + box_w / 2

    # Title
    c.setFont(U.FONT_BOLD, 6.5)
    c.drawCentredString(cx, box_y + box_h - 9, "FIELD POSITIONS")
    c.setLineWidth(0.4)
    c.setStrokeGray(0.6)
    c.line(box_x + 4, box_y + box_h - 14, box_x + box_w - 4, box_y + box_h - 14)
    c.setStrokeGray(0)
    c.setLineWidth(U.GRID_LW)

    diagram_top = box_y + box_h - 14
    hp_y = diagram_top - R_out * 0.9 - cr - 6

    _draw_field_diagram(c, cx, hp_y, d=d, R_out=R_out)

    # 2-column legend
    legend_h = 52
    catcher_bottom = hp_y - 2 * cr  # center - radius - radius
    legend_top = catcher_bottom - 8
    legend_y = legend_top - legend_h
    col_w = box_w / 2
    entries_left  = [("1", "Pitcher"), ("2", "Catcher"), ("3", "First baseman"),
                     ("4", "Second baseman"), ("5", "Third baseman")]
    entries_right = [("6", "Shortstop"), ("7", "Left fielder"), ("8", "Center fielder"),
                     ("9", "Right fielder"), ("", "")]
    row_h_leg = legend_h / 5
    for i, ((n1, p1), (n2, p2)) in enumerate(zip(entries_left, entries_right)):
        ey = legend_top - (i + 0.7) * row_h_leg
        c.setFont(U.FONT_BOLD, 6)
        c.drawString(box_x + 10, ey, f"{n1} :")
        c.setFont(U.FONT_NORMAL, 6)
        c.drawString(box_x + 22, ey, p1)
        if n2:
            c.setFont(U.FONT_BOLD, 6)
            c.drawString(box_x + col_w + 6, ey, f"{n2} :")
            c.setFont(U.FONT_NORMAL, 6)
            c.drawString(box_x + col_w + 18, ey, p2)

    # Separator + Notes label
    sep_y = legend_y - 4
    c.setLineWidth(0.3)
    c.setStrokeGray(0.7)
    c.line(box_x + 4, sep_y, box_x + box_w - 4, sep_y)
    c.setStrokeGray(0)
    c.setFont(U.FONT_NORMAL, 5.5)
    c.setFillColorRGB(*U.COLOR_LABEL_GRAY)
    c.drawString(box_x + 4, box_y + 4, "Notes")
    c.setFillColorRGB(*U.COLOR_BLACK)
    c.setLineWidth(U.GRID_LW)


# ── Page 2: Game summary + scoring reference ──────────────────────────────────

def draw_page2(c):
    """Draw game summary (top half) + scoring reference (bottom half)."""
    content_w = U.PAGE_W - 2 * U.MARGIN
    mid_y = U.PAGE_H / 2
    top_y = U.PAGE_H - U.MARGIN

    # Title
    c.setFont(U.FONT_BOLD, 9)
    c.drawCentredString(U.PAGE_W / 2, top_y - 9, "GAME SUMMARY")
    top_y -= 15
    c.setLineWidth(U.BORDER_LW)
    c.line(U.MARGIN, top_y, U.PAGE_W - U.MARGIN, top_y)
    top_y -= 3

    # SUMS section
    sums_labels  = ["Runs", "Hits", "Errors", "Left on Base"]
    sums_acronym = ["S", "U", "M", "S"]
    sums_row_h   = 14
    acronym_w    = 8
    label_w      = 52
    sums_col_w   = (content_w - acronym_w - label_w) / 11

    for i, (acr, lbl) in enumerate(zip(sums_acronym, sums_labels)):
        row_bot = top_y - sums_row_h
        x = U.MARGIN
        c.setLineWidth(U.GRID_LW)
        c.rect(x, row_bot, acronym_w, sums_row_h, stroke=1, fill=0)
        c.setFont(U.FONT_BOLD, 6)
        c.drawCentredString(x + acronym_w / 2, row_bot + sums_row_h * 0.3, acr)
        x += acronym_w
        c.rect(x, row_bot, label_w, sums_row_h, stroke=1, fill=0)
        c.setFont(U.FONT_NORMAL, 6)
        c.drawString(x + 2, row_bot + sums_row_h * 0.3, lbl)
        x += label_w
        for j in range(11):
            c.rect(x, row_bot, sums_col_w, sums_row_h, stroke=1, fill=0)
            if i == 0:
                label = str(j + 1) if j < 10 else "TOT"
                c.setFont(U.FONT_BOLD, 5)
                c.drawCentredString(x + sums_col_w / 2, top_y - 5, label)
            x += sums_col_w
        top_y = row_bot
    top_y -= 5

    # Pitchers table
    pitcher_cols = ["#", "Pitchers", "W/L/S", "IP", "H", "R", "ER", "BB", "SO", "HB", "BK", "WP", "TBF"]
    p_num_w  = 10
    p_name_w = 55
    p_stat_w = round((content_w - p_num_w - p_name_w) / 11, 1)
    pitcher_col_w = [p_num_w, p_name_w] + [p_stat_w] * 11
    p_row_h = 12

    row_bot = top_y - p_row_h
    c.setFillGray(U.SHADE_HEADER_BG)
    c.rect(U.MARGIN, row_bot, content_w, p_row_h, stroke=0, fill=1)
    c.setFillGray(0)
    x = U.MARGIN
    for lbl, w in zip(pitcher_cols, pitcher_col_w):
        c.setLineWidth(U.GRID_LW)
        c.rect(x, row_bot, w, p_row_h, stroke=1, fill=0)
        c.setFont(U.FONT_BOLD, 5)
        c.drawCentredString(x + w / 2, row_bot + p_row_h * 0.3, lbl)
        x += w
    top_y = row_bot
    for _ in range(5):
        row_bot = top_y - p_row_h
        x = U.MARGIN
        for w in pitcher_col_w:
            c.setLineWidth(U.GRID_LW)
            c.rect(x, row_bot, w, p_row_h, stroke=1, fill=0)
            x += w
        top_y = row_bot
    top_y -= 5

    # Catchers + Umpires side by side
    half_w   = content_w / 2 - 3
    cu_row_h = 11
    cat_cols = ["#", "Catchers", "PB"]
    cat_col_w = [10, half_w - 20, 10]

    row_bot = top_y - cu_row_h
    c.setFillGray(U.SHADE_HEADER_BG)
    c.rect(U.MARGIN, row_bot, half_w, cu_row_h, stroke=0, fill=1)
    c.setFillGray(0)
    x = U.MARGIN
    for lbl, w in zip(cat_cols, cat_col_w):
        c.setLineWidth(U.GRID_LW)
        c.rect(x, row_bot, w, cu_row_h, stroke=1, fill=0)
        c.setFont(U.FONT_BOLD, 5)
        c.drawCentredString(x + w / 2, row_bot + cu_row_h * 0.3, lbl)
        x += w
    cat_header_bot = row_bot
    for row_i in range(3):
        row_bot = cat_header_bot - cu_row_h * (row_i + 1)
        x = U.MARGIN
        for w in cat_col_w:
            c.setLineWidth(U.GRID_LW)
            c.rect(x, row_bot, w, cu_row_h, stroke=1, fill=0)
            x += w

    ump_x     = U.MARGIN + half_w + 6
    ump_w     = content_w - half_w - 6
    ump_cols  = ["HP", "1B", "2B", "3B"]
    ump_label_w = 20
    ump_name_w  = ump_w - ump_label_w
    row_bot = top_y - cu_row_h
    c.setFillGray(U.SHADE_HEADER_BG)
    c.rect(ump_x, row_bot, ump_w, cu_row_h, stroke=0, fill=1)
    c.setFillGray(0)
    c.setLineWidth(U.GRID_LW)
    c.rect(ump_x, row_bot, ump_w, cu_row_h, stroke=1, fill=0)
    c.setFont(U.FONT_BOLD, 5.5)
    c.drawString(ump_x + 3, row_bot + cu_row_h * 0.3, "Umpires")
    ump_header_bot = row_bot
    for pos in ump_cols:
        ump_header_bot -= cu_row_h
        c.setLineWidth(U.GRID_LW)
        c.rect(ump_x, ump_header_bot, ump_label_w, cu_row_h, stroke=1, fill=0)
        c.rect(ump_x + ump_label_w, ump_header_bot, ump_name_w, cu_row_h, stroke=1, fill=0)
        c.setFont(U.FONT_BOLD, 5)
        c.drawCentredString(ump_x + ump_label_w / 2, ump_header_bot + cu_row_h * 0.3, pos)

    # Scoring reference (bottom half)
    ref_y = U.MARGIN
    ref_h = mid_y - U.MARGIN - 5
    ref_w = content_w
    c.setFillGray(U.SHADE_INSTRUCTIONS)
    c.rect(U.MARGIN, ref_y, ref_w, ref_h, stroke=0, fill=1)
    c.setFillGray(0)
    c.setLineWidth(U.BORDER_LW)
    c.rect(U.MARGIN, ref_y, ref_w, ref_h, stroke=1, fill=0)
    c.setFont(U.FONT_BOLD, 8)
    c.drawCentredString(U.PAGE_W / 2, ref_y + ref_h - 12, "SCORING REFERENCE")
    c.setLineWidth(U.GRID_LW)
    c.line(U.MARGIN + 4, ref_y + ref_h - 16, U.PAGE_W - U.MARGIN - 4, ref_y + ref_h - 16)

    col1_x = U.MARGIN + 4
    col2_x = U.PAGE_W / 2 + 2
    line_h  = 7.5

    entries_left = [
        ("HITS & PLAYS", None),
        ("1B  /  —", "Single"),
        ("2B  /  =", "Double"),
        ("3B  /  ≡", "Triple"),
        ("HR", "Home Run"),
        ("BB", "Walk"),
        ("HP", "Hit by Pitch"),
        ("SB", "Stolen Base"),
        ("SH / SAC", "Sacrifice Bunt"),
        ("SF", "Sacrifice Fly"),
        ("FC", "Fielder's Choice"),
        ("E", "Error"),
        ("DP", "Double Play"),
        ("WP", "Wild Pitch"),
        ("PB", "Passed Ball"),
        ("BK", "Balk"),
    ]
    entries_right = [
        ("OUTS & POSITIONS", None),
        ("K", "Strikeout swinging"),
        ("K (bkwd)", "Strikeout looking"),
        ("6-3", "Shortstop to first"),
        ("7", "Fly out to left field"),
        ("U", "Unassisted out"),
        ("FO", "Force Out"),
        ("", ""),
        ("POSITIONS", None),
        ("1 Pitcher", "2 Catcher"),
        ("3 First", "4 Second"),
        ("5 Third", "6 Shortstop"),
        ("7 Left", "8 Center"),
        ("9 Right", ""),
        ("", ""),
        ("SCORING THE DIAMOND", None),
    ]

    def draw_ref_col(entries, x, start_y):
        y = start_y
        for symbol, meaning in entries:
            if meaning is None:
                c.setFont(U.FONT_BOLD, 6)
                c.drawString(x, y, symbol)
                y -= line_h * 0.8
            elif symbol == "" and meaning == "":
                y -= line_h * 0.4
            else:
                c.setFont(U.FONT_BOLD, 5.5)
                c.drawString(x, y, symbol)
                c.setFont(U.FONT_NORMAL, 5.5)
                c.drawString(x + 32, y, meaning)
                y -= line_h

    ref_text_top = ref_y + ref_h - 22
    draw_ref_col(entries_left, col1_x, ref_text_top)
    draw_ref_col(entries_right, col2_x, ref_text_top)

    tip_y = ref_y + 12
    c.setFont(U.FONT_NORMAL, 5)
    c.setFillColorRGB(*U.COLOR_LABEL_GRAY)
    c.drawString(col2_x, tip_y + 8,
                 "Mark where runner reaches: lower-right=1st, upper-right=2nd,")
    c.drawString(col2_x, tip_y,
                 "upper-left=3rd, bottom=home. Shade path. Circle bottom = run scores.")
    c.setFillColorRGB(*U.COLOR_BLACK)
