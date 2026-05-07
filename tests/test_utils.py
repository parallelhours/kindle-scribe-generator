import pytest
from unittest.mock import MagicMock
from templates.scorecard import utils as U


def test_resolve_start_monday(weekly_mod):
    assert weekly_mod._resolve_start("Monday") == 0


def test_resolve_start_sunday(weekly_mod):
    assert weekly_mod._resolve_start("Sunday") == 6


def test_resolve_start_unknown_falls_back_to_monday(weekly_mod):
    assert weekly_mod._resolve_start("Blursday") == 0


def test_resolve_start_case_insensitive(weekly_mod):
    assert weekly_mod._resolve_start("wednesday") == 2


def test_page_dimensions_in_points():
    assert abs(U.PAGE_W - 336.96) < 0.01
    assert abs(U.PAGE_H - 449.28) < 0.01


def test_lineup_columns_sum_to_content_width():
    content_w = U.PAGE_W - 2 * U.MARGIN
    assert abs(sum(U.LINEUP_COLS) - content_w) < 0.5


def test_lineup_rows_fit_on_page():
    # 4 subs; remaining space holds the summary section
    used = (U.MARGIN + U.ROW_TEAM_LABEL + U.ROW_HEADER
            + 9 * U.ROW_STARTER + U.DIVIDER_H
            + 4 * U.ROW_SUB + U.MARGIN)
    assert used <= U.PAGE_H, f"Rows overflow: {used:.1f} > {U.PAGE_H:.1f}"


def test_col_x_positions_are_monotonically_increasing():
    xs = U.col_x_positions()
    for i in range(len(xs) - 1):
        assert xs[i] < xs[i + 1]


def _mock_canvas():
    c = MagicMock()
    path = MagicMock()
    c.beginPath.return_value = path
    return c, path


def test_draw_diamond_calls_begin_path():
    c, path = _mock_canvas()
    U.draw_diamond(c, x=10, y=10, w=18, h=31)
    c.beginPath.assert_called_once()


def test_draw_diamond_closes_path():
    c, path = _mock_canvas()
    U.draw_diamond(c, x=10, y=10, w=18, h=31)
    path.close.assert_called_once()


def test_draw_diamond_draws_no_boxes():
    c, path = _mock_canvas()
    U.draw_diamond(c, x=10, y=10, w=18, h=31)
    assert c.rect.call_count == 0


def test_draw_diamond_labels_result_codes():
    c, path = _mock_canvas()
    U.draw_diamond(c, x=10, y=10, w=18, h=31)
    drawn_strings = [str(a) for a, _ in c.drawString.call_args_list]
    all_text = " ".join(drawn_strings)
    for label in ("1B", "2B", "3B", "HR", "BB"):
        assert label in all_text, f"Missing result label: {label}"
