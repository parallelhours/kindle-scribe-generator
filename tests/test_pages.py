import io
import pytest
from reportlab.pdfgen import canvas as rl_canvas
from pypdf import PdfReader
from core import dimensions as D
from templates.scorecard import template as T


def _canvas_to_reader(draw_fn):
    """Call draw_fn(c) on a single-page canvas, return a PdfReader."""
    buf = io.BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=(D.PAGE_W, D.PAGE_H))
    draw_fn(c)
    c.showPage()
    c.save()
    buf.seek(0)
    return PdfReader(buf)


def test_page1_renders_without_error():
    reader = _canvas_to_reader(T.draw_page1)
    assert len(reader.pages) == 1


def test_lineup_page_renders_without_error():
    reader = _canvas_to_reader(T.draw_lineup_page)
    assert len(reader.pages) == 1


def test_lineup_page_dimensions():
    reader = _canvas_to_reader(T.draw_lineup_page)
    page = reader.pages[0]
    assert abs(float(page.mediabox.width)  - D.PAGE_W) < 1.0
    assert abs(float(page.mediabox.height) - D.PAGE_H) < 1.0


def test_page2_renders_without_error():
    reader = _canvas_to_reader(T.draw_page2)
    assert len(reader.pages) == 1


def test_full_scorecard_has_six_pages():
    buf = io.BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=(D.PAGE_W, D.PAGE_H))
    T.draw_page1(c);  c.showPage()
    T.draw_page2(c);  c.showPage()
    for _ in range(4):
        T.draw_lineup_page(c)
        c.showPage()
    c.save()
    buf.seek(0)
    assert len(PdfReader(buf).pages) == 6


def test_all_pages_have_correct_dimensions():
    buf = io.BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=(D.PAGE_W, D.PAGE_H))
    T.draw_page1(c);  c.showPage()
    T.draw_page2(c);  c.showPage()
    for _ in range(4):
        T.draw_lineup_page(c)
        c.showPage()
    c.save()
    buf.seek(0)
    reader = PdfReader(buf)
    for i, page in enumerate(reader.pages):
        assert abs(float(page.mediabox.width)  - D.PAGE_W) < 1.0, f"Page {i+1} width wrong"
        assert abs(float(page.mediabox.height) - D.PAGE_H) < 1.0, f"Page {i+1} height wrong"


def test_generate_writes_pdf(tmp_path):
    out = str(tmp_path / "test_scorecard.pdf")
    T.generate(out)
    reader = PdfReader(out)
    assert len(reader.pages) == T.METADATA["pages"]


def test_generate_with_cover(tmp_path):
    out = str(tmp_path / "cover_scorecard.pdf")
    T.generate(out, visitor="Mets", home="Rockies", date="2026-05-06")
    reader = PdfReader(out)
    assert len(reader.pages) == T.METADATA["pages"] + 1  # +1 for cover


def test_draw_cover_renders_without_error():
    buf = io.BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=(D.PAGE_W, D.PAGE_H))
    T.draw_cover(c, title="Test Game", visitor="Mets", home="Rockies",
                 date="2026-05-06", ballpark="Coors Field")
    c.showPage()
    c.save()
    buf.seek(0)
    assert len(PdfReader(buf).pages) == 1


def test_draw_cover_renders_with_empty_meta():
    buf = io.BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=(D.PAGE_W, D.PAGE_H))
    T.draw_cover(c)
    c.showPage()
    c.save()
    buf.seek(0)
    assert len(PdfReader(buf).pages) == 1


def test_parse_cover_tokens_basic():
    from generate import _parse_cover_tokens
    result = _parse_cover_tokens(["visitor:Mets", "home:Rockies", "date:2026-05-06"])
    assert result == {"visitor": "Mets", "home": "Rockies", "date": "2026-05-06"}


def test_parse_cover_tokens_empty():
    from generate import _parse_cover_tokens
    assert _parse_cover_tokens([]) == {}


def test_parse_cover_tokens_ignores_invalid():
    from generate import _parse_cover_tokens
    result = _parse_cover_tokens(["visitor:Mets", "notakeyvalue", "home:Rockies"])
    assert result == {"visitor": "Mets", "home": "Rockies"}
