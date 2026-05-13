# Copyright (C) 2026 Paul Monday — GNU GPL v3 or later. See LICENSE.
import io
import os
import tempfile
from reportlab.pdfgen import canvas as rl_canvas
from pypdf import PdfReader
from core import dimensions as D
from templates.scorecard import template as T


def test_weekly_activities_metadata(weekly_mod):
    m = weekly_mod.METADATA
    assert m["name"] == "Weekly Planner"
    assert m["output"] == "weekly-activity-notebook.pdf"
    assert m["pages"] == 7
    assert "template_fields" in m
    fields = {f["name"] for f in m["template_fields"]}
    assert fields == {"first_day", "days"}


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


def test_weekly_activities_default_render(weekly_mod):
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        path = f.name
    try:
        weekly_mod.generate(path)
        reader = PdfReader(path)
        assert len(reader.pages) == 7
        page = reader.pages[0]
        assert abs(float(page.mediabox.width)  - 336.96) < 1.0
        assert abs(float(page.mediabox.height) - 449.28) < 1.0
    finally:
        os.unlink(path)


def test_weekly_activities_custom_params(weekly_mod):
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        path = f.name
    try:
        weekly_mod.generate(path, first_day="Sunday", days="3")
        assert len(PdfReader(path).pages) == 3
    finally:
        os.unlink(path)


def test_weekly_activities_sunday_start(weekly_mod):
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        path = f.name
    try:
        weekly_mod.generate(path, first_day="Sunday", days="7")
        assert len(PdfReader(path).pages) == 7
    finally:
        os.unlink(path)


def test_weekly_activities_more_than_7_days(weekly_mod):
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        path = f.name
    try:
        weekly_mod.generate(path, days="14")
        assert len(PdfReader(path).pages) == 14
    finally:
        os.unlink(path)


def test_weekly_activities_unknown_first_day_falls_back_to_monday(weekly_mod):
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        path = f.name
    try:
        weekly_mod.generate(path, first_day="Blursday", days="1")
        assert len(PdfReader(path).pages) == 1
    finally:
        os.unlink(path)


# ── Prompt Notebook tests ────────────────────────────────────────────────────


def test_prompt_notebook_metadata(prompt_mod):
    m = prompt_mod.METADATA
    assert m["name"] == "Prompt Notebook"
    assert m["output"] == "prompt-notebook.pdf"
    assert m["pages"] == 5
    assert "cover_fields" in m
    assert "template_fields" in m
    fields = {f["name"] for f in m["cover_fields"]}
    assert fields == {"title", "date"}
    fields = {f["name"] for f in m["template_fields"]}
    assert fields == {"count", "layout", "framework"}


def test_prompt_notebook_default_generate(prompt_mod):
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        path = f.name
    try:
        prompt_mod.generate(path)
        reader = PdfReader(path)
        assert len(reader.pages) == 5
        for page in reader.pages:
            assert abs(float(page.mediabox.width)  - D.PAGE_W) < 1.0
            assert abs(float(page.mediabox.height) - D.PAGE_H) < 1.0
    finally:
        os.unlink(path)


def test_prompt_notebook_with_cover(prompt_mod):
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        path = f.name
    try:
        prompt_mod.generate(path, title="My Book", date="2026-05-01")
        reader = PdfReader(path)
        assert len(reader.pages) == 6  # +1 for cover
    finally:
        os.unlink(path)


def test_prompt_notebook_compact_layout(prompt_mod):
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        path = f.name
    try:
        prompt_mod.generate(path, layout="compact")
        reader = PdfReader(path)
        assert len(reader.pages) == 2  # 1 overview + 1 prompt
    finally:
        os.unlink(path)


def test_prompt_notebook_expanded_layout(prompt_mod):
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        path = f.name
    try:
        prompt_mod.generate(path, layout="expanded")
        reader = PdfReader(path)
        assert len(reader.pages) == 5  # 1 overview + 4 expanded
    finally:
        os.unlink(path)


def test_prompt_notebook_multiple_prompts_compact(prompt_mod):
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        path = f.name
    try:
        prompt_mod.generate(path, count="3", layout="compact")
        reader = PdfReader(path)
        assert len(reader.pages) == 4  # 1 overview + 3 prompts
    finally:
        os.unlink(path)


def test_prompt_notebook_multiple_prompts_expanded(prompt_mod):
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        path = f.name
    try:
        prompt_mod.generate(path, count="2", layout="expanded")
        reader = PdfReader(path)
        assert len(reader.pages) == 9  # 1 overview + 2 * 4 pages
    finally:
        os.unlink(path)


def test_prompt_notebook_prompt_framework_compact(prompt_mod):
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        path = f.name
    try:
        prompt_mod.generate(path, framework="prompt", layout="compact")
        reader = PdfReader(path)
        assert len(reader.pages) == 2  # 1 overview + 1 prompt
    finally:
        os.unlink(path)


def test_prompt_notebook_prompt_framework_expanded(prompt_mod):
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        path = f.name
    try:
        prompt_mod.generate(path, framework="prompt", layout="expanded")
        reader = PdfReader(path)
        assert len(reader.pages) == 4  # 1 overview + 3 expanded (6/2)
    finally:
        os.unlink(path)


def test_prompt_notebook_with_cover_and_custom_params(prompt_mod):
    with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
        path = f.name
    try:
        prompt_mod.generate(path, title="My Book", date="2026-05-01",
                            count="2", layout="compact")
        reader = PdfReader(path)
        assert len(reader.pages) == 4  # cover + overview + 2 prompts
    finally:
        os.unlink(path)


def test_prompt_notebook_draw_cover(prompt_mod):
    buf = io.BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=(D.PAGE_W, D.PAGE_H))
    prompt_mod.draw_cover(c, title="Test Notebook", date="2026-05-13")
    c.showPage()
    c.save()
    buf.seek(0)
    assert len(PdfReader(buf).pages) == 1


def test_prompt_notebook_draw_cover_empty(prompt_mod):
    buf = io.BytesIO()
    c = rl_canvas.Canvas(buf, pagesize=(D.PAGE_W, D.PAGE_H))
    prompt_mod.draw_cover(c)
    c.showPage()
    c.save()
    buf.seek(0)
    assert len(PdfReader(buf).pages) == 1
