"""A1: tests for the uv project contract module."""

import runpy
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]

module = runpy.run_path(PROJECT_ROOT / "units" / "a1_project_contract.py")
project_contract = module["project_contract"]


def test_project_contract_matches_committed_metadata() -> None:
    """The runnable module must report the committed project contract."""
    contract = project_contract()

    assert contract["name"] == "python-refresher-2026"
    assert contract["python_requirement"] == ">=3.14"
    assert contract["python_pin"] == "3.14"
    assert contract["lockfile"] == "uv.lock"
    assert contract["environment"] == ".venv is generated locally and is not committed"
