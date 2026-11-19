"""
ReportLab renderer for Cruza y Aprende crossword pages.

draw_cover(c, count, size_label, difficulty, date_str)
draw_puzzle_page(c, puzzle_result, puzzle_num, size_label, difficulty)
draw_solution_page(c, puzzle_result, puzzle_num)

None of these call c.showPage() — the caller does.
"""
from reportlab.lib.colors import black, white, HexColor
from core.dimensions import PAGE_W, PAGE_H, MARGIN

_GRAY = HexColor("#444444")

GRID_OUTER = 2
GRID_INNER = 0.5
CLUE_FONT  = 7
HEADER_FONT = 9
LABEL_FONT = 8


def _draw_grid(c, grid, grid_size, origin_x, origin_y, cell_size, show_letters=False):
    """
    Draw the crossword grid.
    origin_x, origin_y = top-left corner in ReportLab coords (y increases upward).
    """
    total = cell_size * grid_size

    c.setFillColor(white)
    c.rect(origin_x, origin_y - total, total, total, fill=1, stroke=0)

    for row in range(grid_size):
        for col in range(grid_size):
            x = origin_x + col * cell_size
            y = origin_y - (row + 1) * cell_size
            cell = grid[row][col]

            if cell is None:
                c.setFillColor(black)
                c.rect(x, y, cell_size, cell_size, fill=1, stroke=0)
            else:
                c.setFillColor(white)
                c.setStrokeColor(_GRAY)
                c.setLineWidth(GRID_INNER)
                c.rect(x, y, cell_size, cell_size, fill=1, stroke=1)
                if show_letters and cell:
                    c.setFillColor(black)
                    c.setFont("Helvetica-Bold", cell_size * 0.55)
                    c.drawCentredString(x + cell_size / 2, y + cell_size * 0.18, cell)

    c.setStrokeColor(black)
    c.setLineWidth(GRID_OUTER)
    c.rect(origin_x, origin_y - total, total, total, fill=0, stroke=1)


def _draw_cell_numbers(c, placed_words, origin_x, origin_y, cell_size):
    """Draw small clue numbers at top-left of each word's start cell."""
    numbered = {}
    for pw in placed_words:
        key = (pw.row, pw.col)
        if key not in numbered:
            numbered[key] = pw.number
    c.setFont("Helvetica", 4.5)
    c.setFillColor(black)
    for (row, col), num in numbered.items():
        x = origin_x + col * cell_size + 1
        y = origin_y - row * cell_size - 5.5
        c.drawString(x, y, str(num))


CLUE_FONT_STEPS = (7, 6.5, 6)   # shrink clue text before the grid gets tiny
MIN_CELL = 15                    # pt; smallest grid cell worth writing in
_CLUE_INDENT = "00. "


def _wrap_clue(c, number, clue, width, size):
    """Wrap 'N. clue' to width; continuation lines hang under the clue text."""
    indent = c.stringWidth(_CLUE_INDENT, "Helvetica", size)
    lines, cur, avail = [], f"{number}.", width
    for word in clue.split():
        trial = f"{cur} {word}"
        if c.stringWidth(trial, "Helvetica", size) <= avail:
            cur = trial
            continue
        lines.append(cur)
        cur, avail = word, width - indent
        while c.stringWidth(cur, "Helvetica", size) > avail and len(cur) > 1:
            cur = cur[:-2] + "…"
    lines.append(cur)
    return lines


def _clue_columns(placed_words):
    across = sorted([pw for pw in placed_words if pw.direction == "across"], key=lambda pw: pw.number)
    down   = sorted([pw for pw in placed_words if pw.direction == "down"],   key=lambda pw: pw.number)
    return across, down


def _clue_block_height(c, placed_words, col_w, size):
    line_h = size + 1.5
    tallest = 0
    for column in _clue_columns(placed_words):
        n = sum(len(_wrap_clue(c, pw.number, pw.clue, col_w - 4, size)) for pw in column)
        tallest = max(tallest, n)
    return LABEL_FONT + 1 + line_h + 1 + tallest * line_h


def _draw_clues(c, placed_words, area_x, area_y, area_w, area_h, size=CLUE_FONT):
    """
    Draw ACROSS and DOWN clues in two columns, wrapping long clues.
    area_y is the TOP of the clue area in ReportLab coords.
    """
    across, down = _clue_columns(placed_words)
    col_w = area_w / 2
    line_h = size + 1.5
    indent = c.stringWidth(_CLUE_INDENT, "Helvetica", size)

    def _draw_column(clue_list, col_x, header):
        c.setFont("Helvetica-Bold", LABEL_FONT)
        c.setFillColor(black)
        y = area_y - LABEL_FONT - 1
        c.drawString(col_x, y, header)
        c.setLineWidth(0.3)
        c.line(col_x, y - 1, col_x + col_w - 4, y - 1)
        y -= line_h + 1
        c.setFont("Helvetica", size)
        for pw in clue_list:
            for i, line in enumerate(_wrap_clue(c, pw.number, pw.clue, col_w - 4, size)):
                if y < area_y - area_h:
                    return
                c.drawString(col_x + (indent if i else 0), y, line)
                y -= line_h

    _draw_column(across, area_x, "ACROSS")
    _draw_column(down, area_x + col_w, "DOWN")


def puzzle_layout(c, puzzle_result):
    """Return (cell_size, clue_font): the largest grid that leaves room for
    every wrapped clue, shrinking clue text before going below MIN_CELL."""
    gs = puzzle_result.grid_size
    usable_w = PAGE_W - 2 * MARGIN
    header_y = PAGE_H - MARGIN - HEADER_FONT
    avail_h = (header_y - 6) - 6 - MARGIN          # grid top → bottom margin, minus gap
    col_w = usable_w / 2
    for size in CLUE_FONT_STEPS:
        need = _clue_block_height(c, puzzle_result.placed_words, col_w, size)
        cell = min(22, usable_w / gs, (avail_h - need) / gs)
        if cell >= MIN_CELL:
            return cell, size
    return MIN_CELL, CLUE_FONT_STEPS[-1]


def draw_puzzle_page(c, puzzle_result, puzzle_num: int, size_label: str, difficulty: str):
    """Draw a full puzzle page (grid + clues). Caller calls c.showPage()."""
    grid = puzzle_result.grid
    gs = puzzle_result.grid_size

    header = f"Puzzle #{puzzle_num}  —  {size_label}  —  {difficulty.capitalize()}"
    c.setFont("Helvetica-Bold", HEADER_FONT)
    c.setFillColor(black)
    header_y = PAGE_H - MARGIN - HEADER_FONT
    c.drawCentredString(PAGE_W / 2, header_y, header)

    cell_size, clue_font = puzzle_layout(c, puzzle_result)
    grid_w = cell_size * gs
    grid_h = cell_size * gs  # same value — grid is square
    grid_x = (PAGE_W - grid_w) / 2
    grid_top_y = header_y - 6

    _draw_grid(c, grid, gs, grid_x, grid_top_y, cell_size)
    _draw_cell_numbers(c, puzzle_result.placed_words, grid_x, grid_top_y, cell_size)

    clue_top = grid_top_y - grid_h - 6
    clue_h = clue_top - MARGIN
    _draw_clues(c, puzzle_result.placed_words,
                area_x=MARGIN, area_y=clue_top,
                area_w=PAGE_W - 2 * MARGIN, area_h=clue_h, size=clue_font)


def draw_solution_page(c, puzzle_result, puzzle_num: int):
    """Draw the solution page (filled grid, larger cells, no clues). Caller calls c.showPage()."""
    grid = puzzle_result.grid
    gs = puzzle_result.grid_size

    header = f"Puzzle #{puzzle_num}  —  Solution"
    c.setFont("Helvetica-Bold", HEADER_FONT)
    c.setFillColor(black)
    header_y = PAGE_H - MARGIN - HEADER_FONT
    c.drawCentredString(PAGE_W / 2, header_y, header)

    usable_w = PAGE_W - 2 * MARGIN
    usable_h = header_y - 6 - MARGIN
    cell_size = min(usable_w / gs, usable_h / gs)
    grid_w = cell_size * gs
    grid_x = (PAGE_W - grid_w) / 2
    grid_top_y = header_y - 6

    _draw_grid(c, grid, gs, grid_x, grid_top_y, cell_size, show_letters=True)


def draw_cover(c, count: int, size_label: str, difficulty: str, date_str: str):
    """Draw the cover page. Caller calls c.showPage()."""
    cx = PAGE_W / 2

    c.setFont("Helvetica-Bold", 28)
    c.setFillColor(black)
    title_y = PAGE_H * 0.72
    c.drawCentredString(cx, title_y, "Cruza y Aprende")

    c.setFont("Helvetica", 11)
    c.setFillColor(_GRAY)
    c.drawCentredString(cx, title_y - 18, "Cross and Learn")

    c.setStrokeColor(_GRAY)
    c.setLineWidth(0.8)
    c.line(cx - 30, title_y - 28, cx + 30, title_y - 28)

    _draw_mini_crossword(c, cx, title_y - 80)

    meta_y = PAGE_H * 0.28
    c.setFont("Helvetica-Bold", 13)
    c.setFillColor(black)
    c.drawCentredString(cx, meta_y, f"{count} Puzzle{'s' if count != 1 else ''}  ·  {size_label}  ·  {difficulty.capitalize()}")

    c.setFont("Helvetica", 9)
    c.setFillColor(_GRAY)
    c.drawCentredString(cx, meta_y - 16, f"Generated: {date_str}")

    c.setFont("Helvetica", 8)
    c.drawCentredString(cx, MARGIN + 12, "Vocabulary from LinkedIn Learning Spanish Parts 1–4")


def _draw_mini_crossword(c, cx, center_y):
    """
    Decorative mini-crossword: CRUZA across (row 2), APRENDE down (col 1).
    The shared letter is R — CRUZA[1] == APRENDE[2] — so they cross correctly.

    Grid (7 rows × 5 cols), None = black square:
      row 0: [ . A . . . ]
      row 1: [ . P . . . ]
      row 2: [ C R U Z A ]   <- CRUZA across
      row 3: [ . E . . . ]
      row 4: [ . N . . . ]
      row 5: [ . D . . . ]
      row 6: [ . E . . . ]
    """
    cell = 10
    letters = [
        [None, "A", None, None, None],
        [None, "P", None, None, None],
        ["C",  "R", "U",  "Z",  "A" ],
        [None, "E", None, None, None],
        [None, "N", None, None, None],
        [None, "D", None, None, None],
        [None, "E", None, None, None],
    ]
    num_rows = len(letters)
    num_cols = len(letters[0])
    gw = num_cols * cell
    gh = num_rows * cell
    ox = cx - gw / 2
    oy = center_y + gh / 2

    c.setLineWidth(0.5)
    for r in range(num_rows):
        for col in range(num_cols):
            x = ox + col * cell
            y = oy - (r + 1) * cell
            ch = letters[r][col]
            if ch is None:
                c.setFillColor(HexColor("#333333"))
                c.rect(x, y, cell, cell, fill=1, stroke=0)
            else:
                c.setFillColor(white)
                c.setStrokeColor(HexColor("#999999"))
                c.rect(x, y, cell, cell, fill=1, stroke=1)
                c.setFillColor(black)
                c.setFont("Helvetica-Bold", 6)
                c.drawCentredString(x + cell / 2, y + 2, ch)

    c.setStrokeColor(black)
    c.setLineWidth(1.5)
    c.rect(ox, oy - gh, gw, gh, fill=0, stroke=1)
