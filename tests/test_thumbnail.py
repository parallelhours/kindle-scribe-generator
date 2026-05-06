import io
import pytest
from reportlab.pdfgen import canvas as rl_canvas
from pypdf import PdfReader
from core.dimensions import PAGE_W, PAGE_H


def _make_one_page_pdf(path: str) -> None:
    c = rl_canvas.Canvas(path, pagesize=(PAGE_W, PAGE_H))
    c.setFont("Helvetica-Bold", 20)
    c.drawCentredString(PAGE_W / 2, PAGE_H / 2, "Cover")
    c.showPage()
    c.save()


def test_embed_cover_thumbnail_produces_valid_pdf(tmp_path):
    from core.thumbnail import embed_cover_thumbnail
    out = str(tmp_path / "thumb_test.pdf")
    _make_one_page_pdf(out)
    embed_cover_thumbnail(out)
    reader = PdfReader(out)
    assert len(reader.pages) == 1


def test_embed_cover_thumbnail_cleans_up_on_error(tmp_path):
    from core.thumbnail import embed_cover_thumbnail
    import glob
    bad_path = str(tmp_path / "nonexistent.pdf")
    with pytest.raises(Exception):
        embed_cover_thumbnail(bad_path)
    tmp_files = glob.glob(str(tmp_path / "*_thumb_tmp.pdf"))
    assert tmp_files == [], "Temp file should be cleaned up on error"
