import io
from pypdf import PdfReader
from reportlab.pdfgen import canvas as rl_canvas
from core import dimensions as D
from templates.crossword.generator import PlacedWord, PuzzleResult
from templates.crossword.renderer import (
    draw_puzzle_page, draw_solution_page, draw_cover
)

def _make_canvas():
    buf = io.BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=(D.PAGE_W, D.PAGE_H))
    return c, buf

def _make_puzzle_result():
    grid = [[None]*9 for _ in range(9)]
    for i, ch in enumerate("hola"):
        grid[4][2 + i] = ch
    for i, ch in enumerate("hablar"):
        grid[2 + i][3] = ch
    words = [
        PlacedWord("hola",   "hello",    "hola",   4, 2, "across", 1),
        PlacedWord("hablar", "to speak", "hablar", 2, 3, "down",   2),
    ]
    return PuzzleResult(grid=grid, placed_words=words, grid_size=9)

def test_draw_puzzle_page_does_not_raise():
    c, buf = _make_canvas()
    result = _make_puzzle_result()
    draw_puzzle_page(c, result, puzzle_num=1, size_label="Small", difficulty="easy")
    c.showPage()
    c.save()

def test_draw_solution_page_does_not_raise():
    c, buf = _make_canvas()
    result = _make_puzzle_result()
    draw_solution_page(c, result, puzzle_num=1)
    c.showPage()
    c.save()

def test_draw_cover_does_not_raise():
    c, buf = _make_canvas()
    draw_cover(c, count=5, size_label="Large", difficulty="medium", date_str="May 22, 2026")
    c.showPage()
    c.save()

def test_full_notebook_page_count():
    """1 cover + 2*N puzzle pages = 1+2N total."""
    buf = io.BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=(D.PAGE_W, D.PAGE_H))
    result = _make_puzzle_result()

    draw_cover(c, count=3, size_label="Small", difficulty="easy", date_str="May 22, 2026")
    c.showPage()

    for i in range(3):
        draw_puzzle_page(c, result, puzzle_num=i+1, size_label="Small", difficulty="easy")
        c.showPage()
        draw_solution_page(c, result, puzzle_num=i+1)
        c.showPage()

    c.save()
    buf.seek(0)
    reader = PdfReader(buf)
    assert len(reader.pages) == 7  # 1 + 2*3


def test_template_metadata():
    import importlib.util
    from pathlib import Path
    spec = importlib.util.spec_from_file_location(
        "crossword_template",
        Path(__file__).parent.parent / "templates" / "crossword" / "template.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    m = mod.METADATA
    assert m["name"] == "Cruza y Aprende"
    assert m["output"] == "cruza-y-aprende.pdf"
    assert "template_fields" in m
    field_names = {f["name"] for f in m["template_fields"]}
    assert field_names == {"difficulty", "count"}

def test_template_generate_creates_pdf():
    import importlib.util, tempfile, os
    from pathlib import Path
    from pypdf import PdfReader
    spec = importlib.util.spec_from_file_location(
        "crossword_template",
        Path(__file__).parent.parent / "templates" / "crossword" / "template.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        out = f.name
    try:
        mod.generate(out, size="small", difficulty="easy", count="2")
        reader = PdfReader(out)
        assert len(reader.pages) == 5  # 1 cover + 2*2 puzzle pages
    finally:
        os.unlink(out)

def test_template_generate_large_medium():
    import importlib.util, tempfile, os
    from pathlib import Path
    from pypdf import PdfReader
    spec = importlib.util.spec_from_file_location(
        "crossword_template",
        Path(__file__).parent.parent / "templates" / "crossword" / "template.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        out = f.name
    try:
        mod.generate(out, size="large", difficulty="medium", count="1")
        reader = PdfReader(out)
        assert len(reader.pages) == 3  # 1 cover + 2*1
    finally:
        os.unlink(out)


# --- Crossword review 2026-11-18: sentence clues wrap instead of truncating ---
import pytest


@pytest.mark.parametrize("difficulty", ["easy", "medium", "hard"])
def test_wrapped_clues_fit_below_grid(difficulty):
    import io, json, random
    from reportlab.pdfgen import canvas as rl_canvas
    from core.dimensions import PAGE_W, PAGE_H, MARGIN
    from templates.crossword.template import _VOCAB_PATH, _DIFFICULTY_CONFIG
    from templates.crossword.clues import build_candidate_pool
    from templates.crossword.generator import generate_puzzle
    from templates.crossword.renderer import (
        puzzle_layout, _clue_block_height, MIN_CELL, HEADER_FONT)
    with open(_VOCAB_PATH, encoding="utf-8") as f:
        pool = build_candidate_pool(json.load(f), difficulty)
    cfg = _DIFFICULTY_CONFIG[difficulty]
    c = rl_canvas.Canvas(io.BytesIO(), pagesize=(PAGE_W, PAGE_H))
    random.seed(11)
    for _ in range(8):
        result = generate_puzzle(pool, cfg["grid_size"], cfg["target"], mix=cfg["mix"])
        cell, size = puzzle_layout(c, result)
        assert cell >= MIN_CELL
        grid_bottom = PAGE_H - MARGIN - HEADER_FONT - 6 - cell * cfg["grid_size"]
        clue_area = grid_bottom - 6 - MARGIN
        assert _clue_block_height(c, result.placed_words, (PAGE_W - 2 * MARGIN) / 2, size) <= clue_area + 0.01


def test_wrap_clue_never_drops_words():
    import io
    from reportlab.pdfgen import canvas as rl_canvas
    from templates.crossword.renderer import _wrap_clue
    c = rl_canvas.Canvas(io.BytesIO())
    clue = "Con más tiempo, nosotros ___ (contribuir) con dinero."
    lines = _wrap_clue(c, 12, clue, 100, 7)
    assert len(lines) > 1
    assert " ".join(lines) == "12. " + clue
