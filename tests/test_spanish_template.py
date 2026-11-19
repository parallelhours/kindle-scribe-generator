# Copyright (C) 2026 Paul Monday — GNU GPL v3 or later. See LICENSE.
import io

import pytest
from pypdf import PdfReader
from reportlab.pdfgen import canvas as rl_canvas

from core.dimensions import PAGE_H, PAGE_W
from templates.spanish.layout import LayoutOverflow
from templates.spanish.sections import render_topic
from templates.spanish.template import Options, _render, generate, parse_options


@pytest.mark.parametrize("raw,expected", [
    ({}, ("verbs", "phrases", "vocab")),
    ({"sections": "Verbs, VOCAB"}, ("verbs", "vocab")),
    ({"sections": "vocab verbs"}, ("verbs", "vocab")),
    ({"sections": "verbs,all"}, ("verbs", "phrases", "vocab")),
])
def test_parse_sections(raw, expected):
    assert parse_options(raw).sections == expected


@pytest.mark.parametrize("raw", [{"sections": "grammar"}, {"verb_pages": "-2"}, {"verb_pages": "ten"}])
def test_parse_options_rejects(raw):
    with pytest.raises(ValueError, match=list(raw)[0]):
        parse_options(raw)


def test_defaults():
    o = parse_options({})
    assert (o.verb_pages, o.phrase_pages, o.vocab_pages) == (10, 8, 20)


def test_zero_fill_pages_allowed():
    assert parse_options({"verb_pages": "0"}).verb_pages == 0


VARIANTS = ["all", "verbs", "phrases", "vocab", "verbs,vocab"]


@pytest.mark.parametrize("sections", VARIANTS)
def test_generate_each_variant(tmp_path, sections):
    out = tmp_path / "s.pdf"
    generate(str(out), sections=sections, verb_pages="1", phrase_pages="1", vocab_pages="1")
    r = PdfReader(str(out))
    assert "Edición" in r.pages[0].extract_text()
    assert len(r.outline) > 0
    assert len(r.pages) == len(_doc(sections, verb_pages="1", phrase_pages="1",
                                    vocab_pages="1").log)


def _outline_titles(path):
    out = []

    def walk(items):
        for it in items:
            if isinstance(it, list):
                walk(it)
            else:
                out.append(it.title)

    walk(PdfReader(str(path)).outline)
    return out


def test_master_contents_only_when_multiple(tmp_path):
    a, b = tmp_path / "a.pdf", tmp_path / "b.pdf"
    generate(str(a), sections="all", verb_pages="0", phrase_pages="0", vocab_pages="0")
    generate(str(b), sections="verbs", verb_pages="0")
    assert "Contents" in _outline_titles(a)
    assert "Contents" not in _outline_titles(b)
    assert "contents" in _doc("all").dests
    assert "contents" not in _doc("verbs").dests


def _doc(sections="all", **kw):
    opts = parse_options({"sections": sections, **kw})
    c = rl_canvas.Canvas(io.BytesIO(), pagesize=(PAGE_W, PAGE_H))
    doc = _render(c, opts, {}, None)
    return doc


def test_every_topic_followed_by_practice():
    log = _doc().log
    i = 0
    while i < len(log):
        if log[i].kind == "reference":
            tid = log[i].topic_id
            while i < len(log) and log[i].kind == "reference" and log[i].topic_id == tid:
                i += 1
            assert i < len(log) and log[i].kind == "practice" and log[i].topic_id == tid
        else:
            i += 1


def test_practice_false_topic_has_no_practice_page():
    c = rl_canvas.Canvas(io.BytesIO(), pagesize=(PAGE_W, PAGE_H))
    from templates.spanish.doc import Doc
    doc = Doc(c, "2026-01-01")
    render_topic(doc, "vocab", {"id": "x", "title": "X", "practice": False,
                                "pages": [[{"type": "text", "text": "hola"}]]}, level=0)
    assert [r.kind for r in doc.log] == ["nav"]


def test_overflow_names_topic_and_page():
    c = rl_canvas.Canvas(io.BytesIO(), pagesize=(PAGE_W, PAGE_H))
    from templates.spanish.doc import Doc
    doc = Doc(c, "2026-01-01")
    big = {"id": "big", "title": "Big", "pages": [[{"type": "spacer", "h": 5000}]]}
    with pytest.raises(LayoutOverflow, match="big.*page 0"):
        render_topic(doc, "vocab", big, level=0)


@pytest.mark.parametrize("sections", VARIANTS)
def test_no_dangling_links(tmp_path, sections):
    out = tmp_path / "s.pdf"
    generate(str(out), sections=sections, verb_pages="1", phrase_pages="1", vocab_pages="1")
    r = PdfReader(str(out))
    page_ids = {p.indirect_reference.idnum for p in r.pages}
    n_links = 0
    for page in r.pages:
        for a in page.get("/Annots", []) or []:
            a = a.get_object()
            if a.get("/Subtype") != "/Link":
                continue
            n_links += 1
            d = a.get("/Dest")
            if d is None:
                d = a["/A"]["/D"]
            assert d[0].idnum in page_ids
    assert n_links > 0


def test_fill_page_counts():
    log = _doc(verb_pages="3", phrase_pages="2", vocab_pages="4").log
    kinds = [r.kind for r in log]
    assert kinds.count("fill-verb") == 3
    assert kinds.count("fill-phrase") == 2
    assert kinds.count("fill-word") == 4


def test_two_pass_layout_identical():
    opts = parse_options({"verb_pages": "1", "phrase_pages": "1", "vocab_pages": "1"})
    c1 = rl_canvas.Canvas(io.BytesIO(), pagesize=(PAGE_W, PAGE_H))
    d1 = _render(c1, opts, {}, None)
    c2 = rl_canvas.Canvas(io.BytesIO(), pagesize=(PAGE_W, PAGE_H))
    d2 = _render(c2, opts, {}, dict(d1.dests))
    assert d1.log == d2.log and d1.dests == d2.dests


def test_cli_discovers_spanish():
    from generate import discover_templates
    assert "spanish" in discover_templates()
