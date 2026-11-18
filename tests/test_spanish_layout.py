# Copyright (C) 2026 Paul Monday — GNU GPL v3 or later. See LICENSE.
import io

import pytest
from reportlab.pdfbase.pdfmetrics import stringWidth
from reportlab.pdfgen import canvas as rl_canvas

from core import dimensions as D
from templates.spanish.layout import (
    BODY_SIZE, CELL_SIZE, MIN_CELL, VOS_GRAY, FONT_FOR,
    Frame, LayoutOverflow, block_height, draw_block, fit_size,
    parse_rich, wrap_rich,
)

VERBS_STUB = {
    "tener": {
        "en": "to have",
        "present": ["tengo", "tienes", "tiene", "tenemos", "tenéis", "tienen"],
        "preterite": ["tuve", "tuviste", "tuvo", "tuvimos", "tuvisteis", "tuvieron"],
        "imperfect": ["tenía", "tenías", "tenía", "teníamos", "teníais", "tenían"],
        "future": ["tendré", "tendrás", "tendrá", "tendremos", "tendréis", "tendrán"],
        "conditional": ["tendría", "tendrías", "tendría", "tendríamos", "tendríais", "tendrían"],
        "pres_subj": ["tenga", "tengas", "tenga", "tengamos", "tengáis", "tengan"],
        "past_subj": ["tuviera", "tuvieras", "tuviera", "tuviéramos", "tuvierais", "tuvieran"],
        "participle": "tenido", "gerund": "teniendo",
    },
    "ser": {
        "en": "to be",
        "present": ["soy", "eres", "es", "somos", "sois", "son"],
        "preterite": ["fui", "fuiste", "fue", "fuimos", "fuisteis", "fueron"],
        "imperfect": ["era", "eras", "era", "éramos", "erais", "eran"],
        "future": ["seré", "serás", "será", "seremos", "seréis", "serán"],
        "conditional": ["sería", "serías", "sería", "seríamos", "seríais", "serían"],
        "pres_subj": ["sea", "seas", "sea", "seamos", "seáis", "sean"],
        "past_subj": ["fuera", "fueras", "fuera", "fuéramos", "fuerais", "fueran"],
        "participle": "sido", "gerund": "siendo",
    },
}


class CtxStub:
    def __init__(self, known=("a", "b")):
        self.verbs = VERBS_STUB
        self.known = set(known)
        self.links = []

    def link(self, rect, dest):
        self.links.append((rect, dest))
        return dest in self.known

    def page_of(self, dest):
        return 3 if dest in self.known else None


def _canvas(cls=rl_canvas.Canvas):
    return cls(io.BytesIO(), pagesize=(D.PAGE_W, D.PAGE_H))


def test_parse_rich_styles():
    assert parse_rich("Hace **frío** ~it's cold~") == [
        ("normal", "Hace "), ("bold", "frío"), ("normal", " "), ("en", "it's cold")]


def test_wrap_rich_respects_width():
    lines = wrap_rich("palabra " * 40, 100, BODY_SIZE)
    assert len(lines) > 1
    for ln in lines:
        assert sum(stringWidth(t, FONT_FOR[s], BODY_SIZE) for s, t in ln) <= 100 + 0.01


def test_wrap_rich_preserves_styles():
    lines = wrap_rich("uno **dos** ~three~", 300, BODY_SIZE)
    assert lines == [[("normal", "uno "), ("bold", "dos"), ("normal", " "), ("en", "three")]]


def test_fit_size_shrinks_then_overflows():
    assert MIN_CELL <= fit_size("estuviéramos", 40, CELL_SIZE, MIN_CELL) < CELL_SIZE
    with pytest.raises(LayoutOverflow):
        fit_size("estuviéramos estuviéramos", 20, CELL_SIZE, MIN_CELL)


def test_frame_take_overflow():
    f = Frame(x=6, width=300, top=400, bottom=20)
    assert f.remaining() == 380
    assert f.take(300) == 400
    assert f.y == 100
    with pytest.raises(LayoutOverflow):
        f.take(100)


SAMPLES = [
    {"type": "heading", "text": "Los **verbos** ~verbs~"},
    {"type": "text", "text": "Usamos **ser** para identidad ~we use ser for identity~. " * 3},
    {"type": "bullets", "items": ["Primero **uno**", "Segundo ~second~ " * 6]},
    {"type": "example", "es": "Tengo **frío**.", "en": "I am cold."},
    {"type": "spacer", "h": 7},
    {"type": "table", "header": ["Persona", "Forma"],
     "rows": [["yo", "tengo"], ["tú", "tienes ~you have~"]],
     "widths": [0.4, 0.6], "gray_rows": [1]},
    {"type": "conj", "verbs": ["tener", "ser"], "tenses": ["present"]},
    {"type": "conj", "verbs": ["tener"], "tenses": ["present", "preterite"]},
    {"type": "compare", "left": "ser", "right": "estar",
     "rows": [["identidad", "estado ~state~"], ["origen", "ubicación"]]},
    {"type": "timeline", "caption": "Pasado y presente",
     "events": [{"label": "ayer", "pos": 0.2, "mark": "past"},
                {"label": "ahora", "pos": 0.6, "mark": "now"},
                {"label": "mañana", "pos": 0.9, "mark": "point"}]},
    {"type": "chart", "nodes": [
        {"q": "¿Terminó la acción?",
         "answers": [{"label": "sí, una vez", "tense": "pretérito", "dest": "a"},
                     {"label": "no, habitual", "tense": "imperfecto", "dest": "zzz"}]}]},
    {"type": "xref", "text": "Ver **pretérito**", "dest": "a"},
    {"type": "xref", "text": "Sin enlace"},
]


@pytest.mark.parametrize("block", SAMPLES, ids=[s["type"] + str(i) for i, s in enumerate(SAMPLES)])
def test_every_block_draws_and_height_matches(block):
    c = _canvas()
    frame = Frame(D.MARGIN, D.PAGE_W - 2 * D.MARGIN, D.PAGE_H - D.MARGIN, D.MARGIN)
    before = frame.y
    h = block_height(block, frame.width, VERBS_STUB)
    assert h > 0 or block["type"] == "spacer"
    draw_block(c, frame, block, CtxStub())
    assert before - frame.y == pytest.approx(h)
    c.showPage()
    c.save()


def test_links_called_for_chart_and_xref():
    ctx = CtxStub()
    c = _canvas()
    frame = Frame(D.MARGIN, D.PAGE_W - 2 * D.MARGIN, D.PAGE_H - D.MARGIN, D.MARGIN)
    draw_block(c, frame, SAMPLES[10], ctx)
    draw_block(c, frame, SAMPLES[11], ctx)
    assert [d for _, d in ctx.links] == ["a", "zzz", "a"]


def test_table_cell_too_long_raises():
    c = _canvas()
    block = {"type": "table", "header": ["a", "b"], "rows": [["x" * 80, "y"]], "widths": [0.1, 0.9]}
    with pytest.raises(LayoutOverflow):
        draw_block(c, Frame(6, 100, 400, 20), block, CtxStub())


def test_conj_vosotros_row_is_gray():
    events = []

    class Rec(rl_canvas.Canvas):
        def setFillGray(self, g, *a):
            events.append(("gray", g))
            super().setFillGray(g, *a)

        def drawString(self, x, y, text, *a, **k):
            events.append(("text", text))
            super().drawString(x, y, text, *a, **k)

    c = _canvas(Rec)
    frame = Frame(D.MARGIN, D.PAGE_W - 2 * D.MARGIN, D.PAGE_H - D.MARGIN, D.MARGIN)
    draw_block(c, frame, {"type": "conj", "verbs": ["tener"], "tenses": ["present"]}, CtxStub())
    i = events.index(("text", "tenéis"))
    last_gray = [g for k, g in events[:i] if k == "gray"][-1]
    assert last_gray == VOS_GRAY
    j = events.index(("text", "tienen"))
    assert [g for k, g in events[:j] if k == "gray"][-1] != VOS_GRAY


def _drawn_strings(block, ctx):
    texts, fonts = [], []

    class Rec(rl_canvas.Canvas):
        def drawString(self, x, y, text, *a, **k):
            texts.append(text)
            fonts.append(self._fontname)
            super().drawString(x, y, text, *a, **k)

        def drawRightString(self, x, y, text, *a, **k):
            texts.append(text)
            fonts.append(self._fontname)
            super().drawRightString(x, y, text, *a, **k)

    c = _canvas(Rec)
    frame = Frame(D.MARGIN, D.PAGE_W - 2 * D.MARGIN, D.PAGE_H - D.MARGIN, D.MARGIN)
    draw_block(c, frame, block, ctx)
    return texts, fonts


def test_conj_header_uses_friendly_tense_labels():
    block = {"type": "conj", "verbs": ["tener"], "tenses": ["present", "pres_subj"]}
    texts, _ = _drawn_strings(block, CtxStub())
    assert "pres. subjunctive" in texts
    assert not any("pres_subj" in t for t in texts)
    multi = {"type": "conj", "verbs": ["tener", "ser"], "tenses": ["past_subj"]}
    texts, _ = _drawn_strings(multi, CtxStub())
    assert "past subjunctive" in texts and "past_subj" not in texts


def test_xref_to_absent_dest_is_plain_without_page_number():
    block = {"type": "xref", "text": "Ver pretérito", "dest": "zzz"}
    texts, fonts = _drawn_strings(block, CtxStub())
    assert not any(t.startswith("p.") for t in texts)
    assert "Helvetica-Bold" not in fonts
    # height identical whether or not the destination resolves
    assert block_height(block, 200, VERBS_STUB) == block_height({**block, "dest": "a"}, 200, VERBS_STUB)


def test_xref_to_known_dest_is_linked_with_page_number():
    block = {"type": "xref", "text": "Ver pretérito", "dest": "a"}
    texts, fonts = _drawn_strings(block, CtxStub())
    assert "p.3" in texts and "Helvetica-Bold" in fonts
