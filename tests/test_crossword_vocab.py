from templates.crossword.prepare_vocab import (
    classify_entry, extract_key_word, build_vocab_entry, validate_vocab
)

SAMPLE_INDEX = {
    "classes": [{
        "id": "test",
        "name": "Test",
        "filename": "test.pdf",
        "lessons": [{
            "number": 1,
            "title": "Test Lesson",
            "vocabulary": [
                {"term": "hola",          "definition": "hello"},
                {"term": "hasta mañana",  "definition": "see you tomorrow"},
                {"term": "hablar",        "definition": "to speak, to talk"},
                {"term": "¿Qué tal?",     "definition": "How's it going?"},
                {"term": "buenos días",   "definition": "good morning"},
            ]
        }]
    }]
}

def test_classify_word():
    assert classify_entry("hola", "hello") == "word"

def test_classify_verb():
    assert classify_entry("hablar", "to speak, to talk") == "verb"

def test_classify_phrase():
    assert classify_entry("hasta mañana", "see you tomorrow") == "phrase"

def test_classify_question_phrase():
    assert classify_entry("¿Qué tal?", "How's it going?") == "phrase"

def test_extract_key_word_simple():
    # "hasta mañana" → "mañana" (longest non-stopword)
    assert extract_key_word("hasta mañana") == "mañana"

def test_extract_key_word_buenos_dias():
    # "buenos días" → "buenos" or "días" (both 6 chars) → last one: "días"
    result = extract_key_word("buenos días")
    assert result in ("buenos", "días")

def test_extract_key_word_strips_punctuation():
    # "¿Qué tal?" → "Qué" or "tal" — should strip ¿? and return longest
    result = extract_key_word("¿Qué tal?")
    assert result.lower() in ("qué", "tal")

def test_build_vocab_entry_word():
    entry = build_vocab_entry("hola", "hello", "linkedin-learning")
    assert entry["type"] == "word"
    assert entry["entry"] == "hola"
    assert entry["definition"] == "hello"
    assert entry["source"] == "linkedin-learning"
    assert "id" in entry

def test_build_vocab_entry_verb_has_conjugations():
    entry = build_vocab_entry("hablar", "to speak, to talk", "linkedin-learning")
    assert entry["type"] == "verb"
    assert entry["entry"] == "hablar"
    assert "conjugations" in entry
    assert entry["conjugations"]["present"]["yo"] == "hablo"
    assert set(entry["conjugations"].keys()) == {
        "present", "preterite", "imperfect", "future", "conditional", "subjunctive", "imperative"
    }

def test_build_vocab_entry_phrase_has_key_word():
    entry = build_vocab_entry("hasta mañana", "see you tomorrow", "linkedin-learning")
    assert entry["type"] == "phrase"
    assert entry["entry"] == "mañana"
    assert entry["full_phrase"] == "hasta mañana"
    assert entry["clue_template"] == "hasta ___: see you tomorrow"

def test_validate_vocab_catches_duplicate_entries():
    vocab = [
        {"id": "a", "entry": "hola", "type": "word", "definition": "hello"},
        {"id": "b", "entry": "hola", "type": "word", "definition": "hi"},
    ]
    errors = validate_vocab(vocab)
    assert any("duplicate" in e.lower() for e in errors)

def test_validate_vocab_catches_short_entry():
    vocab = [{"id": "a", "entry": "yo", "type": "word", "definition": "I"}]
    errors = validate_vocab(vocab)
    assert any("short" in e.lower() or "length" in e.lower() or "minimum" in e.lower() for e in errors)

def test_validate_vocab_passes_valid():
    vocab = [{"id": "hola", "entry": "hola", "type": "word", "definition": "hello",
              "tags": [], "source": "linkedin-learning"}]
    errors = validate_vocab(vocab)
    assert errors == []
