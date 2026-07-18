import json
from pathlib import Path

from app.models.golden_set import GoldenSet


GOLDEN_SETS_DIR = Path(__file__).resolve().parents[2] / "golden_sets"


def load_golden_set(filename: str) -> list[GoldenSet]:
    file_path = GOLDEN_SETS_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"Golden set file not found: {file_path}"
        )

    if file_path.suffix.lower() != ".json":
        raise ValueError(
            "Golden set file must be a JSON file."
        )

    with file_path.open("r", encoding="utf-8") as file:
        raw_data = json.load(file)

    if not isinstance(raw_data, list):
        raise ValueError(
            "Golden set JSON must contain a list."
        )

    return [GoldenSet(**item) for item in raw_data]