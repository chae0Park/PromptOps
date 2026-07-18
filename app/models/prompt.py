from pydantic import BaseModel


class Prompt(BaseModel):
    name: str
    version: str
    system_prompt: str