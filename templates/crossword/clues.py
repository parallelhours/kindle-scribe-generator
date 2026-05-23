"""
build_candidate_pool(vocab_entries, difficulty) → list of crossword candidates.

Each candidate: {"entry": str, "clue": str, "source_id": str}
"""

from templates.crossword.conjugator import SUBJECTS as _CONJUGATOR_SUBJECTS

DIFFICULTY_TENSES = {
    "easy":   ["present"],
    "medium": ["present", "preterite", "imperfect"],
    "hard":   ["present", "preterite", "imperfect", "future", "conditional", "subjunctive", "imperative"],
}

_TENSE_LABEL = {
    "present":     "present",
    "preterite":   "preterite",
    "imperfect":   "imperfect",
    "future":      "future",
    "conditional": "conditional",
    "subjunctive": "present subjunctive",
    "imperative":  "imperative",
}


def _clue_for_conjugation(subject: str, tense: str, definition: str) -> str:
    label = _TENSE_LABEL[tense]
    short_def = definition.split(",")[0].strip()  # "to speak, to talk" → "to speak"
    if tense == "imperative":
        return f"___ ({subject} command): {short_def}, {label}"
    return f"{subject} ___: {short_def}, {label}"


def build_candidate_pool(vocab_entries: list, difficulty: str) -> list:
    """Return deduplicated list of crossword candidates for the given difficulty."""
    if difficulty not in DIFFICULTY_TENSES:
        raise ValueError(f"Unknown difficulty {difficulty!r}. Expected one of {list(DIFFICULTY_TENSES)}")
    tenses = DIFFICULTY_TENSES[difficulty]
    seen_entries = set()
    candidates = []

    def _add(entry: str, clue: str, source_id: str):
        # First-in wins: if two vocab items share the same inflected form, earlier item's clue is kept
        if len(entry) < 3 or entry in seen_entries:
            return
        seen_entries.add(entry)
        candidates.append({"entry": entry, "clue": clue, "source_id": source_id})

    for item in vocab_entries:
        sid = item["id"]
        kind = item["type"]

        if kind == "word":
            _add(item["entry"], item["definition"], sid)

        elif kind == "phrase":
            _add(item["entry"], item["clue_template"], sid)

        elif kind == "verb":
            infinitive = item["entry"]
            definition = item["definition"]

            # Always add the infinitive itself
            _add(infinitive, f"{definition} (infinitive)", sid)

            # Add conjugated forms — imperative first so its forms take priority
            # when a form collides with an indicative tense spelling.
            ordered_tenses = (
                [t for t in tenses if t == "imperative"]
                + [t for t in tenses if t != "imperative"]
            )
            for tense in ordered_tenses:
                conjugations = item["conjugations"].get(tense, {})
                subjects = _CONJUGATOR_SUBJECTS[tense]
                for subject in subjects:
                    form = conjugations.get(subject)
                    if form:
                        clue = _clue_for_conjugation(subject, tense, definition)
                        _add(form, clue, sid)

    return candidates
