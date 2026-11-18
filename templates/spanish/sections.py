# Copyright (C) 2026 Paul Monday — GNU GPL v3 or later. See LICENSE.
"""Section builders: topics, contents entries and fill-in pages."""
from templates.spanish.content import (
    additions, confused, grammar, phrases, verb_topics, vocab,
)
from templates.spanish.doc import SECTION_NAMES
from templates.spanish.layout import LayoutOverflow, block_height, draw_block
from templates.spanish.pages import (
    WORD_ROWS_PER_PAGE, draw_contents_page, draw_my_verbs_page,
    draw_phrase_blank_page, draw_practice_page, draw_word_page,
)


def _mark(doc, dest):
    """Bookmark the page about to be started (fill-in pages take no dests)."""
    doc.c.bookmarkPage(dest)
    doc.dests[dest] = doc.page + 1


def render_topic(doc, section, topic, level=1):
    tid, title = topic["id"], topic["title"]
    practice = topic.get("practice", True)
    kind = "reference" if practice else "nav"
    for i, blocks in enumerate(topic["pages"]):
        first = i == 0
        f = doc.start_page(kind, title if first else f"{title} (cont.)", section, tid,
                           dests=(f"t-{tid}",) if first else ())
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


def section_entries(section):
    if section == "verbs":
        return (_topic_entries(verb_topics.VERB_TOPICS)
                + [("My Verbs", "verbs-my", 1)])
    if section == "phrases":
        return ([("Phrases", "t-phrase-list", 1)]
                + _topic_entries(grammar.TOPICS)
                + _topic_entries(confused.TOPICS)
                + [("My Phrases", "phrases-my", 1)])
    if section == "vocab":
        return (_topic_entries(vocab.TOPICS)
                + [("Word pages", "vocab-words", 1)])
    raise ValueError(f"unknown section {section!r}")


def _begin(doc, section):
    title = SECTION_NAMES[section]
    doc.outline(title, f"{section}-contents", 0)
    draw_contents_page(doc, section, f"{title} contents", section_entries(section))


# --------------------------------------------------------------------------
# Sections
# --------------------------------------------------------------------------
def build_verbs(doc, opts):
    _begin(doc, "verbs")
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


def _draw_phrase_list(doc):
    f = doc.start_page("nav", "Phrases", "phrases", "phrase-list", dests=("t-phrase-list",))
    doc.outline("Phrases", "t-phrase-list", 1)
    for p in phrases.PHRASES:
        blocks = [{"type": "heading", "text": p["es"]},
                  {"type": "text", "text": f"~{p['en']}~ {p['use']}"}]
        blocks += [{"type": "example", "es": es, "en": en} for es, en in p["examples"]]
        for b in blocks:
            if block_height(b, f.width, doc.verbs) > f.remaining():
                raise LayoutOverflow("phrase listing overflows its page")
            draw_block(doc.c, f, b, doc)
    doc.end_page()


def build_phrases(doc, opts):
    _begin(doc, "phrases")
    _draw_phrase_list(doc)
    for t in grammar.TOPICS:
        render_topic(doc, "phrases", t)
    for t in confused.TOPICS:
        render_topic(doc, "phrases", t)
    if opts.phrase_pages:
        _mark(doc, "phrases-my")
        doc.outline("My Phrases", "phrases-my", 1)
    for _ in range(opts.phrase_pages):
        draw_phrase_blank_page(doc)


def build_vocab(doc, opts):
    _begin(doc, "vocab")
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
