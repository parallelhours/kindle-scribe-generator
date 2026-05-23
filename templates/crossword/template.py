"""
Cruza y Aprende — Spanish Crossword Notebook template.
Auto-discovered by generate.py via METADATA.
"""
import json
from datetime import date
from pathlib import Path
from reportlab.pdfgen import canvas as rl_canvas
from core.dimensions import PAGE_W, PAGE_H

from templates.crossword.clues import build_candidate_pool
from templates.crossword.generator import generate_puzzle
from templates.crossword.renderer import (
    draw_cover as _render_cover,
    draw_puzzle_page,
    draw_solution_page,
)

_VOCAB_PATH = Path(__file__).parent / "vocabulary.json"

# difficulty drives both grid size and word count
_DIFFICULTY_CONFIG = {
    "easy":   {"grid_size": 9,  "target": 8,  "size_label": "Small"},
    "medium": {"grid_size": 11, "target": 10, "size_label": "Medium"},
    "hard":   {"grid_size": 15, "target": 15, "size_label": "Large"},
}

METADATA = {
    "name":        "Cruza y Aprende",
    "description": "Spanish crossword puzzle notebook",
    "output":      "cruza-y-aprende.pdf",
    "pages":       0,  # dynamic: 1 + 2 * count
    "template_fields": [
        {"name": "difficulty", "prompt": "Difficulty (easy/medium/hard)", "default": "easy"},
        {"name": "count",      "prompt": "Number of puzzles",             "default": "3"},
    ],
}


def _load_vocab():
    with open(_VOCAB_PATH, encoding="utf-8") as f:
        return json.load(f)


def draw_cover(c, **meta):
    """Draw cover page. Called by generate.py with cover field values."""
    count      = int(meta.get("count", 3))
    difficulty = meta.get("difficulty", "easy").lower()
    cfg        = _DIFFICULTY_CONFIG.get(difficulty, _DIFFICULTY_CONFIG["easy"])
    date_str   = date.today().strftime("%B %d, %Y")
    _render_cover(c, count=count, size_label=cfg["size_label"], difficulty=difficulty, date_str=date_str)


def generate(output_path: str, **meta):
    """Generate the crossword notebook PDF."""
    difficulty = meta.get("difficulty", "easy").lower()
    count      = int(meta.get("count", 3))

    if difficulty not in _DIFFICULTY_CONFIG:
        raise ValueError(f"Unknown difficulty {difficulty!r}. Expected one of {list(_DIFFICULTY_CONFIG)}")
    cfg          = _DIFFICULTY_CONFIG[difficulty]
    grid_size    = cfg["grid_size"]
    target_words = cfg["target"]
    size_label   = cfg["size_label"]

    vocab          = _load_vocab()
    candidate_pool = build_candidate_pool(vocab, difficulty)

    c = rl_canvas.Canvas(output_path, pagesize=(PAGE_W, PAGE_H))

    draw_cover(c, difficulty=difficulty, count=count)
    c.showPage()

    for i in range(count):
        puzzle = generate_puzzle(candidate_pool, grid_size=grid_size, target_count=target_words)
        draw_puzzle_page(c, puzzle, puzzle_num=i + 1, size_label=size_label, difficulty=difficulty)
        c.showPage()
        draw_solution_page(c, puzzle, puzzle_num=i + 1)
        c.showPage()

    c.save()
