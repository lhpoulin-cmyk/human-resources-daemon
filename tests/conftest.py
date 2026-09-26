import json
from pathlib import Path

import pytest

REPO_ROOT = Path(__file__).resolve().parent.parent
FIXTURES_DIR = REPO_ROOT / "fixtures"


def load_json(*parts: str):
    return json.loads((FIXTURES_DIR.joinpath(*parts)).read_text())


@pytest.fixture
def fixtures_dir() -> Path:
    return FIXTURES_DIR
