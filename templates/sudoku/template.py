# Copyright (C) 2026 Paul Monday — GNU GPL v3 or later. See LICENSE.
"""
Sudoku notebook template.
Auto-discovered by generate.py via METADATA.
"""
from datetime import date
from reportlab.pdfgen import canvas as rl_canvas
from core.dimensions import PAGE_W, PAGE_H
from templates.sudoku.generator import make_puzzle
from templates.sudoku.renderer import draw_cover, draw_puzzle_page, draw_solution_page

_DIFFICULTY_CONFIG = {
    "easy":   {},
    "medium": {},
    "hard":   {},
    "expert": {},
}

METADATA = {
    "name":        "Sudoku",
    "description": "Sudoku puzzle notebook",
    "output":      "sudoku.pdf",
    "pages":       0,  # dynamic: 1 + 2 * count
    "template_fields": [
        {"name": "difficulty", "prompt": "Difficulty (easy/medium/hard/expert)", "default": "easy"},
        {"name": "count",      "prompt": "Number of puzzles",                    "default": "3"},
    ],
}


def generate(output_path: str, **meta) -> None:
    """Generate the Sudoku notebook PDF."""
    difficulty = meta.get("difficulty", "easy").lower()
    count      = int(meta.get("count", 3))
    date_str   = date.today().strftime("%B %d, %Y")

    if difficulty not in _DIFFICULTY_CONFIG:
        raise ValueError(
            f"Unknown difficulty {difficulty!r}. Expected one of {list(_DIFFICULTY_CONFIG)}"
        )

    c = rl_canvas.Canvas(output_path, pagesize=(PAGE_W, PAGE_H))

    draw_cover(c, difficulty=difficulty, count=count, date_str=date_str)
    c.showPage()

    for i in range(count):
        puzzle = make_puzzle(difficulty)
        draw_puzzle_page(c, puzzle, puzzle_num=i + 1, difficulty=difficulty)
        c.showPage()
        draw_solution_page(c, puzzle, puzzle_num=i + 1)
        c.showPage()

    c.save()
