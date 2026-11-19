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
    assert candidate["clue"] == "Todos los días yo ___ (hablar) con Pedro."

def test_preterite_excluded_from_easy():
    assert "hablé" not in _entries("easy")

def test_preterite_included_in_medium():
    assert "hablé" in _entries("medium")

def test_preterite_yo_clue_format():
    pool = _pool("medium")
    candidate = next(c for c in pool if c["entry"] == "hablé")
    assert candidate["clue"] == "Ayer yo ___ (hablar) con Pedro."

def test_future_excluded_from_medium():
    assert "hablaré" not in _entries("medium")

def test_future_included_in_hard():
    assert "hablaré" in _entries("hard")

def test_subjunctive_included_in_hard():
    assert "hable" in _entries("hard")

def test_imperative_tu_clue_format():
    pool = _pool("hard")
    candidate = next(c for c in pool if c["entry"] == "habla")
    assert candidate["clue"] == "¡___ (hablar) con Pedro, Ana! (tú)"

def test_no_duplicate_entries():
    for diff in ("easy", "medium", "hard"):
        entries = [c["entry"] for c in _pool(diff)]
        assert len(entries) == len(set(entries)), f"Duplicate entries in {diff} pool"

def test_minimum_entry_length_three():
    for diff in ("easy", "medium", "hard"):
        for c in _pool(diff):
            assert len(c["entry"]) >= 3, f"Entry too short: {c['entry']}"


# --- Crossword review 2026-11-18: Latin American focus, sentence clues ---
from templates.crossword.clues import normalize_answer, format_phrase_clue, connector_candidates
from templates.crossword.frames import conjugation_clue


def test_vosotros_forms_never_answers():
    entries = _entries("hard")
    for form in ("habláis", "hablasteis", "hablabais", "hablaréis", "hablaríais", "habléis", "hablad"):
        assert form not in entries


def test_candidates_have_kind():
    kinds = {c["kind"] for c in _pool("hard")}
    assert {"vocab", "verb", "connector"} <= kinds


def test_tense_markers_cue_each_tense():
    assert conjugation_clue("comer", "imperfect", "nosotros") == "Antes nosotros siempre ___ (comer) fruta."
    assert conjugation_clue("comer", "future", "ellos") == "Mañana ellos ___ (comer) fruta."
    assert conjugation_clue("comer", "conditional", "tú") == "Con más tiempo, tú ___ (comer) fruta."
    assert conjugation_clue("comer", "subjunctive", "él") == "Ojalá que él ___ (comer) fruta."


def test_commands_name_who_is_addressed():
    assert conjugation_clue("comer", "imperative", "usted") == "¡___ (comer) fruta, señor! (usted)"
    assert conjugation_clue("comer", "imperative", "ustedes") == "¡___ (comer) fruta, chicos! (ustedes)"
    assert conjugation_clue("comer", "imperative", "nosotros") == "¡___ (comer) fruta! (let's)"
    assert conjugation_clue("comer", "imperative", "vosotros") is None


def test_gustar_type_verbs_use_third_person_only():
    assert conjugation_clue("gustar", "present", "él") == "Me ___ (gustar) el café."
    assert conjugation_clue("gustar", "present", "ellos") == "Me ___ (gustar) los perros."
    assert conjugation_clue("molestar", "preterite", "ellos") == "Ayer me ___ (molestar) los mosquitos."
    assert conjugation_clue("parecer", "present", "él") == "Me ___ (parecer) una buena idea."
    assert conjugation_clue("parecer", "future", "él") is None
    assert conjugation_clue("gustar", "imperfect", "él") == "Antes siempre me ___ (gustar) el café."
    assert conjugation_clue("gustar", "conditional", "él") == "Me ___ (gustar) un café, por favor."
    assert conjugation_clue("gustar", "present", "yo") is None
    assert conjugation_clue("gustar", "imperative", "tú") is None


def test_weather_verbs_have_no_subject():
    assert conjugation_clue("llover", "preterite", "él") == "Ayer ___ (llover) mucho."
    assert conjugation_clue("llover", "present", "ellos") is None


def test_haber_drills_perfect_tenses():
    assert conjugation_clue("haber", "present", "yo") == "Hoy yo ya ___ (haber) comido."
    assert conjugation_clue("haber", "imperfect", "yo") == "Cuando llegaste, yo ya ___ (haber) comido."
    assert conjugation_clue("haber", "preterite", "yo") is None


def test_no_command_for_poder():
    assert conjugation_clue("poder", "imperative", "tú") is None


def test_normalize_answer():
    assert normalize_answer("¡Hablen!") == "hablen"
    assert normalize_answer("Soy….") == "soy"
    assert normalize_answer("Hace") == "hace"
    assert normalize_answer("o…o") is None
    assert normalize_answer("plátano/la") is None
    assert normalize_answer("señor") == "señor"


def test_phrase_clue_format_sentence_vs_fragment():
    assert format_phrase_clue("Hace ___.: It’s cool.") == "Hace ___. (It’s cool.)"
    assert format_phrase_clue("la ___: pear") == "la ___: pear"


def test_connectors_come_from_notebook_examples():
    by_entry = {c["entry"]: c for c in connector_candidates()}
    assert by_entry["embargo"]["clue"] == "El hotel era caro. Sin ___, valió la pena. (however)"
    assert by_entry["aunque"]["kind"] == "connector"
    for c in by_entry.values():
        assert c["clue"].count("___") == 1, c


def test_every_clue_is_cp1252_safe_and_blank_bearing_for_verbs():
    import json
    from templates.crossword.template import _VOCAB_PATH
    with open(_VOCAB_PATH, encoding="utf-8") as f:
        vocab = json.load(f)
    for c in build_candidate_pool(vocab, "hard"):
        c["clue"].encode("cp1252")
        if c["kind"] == "verb" and "infinitive" not in c["clue"]:
            assert "___" in c["clue"], c


def test_ser_uses_agreement_safe_sentences():
    assert conjugation_clue("ser", "present", "nosotros") == "Nosotros ___ (ser) de Colombia."
    assert conjugation_clue("ser", "preterite", "él") == "Ayer la fiesta ___ (ser) divertida."
    assert conjugation_clue("ser", "conditional", "yo") is None
    assert conjugation_clue("ser", "imperative", "tú") == "¡___ (ser) paciente, Ana! (tú)"


def test_stative_verbs_skip_daily_marker():
    assert conjugation_clue("saber", "present", "yo") == "Yo ___ (saber) la respuesta."
    assert conjugation_clue("saber", "preterite", "yo") == "Ayer yo ___ (saber) la respuesta."


def test_every_verb_with_forms_has_a_complement_or_override():
    import json
    from templates.crossword.template import _VOCAB_PATH
    from templates.crossword.frames import COMPLEMENT, THIRD_PERSON, SPECIAL
    with open(_VOCAB_PATH, encoding="utf-8") as f:
        verbs = [e["entry"] for e in json.load(f) if e["type"] == "verb"]
    missing = [v for v in verbs if v not in COMPLEMENT and v not in THIRD_PERSON and v not in SPECIAL]
    assert missing == []
