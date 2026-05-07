# Copyright (C) 2026 Paul Monday — GNU GPL v3 or later. See LICENSE.
from reportlab.pdfgen import canvas as rl_canvas
from core import dimensions as D
from core import style as S

METADATA = {
    "name":        "Colorado MyUI Worklog",
    "description": "Colorado UI work-search activity log — 3 pages, 5 entries per page",
    "output":      "colorado-myui-worklog.pdf",
    "pages":       3,
}

_CW = D.PAGE_W - 2 * D.MARGIN  # 324.96 pt

# Column widths
_W_DATE    = 28.0
_W_ACT     = 76.0   # two 38pt sub-columns of checkboxes inside
_W_DETAILS = 87.0
_W_CONTACT = 55.0
_W_HOW     = 46.0
_W_WORK    = _CW - _W_DATE - _W_ACT - _W_DETAILS - _W_CONTACT - _W_HOW  # ~32.96

# Column left-edge x positions
_X_DATE    = D.MARGIN
_X_ACT     = _X_DATE    + _W_DATE
_X_DETAILS = _X_ACT     + _W_ACT
_X_CONTACT = _X_DETAILS + _W_DETAILS
_X_HOW     = _X_CONTACT + _W_CONTACT
_X_WORK    = _X_HOW     + _W_HOW

# Page layout
_TITLE_H  = 36.0
_HEADER_H = 44.0
_ROWS     = 5
_ROW_H    = (D.PAGE_H - 2 * D.MARGIN - _TITLE_H - _HEADER_H) / _ROWS  # ~71.5 pt

# Checkbox labels — \n splits a label across two lines when it's too wide for its cell
_ACT_L = ["Submit\nApplication", "Submit Resume", "Interview", "Test/Exam", "Job Board"]
_ACT_R = ["Referral", "Networking", "Reemployment\nService", "Skills\nDevelopment", "Other"]
_HOW   = ["In Person", "Phone/Fax", "Mail", "Email", "Web Site"]


def generate(output_path: str, **meta) -> None:
    c = rl_canvas.Canvas(output_path, pagesize=(D.PAGE_W, D.PAGE_H))
    for _ in range(METADATA["pages"]):
        _draw_page(c)
        c.showPage()
    c.save()


def _draw_page(c):
    top = D.PAGE_H - D.MARGIN

    # Title
    c.setFont(S.FONT_BOLD, 11)
    c.drawCentredString(D.PAGE_W / 2, top - 12, "Track Your Work-Search Activities")

    # Two-line subtitle
    c.setFont(S.FONT_NORMAL, 4.5)
    c.drawCentredString(
        D.PAGE_W / 2, top - 22,
        "Keep verifiable information for all your work-search activities and download",
    )
    c.drawCentredString(
        D.PAGE_W / 2, top - 28,
        '"What is a Work-Search Activity?" at coloradoui.gov/eligibility for more information.',
    )

    # Rule
    c.setLineWidth(0.4)
    c.setStrokeGray(0.5)
    c.line(D.MARGIN, top - _TITLE_H + 3, D.PAGE_W - D.MARGIN, top - _TITLE_H + 3)
    c.setStrokeGray(0)
    c.setLineWidth(S.GRID_LW)

    # Header row then data rows
    header_top = top - _TITLE_H
    _draw_header_row(c, header_top)
    row_top = header_top - _HEADER_H
    for _ in range(_ROWS):
        _draw_data_row(c, row_top)
        row_top -= _ROW_H


def _col_dividers(c, bot, top, act_subcol=False):
    """Draw vertical lines between the 6 main columns.

    Pass act_subcol=True to also draw the light internal divider inside Activity Completed.
    """
    c.setLineWidth(S.GRID_LW)
    for x in [_X_ACT, _X_DETAILS, _X_CONTACT, _X_HOW, _X_WORK]:
        c.line(x, bot, x, top)
    if act_subcol:
        c.setLineWidth(S.SUBCELL_LW)
        c.line(_X_ACT + _W_ACT / 2, bot, _X_ACT + _W_ACT / 2, top)
        c.setLineWidth(S.GRID_LW)


def _draw_header_row(c, top):
    bot = top - _HEADER_H

    c.setFillGray(S.SHADE_HEADER_BG)
    c.rect(D.MARGIN, bot, _CW, _HEADER_H, stroke=0, fill=1)
    c.setFillGray(0)

    c.setLineWidth(S.BORDER_LW)
    c.rect(D.MARGIN, bot, _CW, _HEADER_H, stroke=1, fill=0)
    c.setLineWidth(S.GRID_LW)
    _col_dividers(c, bot, top, act_subcol=False)

    mid_y = (top + bot) / 2

    # Date
    c.setFont(S.FONT_BOLD, 6)
    c.drawCentredString(_X_DATE + _W_DATE / 2, mid_y + 3, "Date")
    c.setFont(S.FONT_NORMAL, 5)
    c.drawCentredString(_X_DATE + _W_DATE / 2, mid_y - 4, "MM/DD/YY")

    # Activity Completed
    c.setFont(S.FONT_BOLD, 6)
    c.drawCentredString(_X_ACT + _W_ACT / 2, top - 7, "Activity Completed")

    # Completed Activity Details
    cx_det = _X_DETAILS + _W_DETAILS / 2
    c.setFont(S.FONT_BOLD, 6)
    c.drawCentredString(cx_det, top - 7, "Completed Activity Details")
    c.setFont(S.FONT_NORMAL, 4.5)
    for i, line in enumerate([
        "Employer Name, Address, Phone,",
        "Email Address, Website;",
        "Class Name & Location;",
        "Networking Event Name & Location",
    ]):
        c.drawCentredString(cx_det, top - 14 - i * 6, line)

    # Name & Title of Person Contacted or Confirmation Number
    cx_con = _X_CONTACT + _W_CONTACT / 2
    c.setFont(S.FONT_BOLD, 5.5)
    c.drawCentredString(cx_con, top - 7,  "Name & Title of")
    c.drawCentredString(cx_con, top - 14, "Person Contacted")
    c.setFont(S.FONT_NORMAL, 5)
    c.drawCentredString(cx_con, top - 21, "or")
    c.setFont(S.FONT_BOLD, 5.5)
    c.drawCentredString(cx_con, top - 28, "Confirmation")
    c.drawCentredString(cx_con, top - 35, "Number")

    # How Contacted
    cx_how = _X_HOW + _W_HOW / 2
    c.setFont(S.FONT_BOLD, 6)
    c.drawCentredString(cx_how, mid_y + 3, "How")
    c.drawCentredString(cx_how, mid_y - 5, "Contacted")

    # Work Sought or Skills Developed
    cx_wk = _X_WORK + _W_WORK / 2
    c.setFont(S.FONT_BOLD, 5)
    c.drawCentredString(cx_wk, top - 7,  "Work Sought")
    c.setFont(S.FONT_NORMAL, 5)
    c.drawCentredString(cx_wk, top - 14, "or")
    c.setFont(S.FONT_BOLD, 5)
    c.drawCentredString(cx_wk, top - 21, "Skills")
    c.drawCentredString(cx_wk, top - 28, "Developed")


def _draw_data_row(c, top):
    bot = top - _ROW_H

    c.setLineWidth(S.BORDER_LW)
    c.rect(D.MARGIN, bot, _CW, _ROW_H, stroke=1, fill=0)
    c.setLineWidth(S.GRID_LW)
    _col_dividers(c, bot, top, act_subcol=True)

    act_mid = _X_ACT + _W_ACT / 2
    _draw_checkboxes(c, _X_ACT  + 2, top, _ACT_L)
    _draw_checkboxes(c, act_mid + 2, top, _ACT_R)
    _draw_checkboxes(c, _X_HOW  + 2, top, _HOW)


def _draw_checkboxes(c, x, row_top, items):
    """Draw a vertical column of unchecked checkboxes with labels."""
    spacing = _ROW_H / (len(items) + 0.5)
    box_sz = 3.5
    fs = 4.5

    for i, label in enumerate(items):
        y = row_top - (i + 0.75) * spacing
        c.setLineWidth(0.5)
        c.rect(x, y - box_sz / 2, box_sz, box_sz, stroke=1, fill=0)
        c.setFont(S.FONT_NORMAL, fs)
        lx = x + box_sz + 1.5
        if "\n" in label:
            l1, l2 = label.split("\n", 1)
            c.drawString(lx, y + 1.5, l1)
            c.drawString(lx, y + 1.5 - fs - 1, l2)
        else:
            c.drawString(lx, y - fs * 0.38, label)

    c.setLineWidth(S.GRID_LW)
