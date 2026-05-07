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


@pytest.fixture
def weekly_mod():
    return _load_weekly()
