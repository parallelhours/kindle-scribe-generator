from templates.crossword.clues import build_candidate_pool

SAMPLE_VOCAB = [
    {
        "id": "hola", "entry": "hola", "type": "word",
        "definition": "hello", "tags": [], "source": "linkedin-learning"
    },
    {
        "id": "hasta-manana", "entry": "mañana", "type": "phrase",
        "full_phrase": "hasta mañana", "clue_template": "hasta ___: see you tomorrow",
        "definition": "see you tomorrow", "tags": [], "source": "linkedin-learning"
    },
    {
        "id": "hablar", "entry": "hablar", "type": "verb",
        "definition": "to speak, to talk",
        "conjugations": {
            "present":     {"yo": "hablo", "tú": "hablas", "él": "habla",
                            "nosotros": "hablamos", "vosotros": "habláis", "ellos": "hablan"},
            "preterite":   {"yo": "hablé", "tú": "hablaste", "él": "habló",
                            "nosotros": "hablamos", "vosotros": "hablasteis", "ellos": "hablaron"},
            "imperfect":   {"yo": "hablaba", "tú": "hablabas", "él": "hablaba",
                            "nosotros": "hablábamos", "vosotros": "hablabais", "ellos": "hablaban"},
            "future":      {"yo": "hablaré", "tú": "hablarás", "él": "hablará",
                            "nosotros": "hablaremos", "vosotros": "hablaréis", "ellos": "hablarán"},
            "conditional": {"yo": "hablaría", "tú": "hablarías", "él": "hablaría",
                            "nosotros": "hablaríamos", "vosotros": "hablaríais", "ellos": "hablarían"},
            "subjunctive": {"yo": "hable", "tú": "hables", "él": "hable",
                            "nosotros": "hablemos", "vosotros": "habléis", "ellos": "hablen"},
            "imperative":  {"tú": "habla", "usted": "hable", "nosotros": "hablemos",
                            "vosotros": "hablad", "ustedes": "hablen"},
        },
        "irregular": False, "tags": ["ar-verb"], "source": "linkedin-learning"
    },
]

def _pool(difficulty):
    return build_candidate_pool(SAMPLE_VOCAB, difficulty)

def _entries(difficulty):
    return {c["entry"] for c in _pool(difficulty)}

def test_word_always_included():
    for diff in ("easy", "medium", "hard"):
        assert "hola" in _entries(diff)

def test_phrase_always_included():
    for diff in ("easy", "medium", "hard"):
        assert "mañana" in _entries(diff)

def test_phrase_clue_uses_template():
    pool = _pool("easy")
    candidate = next(c for c in pool if c["entry"] == "mañana")
    assert candidate["clue"] == "hasta ___: see you tomorrow"

def test_word_clue_is_definition():
    pool = _pool("easy")
    candidate = next(c for c in pool if c["entry"] == "hola")
    assert candidate["clue"] == "hello"

def test_verb_infinitive_in_easy():
    assert "hablar" in _entries("easy")

def test_verb_infinitive_clue():
    pool = _pool("easy")
    candidate = next(c for c in pool if c["entry"] == "hablar")
    assert "infinitive" in candidate["clue"].lower()
    assert "to speak" in candidate["clue"]

def test_verb_present_yo_in_easy():
    assert "hablo" in _entries("easy")

def test_present_yo_clue_format():
    pool = _pool("easy")
    candidate = next(c for c in pool if c["entry"] == "hablo")
    assert "yo" in candidate["clue"]
    assert "present" in candidate["clue"].lower()
    assert "to speak" in candidate["clue"]

def test_preterite_excluded_from_easy():
    assert "hablé" not in _entries("easy")

def test_preterite_included_in_medium():
    assert "hablé" in _entries("medium")

def test_preterite_yo_clue_format():
    pool = _pool("medium")
    candidate = next(c for c in pool if c["entry"] == "hablé")
    assert "yo" in candidate["clue"]
    assert "preterite" in candidate["clue"].lower()

def test_future_excluded_from_medium():
    assert "hablaré" not in _entries("medium")

def test_future_included_in_hard():
    assert "hablaré" in _entries("hard")

def test_subjunctive_included_in_hard():
    assert "hable" in _entries("hard")

def test_imperative_tu_clue_format():
    pool = _pool("hard")
    candidate = next(c for c in pool if c["entry"] == "habla")
    assert "tú" in candidate["clue"] or "command" in candidate["clue"].lower()
    assert "imperative" in candidate["clue"].lower()

def test_no_duplicate_entries():
    for diff in ("easy", "medium", "hard"):
        entries = [c["entry"] for c in _pool(diff)]
        assert len(entries) == len(set(entries)), f"Duplicate entries in {diff} pool"

def test_minimum_entry_length_three():
    for diff in ("easy", "medium", "hard"):
        for c in _pool(diff):
            assert len(c["entry"]) >= 3, f"Entry too short: {c['entry']}"
