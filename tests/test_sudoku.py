# Copyright (C) 2026 Paul Monday — GNU GPL v3 or later. See LICENSE.
import io

import pytest
from reportlab.pdfgen import canvas as rl_canvas
from pypdf import PdfReader

from core import dimensions as D
from templates.sudoku.generator import count_solutions, fill_grid, make_puzzle
from templates.sudoku.renderer import draw_cover, draw_puzzle_page, draw_solution_page

# A known complete valid grid (no Nones)
_SOLVED = [
    [5,3,4,6,7,8,9,1,2],
    [6,7,2,1,9,5,3,4,8],
    [1,9,8,3,4,2,5,6,7],
    [8,5,9,7,6,1,4,2,3],
    [4,2,6,8,5,3,7,9,1],
    [7,1,3,9,2,4,8,5,6],
    [9,6,1,5,3,7,2,8,4],
    [2,8,7,4,1,9,6,3,5],
    [3,4,5,2,8,6,1,7,9],
]


def test_count_solutions_complete_grid_is_one():
    grid = [row[:] for row in _SOLVED]
    assert count_solutions(grid) == 1


def test_count_solutions_empty_grid_exceeds_one():
    grid = [[None]*9 for _ in range(9)]
    assert count_solutions(grid, limit=2) == 2


def test_count_solutions_unsolvable_returns_zero():
    # Put two 5s in the same row — no solution
    grid = [[None]*9 for _ in range(9)]
    grid[0][0] = 5
    grid[0][1] = 5
    assert count_solutions(grid, limit=2) == 0


def _is_valid_completed_grid(grid):
    """Return True if grid satisfies all Sudoku constraints (all cells filled)."""
    for i in range(9):
        row = [grid[i][c] for c in range(9)]
        col = [grid[r][i] for r in range(9)]
        if sorted(row) != list(range(1, 10)):
            return False
        if sorted(col) != list(range(1, 10)):
            return False
    for br in range(3):
        for bc in range(3):
            box = [grid[br*3+dr][bc*3+dc] for dr in range(3) for dc in range(3)]
            if sorted(box) != list(range(1, 10)):
                return False
    return True


def test_fill_grid_returns_valid_completed_grid():
    grid = [[None] * 9 for _ in range(9)]
    result = fill_grid(grid)
    assert result is True
    assert len(grid) == 9
    assert all(len(row) == 9 for row in grid)
    assert _is_valid_completed_grid(grid)


def test_fill_grid_no_nones():
    grid = [[None] * 9 for _ in range(9)]
    fill_grid(grid)
    assert all(cell is not None for row in grid for cell in row)


@pytest.mark.parametrize("difficulty,target,tolerance", [
    ("easy",   46, 4),
    ("medium", 36, 4),
    ("hard",   28, 4),
    ("expert", 22, 6),
])
def test_make_puzzle_givens_count(difficulty, target, tolerance):
    puzzle = make_puzzle(difficulty)["given"]
    given_count = sum(1 for row in puzzle for v in row if v is not None)
    assert abs(given_count - target) <= tolerance, (
        f"{difficulty}: expected ~{target} givens, got {given_count}"
    )


@pytest.mark.parametrize("difficulty", ["easy", "medium", "hard", "expert"])
def test_make_puzzle_is_unique(difficulty):
    puzzle = make_puzzle(difficulty)["given"]
    assert count_solutions(puzzle) == 1


@pytest.mark.parametrize("difficulty", ["easy", "medium", "hard", "expert"])
def test_make_puzzle_solved_is_valid(difficulty):
    solution = make_puzzle(difficulty)["solved"]
    assert _is_valid_completed_grid(solution)


def test_make_puzzle_structure():
    puzzle = make_puzzle("easy")
    assert "given" in puzzle and "solved" in puzzle
    assert len(puzzle["given"]) == 9
    assert len(puzzle["solved"]) == 9


def _make_canvas():
    buf = io.BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=(D.PAGE_W, D.PAGE_H))
    return c, buf


def test_draw_puzzle_page_renders_without_error():
    puzzle = make_puzzle("easy")
    c, buf = _make_canvas()
    draw_puzzle_page(c, puzzle, puzzle_num=1, difficulty="easy")
    c.showPage()
    c.save()
    buf.seek(0)
    assert len(PdfReader(buf).pages) == 1


def test_draw_solution_page_renders_without_error():
    puzzle = make_puzzle("easy")
    c, buf = _make_canvas()
    draw_solution_page(c, puzzle, puzzle_num=1)
    c.showPage()
    c.save()
    buf.seek(0)
    assert len(PdfReader(buf).pages) == 1


def test_draw_cover_renders_without_error():
    c, buf = _make_canvas()
    draw_cover(c, difficulty="hard", count=5, date_str="June 04, 2026")
    c.showPage()
    c.save()
    buf.seek(0)
    assert len(PdfReader(buf).pages) == 1


def test_sudoku_generate_page_count(sudoku_mod, tmp_path):
    out = str(tmp_path / "sudoku.pdf")
    sudoku_mod.generate(out, difficulty="easy", count="1")
    reader = PdfReader(out)
    # 1 cover + 1 puzzle + 1 solution = 3 pages
    assert len(reader.pages) == 3


def test_sudoku_generate_multi_puzzle_page_count(sudoku_mod, tmp_path):
    out = str(tmp_path / "sudoku3.pdf")
    sudoku_mod.generate(out, difficulty="medium", count="3")
    reader = PdfReader(out)
    # 1 cover + 3 * 2 = 7 pages
    assert len(reader.pages) == 7


def test_sudoku_metadata(sudoku_mod):
    m = sudoku_mod.METADATA
    assert m["name"] == "Sudoku"
    assert m["output"] == "sudoku.pdf"
    fields = {f["name"] for f in m["template_fields"]}
    assert fields == {"difficulty", "count"}


def test_sudoku_invalid_difficulty_raises(sudoku_mod, tmp_path):
    out = str(tmp_path / "bad.pdf")
    with pytest.raises(ValueError, match="Unknown difficulty"):
        sudoku_mod.generate(out, difficulty="impossible")
