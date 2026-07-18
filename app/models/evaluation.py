from pydantic import BaseModel


class EvaluationResult(BaseModel):
    input: str
    expected_output: str
    actual_output: str
    score: float
    passed: bool