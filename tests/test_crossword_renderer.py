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
