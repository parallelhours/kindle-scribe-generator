# Copyright (C) 2026 Paul Monday — GNU GPL v3 or later. See LICENSE.
import importlib.util
from pathlib import Path
import pytest


def _load_weekly():
    spec = importlib.util.spec_from_file_location(
        "weekly_activities",
        Path(__file__).parent.parent / "templates" / "weekly-activities" / "template.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def _load_prompt_notebook():
    spec = importlib.util.spec_from_file_location(
        "prompt_notebook",
        Path(__file__).parent.parent / "templates" / "prompt-notebook" / "template.py",
    )
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


@pytest.fixture
def weekly_mod():
    return _load_weekly()


@pytest.fixture
def prompt_mod():
    return _load_prompt_notebook()


def _load_sudoku():
    import importlib
    return importlib.import_module("templates.sudoku.template")


@pytest.fixture
def sudoku_mod():
    return _load_sudoku()
