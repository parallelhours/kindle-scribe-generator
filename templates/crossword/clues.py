"""
build_candidate_pool(vocab_entries, difficulty) → list of crossword candidates.

Each candidate: {"entry": str, "clue": str, "source_id": str, "kind": str}
kind is "vocab" (words and phrases), "verb" (infinitives and conjugated
forms) or "connector" (phrases from the Cuaderno de español notebook).

Latin American Spanish: vosotros forms are never used as answers.
"""
import re

from templates.crossword.conjugator import SUBJECTS as _CONJUGATOR_SUBJECTS
from templates.crossword.frames import conjugation_clue

DIFFICULTY_TENSES = {
    "easy":   ["present"],
    "medium": ["present", "preterite", "imperfect"],
    "hard":   ["present", "preterite", "imperfect", "future", "conditional", "subjunctive", "imperative"],
}

# Letters allowed in a grid answer (lower case; accents and ñ are kept).
_ANSWER_RE = re.compile(r"^[a-záéíóúüñ]+$")
_EDGE_PUNCT = "¡!¿?.,;:…'’\"() "

# Words that never make a good connector answer on their own.
_CONNECTOR_STOPWORDS = {
    "el", "la", "los", "las", "un", "una", "de", "del", "en", "a", "al", "y",
    "o", "lo", "que", "por", "para", "con", "sin", "es", "ni", "ya", "se",
}
_MAX_CONNECTOR_CLUE = 70


def normalize_answer(entry: str):
    """Grid form of an entry: lower case, edge punctuation stripped.
    Returns None when the entry is not a single word of letters."""
    text = entry.strip(_EDGE_PUNCT).lower()
    return text if _ANSWER_RE.match(text) else None


def format_phrase_clue(template: str) -> str:
    """'Hace ___.: It's cool.' → 'Hace ___. (It's cool.)'; 'la ___: pear' unchanged."""
    blank = template.find("___")
    sep = template.find(": ", blank if blank >= 0 else 0)
    if sep < 0:
        return template
    es, en = template[:sep], template[sep + 2:]
    if es.endswith((".", "?", "!", "…")):
        return f"{es} ({en})"
    return template


def _short_gloss(en: str) -> str:
    gloss = en.split(",")[0].split(";")[0].strip()
    # The clue already wraps the gloss in parentheses; nest with brackets.
    return gloss.replace("(", "[").replace(")", "]")


def _connector_answer(es: str):
    """Pick the answer word from a notebook phrase: the longest non-stopword
    of 3+ letters (ties → last). None if the phrase has no usable word."""
    words = [w.strip(_EDGE_PUNCT) for w in re.sub(r"\(.*?\)", " ", es).split()]
    words = [w for w in words if normalize_answer(w) and w.lower() not in _CONNECTOR_STOPWORDS]
    words = [w for w in words if len(w) >= 3]
    if not words:
        return None
    return max(reversed(words), key=len)


def connector_candidates() -> list:
    """Candidates built from the Cuaderno's connector phrases: the answer word
    is blanked out of one of the notebook's own example sentences."""
    try:
        from templates.spanish.content.phrases import PHRASES
    except ImportError:  # notebook template not present
        return []
    out = []
    for p in PHRASES:
        word = _connector_answer(p["es"])
        if not word:
            continue
        gloss = _short_gloss(p["en"])
        pattern = re.compile(rf"(?<![\wáéíóúüñ]){re.escape(word)}(?![\wáéíóúüñ])", re.IGNORECASE)
        clue = None
        for es, _en in sorted(p.get("examples", []), key=lambda ex: len(ex[0])):
            if pattern.search(es):
                candidate = pattern.sub("___", es, count=1) + f" ({gloss})"
                if len(candidate) <= _MAX_CONNECTOR_CLUE:
                    clue = candidate
                    break
        if clue is None:
            phrase = re.sub(r"\s+", " ", p["es"]).strip()
            clue = pattern.sub("___", phrase, count=1) + f" ({gloss})"
        out.append({"entry": word, "clue": clue,
                    "source_id": f"cuaderno:{p['es']}", "kind": "connector"})
    return out


def build_candidate_pool(vocab_entries: list, difficulty: str) -> list:
    """Return deduplicated list of crossword candidates for the given difficulty."""
    if difficulty not in DIFFICULTY_TENSES:
        raise ValueError(f"Unknown difficulty {difficulty!r}. Expected one of {list(DIFFICULTY_TENSES)}")
    tenses = DIFFICULTY_TENSES[difficulty]
    seen_entries = set()
    candidates = []

    def _add(entry: str, clue: str, source_id: str, kind: str):
        # First-in wins: if two items share the same answer, the earlier clue is kept.
        answer = normalize_answer(entry)
        if not answer or len(answer) < 3 or answer in seen_entries or not clue:
            return
        seen_entries.add(answer)
        candidates.append({"entry": answer, "clue": clue, "source_id": source_id, "kind": kind})

    # Notebook connectors first: their sentence clues beat bare definitions.
    for cand in connector_candidates():
        _add(cand["entry"], cand["clue"], cand["source_id"], "connector")

    for item in vocab_entries:
        sid = item["id"]
        kind = item["type"]

        if kind == "word":
            _add(item["entry"], item["definition"], sid, "vocab")

        elif kind == "phrase":
            _add(item["entry"], format_phrase_clue(item["clue_template"]), sid, "vocab")

        elif kind == "verb":
            infinitive = item["entry"]
            _add(infinitive, f"{item['definition']} (infinitive)", sid, "verb")
            # Imperative first so its clue wins when a command shares a spelling
            # with an indicative/subjunctive form.
            ordered = [t for t in tenses if t == "imperative"] + [t for t in tenses if t != "imperative"]
            for tense in ordered:
                forms = item["conjugations"].get(tense, {})
                for subject in _CONJUGATOR_SUBJECTS[tense]:
                    form = forms.get(subject)
                    if form:
                        _add(form, conjugation_clue(infinitive, tense, subject), sid, "verb")

    return candidates
