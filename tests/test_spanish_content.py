# Copyright (C) 2026 Paul Monday — GNU GPL v3 or later. See LICENSE.
"""Accuracy checks for the spanish template's content modules."""
import importlib
import pkgutil

import pytest

import templates.spanish.content as content_pkg
from templates.crossword.conjugator import conjugate
from templates.spanish.content.verbs_data import VERBS

MASTER = ["ser", "estar", "ir", "tener", "hacer", "decir", "venir", "poder", "querer", "saber",
          "poner", "salir", "dar", "ver", "haber", "oír", "traer"]

TENSES = ["present", "preterite", "imperfect", "future", "conditional", "pres_subj", "past_subj"]

TENSE_MAP = {"present": "present", "preterite": "preterite", "imperfect": "imperfect",
             "future": "future", "conditional": "conditional", "pres_subj": "subjunctive"}
SUBJ = ["yo", "tú", "él", "nosotros", "vosotros", "ellos"]

IMPERSONAL = ("llover", "nevar")

# (verb, tense) -> reason. Only for forms the conjugator cannot represent.
KNOWN_CONJUGATOR_GAPS = {}


def test_master_verbs_present():
    assert set(MASTER) <= set(VERBS)


def test_reference_verbs_present():
    extra = ["hablar", "comer", "vivir", "llover", "nevar"]
    assert set(extra) <= set(VERBS)


@pytest.mark.parametrize("verb", sorted(VERBS))
def test_shapes(verb):
    entry = VERBS[verb]
    assert isinstance(entry["en"], str) and entry["en"].startswith("to ")
    for tense in TENSES:
        forms = entry[tense]
        assert isinstance(forms, list) and len(forms) == 6, (verb, tense)
        if verb in IMPERSONAL:
            assert forms[2], (verb, tense)
            assert [f for i, f in enumerate(forms) if i != 2] == [""] * 5, (verb, tense)
        else:
            assert all(isinstance(f, str) and f for f in forms), (verb, tense)
    assert isinstance(entry["participle"], str) and entry["participle"]
    assert isinstance(entry["gerund"], str) and entry["gerund"].endswith("ndo")


def test_impersonal_forms():
    assert VERBS["llover"]["present"][2] == "llueve"
    assert VERBS["nevar"]["present"][2] == "nieva"


@pytest.mark.parametrize("verb", [v for v in sorted(VERBS) if v not in IMPERSONAL])
def test_matches_conjugator(verb):
    for ours, theirs in TENSE_MAP.items():
        if (verb, ours) in KNOWN_CONJUGATOR_GAPS:
            continue
        assert VERBS[verb][ours] == [conjugate(verb, theirs, s) for s in SUBJ], (verb, ours)


_VOWEL_ACCENT = str.maketrans("aeiou", "áéíóú")


def _past_subj_from(ellos_pret):
    assert ellos_pret.endswith("ron"), ellos_pret
    stem = ellos_pret[:-3]
    # nosotros: accent the stem's last vowel (habla -> hablá, fue -> fué, tuvie -> tuvié)
    last = max(i for i, ch in enumerate(stem) if ch in "aeiou")
    nos_stem = stem[:last] + stem[last].translate(_VOWEL_ACCENT) + stem[last + 1:]
    return [stem + "ra", stem + "ras", stem + "ra", nos_stem + "ramos", stem + "rais", stem + "ran"]


def _impersonal_ellos(el_pret):
    # llover/nevar store only the él form; rebuild the regular ellos form (llovió -> llovieron, nevó -> nevaron)
    return el_pret[:-2] + "ieron" if el_pret.endswith("ió") else el_pret[:-1] + "aron"


@pytest.mark.parametrize("verb", sorted(VERBS))
def test_past_subjunctive_rule(verb):
    pret = VERBS[verb]["preterite"]
    actual = VERBS[verb]["past_subj"]
    if verb in IMPERSONAL:
        assert actual[2] == _past_subj_from(_impersonal_ellos(pret[2]))[2]
    else:
        assert actual == _past_subj_from(pret[5])


def test_past_subjunctive_spot_checks():
    assert VERBS["hablar"]["past_subj"][3] == "habláramos"
    assert VERBS["ser"]["past_subj"][3] == "fuéramos"
    assert VERBS["tener"]["past_subj"][3] == "tuviéramos"


def test_irregular_participles():
    expected = {"hacer": "hecho", "decir": "dicho", "ver": "visto", "poner": "puesto",
                "escribir": "escrito", "volver": "vuelto", "abrir": "abierto", "romper": "roto",
                "morir": "muerto", "cubrir": "cubierto", "descubrir": "descubierto",
                "resolver": "resuelto", "leer": "leído", "oír": "oído", "traer": "traído"}
    for v, p in expected.items():
        assert VERBS[v]["participle"] == p, v


def test_irregular_gerunds():
    expected = {"dormir": "durmiendo", "pedir": "pidiendo", "decir": "diciendo",
                "leer": "leyendo", "oír": "oyendo", "ir": "yendo", "venir": "viniendo",
                "poder": "pudiendo", "sentir": "sintiendo", "seguir": "siguiendo",
                "traer": "trayendo", "incluir": "incluyendo", "morir": "muriendo",
                "preferir": "prefiriendo"}
    for v, g in expected.items():
        assert VERBS[v]["gerund"] == g, v


def _conj_verbs(obj):
    if isinstance(obj, dict):
        if obj.get("type") == "conj":
            yield from obj.get("verbs", [])
        for v in obj.values():
            yield from _conj_verbs(v)
    elif isinstance(obj, (list, tuple)):
        for v in obj:
            yield from _conj_verbs(v)


def _content_modules():
    for info in pkgutil.walk_packages(content_pkg.__path__, content_pkg.__name__ + "."):
        yield importlib.import_module(info.name)


def test_conj_blocks_reference_known_verbs():
    for mod in _content_modules():
        for name, value in vars(mod).items():
            if name.startswith("_"):
                continue
            for verb in _conj_verbs(value):
                assert verb in VERBS, (mod.__name__, verb)


def _strings(obj):
    if isinstance(obj, str):
        yield obj
    elif isinstance(obj, dict):
        for k, v in obj.items():
            yield from _strings(k)
            yield from _strings(v)
    elif isinstance(obj, (list, tuple, set, frozenset)):
        for v in obj:
            yield from _strings(v)


def test_all_content_is_winansi():
    mods = list(_content_modules())
    assert mods
    for mod in mods:
        for name, value in vars(mod).items():
            if name.startswith("__") or callable(value) or isinstance(value, type(pkgutil)):
                continue
            for s in _strings(value):
                try:
                    s.encode("cp1252")
                except UnicodeEncodeError:
                    pytest.fail(f"{mod.__name__}.{name}: non-cp1252 string {s!r}")


# --------------------------------------------------------------------------
# Verb topics (Task 7; extended in Tasks 8 and 9)
# --------------------------------------------------------------------------
from templates.spanish.content.verb_topics import VERB_TOPICS  # noqa: E402

REQUIRED_VERB_TOPICS = ["present", "progressive", "ir-a", "acabar-de", "preterite", "imperfect",
                        "cmp-pret-imp",
                        "future", "conditional", "pres-perfect", "past-perfect", "cmp-perfects",
                        "pres-subj", "past-subj", "subj-when", "cmp-ind-subj",
                        "commands", "reflexive", "gustar", "helpers", "weather"]

NAV_TOPICS = ["which-tense", "master-irregulars", "tense-overview"]


def _blocks(topic):
    for page in topic["pages"]:
        yield from page


def test_verb_topics_present():
    assert [t["id"] for t in VERB_TOPICS if t["id"] in REQUIRED_VERB_TOPICS] == REQUIRED_VERB_TOPICS


def test_verb_topic_ids_unique():
    ids = [t["id"] for t in VERB_TOPICS]
    assert len(ids) == len(set(ids))


def test_every_topic_has_examples():
    for t in VERB_TOPICS:
        if t.get("practice", True) is False:
            continue  # navigation pages (ruling R4)
        ex = [b for b in _blocks(t) if b["type"] == "example"]
        assert len(ex) >= 2, t["id"]
        for b in ex:
            assert b["es"].strip() and b["en"].strip(), (t["id"], b)


def test_verbs_section_renders(tmp_path):
    from templates.spanish.template import generate
    out = tmp_path / "verbs.pdf"
    generate(str(out), sections="verbs", verb_pages="0")  # raises LayoutOverflow on overflow
    assert out.stat().st_size > 0


def test_cmp_perfects_has_two_timelines():
    topic = next(t for t in VERB_TOPICS if t["id"] == "cmp-perfects")
    assert sum(1 for b in _blocks(topic) if b["type"] == "timeline") == 2


# --------------------------------------------------------------------------
# Task 9: navigation pages, commands and special verbs
# --------------------------------------------------------------------------
def _topic(tid):
    return next(t for t in VERB_TOPICS if t["id"] == tid)


def test_verb_topic_order():
    assert [t["id"] for t in VERB_TOPICS[:3]] == NAV_TOPICS
    assert [t["id"] for t in VERB_TOPICS[3:]] == REQUIRED_VERB_TOPICS


def test_chart_links_resolve():
    ids = {t["id"] for t in VERB_TOPICS}
    charts = [b for b in _blocks(_topic("which-tense")) if b["type"] == "chart"]
    assert len(charts) == 1
    dests = [a["dest"] for node in charts[0]["nodes"] for a in node["answers"]]
    assert dests
    for d in dests:
        assert d.startswith("t-") and d[2:] in ids, d
    covered = {d[2:] for d in dests}
    tenses = {"present", "progressive", "ir-a", "acabar-de", "preterite", "imperfect", "future",
              "conditional", "pres-perfect", "past-perfect", "pres-subj", "past-subj", "commands"}
    assert tenses <= covered, tenses - covered


def test_nav_topics_have_no_practice(tmp_path):
    import io
    from reportlab.pdfgen import canvas as rl_canvas
    from core.dimensions import PAGE_H, PAGE_W
    from templates.spanish.template import _render, parse_options
    for tid in NAV_TOPICS:
        assert _topic(tid).get("practice") is False, tid
    opts = parse_options({"sections": "verbs", "verb_pages": "0"})
    doc = _render(rl_canvas.Canvas(io.BytesIO(), pagesize=(PAGE_W, PAGE_H)), opts, {}, None)
    for tid in NAV_TOPICS:
        kinds = {r.kind for r in doc.log if r.topic_id == tid}
        assert kinds == {"nav"}, (tid, kinds)
    for tid in REQUIRED_VERB_TOPICS:
        assert any(r.kind == "practice" and r.topic_id == tid for r in doc.log), tid


def test_master_table_covers_master_verbs():
    verbs = [v for b in _blocks(_topic("master-irregulars")) if b["type"] == "conj"
             for v in b["verbs"]]
    assert sorted(verbs) == sorted(MASTER)
    for b in _blocks(_topic("master-irregulars")):
        if b["type"] == "conj":
            assert b["tenses"] == ["present", "preterite", "imperfect", "future", "conditional",
                                   "pres_subj"]
    text = " ".join(_strings(_topic("master-irregulars")))
    for v in MASTER:  # participle and -ndo form printed under each verb's table
        assert f"participle **{VERBS[v]['participle']}**" in text, v
        assert f"-ndo form **{VERBS[v]['gerund']}**" in text, v
    assert "hay, hubo, había, habrá, habría, haya" in text


def test_weather_verbs_third_person():
    text = " ".join(_strings(_topic("weather")))
    for form in ["llueve", "llovió", "llovía", "va a llover", "lloverá", "ha llovido", "nieva",
                 "hace frío", "hace calor", "hace sol", "hace viento", "hace buen tiempo",
                 "está nublado", "está lloviendo", "hay niebla"]:
        assert form in text.lower().replace("*", ""), form


def test_irregular_tu_commands_listed():
    text = " ".join(_strings(_topic("commands"))).replace("*", "")
    for form in ["di", "haz", "ve", "pon", "sal", "sé", "ten", "ven", "dámelo", "no me lo des",
                 "oiga"]:
        assert f" {form}" in f" {text}", form


def test_irregular_tu_commands_match_conjugator():
    from templates.spanish.content.verb_topics import TU_IRREGULAR
    assert len(TU_IRREGULAR) == 8
    for verb, tu, _en in TU_IRREGULAR:
        assert tu == conjugate(verb, "imperative", "tú"), verb


# --------------------------------------------------------------------------
# Task 10: Phrases & Grammar
# --------------------------------------------------------------------------
from templates.spanish.content.confused import CONFUSED_XREFS  # noqa: E402
from templates.spanish.content.confused import TOPICS as CONFUSED_TOPICS  # noqa: E402
from templates.spanish.content.grammar import TOPICS as GRAMMAR_TOPICS  # noqa: E402
from templates.spanish.content.phrases import PHRASE_COMPARISONS, PHRASES  # noqa: E402
from templates.spanish.pages import phrase_dests, spanish_sort_key  # noqa: E402

SEED = ["a pesar de", "además", "al mismo tiempo", "apenas", "aún", "aunque", "bastante",
        "desde que", "en cambio", "entonces", "hasta", "los que", "por lo que", "sin embargo",
        "sino", "tal vez", "tan", "tanto", "todavía", "ya"]
GRAMMAR_IDS = ["hace", "comparatives", "equality", "superlatives", "negatives", "personal-a",
               "que-cual"]
CONFUSED_IDS = ["ser-estar", "por-para", "saber-conocer", "pedir-preguntar", "llevar-traer",
                "tocar-jugar", "hay-esta", "pero-sino"]
CMP_DESTS = ["t-cmp-pret-imp", "t-cmp-perfects", "t-cmp-ind-subj"]


def test_seed_phrases_included():
    assert set(SEED) <= {p["es"] for p in PHRASES}


def test_phrase_count():
    assert 45 <= len(PHRASES) <= 60


def test_phrase_entries_complete():
    seen = set()
    for p in PHRASES:
        assert p["es"] not in seen, p["es"]
        seen.add(p["es"])
        for k in ("es", "en", "use"):
            assert isinstance(p[k], str) and p[k].strip(), (p["es"], k)
        assert len(p["examples"]) == 2, p["es"]
        for es, en in p["examples"]:
            assert es.strip() and en.strip(), p["es"]


def test_sort_key():
    words = ["ya", "ñandú", "aún", "nunca", "además", "aun", "a pesar de"]
    assert sorted(words, key=spanish_sort_key) == ["a pesar de", "además", "aun", "aún", "nunca",
                                                   "ñandú", "ya"]


def test_phrase_dests_unique_ascii():
    dests = phrase_dests([p["es"] for p in PHRASES])
    assert len(set(dests.values())) == len(PHRASES)
    for d in dests.values():
        assert d.startswith("p-") and d.isascii() and " " not in d and d == d.lower(), d


def test_phrase_comparisons():
    names = {p["es"] for p in PHRASES}
    assert len(PHRASE_COMPARISONS) == 4
    for cmp in PHRASE_COMPARISONS:
        assert cmp["after"] in names, cmp["after"]
        assert cmp["block"]["type"] == "compare" and cmp["block"]["rows"]


class _SpyCanvas:
    """Wraps reportlab's Canvas to record (page, dest) for every drawn link."""

    def __new__(cls, *a, **kw):
        from reportlab.pdfgen import canvas as rl_canvas

        class Spy(rl_canvas.Canvas):
            def __init__(self, *a, **kw):
                super().__init__(*a, **kw)
                self.drawn_links = []

            def linkRect(self, contents, destinationname, Rect=None, **kw):
                self.drawn_links.append((self.getPageNumber(), destinationname, Rect))
                return super().linkRect(contents, destinationname, Rect, **kw)

        return Spy(*a, **kw)


def _two_pass(sections, **kw):
    import io
    from reportlab.pdfgen import canvas as rl_canvas
    from core.dimensions import PAGE_H, PAGE_W
    from templates.spanish.template import _render, parse_options
    opts = parse_options({"sections": sections, **kw})
    d1 = _render(rl_canvas.Canvas(io.BytesIO(), pagesize=(PAGE_W, PAGE_H)), opts, {}, None)
    c2 = _SpyCanvas(io.BytesIO(), pagesize=(PAGE_W, PAGE_H))
    d2 = _render(c2, opts, {}, dict(d1.dests))
    assert d1.log == d2.log and d1.dests == d2.dests
    return d2, c2.drawn_links


def test_index_links_every_entry():
    doc, links = _two_pass("phrases", phrase_pages="1")
    index_pages = {r.page for r in doc.log if r.kind == "phrase-index"}
    assert index_pages
    expected = set(phrase_dests([p["es"] for p in PHRASES]).values())
    on_index = [d for pg, d, _ in links if pg in index_pages and d.startswith("p-")]
    assert sorted(on_index) == sorted(expected)
    entry_pages = {r.page for r in doc.log if r.kind == "phrase-entries"}
    for d in expected:
        assert doc.dests[d] in entry_pages, d
    # no outline entry per phrase: dests exist, but entries are not on contents
    assert "phrases-index" in doc.dests


def test_partial_xrefs_plain(tmp_path):
    from pypdf import PdfReader
    from templates.spanish.template import generate
    out = tmp_path / "p.pdf"
    generate(str(out), sections="phrases", phrase_pages="0")
    text = " ".join(pg.extract_text() for pg in PdfReader(str(out)).pages[:3])
    for x in CONFUSED_XREFS:
        assert x["text"] in text, x["text"]
    _doc, links = _two_pass("phrases", phrase_pages="0")
    assert not {d for _, d, _ in links} & set(CMP_DESTS)
    _doc, links = _two_pass("all", verb_pages="0", phrase_pages="0", vocab_pages="0")
    assert set(CMP_DESTS) <= {d for _, d, _ in links}
    assert sorted(x["dest"] for x in CONFUSED_XREFS) == sorted(CMP_DESTS)


def test_grammar_and_confused_topics():
    assert [t["id"] for t in GRAMMAR_TOPICS] == GRAMMAR_IDS
    assert [t["id"] for t in CONFUSED_TOPICS] == CONFUSED_IDS
    for t in GRAMMAR_TOPICS + CONFUSED_TOPICS:
        ex = [b for b in _blocks(t) if b["type"] == "example"]
        assert 2 <= len(ex) <= 4, t["id"]
        for b in ex:
            assert b["es"].strip() and b["en"].strip(), (t["id"], b)


def test_phrases_section_layout_order():
    doc, _ = _two_pass("phrases", phrase_pages="2")
    kinds = [r.kind for r in doc.log]
    first = {k: kinds.index(k) for k in ("contents", "phrase-index", "phrase-entries",
                                         "fill-phrase")}
    assert first["contents"] < first["phrase-index"] < first["phrase-entries"] < \
        first["fill-phrase"]
    topic_pages = [r for r in doc.log if r.topic_id in GRAMMAR_IDS + CONFUSED_IDS]
    assert topic_pages and min(r.page for r in topic_pages) > \
        max(r.page for r in doc.log if r.kind == "fill-phrase")
    order = [r.topic_id for r in doc.log if r.kind == "reference"]
    order = list(dict.fromkeys(order))
    assert order == GRAMMAR_IDS + CONFUSED_IDS


def test_index_link_rects_full_row_height():
    from templates.spanish.pages import INDEX_ROW_H
    doc, links = _two_pass("phrases", phrase_pages="0")
    index_pages = {r.page for r in doc.log if r.kind == "phrase-index"}
    for pg, d, rect in links:
        if pg in index_pages and d.startswith("p-"):
            assert abs((rect[3] - rect[1]) - INDEX_ROW_H) < 1e-6, (d, rect)


def test_phrases_outline_parts(tmp_path):
    from pypdf import PdfReader
    from templates.spanish.template import generate
    out = tmp_path / "p.pdf"
    generate(str(out), sections="phrases", phrase_pages="1")
    r = PdfReader(str(out))
    rows = []

    def walk(items, depth):
        for it in items:
            if isinstance(it, list):
                walk(it, depth + 1)
            else:
                rows.append((depth, it.title))

    walk(r.outline, 0)
    assert rows[:3] == [(0, "Phrases & Grammar"), (1, "A. Connector phrases A–Z"),
                        (2, "My Phrases")]
    assert (1, "B. Grammar rules") in rows and (1, "C. Commonly confused") in rows
    titles = [t for _, t in rows]
    for t in GRAMMAR_TOPICS + CONFUSED_TOPICS:
        assert (2, t["title"]) in rows, t["id"]
    assert not any(t in titles for t in SEED)  # no outline entry per phrase
