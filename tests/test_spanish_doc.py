# Copyright (C) 2026 Paul Monday — GNU GPL v3 or later. See LICENSE.
import io

from pypdf import PdfReader
from reportlab.pdfgen import canvas as rl_canvas

from core.dimensions import PAGE_H, PAGE_W
from templates.spanish.doc import Doc, PageRecord


def canvas_to_buffer():
    return rl_canvas.Canvas(io.BytesIO(), pagesize=(PAGE_W, PAGE_H))


def canvas_at(path):
    return rl_canvas.Canvas(str(path), pagesize=(PAGE_W, PAGE_H))


def count_link_annots(path):
    n = 0
    for page in PdfReader(str(path)).pages:
        for a in page.get("/Annots", []) or []:
            if a.get_object().get("/Subtype") == "/Link":
                n += 1
    return n


def test_dests_and_log_recorded():
    d = Doc(canvas_to_buffer(), edition="2026-11-18")
    d.start_page("reference", "Preterite", "verbs", "preterite", dests=("t-preterite",))
    d.end_page()
    assert d.dests == {"t-preterite": 1}
    assert d.log[0] == PageRecord(1, "reference", "verbs", "preterite")


def test_link_suppressed_for_unknown_dest_in_pass2(tmp_path):
    d = Doc(canvas_at(tmp_path / "x.pdf"), "2026-11-18", page_of={"a": 1})
    d.start_page("contents", "C", None, dests=("a",))
    assert d.link((10, 10, 50, 20), "a") is True
    assert d.link((10, 30, 50, 40), "missing") is False
    d.end_page()
    d.c.save()
    assert count_link_annots(tmp_path / "x.pdf") == 1


def test_pass1_link_always_true_draws_nothing():
    d = Doc(canvas_to_buffer(), "2026-11-18")
    d.start_page("contents", "C", None)
    assert d.link((10, 10, 50, 20), "anything") is True
    assert d.page_of("anything") is None


def test_header_contents_link_skipped_on_own_contents_page(tmp_path):
    pof = {"verbs-contents": 1, "contents": 1}
    d = Doc(canvas_at(tmp_path / "x.pdf"), "e", page_of=pof)
    d.start_page("contents", "Verbs", "verbs", dests=("verbs-contents",))
    d.end_page()
    d.start_page("reference", "Topic", "verbs", "t")
    d.end_page()
    d.c.save()
    assert count_link_annots(tmp_path / "x.pdf") == 1  # page 2 only


def test_outline_and_footer(tmp_path):
    p = tmp_path / "o.pdf"
    d = Doc(canvas_at(p), "2026-11-18")
    d.start_page("contents", "Contents", None, dests=("contents",))
    d.outline("Contents", "contents", 0)
    d.end_page()
    d.start_page("reference", "Preterite", "verbs", "preterite", dests=("t-preterite",))
    d.outline("Preterite", "t-preterite", 1)
    d.end_page()
    d.c.save()
    r = PdfReader(str(p))
    assert r.outline[0].title == "Contents"
    assert isinstance(r.outline[1], list) and r.outline[1][0].title == "Preterite"
    assert "Edición 2026-11-18 · 1" in r.pages[0].extract_text()
    assert "Edición 2026-11-18 · 2" in r.pages[1].extract_text()


def test_header_section_labels(tmp_path):
    p = tmp_path / "s.pdf"
    d = Doc(canvas_at(p), "e")
    for i, sec in enumerate(("verbs", "phrases", "vocab")):
        d.start_page("reference", "T", sec, f"t{i}")
        d.end_page()
    d.c.save()
    r = PdfReader(str(p))
    for page, label in zip(r.pages, ("Verbs", "Phrases & Grammar", "Vocab")):
        assert label in page.extract_text()
