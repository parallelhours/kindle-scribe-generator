# Copyright (C) 2026 Paul Monday — GNU GPL v3 or later. See LICENSE.
"""Section builders: topics, contents entries and fill-in pages."""
from templates.spanish.content import (
    additions, confused, grammar, phrases, verb_topics, vocab,
)
from templates.spanish.doc import SECTION_NAMES
from templates.spanish.layout import LayoutOverflow, block_height, draw_block
from templates.spanish.pages import (
    WORD_ROWS_PER_PAGE, draw_contents_page, draw_my_verbs_page, draw_phrase_blank_page,
    draw_phrase_entries, draw_phrase_index, draw_practice_page, draw_word_page,
)


def _mark(doc, dest):
    """Bookmark the page about to be started (fill-in pages take no dests)."""
    doc.c.bookmarkPage(dest)
    doc.dests[dest] = doc.page + 1


def render_topic(doc, section, topic, level=1, extra_dests=()):
    tid, title = topic["id"], topic["title"]
    practice = topic.get("practice", True)
    kind = "reference" if practice else "nav"
    for i, blocks in enumerate(topic["pages"]):
        first = i == 0
        f = doc.start_page(kind, title if first else f"{title} (cont.)", section, tid,
                           dests=(f"t-{tid}", *extra_dests) if first else ())
        if first:
            doc.outline(title, f"t-{tid}", level)
        try:
            for b in blocks:
                need = block_height(b, f.width, doc.verbs)
                if need > f.remaining() + 1e-6:
                    raise LayoutOverflow(f"need {need:.1f}pt, only {f.remaining():.1f}pt left")
                draw_block(doc.c, f, b, doc)
        except LayoutOverflow as e:
            raise LayoutOverflow(f"topic {tid!r} page {i}: {e}") from e
        doc.end_page()
    if practice:
        draw_practice_page(doc, section, tid, title)


# --------------------------------------------------------------------------
# Section contents
# --------------------------------------------------------------------------
def _topic_entries(topics, level=1):
    return [(t["title"], f"t-{t['id']}", level) for t in topics]


def section_entries(section, opts):
    """Contents rows for a section; fill-in rows only when those pages will be drawn
    (the same conditions the builders use, so both render passes lay out identically)."""
    if section == "verbs":
        return (_topic_entries(verb_topics.VERB_TOPICS)
                + ([("My Verbs", "verbs-my", 1)]
                   if additions.MY_VERBS or opts.verb_pages else []))
    if section == "phrases":
        return ([(PART_A, "phrases-index", 1)]
                + ([("My Phrases", "phrases-my", 2)] if opts.phrase_pages else [])
                + [(PART_B, "phrases-part-b", 1)]
                + _topic_entries(grammar.TOPICS, 2)
                + [(PART_C, "phrases-part-c", 1)]
                + _topic_entries(confused.TOPICS, 2)
                + [(x["text"], x["dest"], 2) for x in confused.CONFUSED_XREFS])
    if section == "vocab":
        return (_topic_entries(vocab.TOPICS)
                + ([("Word pages", "vocab-words", 1)]
                   if additions.MY_WORDS or opts.vocab_pages else []))
    raise ValueError(f"unknown section {section!r}")


def _begin(doc, section, opts):
    title = SECTION_NAMES[section]
    doc.outline(title, f"{section}-contents", 0)
    draw_contents_page(doc, section, f"{title} contents", section_entries(section, opts))


# --------------------------------------------------------------------------
# Sections
# --------------------------------------------------------------------------
def build_verbs(doc, opts):
    _begin(doc, "verbs", opts)
    for v in additions.MY_VERBS:
        additions.validate_verb(v)
    for t in verb_topics.VERB_TOPICS:
        render_topic(doc, "verbs", t)
    printed = additions.MY_VERBS
    if printed or opts.verb_pages:
        _mark(doc, "verbs-my")
        doc.outline("My Verbs", "verbs-my", 1)
    for i in range(0, len(printed), 2):
        draw_my_verbs_page(doc, filled=printed[i:i + 2])
    for _ in range(opts.verb_pages):
        draw_my_verbs_page(doc)


PART_A = "A. Connector phrases A–Z"
PART_B = "B. Grammar rules"
PART_C = "C. Commonly confused"


def build_phrases(doc, opts):
    _begin(doc, "phrases", opts)
    # Part A: index, printed entries (dests p-..., no outline entry each), blank pages
    doc.outline(PART_A, "phrases-index", 1)
    draw_phrase_index(doc, phrases.PHRASES)
    draw_phrase_entries(doc, phrases.PHRASES, phrases.PHRASE_COMPARISONS)
    if opts.phrase_pages:
        _mark(doc, "phrases-my")
        doc.outline("My Phrases", "phrases-my", 2)
    for _ in range(opts.phrase_pages):
        draw_phrase_blank_page(doc)
    # Parts B and C: topics, each followed by its practice page
    # (outline entries are keyed by dest, so each Part needs its own dest)
    for part, dest, topics in ((PART_B, "phrases-part-b", grammar.TOPICS),
                               (PART_C, "phrases-part-c", confused.TOPICS)):
        doc.outline(part, dest, 1)
        for i, t in enumerate(topics):
            render_topic(doc, "phrases", t, level=2, extra_dests=(dest,) if i == 0 else ())


def build_vocab(doc, opts):
    _begin(doc, "vocab", opts)
    for g in additions.MY_WORDS:
        additions.validate_word_group(g)
    for t in vocab.TOPICS:
        render_topic(doc, "vocab", t)
    if additions.MY_WORDS or opts.vocab_pages:
        _mark(doc, "vocab-words")
        doc.outline("Word pages", "vocab-words", 1)
    for g in additions.MY_WORDS:
        words = g["words"]
        for i in range(0, max(len(words), 1), WORD_ROWS_PER_PAGE):
            draw_word_page(doc, "vocab", words=words[i:i + WORD_ROWS_PER_PAGE],
                           topic=g.get("topic", ""), date=g.get("date", ""))
    for _ in range(opts.vocab_pages):
        draw_word_page(doc, "vocab")
