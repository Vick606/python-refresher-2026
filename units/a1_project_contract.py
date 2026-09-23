"""A1: inspect the files that make a uv project reproducible.

Primary source:
https://docs.astral.sh/uv/concepts/projects/layout/

Run:
    uv run python units/a1_project_contract.py
"""

import tomllib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]


def load_project_metadata() -> dict[str, object]:
    """Read the project's declared metadata from pyproject.toml."""
    project_file = PROJECT_ROOT / "pyproject.toml"

    with project_file.open("rb") as file:
        return tomllib.load(file)


def project_contract() -> dict[str, str]:
    """Return the committed files that define this project's environment."""
    metadata = load_project_metadata()
    project = metadata["project"]

    return {
        "name": str(project["name"]),
        "python_requirement": str(project["requires-python"]),
        "python_pin": (PROJECT_ROOT / ".python-version").read_text().strip(),
        "lockfile": "uv.lock",
        "environment": ".venv is generated locally and is not committed",
    }


def main() -> None:
    """Print the project contract a clean clone needs before uv creates an environment."""
    for label, value in project_contract().items():
        print(f"{label}: {value}")


if __name__ == "__&#8203;main__":
    main()
