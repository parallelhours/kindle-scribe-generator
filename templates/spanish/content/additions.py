# Copyright (C) 2026 Paul Monday — GNU GPL v3 or later. See LICENSE.
"""User additions printed into the notebook. Start empty.

MY_VERBS: list of
    {"verb": "dormir", "en": "to sleep",
     "forms": {"present": [5 forms], "preterite": [...], "imperfect": [...],
               "future": [...], "subjunctive": [...]},      # any subset of these 5 keys
     "examples": [(es, en), (es, en)]}                       # at most 2 pairs
  * The form keys are exactly present, preterite, imperfect, future, subjunctive
    (NOT pres_subj, which is the key used by VERBS).
  * Every form list has exactly 5 entries: yo, tú, él/ella/Ud., nosotros, ellos/Uds.
    There is NO vosotros form; a sixth entry would print in the wrong row.
MY_WORDS: list of
    {"topic": str, "date": str, "words": [(article, word, en), ...]}   # 3-tuples

Both are checked by validate_verb / validate_word_group (called when the notebook
is built), which raise ValueError naming the entry and the problem.
"""
MY_VERBS = []
MY_WORDS = []

FORM_KEYS = ("present", "preterite", "imperfect", "future", "subjunctive")
_VERB_KEYS = {"verb", "en", "forms", "examples"}
_GROUP_KEYS = {"topic", "date", "words"}


def _check_text(owner, what, s):
    if not isinstance(s, str):
        raise ValueError(f"{owner}: {what} must be text, got {s!r}")
    try:
        s.encode("cp1252")
    except UnicodeEncodeError:
        raise ValueError(f"{owner}: {what} {s!r} has characters outside cp1252") from None


def validate_verb(entry) -> None:
    if not isinstance(entry, dict) or not isinstance(entry.get("verb"), str) \
            or not entry["verb"].strip():
        raise ValueError(f"MY_VERBS entry needs a non-empty 'verb': {entry!r}")
    name = f"MY_VERBS {entry['verb']!r}"
    extra = set(entry) - _VERB_KEYS
    if extra:
        raise ValueError(f"{name}: unknown key(s) {sorted(extra)}; allowed {sorted(_VERB_KEYS)}")
    _check_text(name, "verb", entry["verb"])
    _check_text(name, "en", entry.get("en", ""))
    forms = entry.get("forms", {})
    if not isinstance(forms, dict):
        raise ValueError(f"{name}: forms must be a dict of tense -> 5 forms")
    for t, lst in forms.items():
        if t not in FORM_KEYS:
            raise ValueError(f"{name}: unknown form key {t!r}; use exactly {', '.join(FORM_KEYS)}")
        if not isinstance(lst, (list, tuple)) or len(lst) != 5:
            n = len(lst) if isinstance(lst, (list, tuple)) else "not a list"
            raise ValueError(f"{name}: forms[{t!r}] must have exactly 5 entries "
                             f"(yo, tú, él/ella/Ud., nosotros, ellos/Uds.; no vosotros), "
                             f"got {n}")
        for f in lst:
            _check_text(name, f"forms[{t!r}] entry", f)
    exs = entry.get("examples", [])
    if not isinstance(exs, (list, tuple)) or len(exs) > 2:
        raise ValueError(f"{name}: examples must be a list of at most 2 (es, en) pairs")
    for ex in exs:
        if not isinstance(ex, (list, tuple)) or len(ex) != 2:
            raise ValueError(f"{name}: each example must be an (es, en) pair, got {ex!r}")
        for s in ex:
            _check_text(name, "example", s)


def validate_word_group(group) -> None:
    topic = group.get("topic", "") if isinstance(group, dict) else ""
    name = f"MY_WORDS group {topic!r}"
    if not isinstance(group, dict):
        raise ValueError(f"{name}: must be a dict with 'topic', 'date', 'words'")
    extra = set(group) - _GROUP_KEYS
    if extra:
        raise ValueError(f"{name}: unknown key(s) {sorted(extra)}; allowed {sorted(_GROUP_KEYS)}")
    if not isinstance(group.get("words"), (list, tuple)):
        raise ValueError(f"{name}: needs a 'words' list of (article, word, en) tuples")
    _check_text(name, "topic", group.get("topic", ""))
    _check_text(name, "date", group.get("date", ""))
    for w in group["words"]:
        if not isinstance(w, (list, tuple)) or len(w) != 3:
            raise ValueError(f"{name}: word {w!r} must be a 3-tuple (article, word, en)")
        for s in w:
            _check_text(name, "word", s)
