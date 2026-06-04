# Copyright (C) 2026 Paul Monday — GNU GPL v3 or later. See LICENSE.
# templates/sudoku/renderer.py
"""
ReportLab renderer for Sudoku pages.

draw_cover(c, difficulty, count, date_str, **_)
draw_puzzle_page(c, puzzle, puzzle_num, difficulty)
draw_solution_page(c, puzzle, puzzle_num)

None of these call c.showPage() — the caller does.
puzzle = {"given": [[int|None]], "solved": [[int]]}
"""
from reportlab.lib.colors import black, white, HexColor
from core.dimensions import PAGE_W, PAGE_H, MARGIN

_GRAY       = HexColor("#555555")
_LIGHT_GRAY = HexColor("#888888")

_HEADER_FONT = 10
_FOOTER_FONT = 7
_DIGIT_RATIO = 0.55   # digit font size as fraction of cell size

_CELL_SIZE = (PAGE_W - 2 * MARGIN) / 9


def _draw_grid(c, given_grid: list, solved_grid: list, origin_x: float,
               origin_y: float, cell_size: float, show_solution: bool = False) -> None:
    """
    Draw the 9x9 grid.
    origin_x, origin_y = top-left corner (ReportLab y increases upward).
    given_grid[r][c] is an int if pre-filled, None if blank.
    solved_grid[r][c] is always an int.
    """
    total = cell_size * 9
    digit_font_size = cell_size * _DIGIT_RATIO

    # White background
    c.setFillColor(white)
    c.rect(origin_x, origin_y - total, total, total, fill=1, stroke=0)

    for r in range(9):
        for col in range(9):
            x = origin_x + col * cell_size
            y = origin_y - (r + 1) * cell_size
            given_val = given_grid[r][col]

            # Cell background and inner border
            c.setFillColor(white)
            c.setStrokeColor(_LIGHT_GRAY)
            c.setLineWidth(0.4)
            c.rect(x, y, cell_size, cell_size, fill=1, stroke=1)

            if given_val is not None:
                # Given digit -- bold black
                c.setFillColor(black)
                c.setFont("Helvetica-Bold", digit_font_size)
                c.drawCentredString(x + cell_size / 2, y + cell_size * 0.2, str(given_val))
            elif show_solution:
                # Solver-filled digit -- gray, normal weight
                c.setFillColor(_GRAY)
                c.setFont("Helvetica", digit_font_size)
                c.drawCentredString(x + cell_size / 2, y + cell_size * 0.2,
                                    str(solved_grid[r][col]))

    # Heavy 3x3 box borders
    c.setStrokeColor(black)
    c.setLineWidth(1.8)
    for i in range(4):
        offset = i * cell_size * 3
        c.line(origin_x + offset, origin_y, origin_x + offset, origin_y - total)
        c.line(origin_x, origin_y - offset, origin_x + total, origin_y - offset)

    # Outer border
    c.setLineWidth(2.0)
    c.rect(origin_x, origin_y - total, total, total, fill=0, stroke=1)


def _draw_header(c, left_text: str, right_text: str) -> float:
    """Draw page header. Returns y of content area top (below header)."""
    header_y = PAGE_H - MARGIN - _HEADER_FONT
    c.setFont("Helvetica-Bold", _HEADER_FONT)
    c.setFillColor(black)
    c.drawString(MARGIN, header_y, left_text)
    c.drawRightString(PAGE_W - MARGIN, header_y, right_text)
    return header_y - 6


def _draw_footer(c, text: str) -> None:
    c.setFont("Helvetica", _FOOTER_FONT)
    c.setFillColor(_LIGHT_GRAY)
    c.drawCentredString(PAGE_W / 2, MARGIN, text)


def _draw_puzzle_or_solution(c, puzzle: dict, content_top: float,
                              show_solution: bool) -> None:
    """Shared layout helper: compute grid position and delegate to _draw_grid."""
    grid_total = _CELL_SIZE * 9
    origin_x = (PAGE_W - grid_total) / 2
    footer_y = MARGIN + _FOOTER_FONT + 4
    origin_y = content_top - (content_top - footer_y - grid_total) / 2
    _draw_grid(c, puzzle["given"], puzzle["solved"], origin_x, origin_y,
               _CELL_SIZE, show_solution=show_solution)


def draw_puzzle_page(c, puzzle: dict, puzzle_num: int, difficulty: str) -> None:
    """Draw puzzle page with given digits only. Caller calls c.showPage()."""
    content_top = _draw_header(c, f"Sudoku #{puzzle_num}", difficulty.capitalize())
    _draw_footer(c, f"Kindle Sudoku  .  Puzzle {puzzle_num}")
    _draw_puzzle_or_solution(c, puzzle, content_top, show_solution=False)


def draw_solution_page(c, puzzle: dict, puzzle_num: int) -> None:
    """Draw solution page with all digits filled. Caller calls c.showPage()."""
    content_top = _draw_header(c, f"Solution #{puzzle_num}", "SOLUTION")
    _draw_footer(c, f"Kindle Sudoku  .  Solution {puzzle_num}")
    _draw_puzzle_or_solution(c, puzzle, content_top, show_solution=True)


def draw_cover(c, difficulty: str, count: int, date_str: str, **_) -> None:
    """Draw cover page. Caller calls c.showPage()."""
    cx = PAGE_W / 2

    # Title
    c.setFont("Helvetica-Bold", 32)
    c.setFillColor(black)
    title_y = PAGE_H * 0.70
    c.drawCentredString(cx, title_y, "Sudoku")

    # Decorative rule
    c.setStrokeColor(_GRAY)
    c.setLineWidth(0.8)
    c.line(cx - 40, title_y - 14, cx + 40, title_y - 14)

    # Decorative mini 9x9 grid outline
    mini_cell = 8
    mini_total = mini_cell * 9
    mini_x = (PAGE_W - mini_total) / 2
    mini_y = PAGE_H * 0.52
    c.setStrokeColor(_LIGHT_GRAY)
    c.setLineWidth(0.3)
    for i in range(10):
        c.line(mini_x + i * mini_cell, mini_y, mini_x + i * mini_cell, mini_y - mini_total)
        c.line(mini_x, mini_y - i * mini_cell, mini_x + mini_total, mini_y - i * mini_cell)
    c.setStrokeColor(black)
    c.setLineWidth(1.2)
    for i in range(4):
        offset = i * mini_cell * 3
        c.line(mini_x + offset, mini_y, mini_x + offset, mini_y - mini_total)
        c.line(mini_x, mini_y - offset, mini_x + mini_total, mini_y - offset)

    # Metadata line
    meta_y = PAGE_H * 0.26
    puzzle_word = "Puzzle" if count == 1 else "Puzzles"
    c.setFont("Helvetica-Bold", 12)
    c.setFillColor(black)
    c.drawCentredString(cx, meta_y, f"{count} {puzzle_word}  .  {difficulty.capitalize()}")

    c.setFont("Helvetica", 9)
    c.setFillColor(_GRAY)
    c.drawCentredString(cx, meta_y - 16, f"Generated: {date_str}")
