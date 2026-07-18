import json
from pathlib import Path

from app.models.prompt import Prompt


PROMPTS_DIR = Path(__file__).resolve().parents[2] / "data" / "prompts"


def load_prompt(filename: str) -> Prompt:
    file_path = PROMPTS_DIR / filename

    if not file_path.exists():
        raise FileNotFoundError(
            f"Prompt file not found: {file_path}"
        )

    if file_path.suffix.lower() != ".json":
        raise ValueError(
            "Prompt file must be a JSON file."
        )

    with file_path.open("r", encoding="utf-8") as file:
        raw_data = json.load(file)

    return Prompt(**raw_data)