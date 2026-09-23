"""A1: the runtime must satisfy the project's declared Python minimum."""

import sys
import tomllib
from pathlib import Path

PROJECT_ROOT = Path(__file__).parent.parent


def test_runtime_satisfies_declared_python_minimum() -> None:
    """The interpreter running tests must meet this project's declared contract."""
    with (PROJECT_ROOT / "pyproject.toml").open("rb") as project_file:
        metadata = tomllib.load(project_file)

    assert metadata["project"]["requires-python"] == ">=3.14"
    assert sys.version_info >= (3, 14)
