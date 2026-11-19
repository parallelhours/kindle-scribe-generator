# Copyright (C) 2026 Paul Monday — GNU GPL v3 or later. See LICENSE.
"""Edition-workflow hardening: user additions must never hang, clip or print wrong Spanish."""
import io

import pytest
from pypdf import PdfReader
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas as rl_canvas

from core.dimensions import MARGIN, PAGE_H, PAGE_W
from templates.spanish import pages as P
from templates.spanish.content import additions
from templates.spanish.doc import Doc
from templates.spanish.layout import LayoutOverflow
from templates.spanish.sections import build_verbs, build_vocab, section_entries
from templates.spanish.template import Options, _render, parse_options

FORMS = ["a", "b", "c", "d", "e"]


def _spy_doc():
    drawn = []

    class Spy(rl_canvas.Canvas):
        def setFont(self, name, size, leading=None):
            self._spy_font = (name, size)
            return super().setFont(name, size, leading)

        def drawString(self, x, y, text, *a, **kw):
            drawn.append((x, y, text, *self._spy_font))
            return super().drawString(x, y, text, *a, **kw)

    return Doc(Spy(io.BytesIO(), pagesize=(PAGE_W, PAGE_H)), "2026-01-01"), drawn


def _plain_doc():
    return Doc(rl_canvas.Canvas(io.BytesIO(), pagesize=(PAGE_W, PAGE_H)), "2026-01-01")


# ---- 1. phrase index never hangs ------------------------------------------
def test_index_overlong_phrase_raises_not_hangs():
    p = {"es": "x" * 112, "en": "meaning", "use": "u", "examples": [("a", "b")] * 2}
    with pytest.raises(LayoutOverflow, match="xxxx"):
        P.draw_phrase_index(_plain_doc(), [p])


def test_index_long_english_terminates_with_ellipsis():
    p = {"es": "a menudo", "en": "word " * 80, "use": "u", "examples": [("a", "b")] * 2}
    doc, drawn = _spy_doc()
    P.draw_phrase_index(doc, [p])
    assert any(t.endswith("…") for _, _, t, _, _ in drawn)


# ---- 2. My Verbs blocks fit ------------------------------------------------
def _long_verb():
    forms = {t: ["despertábamos", "nos despertábamos", "se despertaban", "me despierto",
                 "nos despertábamos"] for t in
             ("present", "preterite", "imperfect", "future", "subjunctive")}
    return {"verb": "despertarse completamente y del todo", "en": "to wake up " * 6,
            "forms": forms,
            "examples": [("Me despierto muy temprano todos los días de la semana porque "
                          "tengo que ir a trabajar en la ciudad y no quiero llegar tarde.",
                          "I wake up very early every day of the week because I have to go "
                          "to work in the city and I do not want to be late.")] * 2}


def test_verb_block_fits_long_text():
    doc, drawn = _spy_doc()
    P.draw_my_verbs_page(doc, [_long_verb()])
    assert drawn
    pw = (PAGE_W - 2 * MARGIN) * 0.2
    cw = (PAGE_W - 2 * MARGIN - pw) / 5
    for x, y, text, font, size in drawn:
        assert size >= 6.0 - 1e-6, (text, size)
        right = x + stringWidth(text, font, size)
        assert MARGIN - 1e-6 <= x and right <= PAGE_W - MARGIN + 1e-6, (text, x, right)
        if text in ("nos despertábamos", "se despertaban"):
            col = int((x - MARGIN - pw) // cw)
            assert right <= MARGIN + pw + (col + 1) * cw + 1e-6, (text, x, right)


def test_verb_example_too_long_raises():
    e = _long_verb()
    e["examples"] = [("palabra " * 120, "x")]
    with pytest.raises(LayoutOverflow, match="palabra"):
        P.draw_my_verbs_page(_plain_doc(), [e])


# ---- 3. validation ---------------------------------------------------------
def _ok_verb():
    return {"verb": "dormir", "en": "to sleep",
            "forms": {"present": list(FORMS), "preterite": list(FORMS)},
            "examples": [("Duermo.", "I sleep.")]}


def test_valid_verb_and_word_group_pass():
    additions.validate_verb(_ok_verb())
    additions.validate_word_group({"topic": "t", "date": "d", "words": [("el", "a", "b")]})


@pytest.mark.parametrize("mutate, match", [
    (lambda e: e["forms"].update(pres_subj=list(FORMS)), "dormir.*pres_subj"),
    (lambda e: e["forms"].update(present=FORMS + ["vosotros"]), "dormir.*present.*5"),
    (lambda e: e["forms"].update(present=FORMS[:4]), "dormir.*present.*5"),
    (lambda e: e.update(examples=[("a", "b")] * 3), "dormir.*examples"),
    (lambda e: e.update(examples=[("only es",)]), "dormir.*example"),
    (lambda e: e.update(verb=""), "verb"),
    (lambda e: e["forms"].update(present=["a", "b", "c", "d", "中"]), "dormir.*cp1252"),
])
def test_bad_verb_shapes(mutate, match):
    e = _ok_verb()
    mutate(e)
    with pytest.raises(ValueError, match=match):
        additions.validate_verb(e)


@pytest.mark.parametrize("group, match", [
    ({"topic": "Food", "words": [("el", "pan")]}, "Food.*pan.*3"),
    ({"topic": "Food", "words": [("el", "pan", "bread", "x")]}, "Food.*3"),
    ({"topic": "Food"}, "Food.*words"),
    ({"topic": "Food", "wrods": [], "words": []}, "Food.*wrods"),
])
def test_bad_word_groups(group, match):
    with pytest.raises(ValueError, match=match):
        additions.validate_word_group(group)


def test_builders_validate_before_drawing(monkeypatch):
    bad = _ok_verb()
    bad["forms"]["present"] = FORMS + ["vosotros"]
    monkeypatch.setattr(additions, "MY_VERBS", [bad])
    opts = parse_options({})
    with pytest.raises(ValueError, match="dormir"):
        build_verbs(_plain_doc(), opts)
    monkeypatch.setattr(additions, "MY_WORDS", [{"topic": "T", "words": [("el", "pan")]}])
    with pytest.raises(ValueError, match="pan"):
        build_vocab(_plain_doc(), opts)


def test_shipped_additions_validate():
    for v in additions.MY_VERBS:
        additions.validate_verb(v)
    for g in additions.MY_WORDS:
        additions.validate_word_group(g)


def test_filled_verbs_page_never_prints_vosotros(tmp_path):
    e = _ok_verb()
    e["forms"] = {t: ["yo1", "tu1", "el1", "nos1", "ellos1"] for t in
                  ("present", "preterite", "imperfect", "future", "subjunctive")}
    path = tmp_path / "v.pdf"
    doc = Doc(rl_canvas.Canvas(str(path), pagesize=(PAGE_W, PAGE_H)), "e")
    P.draw_my_verbs_page(doc, [e])
    doc.c.save()
    text = PdfReader(str(path)).pages[0].extract_text()
    assert "vosotros" not in text.replace("nosotros", "")
    assert "ellos1" in text


# ---- 4. contents skip undrawn fill-page rows -------------------------------
def test_contents_skip_undrawn_rows(monkeypatch):
    monkeypatch.setattr(additions, "MY_VERBS", [])
    monkeypatch.setattr(additions, "MY_WORDS", [])
    zero = Options(("verbs", "phrases", "vocab"), 0, 0, 0)
    for s, label in (("verbs", "My Verbs"), ("phrases", "My Phrases"),
                     ("vocab", "Word pages")):
        assert label not in [e[0] for e in section_entries(s, zero)]
    full = Options(("verbs", "phrases", "vocab"), 1, 1, 1)
    for s, label in (("verbs", "My Verbs"), ("phrases", "My Phrases"),
                     ("vocab", "Word pages")):
        assert label in [e[0] for e in section_entries(s, full)]


def test_zero_pages_has_no_dead_contents_rows_and_layout_stable():
    opts = parse_options({"verb_pages": "0", "phrase_pages": "0", "vocab_pages": "0"})
    d1 = _render(rl_canvas.Canvas(io.BytesIO(), pagesize=(PAGE_W, PAGE_H)), opts, {}, None)
    d2 = _render(rl_canvas.Canvas(io.BytesIO(), pagesize=(PAGE_W, PAGE_H)), opts, {},
                 dict(d1.dests))
    assert d1.log == d2.log
    assert not {"verbs-my", "phrases-my", "vocab-words"} & set(d1.dests)
