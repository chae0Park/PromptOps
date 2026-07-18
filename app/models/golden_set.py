from pydantic import BaseModel


class GoldenSet(BaseModel):
    input: str
    expected_output: str