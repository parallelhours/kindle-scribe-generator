# templates/sudoku/generator.py
import random

_DIFFICULTY = {
    "easy":   46,
    "medium": 36,
    "hard":   28,
    "expert": 22,
}


def _used_digits(grid: list, r: int, c: int) -> set:
    used = set()
    used.update(v for v in grid[r] if v is not None)
    used.update(grid[rr][c] for rr in range(9) if grid[rr][c] is not None)
    br, bc = (r // 3) * 3, (c // 3) * 3
    used.update(
        grid[br + dr][bc + dc]
        for dr in range(3) for dc in range(3)
        if grid[br + dr][bc + dc] is not None
    )
    return used


def _is_valid_grid(grid: list) -> bool:
    """Return False if any filled cell conflicts with another filled cell."""
    for r in range(9):
        seen = [v for v in grid[r] if v is not None]
        if len(seen) != len(set(seen)):
            return False
    for c in range(9):
        seen = [grid[r][c] for r in range(9) if grid[r][c] is not None]
        if len(seen) != len(set(seen)):
            return False
    for br in range(0, 9, 3):
        for bc in range(0, 9, 3):
            seen = [
                grid[br + dr][bc + dc]
                for dr in range(3) for dc in range(3)
                if grid[br + dr][bc + dc] is not None
            ]
            if len(seen) != len(set(seen)):
                return False
    return True


def _count(grid: list, limit: int, tally: list) -> None:
    """Recursive backtracking counter. Mutates tally[0]; stops at limit."""
    if tally[0] >= limit:
        return
    for r in range(9):
        for c in range(9):
            if grid[r][c] is None:
                used = _used_digits(grid, r, c)
                for d in range(1, 10):
                    if d not in used:
                        grid[r][c] = d
                        _count(grid, limit, tally)
                        grid[r][c] = None
                        if tally[0] >= limit:
                            return
                return  # dead end — no digit worked
    tally[0] += 1  # no empty cell found — complete solution


def count_solutions(grid: list, limit: int = 2) -> int:
    """Return number of solutions up to limit (stops early). Uses a scratch copy."""
    scratch = [row[:] for row in grid]
    if not _is_valid_grid(scratch):
        return 0
    tally = [0]
    _count(scratch, limit, tally)
    return tally[0]


def _fill(grid: list) -> bool:
    """Recursive backtracking helper for fill_grid. Mutates grid in-place."""
    for r in range(9):
        for c in range(9):
            if grid[r][c] is None:
                digits = list(range(1, 10))
                random.shuffle(digits)
                used = _used_digits(grid, r, c)
                for d in digits:
                    if d not in used:
                        grid[r][c] = d
                        if _fill(grid):
                            return True
                        grid[r][c] = None
                return False
    return True


def fill_grid(grid: list) -> bool:
    """Fill grid in-place with a complete valid Sudoku solution. Returns True on success.

    Raises ValueError if grid already contains conflicting pre-filled cells, which would
    cause the backtracking search to exhaust all branches without finding a solution.
    """
    if not _is_valid_grid(grid):
        raise ValueError("fill_grid: input grid has conflicting pre-filled cells")
    return _fill(grid)


def make_puzzle(difficulty: str = "medium") -> dict:
    """Return {"given": grid_with_nones, "solved": complete_grid}."""
    clues = _DIFFICULTY.get(difficulty, 36)
    solution = [[None] * 9 for _ in range(9)]
    fill_grid(solution)

    puzzle = [row[:] for row in solution]
    cells = [(r, c) for r in range(9) for c in range(9)]
    random.shuffle(cells)

    removed = 0
    target = 81 - clues
    for r, c in cells:
        if removed >= target:
            break
        val = puzzle[r][c]
        puzzle[r][c] = None
        if count_solutions(puzzle, limit=2) == 1:
            removed += 1
        else:
            puzzle[r][c] = val  # restore — would create ambiguity

    return {"given": puzzle, "solved": solution}
