# Copyright (C) 2026 Paul Monday — GNU GPL v3 or later. See LICENSE.
"""Export every printed string of the Spanish notebook as Markdown (proofreading, changelog).

    python -m templates.spanish.export > output/spanish-content.md
"""
import re

from templates.spanish.content import (
    additions, confused, grammar, phrases, verb_topics, vocab,
)
from templates.spanish.content.verbs_data import VERBS
from templates.spanish.layout import TENSE_LABELS, _expand_conj
from templates.spanish.pages import spanish_sort_key

_RICH = re.compile(r"\*\*(.+?)\*\*|~(.+?)~")


def _strip(s):
    return _RICH.sub(lambda m: m.group(1) if m.group(1) is not None else f"({m.group(2)})",
                     str(s))


def _cell(s):
    return _strip(s).replace("|", "\\|").replace("\n", " ")


def _table(header, rows):
    out = ["| " + " | ".join(_cell(h) for h in header) + " |",
           "|" + "---|" * len(header)]
    out += ["| " + " | ".join(_cell(c) for c in r) + " |" for r in rows]
    return out


def _block(b):
    t = b["type"]
    if t == "heading":
        return [f"#### {_strip(b['text'])}", ""]
    if t == "text":
        return [_strip(b["text"]), ""]
    if t == "bullets":
        return [f"- {_strip(i)}" for i in b["items"]] + [""]
    if t == "example":
        return [f"> {_strip(b['es'])} — *{_strip(b['en'])}*", ""]
    if t == "spacer":
        return []
    if t == "table":
        return _table(b["header"], b["rows"]) + [""]
    if t == "conj":
        out = []
        for tb in _expand_conj(b, VERBS):
            out += _table(tb["header"], tb["rows"]) + [""]
        return out
    if t == "compare":
        return _table([b["left"], b["right"]], b["rows"]) + [""]
    if t == "timeline":
        evs = sorted(b["events"], key=lambda e: e["pos"])
        out = ["Timeline: " + " → ".join(_strip(e["label"]) for e in evs)]
        if b.get("caption"):
            out.append(_strip(b["caption"]))
        return out + [""]
    if t == "chart":
        out = []
        for n in b["nodes"]:
            out.append(f"- Q: {_strip(n['q'])}")
            for a in n["answers"]:
                out.append(f"  - {_strip(a['label'])} → {_strip(a['tense'])} [{a.get('dest', '')}]")
        return out + [""]
    if t == "xref":
        d = b.get("dest")
        return [f"{_strip(b['text'])}" + (f" [→ {d}]" if d else ""), ""]
    raise ValueError(f"unknown block type {t!r}")


def _topics(topics, level="##"):
    out = []
    for t in topics:
        out += [f"{level} {t['title']} ({t['id']})", ""]
        for i, page in enumerate(t["pages"], 1):
            if len(t["pages"]) > 1:
                out += [f"*page {i}*", ""]
            for b in page:
                out += _block(b)
    return out


def _phrase(p):
    out = [f"### {p['es']} — {p['en']}", "", _strip(p["use"]), ""]
    for es, en in p["examples"]:
        out.append(f"> {_strip(es)} — *{_strip(en)}*")
    return out + [""]


def export_markdown() -> str:
    out = ["# Spanish notebook content", "", "# Verbs", ""]
    out += _topics(verb_topics.VERB_TOPICS)
    out += ["## Verb tables (verb-tables)", ""]
    for v, d in VERBS.items():
        out += [f"### {v} — {d['en']}", ""]
        tenses = [k for k in d if k not in ("en", "participle", "gerund")]
        out += _table([""] + [TENSE_LABELS.get(t, t) for t in tenses],
                      [[p] + [d[t][i] for t in tenses] for i, p in
                       enumerate(["yo", "tú", "él/ella/Ud.", "nosotros", "vosotros",
                                  "ellos/Uds."])])
        out += ["", f"participle: {d['participle']}; -ndo form: {d['gerund']}", ""]
    out += ["# Phrases & Grammar", "", "## A. Connector phrases A–Z (phrases-a)", ""]
    cmp_after = {}
    for c in phrases.PHRASE_COMPARISONS:
        cmp_after.setdefault(c["after"], []).append(c["block"])
    for p in sorted(phrases.PHRASES, key=lambda p: spanish_sort_key(p["es"])):
        out += _phrase(p)
        for b in cmp_after.pop(p["es"], []):
            out += _block(b)
    for k, bl in cmp_after.items():  # comparisons whose "after" is not an entry
        out += [f"### (comparison after unknown entry {k!r})", ""]
        for b in bl:
            out += _block(b)
    out += ["## B. Grammar rules (phrases-part-b)", ""]
    out += _topics(grammar.TOPICS, "###")
    out += ["## C. Commonly confused (phrases-part-c)", ""]
    out += _topics(confused.TOPICS, "###")
    for x in confused.CONFUSED_XREFS:
        out += _block({"type": "xref", **x})
    out += ["# Vocab", ""]
    out += _topics(vocab.TOPICS)
    if additions.MY_VERBS or additions.MY_WORDS:
        out += ["# Additions", ""]
        for v in additions.MY_VERBS:
            out += [f"## {v['verb']} — {v['en']}", ""]
            for t, forms in v["forms"].items():
                out.append(f"- {t}: {', '.join(forms)}")
            out += [f"> {_strip(es)} — *{_strip(en)}*" for es, en in v.get("examples", [])]
            out.append("")
        for g in additions.MY_WORDS:
            out += [f"## {g.get('topic', '')} {g.get('date', '')}", ""]
            out += [f"- {a} {w} — {e}".replace("-  ", "- ") for a, w, e in g["words"]] + [""]
    return "\n".join(out) + "\n"


if __name__ == "__main__":
    print(export_markdown(), end="")
