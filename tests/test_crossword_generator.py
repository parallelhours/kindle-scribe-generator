from templates.crossword.generator import generate_puzzle, PuzzleResult, PlacedWord

SIMPLE_POOL = [
    {"entry": "hablar",    "clue": "to speak",     "source_id": "hablar"},
    {"entry": "hola",      "clue": "hello",         "source_id": "hola"},
    {"entry": "lunes",     "clue": "Monday",        "source_id": "lunes"},
    {"entry": "gracias",   "clue": "thank you",     "source_id": "gracias"},
    {"entry": "casa",      "clue": "house",         "source_id": "casa"},
    {"entry": "libro",     "clue": "book",          "source_id": "libro"},
    {"entry": "agua",      "clue": "water",         "source_id": "agua"},
    {"entry": "amigo",     "clue": "friend",        "source_id": "amigo"},
    {"entry": "clase",     "clue": "class",         "source_id": "clase"},
    {"entry": "mesa",      "clue": "table",         "source_id": "mesa"},
    {"entry": "silla",     "clue": "chair",         "source_id": "silla"},
    {"entry": "trabajo",   "clue": "work",          "source_id": "trabajo"},
]

def test_generate_returns_puzzle_result():
    result = generate_puzzle(SIMPLE_POOL, grid_size=9, target_count=5)
    assert isinstance(result, PuzzleResult)

def test_grid_correct_dimensions():
    result = generate_puzzle(SIMPLE_POOL, grid_size=9, target_count=5)
    assert len(result.grid) == 9
    assert all(len(row) == 9 for row in result.grid)

def test_placed_words_have_required_fields():
    result = generate_puzzle(SIMPLE_POOL, grid_size=9, target_count=5)
    for pw in result.placed_words:
        assert isinstance(pw, PlacedWord)
        assert pw.direction in ("across", "down")
        assert pw.number >= 1
        assert len(pw.entry) >= 3

def test_grid_letters_match_placed_words():
    result = generate_puzzle(SIMPLE_POOL, grid_size=9, target_count=5)
    for pw in result.placed_words:
        for i, ch in enumerate(pw.entry):
            if pw.direction == "across":
                assert result.grid[pw.row][pw.col + i] == ch
            else:
                assert result.grid[pw.row + i][pw.col] == ch

def test_all_words_intersect():
    """No word may be isolated (no shared letter with any other word)."""
    result = generate_puzzle(SIMPLE_POOL, grid_size=9, target_count=5)
    if len(result.placed_words) <= 1:
        return
    for pw in result.placed_words:
        crosses = False
        for other in result.placed_words:
            if other is pw:
                continue
            if pw.direction == "across" and other.direction == "down":
                if (other.col in range(pw.col, pw.col + len(pw.entry)) and
                        pw.row in range(other.row, other.row + len(other.entry))):
                    crosses = True
                    break
            elif pw.direction == "down" and other.direction == "across":
                if (other.row in range(pw.row, pw.row + len(pw.entry)) and
                        pw.col in range(other.col, other.col + len(other.entry))):
                    crosses = True
                    break
        assert crosses, f"Word '{pw.entry}' is isolated"

def test_no_duplicate_entries_in_grid():
    result = generate_puzzle(SIMPLE_POOL, grid_size=9, target_count=8)
    entries = [pw.entry for pw in result.placed_words]
    assert len(entries) == len(set(entries))

def test_no_adjacent_parallel_words():
    """Two across words must not share adjacent rows; two down words must not share adjacent cols."""
    result = generate_puzzle(SIMPLE_POOL, grid_size=9, target_count=5)
    across = [pw for pw in result.placed_words if pw.direction == "across"]
    down   = [pw for pw in result.placed_words if pw.direction == "down"]

    for i, a in enumerate(across):
        for b in across[i+1:]:
            if abs(a.row - b.row) == 1:
                a_cols = set(range(a.col, a.col + len(a.entry)))
                b_cols = set(range(b.col, b.col + len(b.entry)))
                assert not a_cols.intersection(b_cols), \
                    f"Adjacent parallel across: '{a.entry}' row {a.row}, '{b.entry}' row {b.row}"

    for i, d in enumerate(down):
        for e in down[i+1:]:
            if abs(d.col - e.col) == 1:
                d_rows = set(range(d.row, d.row + len(d.entry)))
                e_rows = set(range(e.row, e.row + len(e.entry)))
                assert not d_rows.intersection(e_rows), \
                    f"Adjacent parallel down: '{d.entry}' col {d.col}, '{e.entry}' col {e.col}"

def test_clue_numbers_sequential_top_to_bottom_left_to_right():
    result = generate_puzzle(SIMPLE_POOL, grid_size=9, target_count=5)
    numbered_cells = {}
    for pw in result.placed_words:
        cell = (pw.row, pw.col)
        if cell not in numbered_cells:
            numbered_cells[cell] = pw.number
        else:
            assert numbered_cells[cell] == pw.number
    sorted_numbers = sorted(numbered_cells.values())
    assert sorted_numbers == list(range(1, len(sorted_numbers) + 1))

def test_target_count_respected_approximately():
    result = generate_puzzle(SIMPLE_POOL, grid_size=9, target_count=5)
    assert 2 <= len(result.placed_words) <= 5

def test_generate_large_grid():
    pool_11 = SIMPLE_POOL * 3
    result = generate_puzzle(pool_11, grid_size=11, target_count=10)
    assert len(result.grid) == 11
    assert len(result.placed_words) >= 3


def test_word_termination_constraint():
    """Every word must be bounded by edge or empty cell at both ends."""
    result = generate_puzzle(SIMPLE_POOL * 3, grid_size=9, target_count=8)
    grid = result.grid
    size = result.grid_size
    for pw in result.placed_words:
        n = len(pw.entry)
        if pw.direction == "across":
            before = grid[pw.row][pw.col - 1] if pw.col > 0 else None
            after  = grid[pw.row][pw.col + n] if pw.col + n < size else None
        else:
            before = grid[pw.row - 1][pw.col] if pw.row > 0 else None
            after  = grid[pw.row + n][pw.col] if pw.row + n < size else None
        assert before is None, (
            f"'{pw.entry}' ({pw.direction}) at ({pw.row},{pw.col}) has letter before it"
        )
        assert after is None, (
            f"'{pw.entry}' ({pw.direction}) at ({pw.row},{pw.col}) has letter after it"
        )
