from openai import OpenAI

from app.core.config import settings
from app.models.prompt import Prompt


class PromptRunner:

    def __init__(self):
        self.client = OpenAI(
            api_key=settings.openai_api_key
        )

    def run(
        self,
        prompt: Prompt,
        user_input: str,
    ) -> str:

        response = self.client.chat.completions.create(
            model=settings.openai_model,
            messages=[
                {
                    "role": "system",
                    "content": prompt.system_prompt,
                },
                {
                    "role": "user",
                    "content": user_input,
                },
            ],
        )

        return response.choices[0].message.content