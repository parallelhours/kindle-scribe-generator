"""
prepare_vocab.py — squash index.json → vocabulary.json

Usage:
    python templates/crossword/prepare_vocab.py --source /path/to/index.json
    python templates/crossword/prepare_vocab.py --validate
"""
import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[2]))

from templates.crossword.conjugator import get_all_conjugations

_VOCAB_PATH = Path(__file__).parent / "vocabulary.json"

_STOPWORDS = {
    "el", "la", "los", "las", "un", "una", "unos", "unas",
    "de", "del", "en", "a", "al", "y", "o", "no",
    "me", "te", "le", "lo", "se", "que", "por", "para",
    "con", "sin", "muy", "más", "tan", "ya", "hay",
}

_STRIP_PUNCT = re.compile(r"[¿¡?!.,;:\"\'\(\)]")


def classify_entry(term: str, definition: str) -> str:
    clean = term.strip()
    if " " in clean:
        return "phrase"
    if definition.strip().startswith("to ") and clean[-2:].lower() in ("ar", "er", "ir"):
        return "verb"
    return "word"


def extract_key_word(phrase: str) -> str:
    """Return the longest non-stopword from phrase (ties broken by last occurrence)."""
    words = [_STRIP_PUNCT.sub("", w) for w in phrase.split()]
    candidates = [w for w in words if w.lower() not in _STOPWORDS and len(w) >= 3]
    if not candidates:
        candidates = sorted(words, key=len)
        return candidates[-1] if candidates else words[-1]
    return max(candidates, key=lambda w: (len(w), words.index(w)))


def build_vocab_entry(term: str, definition: str, source: str) -> dict:
    kind = classify_entry(term, definition)
    slug = re.sub(r"[^a-z0-9]", "-", term.lower().strip())

    if kind == "verb":
        return {
            "id": slug,
            "entry": term,
            "type": "verb",
            "definition": definition,
            "conjugations": get_all_conjugations(term),
            "irregular": term in _get_irregular_set(),
            "tags": _infer_verb_tags(term),
            "source": source,
        }

    if kind == "phrase":
        key = extract_key_word(term)
        template = term.replace(key, "___")
        return {
            "id": slug,
            "entry": key,
            "type": "phrase",
            "full_phrase": term,
            "clue_template": f"{template}: {definition}",
            "definition": definition,
            "tags": [],
            "source": source,
        }

    return {
        "id": slug,
        "entry": term,
        "type": "word",
        "definition": definition,
        "tags": [],
        "source": source,
    }


def _get_irregular_set():
    from templates.crossword.conjugator import IRREGULAR_VERBS
    return set(IRREGULAR_VERBS.keys())


def _infer_verb_tags(infinitive: str) -> list:
    tags = []
    if infinitive.endswith("ar"):
        tags.append("ar-verb")
    elif infinitive.endswith("er"):
        tags.append("er-verb")
    elif infinitive.endswith("ir"):
        tags.append("ir-verb")
    if infinitive in _get_irregular_set():
        tags.append("irregular")
    return tags


def validate_vocab(vocab: list) -> list:
    """Return list of error strings. Empty list means valid."""
    errors = []
    seen_entries = {}
    for item in vocab:
        entry = item.get("entry", "")
        if len(entry) < 3:
            errors.append(f"[{item.get('id')}] entry '{entry}' below minimum length of 3")
        if entry in seen_entries:
            errors.append(f"Duplicate entry '{entry}': ids {seen_entries[entry]} and {item.get('id')}")
        else:
            seen_entries[entry] = item.get("id")
    return errors


def squash(source_path: str, out_path: str = None, source_label: str = "linkedin-learning") -> list:
    """Read index.json and return flat list of vocab entries."""
    with open(source_path, encoding="utf-8") as f:
        data = json.load(f)

    entries = []
    seen_terms = set()
    seen_entries = set()  # deduplicate on extracted entry string
    for cls in data["classes"]:
        for lesson in cls["lessons"]:
            for item in lesson["vocabulary"]:
                term = item["term"].strip()
                if term in seen_terms:
                    continue
                seen_terms.add(term)
                vocab_entry = build_vocab_entry(term, item["definition"], source_label)
                entry_str = vocab_entry["entry"]
                if len(entry_str) < 3:
                    continue  # skip short entries
                if entry_str in seen_entries:
                    continue  # skip duplicate entry strings
                seen_entries.add(entry_str)
                entries.append(vocab_entry)

    return entries


def main():
    parser = argparse.ArgumentParser(description="Prepare vocabulary.json for Cruza y Aprende")
    parser.add_argument("--source", help="Path to index.json")
    parser.add_argument("--out", default=str(_VOCAB_PATH), help="Output path")
    parser.add_argument("--existing", default=str(_VOCAB_PATH), help="Path to existing vocabulary.json to preserve user-added entries from")
    parser.add_argument("--validate", action="store_true", help="Validate existing vocabulary.json")
    args = parser.parse_args()

    if args.validate:
        with open(args.out, encoding="utf-8") as f:
            vocab = json.load(f)
        errors = validate_vocab(vocab)
        if errors:
            for e in errors:
                print(f"ERROR: {e}", file=sys.stderr)
            sys.exit(1)
        print(f"OK: {len(vocab)} entries, no errors")
        return

    if not args.source:
        parser.error("--source is required unless --validate is used")

    # Preserve any manually added entries before regenerating
    preserved = []
    existing_path = Path(args.existing)
    if existing_path.exists():
        with open(existing_path, encoding="utf-8") as f:
            existing = json.load(f)
        preserved = [e for e in existing if e.get("source") == "added-by-user"]

    entries = squash(args.source, args.out)

    # Merge preserved entries, skipping any whose entry string already appears
    existing_entry_strings = {e["entry"] for e in entries}
    merged_count = 0
    for e in preserved:
        if e["entry"] not in existing_entry_strings:
            entries.append(e)
            existing_entry_strings.add(e["entry"])
            merged_count += 1

    errors = validate_vocab(entries)
    if errors:
        for e in errors:
            print(f"WARNING: {e}", file=sys.stderr)

    with open(args.out, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)
    print(f"Wrote {len(entries)} entries to {args.out} ({merged_count} user-added preserved)")


if __name__ == "__main__":
    main()
