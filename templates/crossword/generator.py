"""
generate_puzzle(candidate_pool, grid_size, target_count, max_retries=5) -> PuzzleResult

Backtracking crossword placement:
- grid[row][col] is a letter str or None (empty/black square)
- All words must intersect at least one other word
- No two words adjacent and parallel
- No duplicate entry strings
"""
import random
from dataclasses import dataclass

# Maximum placement attempts per backtrack call tree before giving up and retrying.
# Keeps each attempt bounded without using wall-clock time.
_MAX_CALLS = 200_000


@dataclass
class PlacedWord:
    entry: str
    clue: str
    source_id: str
    row: int
    col: int
    direction: str  # "across" | "down"
    number: int = 0  # assigned after all placements


@dataclass
class PuzzleResult:
    grid: list          # list[list[str | None]]
    placed_words: list  # list[PlacedWord], sorted by number
    grid_size: int


def _empty_grid(size):
    return [[None] * size for _ in range(size)]


def _can_place(grid, word, row, col, direction, size):
    """Return True if word fits at (row,col) in direction without conflict.

    Two termination rules, both enforced:
    1. End-of-word: nothing sits immediately before the start or after the end
       of the new word in its own direction.
    2. Per-cell: for every NEW letter we add (non-intersection cells), no
       existing letter sits in the perpendicular direction adjacent to that cell.
       This prevents a down word from putting a letter immediately before/after
       an existing across word's start/end, and vice versa.
    """
    length = len(word)
    if direction == "across":
        if col + length > size:
            return False
        if col > 0 and grid[row][col - 1] is not None:
            return False
        if col + length < size and grid[row][col + length] is not None:
            return False
        for i, ch in enumerate(word):
            cell = grid[row][col + i]
            if cell is not None and cell != ch:
                return False
            if cell is None:
                r, c = row, col + i
                if r > 0 and grid[r - 1][c] is not None:
                    return False
                if r + 1 < size and grid[r + 1][c] is not None:
                    return False
    else:
        if row + length > size:
            return False
        if row > 0 and grid[row - 1][col] is not None:
            return False
        if row + length < size and grid[row + length][col] is not None:
            return False
        for i, ch in enumerate(word):
            cell = grid[row + i][col]
            if cell is not None and cell != ch:
                return False
            if cell is None:
                r, c = row + i, col
                if c > 0 and grid[r][c - 1] is not None:
                    return False
                if c + 1 < size and grid[r][c + 1] is not None:
                    return False
    return True


def _adjacent_parallel_conflict(grid, placed, word, row, col, direction, size):
    """True if placing word would create adjacent parallel words."""
    length = len(word)
    if direction == "across":
        for pw in placed:
            if pw.direction != "across":
                continue
            if abs(pw.row - row) == 1:
                pw_cols = set(range(pw.col, pw.col + len(pw.entry)))
                new_cols = set(range(col, col + length))
                if pw_cols & new_cols:
                    return True
    else:
        for pw in placed:
            if pw.direction != "down":
                continue
            if abs(pw.col - col) == 1:
                pw_rows = set(range(pw.row, pw.row + len(pw.entry)))
                new_rows = set(range(row, row + length))
                if pw_rows & new_rows:
                    return True
    return False


def _place_word(grid, word, row, col, direction):
    for i, ch in enumerate(word):
        if direction == "across":
            grid[row][col + i] = ch
        else:
            grid[row + i][col] = ch


def _find_intersections(placed, word, grid, size):
    """Yield (row, col, direction) positions where word can intersect placed words."""
    for pw in placed:
        for ci, ch in enumerate(word):
            if pw.direction == "across":
                for pi in range(len(pw.entry)):
                    if pw.entry[pi] == ch:
                        r = pw.row - ci
                        c = pw.col + pi
                        if 0 <= r and r + len(word) <= size:
                            yield r, c, "down"
            else:
                for pi in range(len(pw.entry)):
                    if pw.entry[pi] == ch:
                        r = pw.row + pi
                        c = pw.col - ci
                        if 0 <= c and c + len(word) <= size:
                            yield r, c, "across"


def _assign_numbers(placed_words):
    """Assign clue numbers left-to-right, top-to-bottom. Returns updated list."""
    start_cells = {}
    for pw in placed_words:
        key = (pw.row, pw.col)
        if key not in start_cells:
            start_cells[key] = []
        start_cells[key].append(pw)

    number = 1
    for (row, col) in sorted(start_cells.keys()):
        for pw in start_cells[(row, col)]:
            pw.number = number
        number += 1
    return placed_words


def _backtrack(candidates, grid, placed, target, size, used_entries, counter,
               max_positions=15):
    """Return True if target reached; False if search budget exhausted or candidates empty."""
    if len(placed) >= target:
        return True

    if counter[0] > _MAX_CALLS:
        return False

    for cand in candidates:
        entry = cand["entry"]
        if entry in used_entries:
            continue

        positions = list(_find_intersections(placed, entry, grid, size))
        random.shuffle(positions)
        positions = positions[:max_positions]

        for row, col, direction in positions:
            counter[0] += 1
            if counter[0] > _MAX_CALLS:
                return False

            if not _can_place(grid, entry, row, col, direction, size):
                continue
            if _adjacent_parallel_conflict(grid, placed, entry, row, col, direction, size):
                continue

            saved = [row_[:] for row_ in grid]
            _place_word(grid, entry, row, col, direction)
            pw = PlacedWord(entry=entry, clue=cand["clue"], source_id=cand["source_id"],
                            row=row, col=col, direction=direction)
            placed.append(pw)
            used_entries.add(entry)

            if _backtrack(candidates, grid, placed, target, size, used_entries, counter,
                          max_positions=max_positions):
                return True

            placed.pop()
            used_entries.discard(entry)
            for r in range(size):
                grid[r] = saved[r]

    return False


def generate_puzzle(candidate_pool: list, grid_size: int, target_count: int,
                    max_retries: int = 5) -> PuzzleResult:
    """
    Place target_count words from candidate_pool onto a grid_size×grid_size grid.
    Retries up to max_retries times; reduces target by 3 if all retries fail.
    """
    pool = [c for c in candidate_pool if 3 <= len(c["entry"]) <= grid_size]
    if not pool:
        raise ValueError("candidate_pool contains no entries with 3+ character words")

    placed = []
    grid = _empty_grid(grid_size)

    for attempt in range(max_retries + 1):
        current_target = max(3, target_count - (3 if attempt == max_retries else 0))
        random.shuffle(pool)
        working = sorted(pool[:current_target * 4], key=lambda c: len(c["entry"]), reverse=True)

        grid = _empty_grid(grid_size)
        placed = []
        used_entries = set()

        first = working[0]
        center_row = grid_size // 2
        center_col = max(0, (grid_size - len(first["entry"])) // 2)
        _place_word(grid, first["entry"], center_row, center_col, "across")
        placed.append(PlacedWord(
            entry=first["entry"], clue=first["clue"], source_id=first["source_id"],
            row=center_row, col=center_col, direction="across"
        ))
        used_entries.add(first["entry"])

        counter = [0]
        if _backtrack(working[1:], grid, placed, current_target, grid_size, used_entries, counter):
            _assign_numbers(placed)
            placed_sorted = sorted(placed, key=lambda pw: (pw.number, pw.direction))
            return PuzzleResult(grid=grid, placed_words=placed_sorted, grid_size=grid_size)

    # Final fallback: return whatever was placed
    _assign_numbers(placed)
    return PuzzleResult(
        grid=grid,
        placed_words=sorted(placed, key=lambda pw: (pw.number, pw.direction)),
        grid_size=grid_size
    )
